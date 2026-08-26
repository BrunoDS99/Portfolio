import os
import numpy as np
import tensorflow as tf
import json
from PIL import Image

class CatBreedClassifier: #Identidy cat breeds from images
    def __init__(self, model_path = 'models/cat_breed_model.h5', breeds_path='data/cat_breeds.json'):
        print("Loading the model")
        self.model = tf.keras.models.load_model(model_path)
        
        with open(breeds_path, 'r') as f:
            self.cat_breeds = json.load(f)
            
        print(f"Model Loaded! Can classify {len(self.cat_breeds)} cat breeds")
    
    def preprocess_image(self, image):
        #resize to 224x224
        
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        img = image.resize((224, 224))
        img_array = np.array(img)
        
        if len(img_array.shape) == 3 and img_array.shape[-1] == 4:
            img_array = img_array[:, :, :3]
            
        img_array = img_array.astype('float32') / 255.0    
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    
    def predict(self, image, top_k=3):
        img_array = self.preprocess_image(image)
        predictions = self.model.predict(img_array, verbose=0)
        
        top_k_idx = np.argsort(predictions[0])[-top_k:][::-1]
        
        results = []
        for idx in top_k_idx:
            results.append({
                'breed': self.cat_breeds[idx],
                'confidence': float(predictions[0][idx] * 100)
            })
            
        return results