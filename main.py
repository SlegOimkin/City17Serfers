import pygame
import random
import sys

# Constants
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
LANE_WIDTH = SCREEN_WIDTH // 3
PLAYER_WIDTH, PLAYER_HEIGHT = 40, 60
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 40, 60
BACKGROUND_COLOR = (30, 30, 30)
PLAYER_COLOR = (0, 255, 0)
OBSTACLE_COLOR = (255, 0, 0)

pygame.init()
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("City 17 Serfers")

def draw_background():
    screen.fill(BACKGROUND_COLOR)
    # Draw simple citadel silhouette
    pygame.draw.rect(screen, (80, 80, 80), pygame.Rect(SCREEN_WIDTH//2 - 20, 0, 40, SCREEN_HEIGHT))

class Player:
    def __init__(self):
        self.lane = 1  # start in center lane (0 left, 1 middle, 2 right)
        self.y = SCREEN_HEIGHT - PLAYER_HEIGHT - 20
        self.rect = pygame.Rect(self.lane * LANE_WIDTH + (LANE_WIDTH - PLAYER_WIDTH)//2, self.y, PLAYER_WIDTH, PLAYER_HEIGHT)

    def move_left(self):
        if self.lane > 0:
            self.lane -= 1
            self.rect.x = self.lane * LANE_WIDTH + (LANE_WIDTH - PLAYER_WIDTH)//2

    def move_right(self):
        if self.lane < 2:
            self.lane += 1
            self.rect.x = self.lane * LANE_WIDTH + (LANE_WIDTH - PLAYER_WIDTH)//2

    def draw(self, surface):
        pygame.draw.rect(surface, PLAYER_COLOR, self.rect)

class Obstacle:
    def __init__(self, lane, y):
        self.lane = lane
        self.rect = pygame.Rect(lane * LANE_WIDTH + (LANE_WIDTH - OBSTACLE_WIDTH)//2, y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)

    def update(self, speed):
        self.rect.y += speed

    def draw(self, surface):
        pygame.draw.rect(surface, OBSTACLE_COLOR, self.rect)

    def off_screen(self):
        return self.rect.top > SCREEN_HEIGHT

    def collides(self, rect):
        return self.rect.colliderect(rect)

def main():
    player = Player()
    obstacles = []
    obstacle_timer = 0
    speed = 5
    score = 0

    while True:
        dt = clock.tick(60)
        score += dt / 1000.0 * speed
        obstacle_timer += dt
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move_left()
                elif event.key == pygame.K_RIGHT:
                    player.move_right()

        # Spawn new obstacles
        if obstacle_timer > 1500:
            obstacle_timer = 0
            lane = random.randint(0, 2)
            obstacles.append(Obstacle(lane, -OBSTACLE_HEIGHT))

        # Update obstacles
        for ob in obstacles:
            ob.update(speed)
        obstacles = [ob for ob in obstacles if not ob.off_screen()]

        # Collision detection
        for ob in obstacles:
            if ob.collides(player.rect):
                return  # End game on collision

        draw_background()
        player.draw(screen)
        for ob in obstacles:
            ob.draw(screen)

        score_text = font.render(f"Score: {int(score)}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

def run_game():
    while True:
        main()
        # Show Game Over screen
        screen.fill((0, 0, 0))
        text = font.render("Game Over! Press any key to restart", True, (255, 255, 255))
        rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        screen.blit(text, rect)
        pygame.display.flip()
        wait = True
        while wait:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    wait = False

if __name__ == "__main__":
    run_game()
