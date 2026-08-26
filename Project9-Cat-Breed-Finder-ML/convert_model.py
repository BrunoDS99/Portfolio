# convert_to_keras_format.py
import tensorflow as tf

print("Loading original .h5 model...")
model = tf.keras.models.load_model('models/cat_breed_model.h5', compile=False)

print("Saving in .keras format...")
model.save('models/cat_breed_model.keras')

print("Done! Model saved as .keras format")