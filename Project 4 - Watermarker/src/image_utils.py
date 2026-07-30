from PIL import Image

def load_image(path):
    return Image.open(path)

def resize_image(image, max_size=(500, 500)):
    image.thumbnail(max_size)
    return image