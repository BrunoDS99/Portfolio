import tkinter as tk

from config.settings import (
    CARD_COLOR,
    PRIMARY_TEXT,
    SECONDARY_TEXT,
    ACCENT_COLOR,
    STAT_TITLE_FONT,
    STAT_VALUE_FONT
)


class StatCard:

    def __init__(self, parent, title):

        self.frame = tk.Frame(
            parent,
            bg=CARD_COLOR,
            padx=30,
            pady=20,
            highlightthickness=1,
            highlightbackground=CARD_COLOR
        )

        self.frame.pack(
            side="left",
            padx=15
        )


        self.title_label = tk.Label(
            self.frame,
            text=title,
            bg=CARD_COLOR,
            fg=SECONDARY_TEXT,
            font=STAT_TITLE_FONT
        )

        self.title_label.pack()


        self.value_label = tk.Label(
            self.frame,
            text="0",
            bg=CARD_COLOR,
            fg=ACCENT_COLOR,
            font=STAT_VALUE_FONT
        )

        self.value_label.pack(
            pady=(5, 0)
        )


    def update(self, value):

        self.value_label.config(
            text=value
        )