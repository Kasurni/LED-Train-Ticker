import sys
import tkinter as tk
from PIL import Image, ImageFont, ImageDraw

PIXEL_SIZE = 6 # Border is included
BORDER_WIDTH = 1
WIDTH = 210
HEIGHT = 35

WINDOW_WIDTH = PIXEL_SIZE * WIDTH
WINDOW_HEIGHT = PIXEL_SIZE * HEIGHT

FONT_SIZE = 120

class LTT(tk.Frame):
	def __init__(self, root: tk.Tk):
		super().__init__(root)

		root.title(u"LED Train Ticker")
		root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

		self.canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="#111", highlightthickness=0)
		self.canvas.place(x=0,y=0)


		image = Image.new("1", (WIDTH, HEIGHT), color=1)
		draw = ImageDraw.Draw(image)

		self.font = ImageFont.truetype("ヒラギノ明朝 ProN.ttc", 32)
		self.pos = WIDTH
		draw.text((self.pos,1), text="本日はご乗車いただき誠にありがとうございます。", font=self.font, fill=0)

		for x in range(WIDTH):
			for y in range(HEIGHT):
				x1, y1 = x * PIXEL_SIZE + BORDER_WIDTH, y * PIXEL_SIZE + BORDER_WIDTH
				x2, y2 = (x+1) * PIXEL_SIZE - BORDER_WIDTH, (y+1) * PIXEL_SIZE - BORDER_WIDTH
				if image.getpixel((x,y)) == 0:
					self.canvas.create_rectangle(x1, y1+1, x2, y2-1, fill="#ffbf00", width=0)
					self.canvas.create_rectangle(x1+1, y1, x2-1, y2, fill="#ffbf00", width=0)
				else:
					self.canvas.create_rectangle(x1, y1+1, x2, y2-1, fill="#555", width=0)
					self.canvas.create_rectangle(x1+1, y1, x2-1, y2, fill="#555", width=0)

		root.bind("<KeyPress>", self.key_event)

	def key_event(self, e):
		key = e.keysym
		if key == "space":
			image = Image.new("1", (WIDTH, HEIGHT), color=1)
			draw = ImageDraw.Draw(image)
			self.pos -= 1
			draw.text((self.pos,1), text="本日はご乗車いただき誠にありがとうございます。", font=self.font, fill=0)
			for x in range(WIDTH):
				for y in range(HEIGHT):
					x1, y1 = x * PIXEL_SIZE + BORDER_WIDTH, y * PIXEL_SIZE + BORDER_WIDTH
					x2, y2 = (x+1) * PIXEL_SIZE - BORDER_WIDTH, (y+1) * PIXEL_SIZE - BORDER_WIDTH
					if image.getpixel((x,y)) == 0:
						self.canvas.create_rectangle(x1, y1+1, x2, y2-1, fill="#ffbf00", width=0)
						self.canvas.create_rectangle(x1+1, y1, x2-1, y2, fill="#ffbf00", width=0)
					else:
						self.canvas.create_rectangle(x1, y1+1, x2, y2-1, fill="#555", width=0)
						self.canvas.create_rectangle(x1+1, y1, x2-1, y2, fill="#555", width=0)


if __name__ == "__main__":
	root = tk.Tk()
	app = LTT(root)
	root.mainloop()