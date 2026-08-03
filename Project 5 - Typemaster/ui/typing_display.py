import tkinter as tk

from config.settings import (BACKGROUND_COLOR, TEXT_COLOR, FONT_FAMILY, MAIN_FONT_SIZE)

class TypingDisplay:
    def __init__(self, parent):
        
        self.text_widget = tk.Text(
            parent,
            wrap="word",
            height=5,
            width=60,
            background=BACKGROUND_COLOR,
            foreground=TEXT_COLOR,
            font = (FONT_FAMILY, MAIN_FONT_SIZE),
            borderwidth=0,
            highlightthickness=0
        )
        
        self.text_widget.pack(padx=50, pady=80)
        self.configure_tags()
        
    def configure_tags(self):
        self.text_widget.tag_configure("correct", foreground="#808080")
        self.text_widget.tag_configure("wrong", foreground="#FF4444")
        self.text_widget.tag_configure("current", underline=True)
    
    def update_display(self, original_text, typed_text):
        self.text_widget.config(state="normal")
        self.text_widget.delete("1.0", "end")
        
        for index, expected_char in enumerate(original_text):
            tag = None
            if index < len(typed_text): 
                if typed_text[index] == expected_char:
                    tag = "correct"
                else:
                    tag = "wrong"
            elif index == len(typed_text):
                tag = "current"
                
            if tag:
                self.text_widget.insert("end", expected_char, tag)
            else:
                self.text_widget.insert("end", expected_char)
                
        self.text_widget.config(state="disabled")