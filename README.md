## Draw This.

_Draw This_ is a polaroid camera that draws cartoons.
You point, and shoot - and out pops a cartoon; the camera's best interpretation of what it saw.
The camera is a mash up of a neural network for object recognition, the google quickdraw dataset, a thermal printer, and a raspberry pi.

![photo](../master/photos/raspi-camera-cartoons.jpg)

The software can run both on a desktop environment such as a laptop, or an embedded environment on a raspberry pi.

### Desktop installation

- Requirements:
    * Python 2.7
- install dependencies using `pip install -r requirements.txt` from the `cartoonify` subdirectory.
- install app using `pip install -e .` from within the `cartoonify` directory
- run app from command line using `cartoonify`
- you will be asked if you want to download the cartoon dataset and tensorflow model. Select yes.
- close the app using cntrl-C once the downloads have finished.
- start the app again using `cartoonify --gui`

### Raspberry pi wiring

The following wiring diagram will get you started with a shutter button and a status LED.
If the software is working correctly, the status LED should light up for 2-3 seconds when the shutter is pressed
while the raspi is processing an image. If the light stays on, something has gone wrong (most likely the camera is unplugged).

![Wiring diagram](../master/schematics/cartoon_camera_schematic_bb.png)

### Raspberry pi installation

- requirements:
    * raspberry pi 3
    * rasbian stretch image on 16gb SD card (8gb too small)
    * internet access on the raspi
    * pip + python
    * raspi camera v2
    * a button, led, 220 ohm resistor and breadboard
    * (optional) Thermal printer to suit a raspi 3

- install docker on the raspi by running: `curl -sSL https://get.docker.com | sh`
- set up and enable the raspi camera through `raspi-config`
- clone the source code from this repo
- run `./raspi-build.sh`. This will download the google quickdraw dataset and tensorflow model,
then build the required docker image.
- run `./raspi-run.sh`. This will start the docker image.


### Troubleshooting

- Check the log files in the `cartoonify/logs` folder for any error messages.
- The most common issue when running on a raspi is not having the camera plugged in correctly.
- If nothing is printing, check the logs then check whether images are being saved to `cartoonify/images`.
- Check that you can manually print something from the thermal printer from the command line.

