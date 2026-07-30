from PIL import Image, ImageDraw, ImageFont
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

image_path = BASE_DIR / "assets" / "photo.jpg"
output_path = BASE_DIR / "assets" / "watermarked.jpg"

def add_text_watermark(image_path, text, output_path):
    image = Image.open(image_path)
    
    draw = ImageDraw.Draw(image)
    
    font = ImageFont.load_default()
    
    position = (
        image.width - 150,
        image.height - 30
    )
    
    draw.text(
        position,
        text,
        font=font,
        fill="white"
    )
    
    image.save(output_path)
    

add_text_watermark(
    image_path,
    "mywebsite.com",
    output_path
)