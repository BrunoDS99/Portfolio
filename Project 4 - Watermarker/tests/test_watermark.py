from src.watermark import add_logo_watermark
from src.config import WatermarkSettings


settings = WatermarkSettings(
    position="bottom_right",
    logo_scale=0.2
)


add_logo_watermark(
    "assets/photo.jpg",
    "assets/logo.png",
    "assets/logo_result.jpg",
    settings
)