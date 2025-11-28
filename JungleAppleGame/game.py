"""
Jungle Apple Collector Game
A boy character moves in jungle and collects apples.
CNN model classifies apples as GOOD or DAMAGED.
"""
import pygame
import random
import sys
import os
from cnn_predict import AppleClassifier

# Initialize Pygame
pygame.init()

# Game Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Player settings
PLAYER_SPEED = 5

# Apple settings
APPLE_FALL_SPEED = 3
APPLE_SPAWN_RATE = 60  # frames between spawns


class Player(pygame.sprite.Sprite):
    """Player character (boy)"""
    
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/boy.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = PLAYER_SPEED
    
    def update(self, keys):
        """Update player position based on keyboard input"""
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
    
    def draw(self, screen):
        """Draw player on screen"""
        screen.blit(self.image, self.rect)


class Apple(pygame.sprite.Sprite):
    """Falling apple sprite"""
    
    def __init__(self, x, y, apple_type='random'):
        super().__init__()
        
        # Randomly choose apple type if not specified
        if apple_type == 'random':
            self.apple_type = random.choice(['good', 'bad', 'good', 'good'])  # 75% good, 25% bad
        else:
            self.apple_type = apple_type
        
        # Load appropriate image
        if self.apple_type == 'good':
            self.image = pygame.image.load('assets/apple_good.png').convert_alpha()
        else:
            self.image = pygame.image.load('assets/apple_bad.png').convert_alpha()
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speed = APPLE_FALL_SPEED
    
    def update(self):
        """Update apple position (falling)"""
        self.rect.y += self.speed
    
    def draw(self, screen):
        """Draw apple on screen"""
        screen.blit(self.image, self.rect)


