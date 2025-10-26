import pygame
import sys
import random
import math

pygame.init()

# Screen setup
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Luna-Style Emotive Eyes")

clock = pygame.time.Clock()

# Eye geometry
EYE_RADIUS = SCREEN_HEIGHT // 4
PUPIL_RADIUS = EYE_RADIUS // 4
EYE_SPACING = EYE_RADIUS + 100

LEFT_EYE_CENTER = (SCREEN_WIDTH // 2 - EYE_SPACING, SCREEN_HEIGHT // 2)
RIGHT_EYE_CENTER = (SCREEN_WIDTH // 2 + EYE_SPACING, SCREEN_HEIGHT // 2)

# Pupil starting positions
left_pupil = list(LEFT_EYE_CENTER)
right_pupil = list(RIGHT_EYE_CENTER)

# Colors
BG_COLOR = (0, 0, 5)
BLACK = (0, 0, 0)
BLUE = (50, 150, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 120)
RED = (255, 80, 80)
PURPLE = (180, 100, 255)
GRAY = (180, 180, 200)
WHITE = (255, 255, 255)

# Emotion setup
emotions = [
    "neutral", "happy", "sad", "excited", "confused",
    "thinking", "sleepy", "angry", "surprised", "scared"
]
current_emotion = "neutral"

emotion_settings = {
    "neutral":  {"color": BLUE, "speed": 0.05, "glow": 80, "blink_rate": 300},
    "happy":    {"color": CYAN, "speed": 0.07, "glow": 120, "blink_rate": 200},
    "sad":      {"color": (100, 130, 255), "speed": 0.03, "glow": 60, "blink_rate": 500},
    "excited":  {"color": YELLOW, "speed": 0.12, "glow": 150, "blink_rate": 150},
    "confused": {"color": PURPLE, "speed": 0.04, "glow": 90, "blink_rate": 350},
    "thinking": {"color": GRAY, "speed": 0.02, "glow": 60, "blink_rate": 400},
    "sleepy":   {"color": (150, 150, 255), "speed": 0.02, "glow": 40, "blink_rate": 100},
    "angry":    {"color": RED, "speed": 0.08, "glow": 130, "blink_rate": 180},
    "surprised":{"color": WHITE, "speed": 0.1, "glow": 180, "blink_rate": 250},
    "scared":   {"color": (180, 255, 255), "speed": 0.09, "glow": 100, "blink_rate": 200},
}

pupil_move_radius = EYE_RADIUS // 3
move_target = [0, 0]
move_timer = 0
blink_timer = 0
blink_progress = 0
blinking = False

# Utility functions
def move_pupil(center, target, current, speed):
    current[0] += (target[0] - current[0]) * speed
    current[1] += (target[1] - current[1]) * speed
    return current

def get_random_target(center):
    angle = random.uniform(0, 2 * math.pi)
    r = random.uniform(0, pupil_move_radius)
    return [center[0] + r * math.cos(angle), center[1] + r * math.sin(angle)]

def draw_glow(surface, color, position, radius, intensity):
    # Draw layered transparent circles for glow
    for i in range(6):
        layer_alpha = max(0, 50 - i * 8)
        layer_surface = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)
        pygame.draw.circle(layer_surface, (*color, layer_alpha),
                           (radius * 2, radius * 2), radius * (1 + i * 0.3))
        surface.blit(layer_surface, (position[0] - radius * 2, position[1] - radius * 2))

def draw_eye(center, pupil, color, glow_intensity, blink_factor):
    # Draw black digital eye screen area
    eye_surface = pygame.Surface((EYE_RADIUS * 2, EYE_RADIUS * 2), pygame.SRCALPHA)
    pygame.draw.ellipse(eye_surface, (10, 10, 20), (0, 0, EYE_RADIUS * 2, EYE_RADIUS * 2))
    screen.blit(eye_surface, (center[0] - EYE_RADIUS, center[1] - EYE_RADIUS))

    # Adjust pupil for blink (vertically squashed)
    pupil_scale_y = max(0.1, 1 - blink_factor)
    scaled_radius_y = int(PUPIL_RADIUS * pupil_scale_y)

    # Glow and pupil
    draw_glow(screen, color, pupil, PUPIL_RADIUS, glow_intensity)
    pygame.draw.ellipse(screen, color, (pupil[0] - PUPIL_RADIUS, pupil[1] - scaled_radius_y,
                                        PUPIL_RADIUS * 2, scaled_radius_y * 2))

def start_blink():
    global blinking, blink_progress
    blinking = True
    blink_progress = 0

# Main loop
running = True
while running:
    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_ESCAPE, pygame.K_q]:
                running = False
            elif pygame.K_1 <= event.key <= pygame.K_9:
                current_emotion = emotions[event.key - pygame.K_1]
            elif event.key == pygame.K_0:
                current_emotion = emotions[9]

    # Get emotion settings
    settings = emotion_settings[current_emotion]
    color = settings["color"]
    speed = settings["speed"]
    glow = settings["glow"]
    blink_rate = settings["blink_rate"]

    # Random eye movement
    move_timer -= 1
    if move_timer <= 0:
        move_target = get_random_target(LEFT_EYE_CENTER)
        move_timer = random.randint(40, 100)

    left_pupil = move_pupil(LEFT_EYE_CENTER, move_target, left_pupil, speed)
    dx = left_pupil[0] - LEFT_EYE_CENTER[0]
    dy = left_pupil[1] - LEFT_EYE_CENTER[1]
    right_pupil = [RIGHT_EYE_CENTER[0] + dx, RIGHT_EYE_CENTER[1] + dy]

    # Blink logic
    blink_timer += 1
    if not blinking and blink_timer > blink_rate:
        start_blink()
        blink_timer = 0

    if blinking:
        blink_progress += 0.08
        if blink_progress >= 2.0:
            blinking = False
            blink_progress = 0

    blink_factor = math.sin(min(blink_progress, 1) * math.pi)

    # Draw eyes
    draw_eye(LEFT_EYE_CENTER, left_pupil, color, glow, blink_factor)
    draw_eye(RIGHT_EYE_CENTER, right_pupil, color, glow, blink_factor)

    # Emotion label
    font = pygame.font.SysFont("Arial", 36, bold=True)
    text = font.render(current_emotion.upper(), True, (150, 200, 255))
    screen.blit(text, (40, 40))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
