# KOKO - Run Instructions

1. Create virtualenv and install dependencies:
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

2. Connect your OV5647 camera and ensure it's accessible via /dev/video0.
   If using Raspberry Camera via libcamera, you may need v4l2loopback or use OpenCV with appropriate backend.

3. (Optional) Connect robot controller (Arduino) to USB and set ROBOT_SERIAL in main.py to '/dev/ttyUSB0'.

4. Run:
   python3 main.py

5. The 9.7" display will open fullscreen with animated eyes.
   Press Ctrl+C to stop. If using keyboard on display, press ESC will close Pygame window.

Notes:
- If FER is slow on Pi, consider running a smaller model or lowering camera resolution.
- Tune LOOP_DELAY and AFTER_DELAY in main.py for better responsiveness.
- Review robot_controller.command_map to match your robot firmware commands.
