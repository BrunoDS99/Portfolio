import tkinter as tk
from tkinter import filedialog, ttk

from PIL import ImageTk
from src.image_utils import load_image, resize_image
from src.config import WatermarkSettings
from src import window_config

class Watermarker:
    
    def __init__(self):
        self.window = tk.Tk()
        
        self.window.title(window_config.WINDOW_TITLE)
        self.window.geometry(f"{window_config.WINDOW_WIDTH}x{window_config.WINDOW_HEIGHT}")
        self.window.configure(bg=window_config.BACKGROUND_COLOR)
        
        self.toolbar = tk.Frame(self.window, bg=window_config.FRAME_COLOR, bd=2, relief="groove")
        self.toolbar.pack(side="top", fill="x", padx=window_config.WINDOW_PADDING, pady=window_config.WINDOW_PADDING)
        self.preview_frame = tk.Frame(self.window, bg=window_config.FRAME_COLOR, bd=2, relief="groove")
        self.preview_frame.pack(expand=True, fill="both", padx=window_config.WINDOW_PADDING)
        self.controls_frame = tk.Frame(self.window, bg=window_config.FRAME_COLOR, bd=2, relief="groove")
        self.controls_frame.pack(side="bottom", fill="x", pady=window_config.WINDOW_PADDING, padx=window_config.WINDOW_PADDING)        
        
        self.current_image = None
        self.preview_image = None
        self.watermark_text = tk.StringVar()
        self.font_size = tk.IntVar(value=40)
        self.opacity = tk.IntVar(value=128)
        self.position = tk.StringVar(
            value="bottom_right"
            )
        
        self.open_button = tk.Button(
            self.toolbar,
            text="Open Image",
            command=self.open_image,
            font= window_config.BUTTON_FONT,
            bg=window_config.BUTTON_COLOR,
            fg="white",
            padx=10,
            pady=5
        )
        
        self.open_button.pack(padx=10, pady=10)
        self.image_label = tk.Label(self.window)
        self.image_label.pack(in_=self.preview_frame, expand=True)

        controls = self.controls_frame
        controls.pack(pady=20)
        
        #Text input
        tk.Label(controls,text="Watermark Text").grid(row=0, column=0)
        tk.Entry(controls, textvariable=self.watermark_text).grid(row=0, column=1)
        
        #Font Size slider
        tk.Label(controls, text="Font Size").grid(row=1, column=0)
        tk.Scale(controls, from_=100, to=100, orient="horizontal", variable=self.font_size).grid(row=1, column=1)
        
        #Opacity Slider
        tk.Label(controls, text="Opacity").grid(row=2, column=0)
        tk.Scale(controls, from_=0, to=255, orient="horizontal", variable=self.opacity).grid(row=2, column=1)
        
        #Settings button 
        tk.Button(controls,text="Print Settings",command=lambda: print(self.get_settings())).grid(row=4, column=0)
        
        positions = [
            ("Top Left", "top_left"),
            ("Top Right", "top_right"),
            ("Bottom Left", "bottom_left"),
            ("Bottom Right", "bottom_right")
            ]
        
        for index, (text, value) in enumerate(positions):
            tk.Radiobutton(controls, text=text, variable=self.position, value=value).grid(row=3, column=index)
        
    def open_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Images", "*.png *.jpg *.jpeg")
            ]
        )
        
        if file_path:
            image = load_image(file_path)
            image = resize_image(image)
            
            self.current_image = image
            self.preview_image = ImageTk.PhotoImage(image) #TKinter cant display Pillow images, so we convert
            self.image_label.config(image=self.preview_image)

    
    def get_settings(self):
        return WatermarkSettings(
            text=self.watermark_text.get(),
            font_size=self.font_size.get(),
            opacity=self.opacity.get(),
            position=self.position.get()
        )
        
        
    def run(self):
        self.window.mainloop()