"""
robot_controller.py
Handles serial communication between Raspberry Pi and Arduino Nano.

- Sends emotion commands as plain text (e.g., 'HAPPY', 'SAD', etc.)
- Reads and prints Arduino responses for debugging
- Baud Rate: 9600
"""

import serial
import time

class RobotController:
    def __init__(self, serial_port="/dev/ttyUSB0", baud_rate=9600):
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.ser = None

        if serial_port:
            try:
                print(f"[ROBOT] Connecting to {serial_port} at {baud_rate} baud...")
                self.ser = serial.Serial(serial_port, baud_rate, timeout=1)
                time.sleep(2)  # Allow Arduino to reset
                print("[ROBOT] Connection established.")
            except Exception as e:
                print(f"[ERROR] Could not open serial port: {e}")
                self.ser = None
        else:
            print("[ROBOT] No serial port provided. Running in simulation mode.")

    def send_action(self, emotion):
        """Send an emotion command to the Arduino and print any response."""
        emotion = emotion.strip().upper()

        if self.ser:
            try:
                # Send emotion command
                self.ser.write((emotion + "\n").encode())
                print(f"[ROBOT] Sent: {emotion}")

                # Optional: read back Arduino response (for confirmation)
                time.sleep(0.3)
                if self.ser.in_waiting > 0:
                    response = self.ser.readline().decode().strip()
                    if response:
                        print(f"[ROBOT] Received: {response}")
            except Exception as e:
                print(f"[ERROR] Failed to send/read data: {e}")
        else:
            # Simulation mode (no Arduino connected)
            print(f"[ROBOT SIM] Would send: {emotion}")

    def close(self):
        """Close serial connection safely."""
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("[ROBOT] Serial connection closed.")
        else:
            print("[ROBOT SIM] Closed simulation controller.")
