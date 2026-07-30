from dataclasses import dataclass

@dataclass
class WatermarkSettings:
    text: str = ""
    font_size: int = 35 
    opacity: int = 128
    position: str = "bottom_right"
    
    logo_path: str = None
    logo_opacity: float = 0.5
    logo_scale: float = 0.2