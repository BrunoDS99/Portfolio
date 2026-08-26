import tensorflow as tf
import tensorflow_datasets as tfds
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from PIL import Image
import os

# Suppress warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

print("Loading dataset...")
dataset, info = tfds.load('oxford_iiit_pet', with_info=True, as_supervised=True)
all_breeds = info.features['label'].names

# Identify cat breeds (capitalized names)
cat_breeds = [breed for breed in all_breeds if breed[0].isupper()]
cat_breed_indices = [all_breeds.index(breed) for breed in cat_breeds]
print(f"\nCat breeds ({len(cat_breeds)}):")
for i, breed in enumerate(cat_breeds):
    print(f"  {i}: {breed}")

# Convert dataset to numpy arrays, filtering cats only and resizing
def get_cat_data(dataset, cat_breed_indices, target_size=(224, 224)):
    images = []
    labels = []
    
    print("Processing images (this may take a minute)...")
    for i, (image, label) in enumerate(tfds.as_numpy(dataset)):
        if label in cat_breed_indices:
            # Resize image to target size
            img = Image.fromarray(image)
            img = img.resize(target_size)
            img_array = np.array(img)
            
            # Ensure it's RGB (3 channels)
            if img_array.shape == (target_size[0], target_size[1], 3):
                images.append(img_array)
                labels.append(label)
        
        # Print progress
        if (i + 1) % 500 == 0:
            print(f"  Processed {i + 1} images...")
    
    return np.array(images), np.array(labels)

# Process training data
train_images, train_labels = get_cat_data(dataset['train'], cat_breed_indices)
print(f"Training images: {train_images.shape}")
print(f"Training labels: {train_labels.shape}")

# Process test data
test_images, test_labels = get_cat_data(dataset['test'], cat_breed_indices)
print(f"Test images: {test_images.shape}")
print(f"Test labels: {test_labels.shape}")

# Remap labels to 0-11
def remap_labels(labels, cat_breed_indices):
    label_map = {original: new for new, original in enumerate(cat_breed_indices)}
    return np.array([label_map[label] for label in labels])

train_labels_remapped = remap_labels(train_labels, cat_breed_indices)
test_labels_remapped = remap_labels(test_labels, cat_breed_indices)

print(f"\nRemapped training labels: {train_labels_remapped[:10]}")
print(f"Unique labels in training: {np.unique(train_labels_remapped)}")

# Show distribution
print("\n=== Images per Cat Breed (Training) ===")
breed_counts = Counter(train_labels_remapped)
for idx, count in sorted(breed_counts.items()):
    print(f"{cat_breeds[idx]}: {count}")

print("\n=== Images per Cat Breed (Test) ===")
test_breed_counts = Counter(test_labels_remapped)
for idx, count in sorted(test_breed_counts.items()):
    print(f"{cat_breeds[idx]}: {count}")


# Save data
np.save('train_images.npy', train_images)
np.save('train_labels.npy', train_labels_remapped)
np.save('test_images.npy', test_images)
np.save('test_labels.npy', test_labels_remapped)

# Save breed names
import json
with open('cat_breeds.json', 'w') as f:
    json.dump(cat_breeds, f)

print("Data saved successfully!")
print(f"\nSummary:")
print(f"  - {len(cat_breeds)} cat breeds")
print(f"  - {len(train_images)} training images")
print(f"  - {len(test_images)} test images")