"""
display_eyes.py
Pygame-based fullscreen animated eyes for each emotion.
This draws procedural eyes (no external images required) and changes pupil size, blink rate, eye tilt, color, etc. per emotion.

Usage:
    from display_eyes import EyeDisplay
    disp = EyeDisplay(fullscreen=True)
    disp.show_emotion('happy')
    disp.update_loop()  # returns until stop requested in main loop
    disp.close()
"""

import pygame
import time
import math
import threading

class EyeDisplay:
    def __init__(self, width=1024, height=768, fullscreen=True):
        pygame.init()
        self.width = width
        self.height = height
        flags = pygame.FULLSCREEN if fullscreen else 0
        self.screen = pygame.display.set_mode((width, height), flags)
        pygame.display.set_caption("KOKO Eyes")
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_emotion = "neutral"
        self.lock = threading.Lock()
        self.bg_color = (20, 20, 30)
        # start event pump thread to keep window responsive if needed
        self._start_thread()

    def _start_thread(self):
        self.thread = threading.Thread(target=self._event_loop, daemon=True)
        self.thread.start()

    def _event_loop(self):
        while self.running:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    self.running = False
                elif ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE:
                        self.running = False
            time.sleep(0.02)

    def show_emotion(self, emotion):
        with self.lock:
            self.current_emotion = emotion

    def _emotion_params(self, emotion):
        # returns dict: pupil_scale, blink_rate, eye_color, offset, tilt
        params = {
            "happy": {"pupil": 0.35, "blink": 4.0, "color": (50,200,120), "tilt": 5},
            "sad": {"pupil": 0.25, "blink": 1.5, "color": (120,170,230), "tilt": -6},
            "angry": {"pupil": 0.2, "blink": 6.0, "color": (220,80,60), "tilt": -12},
            "neutral": {"pupil": 0.3, "blink": 3.0, "color": (200,200,200), "tilt": 0},
            "surprise": {"pupil": 0.5, "blink": 8.0, "color": (255,255,180), "tilt": 0},
            "fear": {"pupil": 0.15, "blink": 1.0, "color": (200,150,255), "tilt": 0}
        }
        return params.get(emotion, params["neutral"])

    def draw_eyes(self, t):
        with self.lock:
            emo = self.current_emotion
        p = self._emotion_params(emo)
        self.screen.fill(self.bg_color)
        # eye positions
        margin_x = int(self.width * 0.12)
        eye_w = int(self.width * 0.36)
        eye_h = int(self.height * 0.5)
        left_center = (margin_x + eye_w//2, self.height//2)
        right_center = (self.width - margin_x - eye_w//2, self.height//2)

        for center in (left_center, right_center):
            cx, cy = center
            # white sclera
            sclera_rect = pygame.Rect(0,0, eye_w, eye_h)
            sclera_rect.center = (cx, cy)
            pygame.draw.ellipse(self.screen, (245,245,245), sclera_rect)

            # eye tilt transform (simple: shift pupil y slightly)
            tilt = p["tilt"]
            # pupil movement oscillation to look alive
            ox = int(math.sin(t*1.2 + cx) * 10)
            oy = int(math.cos(t*0.8 + cy) * 6) + tilt

            # iris circle
            iris_radius = int(min(eye_w, eye_h) * 0.18)
            iris_pos = (cx + ox, cy + oy)
            pygame.draw.circle(self.screen, p["color"], iris_pos, iris_radius)

            # pupil
            pupil_radius = int(iris_radius * (p["pupil"]))
            pygame.draw.circle(self.screen, (20,20,20), iris_pos, pupil_radius)

            # highlight
            pygame.draw.circle(self.screen, (255,255,255), (iris_pos[0]-int(pupil_radius*0.4), iris_pos[1]-int(pupil_radius*0.4)), max(2, pupil_radius//4))

            # subtle eyelid (blink)
            blink = (math.sin(t * p["blink"]) + 1.0) / 2.0  # 0..1
            lid_height = int(eye_h * (0.08 + 0.25 * (1.0 - blink)))  # when blink small -> open
            top_lid = pygame.Rect(sclera_rect.left, sclera_rect.top, sclera_rect.width, lid_height)
            bottom_lid = pygame.Rect(sclera_rect.left, sclera_rect.bottom - lid_height, sclera_rect.width, lid_height)
            pygame.draw.rect(self.screen, self.bg_color, top_lid)
            pygame.draw.rect(self.screen, self.bg_color, bottom_lid)

        # small text optional
        # font = pygame.font.SysFont(None, 28)
        # text = font.render(emo.upper(), True, (200,200,200))
        # self.screen.blit(text, (10, 10))

    def update(self, fps=30):
        # call in your main loop to update display
        t = time.time()
        self.draw_eyes(t)
        pygame.display.flip()
        self.clock.tick(fps)

    def close(self):
        self.running = False
        pygame.quit()
