from picamera2 import Picamera2
from fer import FER
import cv2
import numpy as np
import time

def main():
    # Initialize FER detector
    detector = FER(mtcnn=True)
    
    # Initialize PiCamera2
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(main={"format": "XRGB8888", "size": (640, 480)})
    picam2.configure(config)
    picam2.start()
    time.sleep(2)  # Allow camera to warm up

    print("KOKO Emotion Detection Started")
    print("Press 'q' to quit.")

    while True:
        # Capture frame from camera
        frame = picam2.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.rotate(frame, cv2.ROTATE_180)  # ?? Rotate 180 degrees
        # Detect emotions
        results = detector.detect_emotions(frame)

        if results:
            face = max(results, key=lambda x: x['box'][2] * x['box'][3])
            emotions = face['emotions']
            emotion = max(emotions, key=emotions.get)
            conf = emotions[emotion]
            print(f"Emotion: {emotion}  |  Confidence: {conf:.2f}")
        else:
            print("No face detected")

        # Show the live camera feed
        cv2.imshow("KOKO Emotion Detection", frame)

        # Press 'q' to quit safely
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Shutting down...")
            break

    picam2.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
