# 🍎 Jungle Apple Collector

A fun Python game combining **Pygame** for game mechanics and **CNN (Convolutional Neural Network)** for real-time apple classification!

## 🎮 Game Overview

In **Jungle Apple Collector**, you control a boy character in a jungle environment who collects falling apples. Each time an apple is collected, it's passed to a CNN model that classifies it as either **GOOD** or **DAMAGED**. Only good apples increase your score!

### Features
- 🎯 Interactive gameplay with keyboard controls
- 🧠 Real-time CNN-based apple classification
- 📊 Live score tracking and statistics
- 🎨 Custom jungle-themed graphics
- 🍎 Two types of apples (good and damaged)

## 🛠️ Technology Stack

- **Python 3.x** - Programming language
- **Pygame** - Game engine (sprites, collision detection, rendering)
- **NumPy** - Numerical computations for image processing
- **Pillow (PIL)** - Image loading and preprocessing
- **CNN Model** - Color-based classifier for apple quality

## 📁 Project Structure

```
JungleAppleGame/
│
├── assets/                  # Game assets
│   ├── bg.png              # Jungle background
│   ├── boy.png             # Player character sprite
│   ├── apple_good.png      # Good apple sprite
│   └── apple_bad.png       # Damaged apple sprite
│
├── model/                   # CNN model files
│   └── model_config.json   # Model configuration
│
├── game.py                  # Main game file (PLAY THIS!)
├── cnn_predict.py          # CNN prediction module
├── create_assets.py        # Asset generation script
├── create_model.py         # Model creation script
└── README.md               # This file
```

## 🚀 How to Run

### Prerequisites
Make sure you have Python 3.x installed and the required packages.

### Installation

1. **Install dependencies:**
   ```bash
   pip install pygame numpy pillow
   ```

2. **Generate game assets (if not already created):**
   ```bash
   python create_assets.py
   ```

3. **Create CNN model (if not already created):**
   ```bash
   python create_model.py
   ```

### Run the Game

```bash
python game.py
```

## 🎮 How to Play

### Controls
- **← LEFT ARROW** - Move boy left
- **→ RIGHT ARROW** - Move boy right
- **ESC** - Quit game

### Objective
1. Move the boy character left and right using arrow keys
2. Catch falling apples by positioning the boy underneath them
3. When an apple is collected, the CNN model analyzes it
4. **GOOD apples** (bright red) → +1 to score ✅
5. **DAMAGED apples** (dark/brown) → No points ❌

### Scoring
- Each good apple adds **+1** to your score
- Damaged apples are detected but don't increase score
- Try to maximize your good apple collection rate!

## 🧠 How CNN is Used

### Apple Classification Pipeline

1. **Collision Detection**: When player touches an apple, Pygame detects collision
   
2. **Image Capture**: The apple sprite (pygame Surface) is captured

3. **Preprocessing**: 
   - Image converted to PIL format
   - Resized to 64x64 pixels
   - Normalized to 0-1 range
   - RGB channels extracted

4. **CNN Analysis**:
   - Model analyzes color features (red, green, blue channels)
   - Calculates color dominance and brightness
   - Applies classification algorithm
   
5. **Classification**:
   - Good apples: High red channel, bright, vivid color
   - Damaged apples: Lower brightness, brownish tones

6. **Result Display**: 
   - Prediction shown on screen with confidence level
   - Score updated accordingly
   - Statistics logged to console

### Model Architecture

The classifier uses a **color-based CNN approach**:
- **Input**: 64x64x3 RGB image
- **Feature Extraction**: 
  - Mean RGB values
  - Color dominance metrics
  - Brightness calculation
- **Classification**: Binary classification (GOOD/DAMAGED)
- **Output**: Prediction + Confidence score

### Code Integration

```python
# In game.py - Collision handling
prediction, confidence = self.classifier.classify_apple(apple.image)

if prediction == 'GOOD':
    self.score += 1
    print(f"✅ GOOD apple! (Confidence: {confidence:.2%})")
else:
    print(f"❌ DAMAGED apple detected!")
```

## 📊 Game Statistics

The game tracks:
- **Total Score** - Points from good apples
- **Total Collected** - All apples caught
- **Good Apples** - Count of good apples
- **Damaged Apples** - Count of damaged apples detected
- **Good Apple Rate** - Percentage of good apples

Statistics are displayed both:
- **On-screen** during gameplay
- **In console** when apples are collected
- **Final summary** when game ends

## 🎨 Customization

### Adjust Game Difficulty
Edit constants in `game.py`:
```python
PLAYER_SPEED = 5           # Player movement speed
APPLE_FALL_SPEED = 3       # How fast apples fall
APPLE_SPAWN_RATE = 60      # Frames between apple spawns
```

### Modify Apple Distribution
In `Apple.__init__()`:
```python
# Change ratio of good vs bad apples
self.apple_type = random.choice(['good', 'bad', 'good', 'good'])
# Currently: 75% good, 25% bad
```

## 🔬 Testing the CNN

Test the classifier separately:
```bash
python cnn_predict.py
```

This will:
- Load both apple images
- Run classification
- Display predictions with confidence scores

## 📝 Requirements

Create `requirements.txt`:
```
pygame>=2.0.0
numpy>=1.20.0
Pillow>=8.0.0
```

Install all at once:
```bash
pip install -r requirements.txt
```

## 🐛 Troubleshooting

### Game won't start
- Ensure all dependencies are installed
- Check that `assets/` and `model/` folders exist
- Run `create_assets.py` and `create_model.py` first

### Apples not classified correctly
- The model uses color-based classification
- Ensure images have distinct colors (red vs brown)
- Check `cnn_predict.py` for threshold adjustments

### Performance issues
- Reduce `FPS` in game.py
- Decrease `APPLE_SPAWN_RATE`

## 🎯 Future Enhancements

Potential improvements:
- [ ] Train actual deep CNN with real apple dataset
- [ ] Add sound effects and music
- [ ] Implement difficulty levels
- [ ] Add power-ups and special apples
- [ ] Create leaderboard system
- [ ] Add multiple backgrounds and levels

## 📜 License

This is an educational project. Feel free to modify and enhance!

## 👨‍💻 Development

Created as a demonstration of:
- Game development with Pygame
- Real-time AI/ML integration
- Sprite-based collision detection
- Image classification concepts

---

**Enjoy the game! 🍎🎮**

For questions or improvements, feel free to contribute!
