"""
Script to generate placeholder game assets
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_background():
    """Create attractive jungle background with depth and details"""
    img = Image.new('RGB', (800, 600), color='#87CEEB')  # Sky blue
    draw = ImageDraw.Draw(img)
    
    # Sky gradient (top to bottom: light blue to lighter)
    for y in range(0, 350):
        color_val = int(135 + (y / 350) * 50)
        draw.rectangle([0, y, 800, y+1], fill=(135, 206, color_val))
    
    # Distant mountains (background layer)
    mountain_points = [
        (0, 280), (150, 220), (300, 260), (450, 200), 
        (600, 240), (800, 220), (800, 350), (0, 350)
    ]
    draw.polygon(mountain_points, fill='#4a6741', outline='#3d5535')
    
    # Mid-ground hills
    for hill_x in [100, 350, 600]:
        draw.ellipse([hill_x-100, 280, hill_x+100, 380], fill='#2d5016')
    
    # Ground - layered jungle floor
    draw.rectangle([0, 350, 800, 600], fill='#1a3d0a')  # Dark green base
    
    # Background trees (darker, smaller for depth)
    for x in range(50, 800, 120):
        trunk_h = 200 + (x % 80)
        # Trunk
        draw.rectangle([x-8, 600-trunk_h, x+8, 600], fill='#2d1810')
        # Tree crown - layered circles for bushier look
        for offset in [(0, -40), (-15, -25), (15, -25), (0, -10)]:
            cx, cy = x + offset[0], 600 - trunk_h + offset[1]
            draw.ellipse([cx-35, cy-35, cx+35, cy+35], fill='#0d2d0a')
    
    # Foreground trees (brighter, bigger)
    tree_positions = [80, 250, 450, 650]
    for x in tree_positions:
        # Large trunk with texture
        trunk_color = '#4a2511'
        draw.rectangle([x-15, 350, x+15, 600], fill=trunk_color)
        # Add bark texture lines
        for ty in range(370, 600, 30):
            draw.line([x-15, ty, x+15, ty], fill='#3d1f0d', width=2)
        
        # Lush tree crown - multiple overlapping circles
        crown_colors = ['#1a3d0a', '#2d5016', '#3d7a1f']
        positions = [
            (0, -70, 0), (-30, -50, 1), (30, -50, 1),
            (-20, -30, 2), (20, -30, 2), (0, -20, 1)
        ]
        for px, py, c_idx in positions:
            cx, cy = x + px, 350 + py
            color = crown_colors[c_idx % 3]
            draw.ellipse([cx-40, cy-40, cx+40, cy+40], fill=color)
    
    # Vines hanging from trees
    for vine_x in [100, 270, 470, 670]:
        for v in range(3):
            vx = vine_x + (v * 15) - 15
            draw.line([vx, 280, vx-5, 380], fill='#2d5016', width=3)
            draw.line([vx, 280, vx-5, 380], fill='#3d7a1f', width=1)
    
    # Tropical plants/bushes at ground level
    for bush_x in range(30, 800, 80):
        # Large leaves
        for leaf_offset in [-20, 0, 20]:
            lx = bush_x + leaf_offset
            draw.ellipse([lx-25, 550, lx+25, 600], fill='#2d5016')
            draw.ellipse([lx-20, 555, lx+20, 595], fill='#3d7a1f')
    
    # Colorful flowers scattered around
    flower_colors = ['#FF1493', '#FFD700', '#FF6347', '#9370DB']
    for i in range(20):
        fx = 40 + (i * 38)
        fy = 560 + (i % 3) * 15
        f_color = flower_colors[i % 4]
        # Flower petals
        for petal in [(0, -3), (3, 0), (0, 3), (-3, 0)]:
            draw.ellipse([
                fx + petal[0] - 3, fy + petal[1] - 3,
                fx + petal[0] + 3, fy + petal[1] + 3
            ], fill=f_color)
        # Flower center
        draw.ellipse([fx-2, fy-2, fx+2, fy+2], fill='#FFD700')
    
    # Add butterflies
    for bf in [(150, 200), (400, 250), (650, 180)]:
        # Wings
        draw.ellipse([bf[0]-8, bf[1]-5, bf[0]-2, bf[1]+5], fill='#FF1493')
        draw.ellipse([bf[0]+2, bf[1]-5, bf[0]+8, bf[1]+5], fill='#FF1493')
        # Body
        draw.ellipse([bf[0]-1, bf[1]-3, bf[0]+1, bf[1]+3], fill='#000000')
    
    # Sun rays through canopy
    for ray in [(200, 150), (400, 100), (600, 130)]:
        for i in range(5):
            alpha_rect = Image.new('RGBA', (30, 200), (255, 255, 150, 30))
            img.paste(alpha_rect, (ray[0] + i*10, ray[1]), alpha_rect)
    
    # Grass details on ground
    for i in range(0, 800, 5):
        grass_h = 15 + (i % 10)
        grass_color = '#3d7a1f' if i % 2 == 0 else '#2d5016'
        draw.line([i, 600, i, 600 - grass_h], fill=grass_color, width=2)
    
    img.save('assets/bg.png')
    print("✓ Created enhanced attractive jungle bg.png")

def create_boy():
    """Create standing man character sprite"""
    img = Image.new('RGBA', (64, 64), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Head
    draw.ellipse([22, 6, 42, 26], fill='#f1c27d')  # skin tone
    # Hair
    draw.rectangle([22, 6, 42, 14], fill='#2b2b2b')
    draw.ellipse([20, 8, 26, 18], fill='#2b2b2b')
    draw.ellipse([38, 8, 44, 18], fill='#2b2b2b')
    # Neck
    draw.rectangle([30, 26, 34, 30], fill='#e0ac69')
    
    # Torso (shirt)
    draw.rectangle([22, 30, 42, 46], fill='#2f6af6')  # blue shirt
    # Sleeves
    draw.rectangle([18, 30, 22, 40], fill='#2f6af6')
    draw.rectangle([42, 30, 46, 40], fill='#2f6af6')
    # Arms/Hands
    draw.rectangle([16, 40, 22, 50], fill='#f1c27d')
    draw.rectangle([42, 40, 48, 50], fill='#f1c27d')
    
    # Pants
    draw.rectangle([24, 46, 40, 60], fill='#2f2f2f')  # dark pants
    # Belt
    draw.rectangle([24, 46, 40, 48], fill='#1d1d1d')
    
    # Legs
    draw.rectangle([24, 60, 30, 64], fill='#2f2f2f')
    draw.rectangle([34, 60, 40, 64], fill='#2f2f2f')
    
    # Shoes
    draw.rectangle([22, 62, 30, 64], fill='#000000')
    draw.rectangle([34, 62, 42, 64], fill='#000000')
    
    # Subtle highlights
    draw.rectangle([24, 32, 28, 44], fill=(255, 255, 255, 60))
    
    img.save('assets/boy.png')
    print("✓ Created standing man sprite (boy.png)")

def create_apple_good():
    """Create good apple sprite"""
    img = Image.new('RGBA', (48, 48), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Apple body
    draw.ellipse([8, 12, 40, 44], fill='#ff0000')
    # Shine effect
    draw.ellipse([14, 16, 22, 24], fill='#ff6666')
    # Stem
    draw.rectangle([22, 8, 26, 14], fill='#8b4513')
    # Leaf
    draw.ellipse([26, 6, 34, 14], fill='#228b22')
    
    img.save('assets/apple_good.png')
    print("✓ Created apple_good.png")

def create_apple_bad():
    """Create damaged apple sprite"""
    img = Image.new('RGBA', (48, 48), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Apple body (darker, bruised)
    draw.ellipse([8, 12, 40, 44], fill='#8b0000')
    # Brown spots (damage marks)
    draw.ellipse([12, 20, 20, 28], fill='#4a2511')
    draw.ellipse([28, 26, 34, 32], fill='#4a2511')
    # Stem
    draw.rectangle([22, 8, 26, 14], fill='#654321')
    # Wilted leaf
    draw.ellipse([26, 6, 34, 14], fill='#556b2f')
    
    img.save('assets/apple_bad.png')
    print("✓ Created apple_bad.png")

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    create_background()
    create_boy()
    create_apple_good()
    create_apple_bad()
    print("\n✅ All assets created successfully!")