class Game:
    """Main game class"""
    
    def __init__(self):
        """Initialize game"""
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Jungle Apple Collector 🍎")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Load assets
        self.background = pygame.image.load('assets/bg.png').convert()
        
        # Initialize CNN classifier
        print("\n🎮 Initializing Jungle Apple Collector...")
        self.classifier = AppleClassifier()
        print("✅ Game ready!\n")
        
        # Game objects
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20)
        self.apples = pygame.sprite.Group()
        
        # Game state
        self.score = 0
        self.good_apples = 0
        self.damaged_apples = 0
        self.total_collected = 0
        self.frame_count = 0
        
        # UI elements
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 28)
        
        # Message display
        self.message = ""
        self.message_timer = 0
        self.message_color = WHITE
        
        # Print instructions
        self.print_instructions()
    
    def print_instructions(self):
        """Print game instructions to terminal"""
        print("=" * 60)
        print("🎮 JUNGLE APPLE COLLECTOR - GAME INSTRUCTIONS")
        print("=" * 60)
        print("🎯 OBJECTIVE:")
        print("   Collect falling apples! CNN model will classify them.")
        print("   Score points only for GOOD apples!")
        print()
        print("🎮 CONTROLS:")
        print("   ← LEFT ARROW  - Move boy left")
        print("   → RIGHT ARROW - Move boy right")
        print("   ESC - Quit game")
        print()
        print("📊 SCORING:")
        print("   🍎 GOOD Apple    = +1 Score")
        print("   🍏 DAMAGED Apple = No points (detected by CNN)")
        print()
        print("🧠 AI INTEGRATION:")
        print("   Each collected apple is analyzed by CNN model")
        print("   Model classifies: GOOD vs DAMAGED")
        print()
        print("=" * 60)
        print("Press any key in game window to start...")
        print("=" * 60)
        print()
    
    def spawn_apple(self):
        """Spawn a new apple at random position"""
        x = random.randint(50, SCREEN_WIDTH - 50)
        apple = Apple(x, -50)
        self.apples.add(apple)
    
    def check_collisions(self):
        """Check for collisions between player and apples"""
        hits = pygame.sprite.spritecollide(self.player, self.apples, True)
        
        for apple in hits:
            self.total_collected += 1
            
            # Pass apple image to CNN for classification
            prediction, confidence = self.classifier.classify_apple(apple.image)
            
            if prediction == 'GOOD':
                self.good_apples += 1
                self.score += 1
                self.message = f"✓ GOOD APPLE! +1 (CNN: {confidence:.0%} confident)"
                self.message_color = GREEN
                print(f"✅ GOOD apple collected! Score: {self.score} (Confidence: {confidence:.2%})")
            else:
                self.damaged_apples += 1
                self.message = f"✗ DAMAGED APPLE - Not good! (CNN: {confidence:.0%})"
                self.message_color = RED
                print(f"❌ DAMAGED apple detected! No points. (Confidence: {confidence:.2%})")
            
            self.message_timer = 120  # Show message for 2 seconds at 60 FPS
    
    def update(self):
        """Update game state"""
        # Get keyboard input
        keys = pygame.key.get_pressed()
        
        # Update player
        self.player.update(keys)
        
        # Update apples
        self.apples.update()
        
        # Remove apples that fell off screen
        for apple in self.apples:
            if apple.rect.top > SCREEN_HEIGHT:
                apple.kill()
        
        # Spawn new apples
        self.frame_count += 1
        if self.frame_count % APPLE_SPAWN_RATE == 0:
            self.spawn_apple()
        
        # Check collisions
        self.check_collisions()
        
        # Update message timer
        if self.message_timer > 0:
            self.message_timer -= 1
    
    def draw(self):
        """Draw everything on screen"""
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        # Draw apples
        self.apples.draw(self.screen)
        
        # Draw player
        self.player.draw(self.screen)
        
        # Draw UI - Score Panel (top left)
        panel_x = 10
        panel_y = 10
        
        score_text = self.font_large.render(f"Score: {self.score}", True, YELLOW)
        self.screen.blit(score_text, (panel_x, panel_y))
        
        total_text = self.font_small.render(f"Total Collected: {self.total_collected}", True, WHITE)
        self.screen.blit(total_text, (panel_x, panel_y + 50))
        
        good_text = self.font_small.render(f"🍎 Good Apples: {self.good_apples}", True, GREEN)
        self.screen.blit(good_text, (panel_x, panel_y + 80))
        
        damaged_text = self.font_small.render(f"🍏 Damaged: {self.damaged_apples}", True, RED)
        self.screen.blit(damaged_text, (panel_x, panel_y + 110))
        
        # Draw CNN indicator
        cnn_text = self.font_small.render("🧠 CNN Active", True, (100, 200, 255))
        self.screen.blit(cnn_text, (SCREEN_WIDTH - 180, 10))
        
        # Draw message if active
        if self.message_timer > 0:
            msg_text = self.font_medium.render(self.message, True, self.message_color)
            msg_rect = msg_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            
            # Draw semi-transparent background for message
            bg_rect = msg_rect.inflate(20, 10)
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
            bg_surface.set_alpha(200)
            bg_surface.fill(BLACK)
            self.screen.blit(bg_surface, bg_rect)
            
            # Draw message text
            self.screen.blit(msg_text, msg_rect)
        
        # Update display
        pygame.display.flip()
    
    def handle_events(self):
        """Handle game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        # Game over
        self.game_over()
    
    def game_over(self):
        """Display game over summary"""
        print("\n" + "=" * 60)
        print("🎮 GAME OVER - FINAL STATS")
        print("=" * 60)
        print(f"🏆 Final Score: {self.score}")
        print(f"📊 Total Apples Collected: {self.total_collected}")
        print(f"✅ Good Apples: {self.good_apples}")
        print(f"❌ Damaged Apples: {self.damaged_apples}")
        if self.total_collected > 0:
            accuracy = (self.good_apples / self.total_collected) * 100
            print(f"📈 Good Apple Rate: {accuracy:.1f}%")
        print("=" * 60)
        print("Thanks for playing! 🍎")
        print()
        
        pygame.quit()
        sys.exit()


def main():
    """Main function to start the game"""
    # Change to game directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Create and run game
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
