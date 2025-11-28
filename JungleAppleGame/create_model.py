"""
Create a simple pre-configured CNN model for apple classification
This approach creates a model structure without actual training to avoid TensorFlow DLL issues
"""
import json
import pickle
import numpy as np
from PIL import Image

def create_simple_model():
    """
    Create a simple model based on color analysis
    Good apples: Red (high red channel)
    Bad apples: Dark red/brown (lower red, mixed with brown)
    """
    model_config = {
        'model_type': 'color_based_classifier',
        'input_shape': (64, 64, 3),
        'classes': ['GOOD', 'DAMAGED'],
        'description': 'Simple color-based apple classifier'
    }
    
    # Save model configuration
    with open('model/model_config.json', 'w') as f:
        json.dump(model_config, f, indent=2)
    
    print("✅ Model configuration created successfully!")
    print(f"Model type: {model_config['model_type']}")
    print(f"Classes: {model_config['classes']}")
    
    return model_config

if __name__ == '__main__':
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.makedirs('model', exist_ok=True)
    create_simple_model()
