import tkinter as tk
from PIL import Image, ImageFont, ImageDraw
import math
import config
from control_panel import ControlPanel

class App(tk.Frame):
	def __init__(self, root: tk.Tk):
		super().__init__(root)
		root.title(f"{config.TITLE}")
		root.resizable(False, False)
		root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
		self.canvas = tk.Canvas(
			root, 
			width=config.WINDOW_WIDTH, 
			height=config.WINDOW_HEIGHT, 
			bg="#111111", 
			highlightthickness=0
		)
		self.canvas.place(x=0, y=0)

		text = "本日はご乗車いただき誠にありがとうございます。"
		font = ImageFont.truetype("ヒラギノ明朝 ProN.ttc", config.GRID_HEIGHT)
		self.image_width = math.ceil(font.getlength(text))
		self.image = Image.new(
			"1", 
			(self.image_width, config.GRID_HEIGHT), 
			color=1
		)
		ImageDraw.Draw(self.image).text(
			(0,0), 
			text=text, 
			font=font, 
			fill=0
		)

		self.pos = 0

		self.tick_draw()

		self.waiting_key = None
		root.bind("<KeyPress>", self.key_event)

	def tick_left(self):
		if self.pos >= self.image_width:
			return
		update_width = config.GRID_WIDTH
		if self.pos + config.GRID_WIDTH >= self.image_width:
			update_width = self.image_width - self.pos - 1
			for y in range(config.GRID_HEIGHT):
				self.canvas.itemconfig(self.rect_ids[y][update_width][0], fill="#555555")
				self.canvas.itemconfig(self.rect_ids[y][update_width][1], fill="#555555")

		for y in range(config.GRID_HEIGHT):
			current = self.image.getpixel((self.pos, y))
			for x in range(update_width):
				next = self.image.getpixel((self.pos + x + 1, y))
				if current != next:
					fill_color = "#ffbf00" if next == 0 else "#555555"
					self.canvas.itemconfig(self.rect_ids[y][x][0], fill=fill_color)
					self.canvas.itemconfig(self.rect_ids[y][x][1], fill=fill_color)
				current = next
		
		self.pos += 1

	def tick_draw(self):
		self.canvas.delete("all")
		self.rect_ids = []

		draw_width = config.GRID_WIDTH
		if self.pos + config.GRID_WIDTH >= self.image_width:
			draw_width = self.image_width - self.pos
		for y in range(config.GRID_HEIGHT):
			row = []
			for x in range(config.GRID_WIDTH):
				x1, y1 = x * config.DOT_SIZE + config.DOT_BORDER_WIDTH, y * config.DOT_SIZE + config.DOT_BORDER_WIDTH
				x2, y2 = (x+1) * config.DOT_SIZE - config.DOT_BORDER_WIDTH, (y+1) * config.DOT_SIZE - config.DOT_BORDER_WIDTH
				fill_color = "#ffbf00" if self.image.getpixel((self.pos + x, y)) == 0 and x < draw_width else "#555555"
				id1 = self.canvas.create_rectangle(x1, y1+1, x2, y2-1, fill=fill_color, width=0)
				id2 = self.canvas.create_rectangle(x1+1, y1, x2-1, y2, fill=fill_color, width=0)
				row.append([id1, id2])
			self.rect_ids.append(row)

	def ticking_left(self):
		if not self.ticking:
			return
		self.tick_left()
		self.master.after(25, self.ticking_left)

	def key_event(self, e):
		key = e.keysym
		if self.waiting_key:
			if key == "Left":
				self.ticking = True
				self.ticking_left()
			self.master.title(u"LED Train Ticker")
			self.waiting_key = None
		else:
			if key == "Left":
				self.tick_left()
			if key == "r":
				self.tick_draw()
			if key == "space":
				self.ticking = False
			if key == "e":
				ctrl_panel = tk.Toplevel()
				ControlPanel(ctrl_panel)
			if key == "z":
				self.master.title(u"LED Train Ticker { Press ← or → to start... }")
				self.waiting_key = "z"


if __name__ == "__main__":
	root = tk.Tk()
	app = App(root)
	root.mainloop()