from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from src.config import WatermarkSettings


BASE_DIR = Path(__file__).resolve().parent.parent

image_path = BASE_DIR / "assets" / "photo.jpg"
output_path = BASE_DIR / "assets" / "watermarked.jpg"

def add_text_watermark(image_path, output_path, settings):
    image = Image.open(image_path).convert("RGBA")
    overlay = Image.new(
    "RGBA",
    image.size,
    (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    font = ImageFont.truetype("arial.ttf", settings.font_size)
    
    text_box = draw.textbbox(
        (0,0),
        settings.text,
        font=font
    )
    
    text_width = text_box[2] - text_box[0]   
    text_height = text_box[3] - text_box[1]
    
    if settings.position == "bottom_right": #keep text in the bottom right
        position = (
            image.width - text_width - 20,
            image.height - text_height -20
        )
    
    elif settings.position == "top_left":
        position = (20, 20)
        
    elif settings.position == "top_right":
        position = (
            image.width - text_width - 20, 
            20)
        
    else:
        position = (20, 20)
        
        
    draw.text(
        position,
        settings.text,
        font=font,
        fill=(255, 255, 255, settings.opacity)
    )
    
    watermakerd = Image.alpha_composite(
        image,
        overlay
    )
    
    watermakerd.convert("RGB").save(output_path)
    
def load_image(image_path):
    try:
        return Image.open(image_path)
    except FileNotFoundError:
        print("File not found")
        
    except Exception as e:
        print("Error loading image: {e}")
        
def add_logo_watermark(image_path, logo_path, output_path, settings):
    # Open images
    image = Image.open(image_path).convert("RGBA")
    logo = Image.open(logo_path).convert("RGBA")
    
    # Calculate new size based on logo_scale from settings
    new_width = int(image.width * settings.logo_scale)
    ratio = new_width / logo.width
    new_height = int(logo.height * ratio)
    logo = logo.resize((new_width, new_height))
    
    # Apply opacity to the resized logo
    if logo.mode == 'RGBA':
        # Split the logo into RGB and Alpha channels
        r, g, b, a = logo.split()
        # Apply opacity to alpha channel
        a = a.point(lambda p: int(p * settings.opacity / 255))
        # Merge back
        logo = Image.merge('RGBA', (r, g, b, a))
    
    # Position the logo
    if settings.position == "bottom_right":
        position = (
            image.width - logo.width - 20,
            image.height - logo.height - 20
        )
    elif settings.position == "top_left":
        position = (20, 20)
    elif settings.position == "top_right":
        position = (
            image.width - logo.width - 20,
            20
        )
    elif settings.position == "bottom_left":
        position = (20, image.height - logo.height - 20)
    else:
        position = (20, 20)  # Default to top-left
    
    # Composite the logo onto the image
    image.alpha_composite(logo, position)
    image.convert("RGB").save(output_path)
    print(f"Logo watermark applied with opacity: {settings.opacity}")