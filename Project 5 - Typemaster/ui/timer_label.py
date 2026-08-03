import tkinter as tk

from config.settings import (BACKGROUND_COLOR, TEXT_COLOR, FONT_FAMILY, MAIN_FONT_SIZE)

class TimerLabel:
    def __init__(self, parent):
        self.label = tk.Label(
            parent,
            text="Time: 0s",
            background=BACKGROUND_COLOR,
            foreground=TEXT_COLOR,
            font=(FONT_FAMILY, MAIN_FONT_SIZE)
        )
        self.label.pack(pady=10)

    def update(self, seconds):
        self.label.config(text=f"Time: {int(seconds)}s")