from app import create_app
import os, warnings

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
warnings.filterwarnings('ignore')

app = create_app()

if __name__ == '__main__':
    app.run(debug=False, port=5000)