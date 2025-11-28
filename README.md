Jungle Apple Collection Simulation with CNN-Based Apple Quality Prediction
Project Overview

This project is an interactive jungle simulation game where a character collects apples. A Convolutional Neural Network (CNN) is integrated to classify the collected apples as either "Good" or "Damaged". The game logic controls the player's movements and apple interactions, while the machine learning model provides real-time quality predictions.

This submission fulfills the technical assessment requirement for JG Tech Group.

CNN Model Overview

Model Type: Convolutional Neural Network (CNN)

Framework: TensorFlow/Keras (or PyTorch)

Classes: Good Apple, Damaged Apple

Input Size: 64x64 RGB images

Model File: apple_quality_model.h5 (or .pt, .tflite)

Training Data: Apple images collected from open sources or self-created dataset

The trained model is loaded in real time during gameplay to validate apple quality.

Features

Interactive game using Pygame

Real-time apple quality prediction using CNN

Score increases only if apple is good

Modular codebase (game and ML logic separated)

Works on Windows, macOS, and Linux

Project Structure
JGTechGroup_FullStackAssessment_YourName/
│
├── source_code/
│   ├── game/
│   │   ├── main.py
│   │   ├── sprites.py
│   │   └── utils.py
│   └── ml_model/
│       ├── apple_predictor.py
│       └── model_loader.py
│
├── model/
│   └── apple_quality_model.h5
│
├── requirements.txt
├── README.md
└── demo_video.mp4 (optional)

Installation and Setup
Step 1: Create a virtual environment
python -m venv venv

Step 2: Activate the environment

Windows:

venv\Scripts\activate


Mac/Linux:

source venv/bin/activate

Step 3: Install dependencies
pip install -r requirements.txt

Step 4: Place the trained model in the model/ folder
How to Run the Game
cd source_code/game
python main.py

Integration Logic (Game + CNN)

When an apple is collected, the image is captured.

Image is sent to the model for prediction.

If prediction is "Good", score increases.

If "Damaged", feedback is shown and score does not increase.

Example snippet:

from model_loader import predict_apple_quality

prediction = predict_apple_quality(image_path)
if prediction == "Good":
    score += 1
else:
    show_damaged_feedback()

Model Training Summary

Framework: TensorFlow/Keras

Loss Function: Binary Crossentropy

Optimizer: Adam

Batch Size: 32

Epochs: 20–30

Techniques Used: Image normalization and augmentation

Training notebook is included in the ml_model folder.

Technologies Used
Component	Technology
Game Development	Pygame
Machine Learning	TensorFlow / PyTorch
Image Processing	OpenCV, PIL
Language	Python
IDE	VS Code / PyCharm
Possible Future Improvements

Use object detection to automatically detect apples in game scene

Add sound and advanced animations

Build web-based version using Flask or FastAPI

Extend CNN for multi-class defect classification

Contact

Developer: Your Name
Email: bkmce129@gmail.com
