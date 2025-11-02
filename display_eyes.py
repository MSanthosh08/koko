"""
display_eyes_reactive.py
Emotion-reactive glowing rectangular eyes using Pygame.
Robot reacts visually to user's detected emotion.
Press ESC or Q to exit safely.
"""

import pygame
import time
import math
import threading
import sys

class EyeDisplay:
    def __init__(self, width=1024, height=768, fullscreen=False):
        pygame.init()
        self.width = width
        self.height = height
        flags = pygame.FULLSCREEN if fullscreen else 0
        self.screen = pygame.display.set_mode((width, height), flags)
        pygame.display.set_caption("KOKO Emotion-Reactive Eyes")
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_emotion = "neutral"
        self.lock = threading.Lock()
        self.bg_color = (10, 10, 20)
        self._start_thread()

    def _start_thread(self):
        """Start background thread for key handling."""
        thread = threading.Thread(target=self._event_loop, daemon=True)
        thread.start()

    def _event_loop(self):
        """Handle ESC/Q press to quit."""
        while self.running:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    self.stop()
                elif ev.type == pygame.KEYDOWN:
                    if ev.key in (pygame.K_ESCAPE, pygame.K_q):
                        self.stop()
            time.sleep(0.02)

    def stop(self):
        self.running = False
        pygame.quit()
        sys.exit(0)

    def show_emotion(self, emotion):
        with self.lock:
            self.current_emotion = emotion

    def _emotion_params(self, emotion):
        """Define visual style for each emotion."""
        params = {
            "happy":    {"height": 0.45, "tilt": 0,  "color": (0, 255, 180), "blink": 0.0, "brightness": 1.0},
            "sad":      {"height": 0.25, "tilt": 10, "color": (100, 150, 255), "blink": 0.0, "brightness": 0.7},
            "angry":    {"height": 0.55, "tilt": -10, "color": (255, 60, 60), "blink": 0.5, "brightness": 1.0},
            "neutral":  {"height": 0.4, "tilt": 0,  "color": (180, 180, 255), "blink": 0.0, "brightness": 0.8},
            "surprise": {"height": 0.6, "tilt": 0,  "color": (255, 255, 100), "blink": 0.0, "brightness": 1.0},
            "fear":     {"height": 0.3, "tilt": 0,  "color": (200, 100, 255), "blink": 0.0, "brightness": 0.8}
        }
        return params.get(emotion, params["neutral"])

    def draw_eyes(self, t):
        with self.lock:
            emo = self.current_emotion
        p = self._emotion_params(emo)

        self.screen.fill(self.bg_color)
        margin_x = int(self.width * 0.18)
        eye_w = int(self.width * 0.25)
        eye_h = int(self.height * p["height"])
        base_left_center = (margin_x + eye_w//2, self.height//2)
        base_right_center = (self.width - margin_x - eye_w//2, self.height//2)

        # Subtle movement animations per emotion
        if emo == "happy":
            jitter_x = int(8 * math.sin(t * 10))
            jitter_y = int(5 * math.cos(t * 8))
            left_center = (base_left_center[0] + jitter_x, base_left_center[1] + jitter_y)
            right_center = (base_right_center[0] + jitter_x, base_right_center[1] + jitter_y)
        elif emo == "sad":
            left_center = (base_left_center[0], base_left_center[1] + 20)
            right_center = (base_right_center[0], base_right_center[1] + 20)
        elif emo == "angry":
            offset = int(10 * math.sin(t * 15))
            left_center = (base_left_center[0] - offset, base_left_center[1])
            right_center = (base_right_center[0] + offset, base_right_center[1])
        elif emo == "surprise":
            offset = int(8 * math.sin(t * 20))
            left_center = (base_left_center[0], base_left_center[1] - offset)
            right_center = (base_right_center[0], base_right_center[1] - offset)
        else:
            left_center = base_left_center
            right_center = base_right_center

        # Blink (for angry/fear)
        blink_open = 1.0
        if p["blink"] > 0:
            blink_open = abs(math.sin(t * p["blink"] * 5))
            blink_open = max(0.2, blink_open)

        # Draw both eyes
        for i, center in enumerate([left_center, right_center]):
            cx, cy = center
            rect_h = int(eye_h * blink_open)
            tilt = p["tilt"]
            color = tuple(int(c * p["brightness"]) for c in p["color"])

            # Glow effect
            for glow in range(4, 0, -1):
                alpha = max(20, 60 - glow * 10)
                glow_rect = pygame.Surface((eye_w + glow*10, rect_h + glow*6), pygame.SRCALPHA)
                glow_color = (*color, alpha)
                pygame.draw.rect(glow_rect, glow_color, glow_rect.get_rect(), border_radius=20)
                rotated = pygame.transform.rotate(glow_rect, tilt if i == 0 else -tilt)
                rect = rotated.get_rect(center=(cx, cy))
                self.screen.blit(rotated, rect)

            # Main eye
            eye_surface = pygame.Surface((eye_w, rect_h), pygame.SRCALPHA)
            pygame.draw.rect(eye_surface, color, eye_surface.get_rect(), border_radius=20)
            rotated_eye = pygame.transform.rotate(eye_surface, tilt if i == 0 else -tilt)
            rect = rotated_eye.get_rect(center=(cx, cy))
            self.screen.blit(rotated_eye, rect)

    def update(self, fps=30):
        t = time.time()
        self.draw_eyes(t)
        pygame.display.flip()
        self.clock.tick(fps)

    def close(self):
        self.stop()


# --- Emotion Mapping Logic ---
def get_robot_reaction(user_emotion):
    """Robot reacts visually to user's emotion (comforting/empathetic)."""
    mapping = {
        "happy": "happy",        # mirror your joy
        "sad": "happy",          # cheer you up
        "angry": "fear",         # calm or cautious
        "neutral": "neutral",    # stay calm
        "surprise": "surprise",  # share surprise
        "fear": "happy"          # reassure you
    }
    return mapping.get(user_emotion, "neutral")


# --- Standalone Demo Mode ---
if __name__ == "__main__":
    disp = EyeDisplay(fullscreen=False)
    user_emotions = ["happy", "angry", "sad", "fear", "surprise", "neutral"]
    idx = 0
    last_switch = time.time()

    while disp.running:
        disp.update()
        if time.time() - last_switch > 2:
            user_emotion = user_emotions[idx]
            robot_emotion = get_robot_reaction(user_emotion)
            print(f"User: {user_emotion} → Robot shows: {robot_emotion}")
            disp.show_emotion(robot_emotion)
            idx = (idx + 1) % len(user_emotions)
            last_switch = time.time()

    disp.close()
