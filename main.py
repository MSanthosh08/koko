"""
main.py
Orchestrates FER -> Recommender -> Display -> Robot actions
Run this on your Raspberry Pi. Adjust serial port for your robot in ROBOT_SERIAL variable.

Behavior:
 - Detects emotion from camera
 - Shows appropriate eyes on fullscreen display
 - Sends robot motor/behavior commands
 - After performing action, waits a few seconds and re-checks emotion to record feedback
"""

import time
import random
from fer_integration import FERWrapper
from recommender_engine import load_profiles, save_profiles, recommend_for_child, apply_feedback, ASSETS
from robot_controller import RobotController
from display_eyes import EyeDisplay

# Config
ROBOT_SERIAL = None   # e.g. '/dev/ttyUSB0' if you use Arduino; None = no hardware (prints only)
CAMERA_DEVICE = 0
LOOP_DELAY = 1.0      # seconds between detections
AFTER_DELAY = 3.0     # seconds to wait after action and then re-evaluate emotion for feedback
ITERATIONS = None     # None for infinite loop, or int to limit

def main():
    print("Starting KOKO main loop...")
    profiles = load_profiles()
    child_id = "child_001"
    profile = profiles[child_id]

    # init modules
    fer = FERWrapper(device=CAMERA_DEVICE)
    robot = RobotController(serial_port=ROBOT_SERIAL)
    display = EyeDisplay(fullscreen=True)  # will open 9.7" display in fullscreen (or monitor)

    try:
        counter = 0
        while True:
            counter += 1
            if ITERATIONS and counter > ITERATIONS:
                break
            # detect before emotion
            frame, ok = fer.read_frame()
            if ok:
                before_emotion, conf = fer.detect(frame)
            else:
                before_emotion, conf = "neutral", 0.0
            print(f"[MAIN] BEFORE: {before_emotion} (conf {conf:.2f})")

            # get recommendation (single best)
            picks = recommend_for_child(profile, before_emotion, top_k=1)
            if not picks:
                action_key = "idle_patrol"
            else:
                action_key = picks[0]
            print(f"[MAIN] ACTION -> {action_key}")

            # show eyes animation for this emotion
            display.show_emotion(before_emotion)

            # send robot action
            # map action_key to asset choices if required
            asset_list = ASSETS.get(action_key, [action_key])
            chosen_asset = random.choice(asset_list)
            robot.send_action(action_key)  # robot_controller expects the action_key

            # update display for a bit while action runs
            t0 = time.time()
            while time.time() - t0 < AFTER_DELAY:
                display.update(fps=30)

            # evaluate after emotion for feedback
            frame2, ok2 = fer.read_frame()
            if ok2:
                after_emotion, conf2 = fer.detect(frame2)
            else:
                after_emotion, conf2 = "neutral", 0.0
            print(f"[MAIN] AFTER: {after_emotion} (conf {conf2:.2f})")

            # apply feedback to adjust learned scores
            delta = apply_feedback(profile, action_key, before_emotion, after_emotion)
            print(f"[MAIN] Feedback applied: {delta:+.2f} to {action_key}")

            # persist profiles
            save_profiles(profiles)

            # keep updating display while waiting for next iteration
            t1 = time.time()
            while time.time() - t1 < LOOP_DELAY:
                display.update(fps=30)

    except KeyboardInterrupt:
        print("Interrupted by user, shutting down.")
    finally:
        print("Cleaning up...")
        display.close()
        fer.release()
        robot.close()
        save_profiles(profiles)
        print("Shutdown complete.")

if __name__ == "__main__":
    main()
