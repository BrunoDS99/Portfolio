import tkinter as tk

from ui.stat_card import StatCard
from config.settings import BACKGROUND_COLOR


class StatisticsBoard:

    def __init__(self, parent):

        self.frame = tk.Frame(parent,bg=BACKGROUND_COLOR)
        self.frame.pack(pady=20)
        self.wpm_card = StatCard(self.frame,"WPM")
        self.accuracy_card = StatCard(self.frame,"Accuracy")
        self.errors_card = StatCard(self.frame,"Errors")

    def update(self, wpm, accuracy, errors):

        self.wpm_card.update(wpm)
        self.accuracy_card.update(f"{accuracy}%")
        self.errors_card.update(errors)