import tkinter as tk
from tkinter import messagebox

from config.settings import (WINDOW_TITLE, WINDOW_HEIGHT, WINDOW_WIDTH, BACKGROUND_COLOR)
from data.word_generator import generate_random_words
from ui.typing_display import TypingDisplay
from core.typing_test import TypingTest
from core.statistics import Statistics 
from ui.statistics_board import StatisticsBoard
from core.timer import Timer
from ui.timer_label import TimerLabel
from core.statistics import Statistics
from ui.controls import Controls
from ui.header import Header
from core.score_manager import ScoreManager

class AppWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(900,800)
        self.root.configure(background=BACKGROUND_COLOR)
        self.timer = Timer()
        self.started = False
        self.statistics = Statistics()
        self.score_manager = ScoreManager()
        
        #Main Container
        self.main_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        self.main_frame.pack(expand=True, fill="both", padx=60, pady=40)
        
        self.create_widgets()
        self.update_timer()  # Start the timer update loop
        
    
    def create_widgets(self):
        text = generate_random_words(50)
        self.typing_test = TypingTest(text)
        self.header = Header(self.main_frame)
        self.statistics = Statistics()
        self.statistics_board = StatisticsBoard(self.root)
        self.typing_display = TypingDisplay(self.root)
        self.typing_display.update_display(text, "")
        self.timer_label = TimerLabel(self.root)
        self.controls = Controls(self.root, self.start_test, self.restart_test)
        self.root.bind("<Key>", self.handle_keypress)
       
    def handle_keypress(self, event):
        
        if not self.started:
            return
        
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
        
        if self.typing_test.finished:
            self.finish_test()
        
    def update_timer(self):
        if self.started:
            elapsed = self.timer.elapsed()
            self.timer_label.update(elapsed)
        self.root.after(100, self.update_timer)  # Update every 100 ms
    
    def start_test(self):
        self.root.focus_set()
        self.started = False
        self.timer = Timer()
        self.statistics = Statistics()
    
    def restart_test(self):
        text = generate_random_words(50)
        self.typing_test = TypingTest(text)
        self.statistics = Statistics()
        self.timer = Timer()
        self.started = False
        
        self.typing_display.update_display(text, "")
        self.statistics_board.update(0, 100, 0)
    
    def finish_test(self):
        self.timer.stop()
        self.started = False
        elapsed = self.timer.elapsed()
        wpm = self.statistics.wpm(elapsed)
        accuracy = self.statistics.accuracy()
        
        self.score_manager.save_score(wpm, accuracy, self.statistics.errors)

        self.score_manager.save_score(wpm, accuracy, self.statistics.errors)

        messagebox.showinfo(
            "Test Complete",
            (
                f"WPM: {wpm}\n"
                f"Accuracy: {accuracy}%\n"
                f"Errors: {self.statistics.errors}\n\n"
            )
        )

    def start(self):
        self.root.mainloop()