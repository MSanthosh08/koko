# KOKO: Emotion-Aware Interactive Robot

KOKO is a Raspberry Pi 5 project that detects human emotions using a PiCamera, shows animated eyes on a 9.7" display, and triggers robot actions based on the detected emotion.

## Features

- Emotion detection via FER (Facial Expression Recognition)
- Fullscreen animated eyes using Pygame
- Robot actions mapped to emotions
- Feedback loop for iterative improvements (stubbed)

## Setup

1. **Clone the repo:**

```bash
git clone https://github.com/MSanthosh08/KOKO.git
cd KOKO

Run the setup script:
Run the setup script:

chmod +x setup_instructions.sh
./setup_instructions.sh


Activate virtual environment:

source ~/koko_venv/bin/activate


Test camera and FER:

python3 test_emotion.py


Run KOKO main program:

python3 main.py


Press q or ESC to quit safely.

Repo Structure
KOKO/
│ main.py
│ test_emotion.py
│ display_eyes.py
│ robot_controller.py
│ recommender_engine.py
│ requirements.txt
│ setup_instructions.sh
│ README.md

Robot Actions Mapping
Emotion	Action
happy	spin
sad	gentle_forward
angry	calm_movement
neutral	idle
surprise	jump
fear	hide
License

MIT License

This repo is fully ready to use:

main.py runs the robot loop.

test_emotion.py tests camera + emotion detection.

display_eyes.py handles the animated eyes.

robot_controller.py handles hardware or prints actions.

recommender_engine.py is stubbed for now.

setup_instructions.sh sets everything up.
