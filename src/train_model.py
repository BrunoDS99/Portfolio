import tensorflow as tf
import numpy as np
import json
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import os
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix

# Suppress warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Load the data
print("Loading data...")
train_images = np.load('data/train_images.npy')
train_labels = np.load('data/train_labels.npy')
test_images = np.load('data/test_images.npy')
test_labels = np.load('data/test_labels.npy')

with open('data/cat_breeds.json', 'r') as f:
    cat_breeds = json.load(f)

print(f"Training images: {train_images.shape}")
print(f"Training labels: {train_labels.shape}")
print(f"Test images: {test_images.shape}")
print(f"Test labels: {test_labels.shape}")
print(f"Number of breeds: {len(cat_breeds)}")

# Normalize pixel values to [0, 1]
print("\nNormalizing images...")
train_images = train_images.astype('float32') / 255.0
test_images = test_images.astype('float32') / 255.0

# Create validation set from training data
X_train, X_val, y_train, y_val = train_test_split(
    train_images, train_labels, 
    test_size=0.2, 
    random_state=42,
    stratify=train_labels
)

print(f"\nTraining set: {X_train.shape}")
print(f"Validation set: {X_val.shape}")
print(f"Test set: {test_images.shape}")

# Data augmentation using tf.image
def augment_image(image):

    if tf.random.uniform(()) > 0.5:
        image = tf.image.flip_left_right(image)
    if tf.random.uniform(()) > 0.5:
        image = tf.image.rot90(image)
    image = tf.image.random_brightness(image, max_delta=0.1)
    
    return image

def augment_dataset(images, labels):
    """Apply augmentation to a batch of images"""
    augmented_images = tf.map_fn(augment_image, images)
    return augmented_images, labels

# Build the model
def create_model(num_classes):
    # Load pre-trained MobileNetV2 without top layer
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(224, 224, 3),
        include_top=False,
        weights='imagenet'
    )
    
    # Freeze the base model
    base_model.trainable = False
    
    # Build the full model
    model = tf.keras.Sequential([
        base_model,
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(num_classes, activation='softmax')
    ])
    
    return model

# Create the model
print("\nCreating model...")
model = create_model(len(cat_breeds))

# Compile the model
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Print model summary
model.summary()

# Callbacks
callbacks = [
    tf.keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True, monitor='val_accuracy'),
    tf.keras.callbacks.ReduceLROnPlateau(factor=0.2, patience=3, monitor='val_loss', min_lr=1e-6),
    tf.keras.callbacks.ModelCheckpoint('models/best_model.h5', save_best_only=True, monitor='val_accuracy')
]

# Train the model
print("\nStarting training...")
history = model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=30,
    batch_size=32,
    callbacks=callbacks,
    verbose=1
)

# Evaluate on test set
print("\nEvaluating on test set...")
test_loss, test_accuracy = model.evaluate(test_images, test_labels, verbose=0)
print(f"Test accuracy: {test_accuracy:.4f}")
print(f"Test loss: {test_loss:.4f}")

# Save the final model
model.save('models/cat_breed_model.h5')
print("\nModel saved as 'cat_breed_model.h5'")

# Plot training history
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

plt.tight_layout()
plt.savefig('visualizations/training_history.png')
plt.show()

# Print final metrics
print("\n=== Training Summary ===")
print(f"Best validation accuracy: {max(history.history['val_accuracy']):.4f}")
print(f"Test accuracy: {test_accuracy:.4f}")

# Get predictions
test_predictions = model.predict(test_images)
test_pred_classes = np.argmax(test_predictions, axis=1)

# Print classification report
print("\n=== Classification Report ===")
print(classification_report(test_labels, test_pred_classes, target_names=cat_breeds))

# Plot confusion matrix
plt.figure(figsize=(12, 10))
cm = confusion_matrix(test_labels, test_pred_classes)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=cat_breeds, yticklabels=cat_breeds)
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig('visualizations/confusion_matrix.png')
plt.show()