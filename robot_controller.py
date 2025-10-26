"""
robot_controller.py
Abstracts sending motion commands to the mobile robot.
Preferred: microcontroller (Arduino) receives simple text commands over serial (USB/TTL).
Fallback: uses print only so you can test without hardware.

Customize the `command_map` to match your robot firmware commands.
"""

import time

class RobotController:
    def __init__(self, serial_port=None, baud=115200, use_gpio=False):
        """
        serial_port: e.g. '/dev/ttyUSB0' or None for no serial (fallback)
        use_gpio: if True, attempt to use RPi GPIO-based motor control (not implemented here)
        """
        self.serial_port = serial_port
        self.baud = baud
        self.connected = False
        self.serial = None
        self.use_gpio = use_gpio
        if serial_port:
            try:
                import serial
                self.serial = serial.Serial(serial_port, baud, timeout=1)
                self.connected = True
                print(f"[RobotController] Serial connected at {serial_port}")
            except Exception as e:
                print("[RobotController] Serial connect failed:", e)
                self.connected = False
        else:
            print("[RobotController] Running in NO-HARDWARE fallback mode (prints only)")

        # mapping high-level action -> simple robot command (string)
        self.command_map = {
            "gentle_forward": "MOVE FORWARD SLOW",
            "gentle_spin": "SPIN LEFT SLOW",
            "dance_pattern": "DANCE SIMPLE",
            "quick_spin": "SPIN RIGHT FAST",
            "slow_back": "MOVE BACK SLOW",
            "retreat_slow": "MOVE BACK SLOW",
            "idle_patrol": "PATROL",
            "celebrate_pattern": "DANCE CELEBRATE",
            "show_surprised_eyes": "POSE SURPRISE",
            "play_cheer_music": "PLAY_MUSIC cheer1.mp3",
            "comfort_video": "PLAY_VIDEO comfort_clip.mp4",
            "soothing_audio": "PLAY_AUDIO sooth.mp3",
            "parent_notify": "NOTIFY PARENT"
        }

    def send_action(self, action_key):
        """
        action_key: a key from ASSETS or recommender result
        """
        cmd = self.command_map.get(action_key, None)
        if cmd is None:
            # fallback: treat action_key as raw command
            cmd = f"ACTION {action_key}"
        # send over serial if available otherwise print
        if self.connected and self.serial:
            try:
                self.serial.write((cmd + "\n").encode('utf-8'))
                time.sleep(0.05)
            except Exception as e:
                print("[RobotController] Serial write failed:", e)
        else:
            print(f"[RobotController] (FALLBACK) CMD -> {cmd}")

    def close(self):
        if self.connected and self.serial:
            try:
                self.serial.close()
            except Exception:
                pass
