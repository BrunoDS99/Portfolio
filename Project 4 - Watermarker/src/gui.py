import tkinter as tk
from tkinter import filedialog

class Watermarker:
    
    def __init__(self):
        self.window = tk.Tk()
        
        self.window.title("Image Watermarker")
        self.window.geometry("800x600")
        
        self.open_button = tk.Button(
            self.window,
            text="Open Image",
            command=self.open_image
        )
        
        self.open_button.pack(
            pady=20
        )
        
    def open_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Images", "*.png *.jpg *.jpeg")
            ]
        )
        print(file_path)
    
    def run(self):
        self.window.mainloop()