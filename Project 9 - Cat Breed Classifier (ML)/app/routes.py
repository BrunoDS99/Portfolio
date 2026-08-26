from flask import Blueprint, request, render_template, jsonify
from PIL import Image
import io, os, warnings, traceback
from app.model import CatBreedClassifier

main_bp = Blueprint('main', __name__)
classifier = None

def get_classifier():
    global classifier
    if classifier is None:
        classifier = CatBreedClassifier()
    return classifier

@main_bp.route('/')
def index():
    classifier = get_classifier()
    return render_template('index.html', breeds=classifier.cat_breeds)

@main_bp.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    # Check if filename is empty
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400
    
    try:
        # Read the file data into memory
        file_data = file.read()
        
        # Check if file is empty
        if not file_data or len(file_data) == 0:
            return jsonify({'success': False, 'error': 'Empty file received'}), 400
        
        # Open image from bytes
        img = Image.open(io.BytesIO(file_data))
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Get classifier and predict
        classifier_instance = get_classifier()
        predictions = classifier_instance.predict(img)
        
        # Return results
        return jsonify({
            'success': True,
            'top_prediction': predictions[0]['breed'],
            'confidence': predictions[0]['confidence'],
            'all_predictions': predictions
        })
        
    except Exception as e:
        # Log the full error for debugging
        print(f"Error in predict route: {str(e)}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500