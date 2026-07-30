from dataclasses import dataclass


@dataclass
class WatermarkSettings:
    text: str = ""
    font_size: int = 40
    opacity: int = 128
    position: str = "bottom_right"
    logo_scale: float = 0.2