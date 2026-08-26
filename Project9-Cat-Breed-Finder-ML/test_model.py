# test_model_direct.py
from PIL import Image
import numpy as np
from app.model import CatBreedClassifier

# Initialize
classifier = CatBreedClassifier()

# Load a test image
test_images = np.load('data/test_images.npy')
test_labels = np.load('data/test_labels.npy')

# Convert first test image to PIL
img_array = (test_images[0] * 255).astype(np.uint8)
pil_img = Image.fromarray(img_array)

# Predict
result = classifier.predict(pil_img)
print("Prediction:", result)