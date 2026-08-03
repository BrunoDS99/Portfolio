import tkinter as tk

from config.settings import (BACKGROUND_COLOR, TEXT_COLOR, FONT_FAMILY, STAT_FONT_SIZE)


class StatisticsBoard:
    
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg=BACKGROUND_COLOR)
        
        self.frame.pack(pady=20)
        
        self.wpm_label = tk.Label(self.frame, text="WPM: 0", font=(FONT_FAMILY, STAT_FONT_SIZE), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.accuracy_label = tk.Label(self.frame, text="Accuracy: 100%", font=(FONT_FAMILY, STAT_FONT_SIZE), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.error_label = tk.Label(self.frame, text="Errors: 0", font=(FONT_FAMILY, STAT_FONT_SIZE), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        
        self.wpm_label.pack(side="left", padx=25)
        self.accuracy_label.pack(side="left", padx=25)
        self.error_label.pack(side="left", padx=25)
        
    def update(self, wpm, accuracy, errors):
        self.wpm_label.config(text=f"WPM: {wpm}")
        self.accuracy_label.config(text=f"Accuracy: {accuracy}%")
        self.error_label.config(text=f"Errors: {errors}")
        