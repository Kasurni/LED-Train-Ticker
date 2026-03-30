import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser
from tkmacosx import Button as MacButton
import config

class ControlPanel(tk.Frame):
    def __init__(self, root:tk.Tk):
        root.title(f"{config.TITLE}")
        root.geometry(f"{config.SUB_WINDOW_WIDTH}x{config.SUB_WINDOW_HEIGHT}")
        root["padx"], root["pady"] = 10, 10

        # Font config
        self.font = tk.font.Font(
            root,
            family="Hiragino Sans",
            size=config.FONT_SIZE
        )

        # Header
        header = ttk.Label(
            root, 
            text="Tick Blocks",
            font=("Hiragino Sans", config.FONT_SIZE_HEAD)
        )
        header.pack(anchor="nw")

        # Blocks container
        blocks_frame = ttk.Frame(root)
        blocks_frame.pack(anchor="nw", fill="x")

        self.blocks_data = []

        self.add_block(
            frame=blocks_frame, 
            text="本日はご乗車いただき誠にありがとうございます",
            color="#ffbf00",
        )

        add_block_button = ttk.Button(
            root, 
            text="Add block", 
            command=lambda: self.add_block(
                frame=blocks_frame, 
                text="本日はご乗車いただき誠にありがとうございます",
                color="#ffbf00",
            )
        )
        add_block_button.pack()

    def pick_color(self, target_button:MacButton, style_name:str):
        # Open colorpicker and get color code
        color_code = colorchooser.askcolor(initialcolor=target_button["background"])
        if color_code[1]:
            ttk.Style().configure(style_name, foreground=color_code[1]) # Entry text color
            target_button.configure(background=color_code[1], activebackground=color_code[1]) # Button color
        return
    
    def remove_block(self, frame:ttk.Frame, target_block_id:int):
        num_blocks = len(self.blocks_data)
        target_block_index = next(
            (i for i in range(num_blocks) if self.blocks_data[i]["id"] == target_block_id),
            None
        )
        if target_block_index:
            self.blocks_data.pop(target_block_index)
            frame.pack_slaves()[target_block_index].destroy()
        return

    def swap_blocks_above(self, frame:ttk.Frame, target_block_id:int):
        ids = [data["id"] for data in self.blocks_data]
        if not target_block_id in ids or ids.index(target_block_id) == 0:
            return
        target_block_index = ids.index(target_block_id)
        self.blocks_data[target_block_index], self.blocks_data[target_block_index-1] = self.blocks_data[target_block_index-1], self.blocks_data[target_block_index]
        blocks = frame.pack_slaves()
        for block in blocks:
            block.pack_forget()
        for data in self.blocks_data:
            block = next((b for b in blocks if id(b) == data["id"]))
            block.pack(anchor="nw", fill="x", expand=True)
        return

    def swap_blocks_below(self, frame:ttk.Frame, target_block_id:int):
        ids = [data["id"] for data in self.blocks_data]
        if not target_block_id in ids or ids.index(target_block_id) == len(ids) - 1:
            return
        target_block_index = ids.index(target_block_id)
        self.blocks_data[target_block_index], self.blocks_data[target_block_index+1] = self.blocks_data[target_block_index+1], self.blocks_data[target_block_index]
        blocks = frame.pack_slaves()
        for block in blocks:
            block.pack_forget()
        for data in self.blocks_data:
            block = next((b for b in blocks if id(b) == data["id"]))
            block.pack(anchor="nw", fill="x", expand=True)
        return
    
    def add_block(self, frame:ttk.Frame, text:str, color:str):
        # Make block as container of entry and buttons
        block = ttk.Frame(frame)
        block_id = id(block)
        block.pack(anchor="nw", fill="x", expand=True)
        
        # Entry
        style_name = f"{block_id}.TEntry"
        ttk.Style().configure(style_name, foreground=color)
        text_var = tk.StringVar(value=text)
        ttk.Entry(
            block,
            textvariable=text_var,
            font=self.font,
            style=style_name
        ).pack(side="left", fill="x", expand=True)

        # Button for swaping above
        ttk.Button(
            block,
            text="↑",
            command=lambda: self.swap_blocks_above(frame, block_id)
        ).pack(side="left")

        # Button for swaping below
        ttk.Button(
            block,
            text="↓",
            command=lambda: self.swap_blocks_below(frame, block_id)
        ).pack(side="left")

        # Button for choosing text color
        initial_color = color
        pick_color_button = MacButton(
            block,
            text=" ",
            background=initial_color,
            activebackground=initial_color,
            focusthickness=0,
            highlightthickness=0,
            bd=0,
            width=40,
        )
        pick_color_button.configure(command=lambda: self.pick_color(pick_color_button, style_name))
        pick_color_button.pack(side="left")

        # Button for removing
        ttk.Button(
            block,
            text="x",
            command=lambda: self.remove_block(frame, block_id)
        ).pack(side="left")

        # Add block to list
        self.blocks_data.append(
            {"id":block_id, "text_var":text_var, "color":color}
        )
        return
        