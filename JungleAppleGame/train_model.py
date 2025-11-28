"""
Script to create and train a simple CNN model for apple classification
"""
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
from PIL import Image
import os

def create_training_data():
    """
    Generate synthetic training data based on apple images
    Since we have limited real images, we'll create variations
    """
    # Load the base apple images
    good_apple = Image.open('assets/apple_good.png').convert('RGB')
    bad_apple = Image.open('assets/apple_bad.png').convert('RGB')
    
    # Resize to standard size
    img_size = (64, 64)
    good_apple = good_apple.resize(img_size)
    bad_apple = bad_apple.resize(img_size)
    
    # Convert to numpy arrays
    good_array = np.array(good_apple) / 255.0
    bad_array = np.array(bad_apple) / 255.0
    
    # Create augmented dataset
    X_train = []
    y_train = []
    
    # Generate 500 variations of good apples
    for i in range(500):
        # Add slight random noise for variation
        noise = np.random.normal(0, 0.05, good_array.shape)
        augmented = np.clip(good_array + noise, 0, 1)
        X_train.append(augmented)
        y_train.append([1, 0])  # [good, bad]
    
    # Generate 500 variations of bad apples
    for i in range(500):
        noise = np.random.normal(0, 0.05, bad_array.shape)
        augmented = np.clip(bad_array + noise, 0, 1)
        X_train.append(augmented)
        y_train.append([0, 1])  # [good, bad]
    
    # Shuffle the data
    indices = np.random.permutation(len(X_train))
    X_train = np.array(X_train)[indices]
    y_train = np.array(y_train)[indices]
    
    return X_train, y_train

def create_cnn_model():
    """Create a simple CNN model for binary classification"""
    model = keras.Sequential([
        # Input layer
        layers.Input(shape=(64, 64, 3)),
        
        # First convolutional block
        layers.Conv2D(32, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        
        # Second convolutional block
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        
        # Third convolutional block
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        
        # Flatten and dense layers
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(2, activation='softmax')  # 2 classes: good, bad
    ])
    
    return model

def train_and_save_model():
    """Train the model and save it"""
    print("🔄 Generating training data...")
    X_train, y_train = create_training_data()
    
    print(f"✓ Training data shape: {X_train.shape}")
    print(f"✓ Labels shape: {y_train.shape}")
    
    print("\n🔄 Creating CNN model...")
    model = create_cnn_model()
    
    print("\n📊 Model Summary:")
    model.summary()
    
    # Compile the model
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    print("\n🔄 Training model...")
    history = model.fit(
        X_train, y_train,
        epochs=20,
        batch_size=32,
        validation_split=0.2,
        verbose=1
    )
    
    # Save the model
    os.makedirs('model', exist_ok=True)
    model.save('model/apple_cnn_model.h5')
    print("\n✅ Model saved to model/apple_cnn_model.h5")
    
    # Test the model with original images
    print("\n🧪 Testing model with original images...")
    good_apple = Image.open('assets/apple_good.png').convert('RGB').resize((64, 64))
    bad_apple = Image.open('assets/apple_bad.png').convert('RGB').resize((64, 64))
    
    good_pred = model.predict(np.array([np.array(good_apple) / 255.0]), verbose=0)
    bad_pred = model.predict(np.array([np.array(bad_apple) / 255.0]), verbose=0)
    
    print(f"Good apple prediction: GOOD={good_pred[0][0]:.2f}, BAD={good_pred[0][1]:.2f}")
    print(f"Bad apple prediction: GOOD={bad_pred[0][0]:.2f}, BAD={bad_pred[0][1]:.2f}")
    
    return model

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    train_and_save_model()
