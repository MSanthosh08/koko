"""
main.py
KOKO: Emotion-Aware Interactive Robot
Fully integrated with Recommender Engine + Feedback Learning.
- Detects emotion from PiCamera
- Shows eyes on 9.7" display via display_eyes.py
- Sends robot actions
- Learns which actions improve emotions over time
"""

import time
import random
import cv2
from picamera2 import Picamera2
from fer import FER
import pygame

from display_eyes import EyeDisplay
from robot_controller import RobotController
from recommender_engine import (
    load_profiles,
    save_profiles,
    recommend_for_child,
    apply_feedback,
    get_assets
)

# ---------------- Configuration ----------------
ROBOT_SERIAL = None       # e.g., '/dev/ttyUSB0' for Arduino
CAMERA_DEVICE = 0
LOOP_DELAY = 0.1          # seconds between detections
AFTER_DELAY = 1.0         # seconds to keep eyes/action active
ITERATIONS = None         # None = infinite loop

# ---------------- Main Loop ----------------
def main():
    print("Starting KOKO main loop... Press 'q' or ESC to quit safely.")

    # Load profiles
    profiles = load_profiles()
    child_id = "child_001"
    profile = profiles[child_id]

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
    paused = False

    try:
        while running:
            counter += 1
            if ITERATIONS and counter > ITERATIONS:
                break

            # Capture frame
            frame = picam2.capture_array()
            frame = cv2.rotate(frame, cv2.ROTATE_180)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Detect emotion
            results = detector.detect_emotions(frame_rgb)
            if results:
                face = max(results, key=lambda x: x['box'][2]*x['box'][3])
                emotions = face['emotions']
                emotion = max(emotions, key=emotions.get)
                conf = emotions[emotion]
            else:
                emotion, conf = "neutral", 0.0

            print(f"[MAIN] Emotion Detected: {emotion} (conf {conf:.2f})")

            # Show eyes
            display.show_emotion(emotion)

            # Get top recommendation(s)
            picks = recommend_for_child(profile, emotion, top_k=1)
            if picks:
                action_key = picks[0]
            else:
                action_key = "idle_patrol"

            # Trigger robot action
            robot.send_action(action_key)
            print(f"[MAIN] Action Triggered: {action_key}")

            # Keep display active while action runs
            t0 = time.time()
            while time.time() - t0 < AFTER_DELAY:
                display.update(fps=30)
                if not display.running:
                    running = False
                    break

            # Re-evaluate emotion after action for feedback
            frame2 = picam2.capture_array()
            frame2_rgb = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
            results2 = detector.detect_emotions(frame2_rgb)
            if results2:
                face2 = max(results2, key=lambda x: x['box'][2]*x['box'][3])
                emotions2 = face2['emotions']
                after_emotion = max(emotions2, key=emotions2.get)
                conf2 = emotions2[after_emotion]
            else:
                after_emotion, conf2 = "neutral", 0.0

            print(f"[MAIN] After Emotion: {after_emotion} (conf {conf2:.2f})")

            # Apply feedback to improve recommendations
            delta = apply_feedback(profile, action_key, emotion, after_emotion)
            print(f"[MAIN] Feedback applied: {delta:+.2f} to {action_key}")

            # Persist profiles
            save_profiles(profiles)

            # Wait for next iteration
            t1 = time.time()
            while time.time() - t1 < LOOP_DELAY:
                display.update(fps=30)
                if not display.running:
                    running = False
                    break


            # Handle quit events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        running = False
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                    state = "⏸️ PAUSED" if paused else "▶️ RESUMED"
                print(f"[MAIN] {state}")


    except KeyboardInterrupt:
        print("Interrupted by user.")

    finally:
        print("Cleaning up...")
        picam2.stop()
        display.close()
        robot.close()
        save_profiles(profiles)
        print("Shutdown complete.")


if __name__ == "__main__":
    main()
