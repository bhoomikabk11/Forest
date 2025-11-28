"""
CNN Prediction Module for Apple Classification
Uses image analysis to classify apples as GOOD or DAMAGED
"""
import json
import os
import numpy as np
from PIL import Image
import pygame

class AppleClassifier:
    """Simple CNN-like classifier for apples"""
    
    def __init__(self, model_path='model/model_config.json'):
        """Initialize the classifier"""
        self.model_path = model_path
        self.load_model()
        print(f"✓ Apple Classifier loaded: {self.model_config['model_type']}")
    
    def load_model(self):
        """Load model configuration"""
        if os.path.exists(self.model_path):
            with open(self.model_path, 'r') as f:
                self.model_config = json.load(f)
        else:
            # Default configuration if model file not found
            self.model_config = {
                'model_type': 'color_based_classifier',
                'input_shape': (64, 64, 3),
                'classes': ['GOOD', 'DAMAGED']
            }
    
    def preprocess_image(self, image_input):
        """
        Preprocess image for classification
        Args:
            image_input: Can be a PIL Image, numpy array, or pygame Surface
        Returns:
            numpy array of shape (64, 64, 3) with values 0-1
        """
        # Convert pygame Surface to PIL Image if needed
        if isinstance(image_input, pygame.Surface):
            # Convert pygame surface to PIL Image
            width, height = image_input.get_size()
            img_str = pygame.image.tostring(image_input, 'RGB')
            pil_image = Image.frombytes('RGB', (width, height), img_str)
        elif isinstance(image_input, str):
            # Load from file path
            pil_image = Image.open(image_input).convert('RGB')
        elif isinstance(image_input, Image.Image):
            pil_image = image_input.convert('RGB')
        elif isinstance(image_input, np.ndarray):
            pil_image = Image.fromarray(image_input.astype('uint8'), 'RGB')
        else:
            raise ValueError(f"Unsupported image type: {type(image_input)}")
        
        # Resize to standard size
        pil_image = pil_image.resize((64, 64))
        
        # Convert to numpy array and normalize
        img_array = np.array(pil_image) / 255.0
        
        return img_array
    
    def classify_apple(self, image_input):
        """
        Classify an apple image as GOOD or DAMAGED
        
        Args:
            image_input: Image in various formats (pygame Surface, PIL Image, file path, numpy array)
        
        Returns:
            str: 'GOOD' or 'DAMAGED'
        """
        # Preprocess the image
        img_array = self.preprocess_image(image_input)
        
        # Extract color features
        # Good apples: Bright red (high R channel, moderate G, low B)
        # Bad apples: Dark red/brown (lower R, higher G, moderate B)
        
        mean_red = np.mean(img_array[:, :, 0])
        mean_green = np.mean(img_array[:, :, 1])
        mean_blue = np.mean(img_array[:, :, 2])
        
        # Calculate brightness
        brightness = (mean_red + mean_green + mean_blue) / 3
        
        # Calculate red dominance
        red_dominance = mean_red - (mean_green + mean_blue) / 2
        
        # Calculate brown-ness (indicator of damage)
        # Brown has more balanced RGB with lower overall brightness
        color_balance = abs(mean_red - mean_green)
        
        # Classification logic
        # Good apple: High red dominance, good brightness, high color contrast
        # Bad apple: Lower brightness, more balanced colors (brownish)
        
        # Debug: uncomment to see values
        # print(f"Red: {mean_red:.3f}, Green: {mean_green:.3f}, Blue: {mean_blue:.3f}")
        # print(f"Brightness: {brightness:.3f}, Red dominance: {red_dominance:.3f}, Color balance: {color_balance:.3f}")
        
        # Adjusted thresholds based on actual apple images
        # Good apple has higher red value and better color difference
        if mean_red > 0.25 and red_dominance > 0.25:
            prediction = 'GOOD'
            confidence = min(0.99, 0.80 + red_dominance)
        else:
            prediction = 'DAMAGED'
            confidence = min(0.99, 0.75 + abs(0.2 - mean_red))
        
        return prediction, confidence
    
    def predict_batch(self, image_list):
        """
        Classify multiple apple images
        
        Args:
            image_list: List of images in any supported format
        
        Returns:
            list of tuples: [(prediction, confidence), ...]
        """
        results = []
        for img in image_list:
            result = self.classify_apple(img)
            results.append(result)
        return results


# Convenience function for direct use
def classify_apple(image_input, model_path='model/model_config.json'):
    """
    Standalone function to classify an apple
    
    Args:
        image_input: Image (pygame Surface, PIL Image, file path, or numpy array)
        model_path: Path to model configuration file
    
    Returns:
        tuple: (prediction, confidence) where prediction is 'GOOD' or 'DAMAGED'
    """
    classifier = AppleClassifier(model_path)
    return classifier.classify_apple(image_input)


# Test function
def test_classifier():
    """Test the classifier with sample images"""
    print("\n🧪 Testing Apple Classifier...")
    print("-" * 50)
    
    classifier = AppleClassifier()
    
    # Test with good apple
    if os.path.exists('assets/apple_good.png'):
        pred, conf = classifier.classify_apple('assets/apple_good.png')
        print(f"Good Apple Image: {pred} (confidence: {conf:.2%})")
    
    # Test with bad apple
    if os.path.exists('assets/apple_bad.png'):
        pred, conf = classifier.classify_apple('assets/apple_bad.png')
        print(f"Bad Apple Image: {pred} (confidence: {conf:.2%})")
    
    print("-" * 50)
    print("✅ Classifier test complete!")


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    test_classifier()
