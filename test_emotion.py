# test_emotion.py
from fer import FER
import cv2

def main():
    detector = FER(mtcnn=True)
    cap = cv2.VideoCapture(0)  # Camera index (0 for USB cam or CSI cam)

    print("Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Camera not detected!")
            break

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

        # Show live feed
        cv2.imshow("KOKO Emotion Detection", frame)

        # Quit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Shutting down...")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
