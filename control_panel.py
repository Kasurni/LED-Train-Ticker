import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser
from tkmacosx import Button as MacButton

class ControlPanel(tk.Frame):
    def __init__(self, root:tk.Tk):
        root.title("LED Train Ticker")
        root.geometry("600x400")
        root["padx"], root["pady"] = 10, 10

        # Font config
        font_size = 10
        font_size_head = 13
        font = tk.font.Font(
            root,
            family="Hiragino Sans",
            size=font_size
        )

        # Header
        label_head = ttk.Label(
            root, 
            text="Tick Blocks",
            font=("Hiragino Sans", font_size_head)
        )
        label_head.pack(anchor="nw")

        # Blocks container
        frame_blocks = ttk.Frame(root)
        frame_blocks.pack(anchor="nw", fill="x")

        blocks = []

        self.add_block(
            blocks=blocks, 
            parent=frame_blocks, 
            text="本日はご乗車いただき誠にありがとうございます",
            color="#ffbf00",
            font=font
        )

        button_add_block = ttk.Button(
            root, 
            text="Add block", 
            command=lambda: self.add_block(
                blocks=blocks, 
                parent=frame_blocks, 
                text="本日はご乗車いただき誠にありがとうございます",
                color="#ffbf00",
                font=font
            )
        )
        button_add_block.pack()

    def pick_color(self, target_button, style_name):
        # Open colorpicker and get color code
        color_code = colorchooser.askcolor(initialcolor=target_button["background"])
        if color_code[1]:
            ttk.Style().configure(style_name, foreground=color_code[1]) # Entry text color
            target_button.configure(background=color_code[1], activebackground=color_code[1]) # Button color
        return
    
    def remove_block(self, blocks, parent, target_block_id:int):
        num_blocks = len(blocks)
        target_block_index = next(
            (i for i in range(num_blocks) if blocks[i]["id"] == target_block_id),
            None
        )
        blocks.pop(target_block_index)
        parent.pack_slaves()[target_block_index].destroy()

    def swap_blocks_above(self, blocks, parent, target_block_id:int):
        ids = [block["id"] for block in blocks]
        if not target_block_id in ids or ids.index(target_block_id) == 0:
            return
        target_block_index = ids.index(target_block_id)
        blocks[target_block_index], blocks[target_block_index-1] = blocks[target_block_index-1], blocks[target_block_index]
        wblocks = parent.pack_slaves()
        for wblock in wblocks:
            wblock.pack_forget()
        for b in blocks:
            wb = next((_wb for _wb in wblocks if id(_wb) == b["id"]))
            wb.pack(anchor="nw", fill="x", expand=True)

    def swap_blocks_below(self, blocks, parent, target_block_id:int):
        ids = [block["id"] for block in blocks]
        if not target_block_id in ids or ids.index(target_block_id) == len(ids) - 1:
            return
        target_block_index = ids.index(target_block_id)
        blocks[target_block_index], blocks[target_block_index+1] = blocks[target_block_index+1], blocks[target_block_index]
        wblocks = parent.pack_slaves()
        for wblock in wblocks:
            wblock.pack_forget()
        for b in blocks:
            wb = next((_wb for _wb in wblocks if id(_wb) == b["id"]))
            wb.pack(anchor="nw", fill="x", expand=True)
    
    def add_block(self, blocks, parent, text, color, font):
        # Make frame as container of entry and buttons
        block = ttk.Frame(parent)
        block_id = id(block)
        block.pack(anchor="nw", fill="x", expand=True)
        
        # Entry
        style_name = f"{block_id}.TEntry"
        ttk.Style().configure(style_name, foreground=color)
        text_var = tk.StringVar(value=text)
        ttk.Entry(
            block,
            textvariable=text_var,
            font=font,
            style=style_name
        ).pack(side="left", fill="x", expand=True)

        # Button for swaping above
        ttk.Button(
            block,
            text="↑",
            command=lambda: self.swap_blocks_above(blocks, parent, block_id)
        ).pack(side="left")

        # Button for swaping below
        ttk.Button(
            block,
            text="↓",
            command=lambda: self.swap_blocks_below(blocks, parent, block_id)
        ).pack(side="left")

        # Button for choosing text color
        initial_color = color
        button_pick_color = MacButton(
            block,
            text=" ",
            background=initial_color,
            activebackground=initial_color,
            focusthickness=0,
            highlightthickness=0,
            bd=0,
            width=40,
        )
        button_pick_color.configure(command=lambda: self.pick_color(button_pick_color, style_name))
        button_pick_color.pack(side="left")

        # Button for removing
        ttk.Button(
            block,
            text="x",
            command=lambda: self.remove_block(blocks, parent, block_id)
        ).pack(side="left")

        # Add block to list
        blocks.append(
            {"id":block_id, "text_var":text_var, "color":color}
        )

        return
        