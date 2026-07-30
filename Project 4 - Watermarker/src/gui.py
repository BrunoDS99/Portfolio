import tkinter as tk
from tkinter import filedialog, ttk

from PIL import ImageTk
from src.image_utils import load_image, resize_image
from src.config import WatermarkSettings
from src import window_config
from src.watermark import add_text_watermark, add_logo_watermark

class Watermarker:
    
    def __init__(self):
        self.window = tk.Tk()
        
        self.window.title(window_config.WINDOW_TITLE)
        self.window.geometry(f"{window_config.WINDOW_WIDTH}x{window_config.WINDOW_HEIGHT}")
        self.window.configure(bg=window_config.BACKGROUND_COLOR)
        self.current_image_path = None
        self.logo_path = None
        self.logo_scale = tk.DoubleVar(value=0.2)
        self.watermark_type = tk.StringVar(value="text")
        
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
        
        # Toolbar buttons
        toolbar_left = tk.Frame(self.toolbar, bg=window_config.FRAME_COLOR)
        toolbar_left.pack(side="left", padx=10, pady=5)
        
        toolbar_right = tk.Frame(self.toolbar, bg=window_config.FRAME_COLOR)
        toolbar_right.pack(side="right", padx=10, pady=5)
        
        self.open_button = tk.Button(
            toolbar_left,
            text="Open Image",
            command=self.open_image,
            font=window_config.BUTTON_FONT,
            bg=window_config.BUTTON_COLOR,
            fg="white",
            padx=10,
            pady=5
        )
        self.open_button.pack(side="left", padx=5)
        
        self.save_button = tk.Button(
            toolbar_left,
            text="Save Image",
            command=self.save_image,
            font=window_config.BUTTON_FONT,
            bg=window_config.BUTTON_COLOR,
            fg="white",
            padx=10,
            pady=5
        )
        self.save_button.pack(side="left", padx=5)
        
        self.apply_button = tk.Button(
            toolbar_right,
            text="Apply Watermark",
            command=self.apply_watermark,
            font=window_config.BUTTON_FONT,
            bg=window_config.BUTTON_COLOR,
            fg="white",
            padx=10,
            pady=5
        )
        self.apply_button.pack(side="left", padx=5)
        
        self.settings_button = tk.Button(
            toolbar_right,
            text="Print Settings",
            command=lambda: print(self.get_settings()),
            font=window_config.BUTTON_FONT,
            bg=window_config.BUTTON_COLOR,
            fg="white",
            padx=10,
            pady=5
        )
        self.settings_button.pack(side="left", padx=5)
        
        self.image_label = tk.Label(self.preview_frame, bg="white")
        self.image_label.pack(expand=True)

        # Controls - organized into sections
        controls = self.controls_frame
        
        # Left section - Watermark Type
        left_section = tk.LabelFrame(controls, text="Watermark Type", bg=window_config.FRAME_COLOR)
        left_section.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        tk.Radiobutton(left_section, text="Text", variable=self.watermark_type, value="text", bg=window_config.FRAME_COLOR).pack(anchor="w", padx=10, pady=5)
        tk.Radiobutton(left_section, text="Logo", variable=self.watermark_type, value="logo", bg=window_config.FRAME_COLOR).pack(anchor="w", padx=10, pady=5)
        
        self.logo_button = tk.Button(
            left_section,
            text="Upload Logo",
            command=self.upload_logo,
            font=window_config.BUTTON_FONT,
            bg=window_config.BUTTON_COLOR,
            fg="white"
        )
        self.logo_button.pack(pady=10, padx=10)
        
        tk.Label(left_section, text="Logo Scale", bg=window_config.FRAME_COLOR).pack(anchor="w", padx=10)
        tk.Scale(
            left_section,
            from_=0.05,
            to=0.5,
            resolution=0.05,
            orient="horizontal",
            variable=self.logo_scale
        ).pack(padx=10, pady=5, fill="x")
        
        # Middle section - Text Settings
        middle_section = tk.LabelFrame(controls, text="Text Settings", bg=window_config.FRAME_COLOR)
        middle_section.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        tk.Label(middle_section, text="Watermark Text", bg=window_config.FRAME_COLOR).pack(anchor="w", padx=10, pady=(10, 0))
        tk.Entry(middle_section, textvariable=self.watermark_text).pack(padx=10, pady=5, fill="x")
        
        tk.Label(middle_section, text="Font Size", bg=window_config.FRAME_COLOR).pack(anchor="w", padx=10, pady=(10, 0))
        tk.Scale(middle_section, from_=10, to=100, orient="horizontal", variable=self.font_size).pack(padx=10, pady=5, fill="x")
        
        tk.Label(middle_section, text="Opacity", bg=window_config.FRAME_COLOR).pack(anchor="w", padx=10, pady=(10, 0))
        tk.Scale(middle_section, from_=0, to=255, orient="horizontal", variable=self.opacity).pack(padx=10, pady=5, fill="x")
        
        # Right section - Position
        right_section = tk.LabelFrame(controls, text="Position", bg=window_config.FRAME_COLOR)
        right_section.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        
        positions = [
            ("Top Left", "top_left"),
            ("Top Right", "top_right"),
            ("Bottom Left", "bottom_left"),
            ("Bottom Right", "bottom_right")
        ]
        
        for text, value in positions:
            tk.Radiobutton(right_section, text=text, variable=self.position, value=value, bg=window_config.FRAME_COLOR).pack(anchor="w", padx=10, pady=5)
        
        # Configure grid weights
        controls.grid_columnconfigure(0, weight=1)
        controls.grid_columnconfigure(1, weight=1)
        controls.grid_columnconfigure(2, weight=1)
        
        self.preview_output_path = None
        
    def open_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Images", "*.png *.jpg *.jpeg")
            ]
        )
        
        print(file_path)
        
        if file_path:
            
            self.current_image_path = file_path
            self.update_preview(file_path)
            

    def update_preview(self, image_path):
        image = load_image(image_path)
        image = resize_image(image)
        
        self.preview_image = ImageTk.PhotoImage(image)
        
        self.image_label.config(image=self.preview_image)
    
    def get_settings(self):

        return WatermarkSettings(
            text=self.watermark_text.get(),
            font_size=self.font_size.get(),
            opacity=self.opacity.get(),
            position=self.position.get(),
            logo_scale=self.logo_scale.get()
        )
        
    def upload_logo(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("PNG Images", "*.png"),
            ("Images", "*.png *.jpg *.jpeg")    
            ]
        )
        
        if file_path:
            self.logo_path = file_path
            
            print("Logo selected", file_path)    
     
    def apply_watermark(self):
        if not self.current_image_path:
            print("no image selected")
            return
        
        settings = self.get_settings()
        self.preview_output_path = "assets/temp_result.png"
        
        if self.watermark_type.get() == "text":
            add_text_watermark(self.current_image_path, self.preview_output_path, settings)
        
        elif self.watermark_type.get() == "logo":
            if not self.logo_path:
                print("No logo selected")
                return
            
            add_logo_watermark(
                self.current_image_path,
                self.logo_path,
                self.preview_output_path,
                settings  # Pass the settings object that includes logo_scale
            )
        
        self.update_preview(self.preview_output_path)     
        print("Watermark applied.")
    
    def save_image(self):
        if not self.preview_output_path:
            print("No image available")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG Image", "*.png"),
                ("JPEG Image", "*.jpeg"),
            ]
        )
        
        if save_path:
            image = load_image(self.preview_output_path)
            if not save_path.lower().endswith((".png", ".jpg", ".jpeg")):
                save_path += ".png"
            image.save(save_path)
            print("Saved:", save_path)
            
    def run(self):
        self.window.mainloop()