"""
fer_integration.py
Simple wrapper to get emotion + confidence from camera frames using `fer` library.
Uses OpenCV VideoCapture(0) — on Raspberry Pi your OV5647 camera should be available via /dev/video0
(if you use raspicam driver, ensure v4l2 is configured).

Usage:
    from fer_integration import FERWrapper
    fer = FERWrapper(device=0)
    frame, ok = fer.read_frame()
    if ok:
        emotion, conf = fer.detect(frame)
    fer.release()
"""

from fer import FER
import cv2
import numpy as np

class FERWrapper:
    def __init__(self, device=0, mtcnn=False):
        # mtcnn True uses MTCNN face detection (slower), default False uses opencv detector inside fer
        self.detector = FER(mtcnn=mtcnn)
        # OpenCV capture
        self.cap = cv2.VideoCapture(device)
        # Recommended capture properties (tweak for your camera / Pi)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def read_frame(self):
        """Return (frame, ok). frame is BGR numpy array (OpenCV format)."""
        if not self.cap or not self.cap.isOpened():
            return None, False
        ret, frame = self.cap.read()
        if not ret or frame is None:
            return None, False
        return frame, True

    def detect(self, frame):
        """
        Returns: (emotion_label, confidence_float)
        If no face detected, returns ("neutral", 0.0)
        """
        try:
            results = self.detector.detect_emotions(frame)
            if not results:
                return "neutral", 0.0
            # choose face with largest box area
            face = max(results, key=lambda x: x['box'][2] * x['box'][3])
            emotions = face.get('emotions', {})
            if not emotions:
                return "neutral", 0.0
            # emotion with highest score
            emotion = max(emotions, key=emotions.get)
            confidence = float(emotions[emotion])
            return emotion, confidence
        except Exception as e:
            # on failure return neutral to be safe
            print("[FERWrapper] detect error:", e)
            return "neutral", 0.0

    def release(self):
        try:
            if self.cap:
                self.cap.release()
        except Exception:
            pass
