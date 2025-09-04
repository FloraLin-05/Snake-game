import pygame
import random # Library to generate random food positions

# ------- Basic parameters -------
# Initialize the pygame framework
pygame.init()
W = 800
H = 600

# Grid settings
ROW = 30
COL = 40

# Set window size
size = (W, H)
window = pygame.display.set_mode(size)
pygame.display.set_caption('snake game')

# Colors
bg_color = (255,255,255) # White
snake_color = (200,200,200) # Light gray
head_color = (0,128,128) # Blue-green
food_color = (255,255,0) # Yelow

# Fonts
font_big = pygame.font.SysFont('Arial', 56)
font_hud = pygame.font.SysFont('Arial', 24)


# ------- Basic data structure -------
class Point:
    row = 0
    col = 0
    def __init__(self,row,col): # Each point is represented by row and col, instead of x and y
        self.row = row
        self.col = col
    def copy(self):
        return Point(row = self.row, col = self.col)

# Helper function to draw a grid cell (rectangle)
def rect(point,color):
    cell_width = W/COL
    cell_height = H / ROW
    left = point.col * cell_width
    top = point.row * cell_height
    pygame.draw.rect(window, color,(left,top,cell_width,cell_height))

# Generate food at a random position, avoiding the snake's head and body
def gen_food():
    while True:
            p = Point(row=random.randint(0, ROW - 1), col=random.randint(0, COL - 1))
            head_collide = (p.row == head.row and p.col == head.col)
            body_collide = any(p.row == s.row and p.col == s.col for s in snakes)
            if not head_collide and not body_collide:
                return p

# ------- Initial state -------
# Initial snake position
head = Point(row = ROW//2, col = COL//2) # Place the snake head in the center
snakes =[                                # Snake body (segments behind the head)
    Point(row=head.row, col=head.col+1),
    Point(row=head.row, col=head.col+2),
    Point(row=head.row, col=head.col+3)
]
direction = 'left' # Initial movement direction; can be 'left', 'right', 'up', or 'down'
food = gen_food()


# ------- Main game loop -------
clock = pygame.time.Clock()  # Game clock for controlling frame rate
exiting = False  # Global flag to exit the program

while not exiting:
    running = True
    game_over = False
    score = 0

    while running:
        # 1) Event handling: check user inputs (quit, keypress, etc.)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # If the user clicks the window close button
                exiting = True
                running = False
                game_over = False
            elif event.type == pygame.KEYDOWN: # If a key is pressed
                if event.key in (pygame.K_UP, pygame.K_w): # ↑ or W, move up
                    if direction == 'left' or direction == 'right': # Prevent 180° reversal; only allow orthogonal turns
                        direction = 'up'
                elif event.key in (pygame.K_DOWN, pygame.K_s): # ↓ or S, move down
                    if direction == 'left' or direction == 'right':
                        direction = 'down'
                elif event.key in (pygame.K_LEFT, pygame.K_a): # ← or A, move left
                    if direction == 'up' or direction == 'down':
                        direction = 'left'
                elif event.key in (pygame.K_RIGHT, pygame.K_d): # → or D，move right
                    if direction == 'up' or direction == 'down':
                        direction = 'right'
        if exiting:
            break

        # 2) Game logic update (movement, eating, growing)
        # Add a copy of the head to the front of the body (simulate forward movement)
        snakes.insert(0, head.copy())
        # Move the head in the current direction
        if direction == 'left':
            head.col -= 1
        elif direction == 'right':
            head.col += 1
        elif direction == 'up':
            head.row -= 1
        elif direction == 'down':
            head.row += 1

        # Collision detection: wall or self
        hit_wall = head.col < 0 or head.col >= COL or head.row < 0 or head.row >= ROW
        hit_self = any(head.row == s.row and head.col == s.col for s in snakes)
        '''
        Iterate through all snake body segments (snakes).
        If any segment has the same (row, col) as the head → collision with itself.
        any(...) returns True if at least one match is found.
        '''
        if hit_wall or hit_self:
            running = False
            game_over = True

        # Eating food
        else:
            eat = (head.row == food.row and head.col == food.col) # Head overlaps food cell
            if eat:
                score += 1
                food = gen_food() # Grow by keeping the tail and spawn a new food
            else:
                snakes.pop() # Remove tail to maintain length if no food eaten

            # 3) Rendering
            pygame.draw.rect(window, bg_color, (0, 0, W, H))  # Clear screen
            rect(food, food_color)                            # Draw food
            rect(head, head_color)                            # Draw head
            for s in snakes:                                  # Draw body
                rect(s, snake_color)

            # Draw score (top-left corner)
            score_surf = font_hud.render(f"Score: {score}", True, (0, 0, 0))
            window.blit(score_surf, (10, 8))

            pygame.display.flip()
            clock.tick(10)    # Control frame rate (snake speed)

        if exiting:
            break

        # Game Over screen (only if snake dies in this round)
        if game_over:
            txt_over = font_big.render("GAME OVER", True, (255, 0, 0))
            txt_score = font_hud.render(f"Score: {score}", True, (0, 0, 0))

            waiting = True
            while waiting:
                pygame.draw.rect(window, bg_color, (0, 0, W, H))
                window.blit(txt_over, (W // 2 - txt_over.get_width() // 2, H // 2 - txt_over.get_height()))
                window.blit(txt_score, (W // 2 - txt_score.get_width() // 2, H // 2 + 10))
                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exiting = True
                        waiting = False

pygame.quit()