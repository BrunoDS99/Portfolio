import tkinter as tk

from config.settings import (BACKGROUND_COLOR, CARD_COLOR, CORRECT_COLOR, CURRENT_COLOR, ERROR_COLOR, PRIMARY_TEXT, TEXT_COLOR, FONT_FAMILY, MAIN_FONT_SIZE, TEXT_FONT)

class TypingDisplay:
    def __init__(self, parent):
        
        self.card = tk.Frame(
        parent,
        bg=CARD_COLOR,
        padx=30,
        pady=30
        )

        self.card.pack(
        fill="x",
        pady=20
        )
        
        self.text_widget = tk.Text(
        self.card,
        wrap="word",
        height=5,
        width=50,
        bg=CARD_COLOR,
        fg=PRIMARY_TEXT,
        insertbackground=PRIMARY_TEXT,
        relief="flat",
        bd=0,
        highlightthickness=0,
        font=TEXT_FONT
    )

        self.text_widget.pack(fill="both")
        self.configure_tags()
        
    def configure_tags(self):
        self.text_widget.tag_configure("correct", foreground=CORRECT_COLOR)
        self.text_widget.tag_configure("wrong", foreground=ERROR_COLOR)
        self.text_widget.tag_configure("current", foreground=CURRENT_COLOR, underline=True)
    
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