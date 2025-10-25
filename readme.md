Step 1: Activate Your Conda Environment
conda activate koko


(You should see (koko) appear at the start of your prompt.)

🐍 Step 2: Install What Conda Can Handle (Fast + Precompiled)

Conda installs pre-built ARM-compatible binaries — this saves tons of compile time on the Pi.

conda install -y \
  flask \
  opencv \
  numpy \
  pandas \
  scikit-learn \
  pyserial


⚠️ opencv from conda provides the same functionality as opencv-python.
You can skip opencv-python from pip after this.

🌐 Step 3: Install the Rest via pip

Some packages aren’t on Conda or are better installed from PyPI:

pip install flask-socketio eventlet fer deepface


These will install additional dependencies (like TensorFlow or PyTorch for DeepFace).
On Raspberry Pi, this might take time or even fail if there’s not enough RAM.
You can use swap space if needed:

sudo dphys-swapfile swapoff
sudo dphys-swapfile setup 2048
sudo dphys-swapfile swapon

🤖 Step 4: Install ROS Python Library Separately

rospy is not a pip or conda package — it’s part of ROS.
Install it with apt:

For ROS Noetic:

sudo apt install ros-noetic-rospy


For ROS 2 (Humble, Foxy, etc.):

sudo apt install ros-humble-rospy


(Replace humble with your actual ROS distro.)

✅ Step 5: Verify Installations

After everything installs, test in Python:

python -c "import flask, flask_socketio, eventlet, cv2, numpy, pandas, sklearn, fer, deepface, serial; print('✅ all imports OK')"


If you see “✅ all imports OK”, you’re good to go.