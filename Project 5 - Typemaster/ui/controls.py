import tkinter as tk
from config.settings import *

class Controls:
    def __init__(self, parent, start_command, restart_command):
        self.frame = tk.Frame(parent, bg=BACKGROUND_COLOR)
        self.frame.pack(pady=20)

        self.start_button = self.create_button("Start",start_command)
        self.start_button.pack(side="left", padx=20)

        self.restart_button = self.create_button("Restart",restart_command)

        self.start_button.pack(side="left", padx=10)
        self.restart_button.pack(side="left", padx=10)
    
    def create_button(self, text, command):

        button = tk.Button(
            self.frame,
            text=text,
            command=command,
            bg=BUTTON_COLOR,
            fg=PRIMARY_TEXT,
            activebackground=BUTTON_HOVER,
            activeforeground=PRIMARY_TEXT,
            relief="flat",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            font=BUTTON_FONT
        )

        button.bind(
            "<Enter>",
            lambda e: button.config(bg=BUTTON_HOVER)
        )

        button.bind(
            "<Leave>",
            lambda e: button.config(bg=BUTTON_COLOR)
        )

        return button