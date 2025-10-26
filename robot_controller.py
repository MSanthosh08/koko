"""
robot_controller.py
Simulates or sends commands to the robot hardware.
Replace send_action() with actual motor commands if using Arduino/Raspberry Pi GPIO.
"""

class RobotController:
    def __init__(self, serial_port=None):
        self.serial_port = serial_port
        if serial_port:
            print(f"Connecting to robot at {serial_port}...")
            # TODO: implement serial connection
        else:
            print("No robot hardware connected, using simulation mode.")

    def send_action(self, action):
        if self.serial_port:
            # TODO: send serial commands
            print(f"[ROBOT] Sending command: {action}")
        else:
            print(f"[ROBOT SIM] Action: {action}")

    def close(self):
        print("Closing robot controller.")
        # TODO: close serial connection if any
