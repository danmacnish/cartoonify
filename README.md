### First use

- install app using `pip install setup.py .`
- run app from command line using `cartoonify`
- you will be asked if you want to download the cartoon dataset and image recognition network. Select yes.
- close the app using cntrl-C
- start the app again using `cartoonify --gui`

### raspberry pi installation

- install libffi-dev using `sudo apt-get install libffi-dev`
- install the camera driver using `sudo apt-get install python3-picamera`
- install h5py using `sudo apt-get install python3-h5py`
- install cython using `pip install cython`
- `wget https://github.com/samjabrahams/tensorflow-on-raspberry-pi/releases/download/v1.1.0/tensorflow-1.1.0-cp34-cp34m-linux_armv7l.whl`
- `sudo pip3 install tensorflow-1.1.0-cp34-cp34m-linux_armv7l.whl`
