import tkinter as tk

from config.settings import (WINDOW_TITLE, WINDOW_HEIGHT, WINDOW_WIDTH, BACKGROUND_COLOR)
from data.word_generator import generate_random_words
from ui.typing_display import TypingDisplay
from core.typing_test import TypingTest
from core.statistics import Statistics 
from ui.statistics_board import StatisticsBoard
from core.timer import Timer
from ui.timer_label import TimerLabel
from core.statistics import Statistics

class AppWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(background=BACKGROUND_COLOR)
        self.timer = Timer()
        self.started = False
        self.statistics = Statistics()
        self.create_widgets()
        self.update_timer()  # Start the timer update loop
        
    
    def create_widgets(self):
        text = generate_random_words(50)
        self.typing_test = TypingTest(text)
        self.statistics = Statistics()
        self.statistics_board = StatisticsBoard(self.root)
        self.typing_display = TypingDisplay(self.root)
        self.typing_display.update_display(text, "")
        self.timer_label = TimerLabel(self.root)
        
        self.root.bind("<Key>", self.handle_keypress)
       
    def handle_keypress(self, event):
        
        if not self.started:
            self.timer.start()
            self.started = True
        result = self.typing_test.process_key(event.keysym, event.char)
        
        if result is not None:
            self.statistics.register_results(result)
        self.typing_display.update_display(self.typing_test.original_text, self.typing_test.typed_text)
        self.statistics_board.update(
            self.statistics.wpm(self.timer.elapsed()),
            self.statistics.accuracy(),
            self.statistics.errors
        )
        
    def update_timer(self):
        if self.started:
            seconds = self.timer.elapsed()
            self.timer_label.update(seconds)
        self.root.after(100, self.update_timer)  # Update every 100 ms
    
    def start(self):
        self.root.mainloop()