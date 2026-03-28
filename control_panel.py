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
    
    def remove_block(self, blocks, target_block_id:int):
        num_blocks = len(blocks)
        target_block_index = [i for i in range(num_blocks) if blocks[i]["id"] == target_block_id][0]
        blocks.pop(target_block_index)["widget"].destroy()
    
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
        ).pack(side="left")

        # Button for swaping below
        ttk.Button(
            block,
            text="↓",
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
            command=lambda: self.remove_block(blocks, block_id)
        ).pack(side="left")

        # Add block to list
        blocks.append(
            {"id":block_id, "text_var":text_var, "color":color, "widget":block}
        )

        return
        