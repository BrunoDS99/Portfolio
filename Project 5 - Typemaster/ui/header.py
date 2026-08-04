import tkinter as tk


from config.settings import *

class Header:
    
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg=BACKGROUND_COLOR)
        self.frame.pack(pady=(0, 30))

        title = tk.Label(
            self.frame,
            text="TypeMaster",
            background=BACKGROUND_COLOR,
            foreground=PRIMARY_TEXT,
            font=TITLE_FONT,
        )
        title.pack()
        
        subtitle = tk.Label(
            self.frame,
            text="Typing Speed Analyzer",
            background=BACKGROUND_COLOR,
            foreground=SECONDARY_TEXT,
            font=SUBTITLE_FONT,
        )
        subtitle.pack()