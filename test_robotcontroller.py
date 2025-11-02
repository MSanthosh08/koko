"""
test_robotcontroller.py
Tests two-way serial communication between Raspberry Pi/PC and Arduino.
Sends each emotion and prints whatever Arduino sends back.
"""

import time
import serial

# 🔧 Change this to your actual Arduino port
# For Raspberry Pi:  "/dev/ttyUSB0"  or  "/dev/ttyACM0"
# For Windows:       "COM3"
PORT = "/dev/ttyUSB0"
BAUD_RATE = 9600

# Connect to Arduino
print(f"[INFO] Connecting to {PORT} at {BAUD_RATE} baud...")
arduino = serial.Serial(PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # Wait for Arduino reset

# List of test emotions
emotions = ["HAPPY", "SAD", "ANGRY", "NEUTRAL", "SURPRISE"]

print("\n[TEST] Starting send/receive test...\n")

try:
    for emo in emotions:
        # Send emotion
        cmd = emo + "\n"
        arduino.write(cmd.encode())
        print(f"[SENT] {emo}")

        # Wait a bit and read any response
        time.sleep(0.5)
        response = arduino.readline().decode().strip()
        if response:
            print(f"[RECEIVED] {response}")
        else:
            print("[RECEIVED] (no response)")

        time.sleep(2)

    print("\n[TEST] Completed successfully!")

except KeyboardInterrupt:
    print("\n[TEST] Interrupted by user.")

finally:
    arduino.close()
    print("[INFO] Connection closed.")
