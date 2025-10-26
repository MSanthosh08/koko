"""
main.py
KOKO: Emotion-Aware Interactive Robot
Detects emotion from PiCamera5, shows eyes on 9.7" display via display_eyes.py, triggers robot actions.
Press 'q' or ESC to quit safely.
"""

import time
import random
import cv2
import pygame
from picamera2 import Picamera2
from fer import FER

from display_eyes import EyeDisplay
from robot_controller import RobotController  # your robot action module

# ---------------- Configuration ----------------
ROBOT_SERIAL = None       # e.g., '/dev/ttyUSB0' if you have Arduino/robot
LOOP_DELAY = 1.0          # seconds between detections
AFTER_DELAY = 3.0         # seconds to keep eyes/action active
ITERATIONS = None         # None = infinite loop

# Emotion -> Robot Action mapping
EMO_ACTION_MAP = {
    "happy": "spin",
    "sad": "gentle_forward",
    "angry": "calm_movement",
    "neutral": "idle",
    "surprise": "jump",
    "fear": "hide"
}

# ---------------- Main Loop ----------------
def main():
    print("Starting KOKO main loop... Press 'q' or ESC to quit.")

    # Initialize modules
    detector = FER(mtcnn=True)
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(
        main={"format": "XRGB8888", "size": (640, 480)}
    )
    picam2.configure(config)
    picam2.start()
    time.sleep(2)  # warm-up

    robot = RobotController(serial_port=ROBOT_SERIAL)
    display = EyeDisplay(fullscreen=True)

    counter = 0
    running = True

    try:
        while running:
            counter += 1
            if ITERATIONS and counter > ITERATIONS:
                break

            # Capture frame from PiCamera
            frame = picam2.capture_array()
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Detect emotions
            results = detector.detect_emotions(frame_rgb)
            if results:
                face = max(results, key=lambda x: x['box'][2]*x['box'][3])
                emotions = face['emotions']
                emotion = max(emotions, key=emotions.get)
                conf = emotions[emotion]
            else:
                emotion, conf = "neutral", 0.0

            print(f"[MAIN] Emotion: {emotion} (conf {conf:.2f})")

            # Show eyes
            display.show_emotion(emotion)

            # Trigger robot action
            action = EMO_ACTION_MAP.get(emotion, "idle")
            robot.send_action(action)
            print(f"[MAIN] Action: {action}")

            # Keep display updated while waiting AFTER_DELAY
            t0 = time.time()
            while time.time() - t0 < AFTER_DELAY:
                display.update(fps=30)

            # Wait before next detection
            t1 = time.time()
            while time.time() - t1 < LOOP_DELAY:
                display.update(fps=30)

            # Check for quit via pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_q, pygame.K_ESCAPE]:
                        running = False

    except KeyboardInterrupt:
        print("Interrupted by user.")

    finally:
        print("Cleaning up...")
        picam2.stop()
        display.close()
        robot.close()
        print("Shutdown complete.")


if __name__ == "__main__":
    main()
