### desktop installation

- install app using `pip install -e .`
- run app from command line using `cartoonify`
- you will be asked if you want to download the cartoon dataset and tensorflow model. Select yes.
- close the app using cntrl-C
- start the app again using `cartoonify --gui`

### raspberry pi installation

- requirements:
    * rasbian stretch image on 16gb SD card (8gb too small)
    * internet access on the raspi
    * (optional) raspi camera v2
- install docker on the raspi `curl -sSL https://get.docker.com | sh`
- run `raspi-build.sh`. This will download the google quickdraw dataset and tensorflow model,
then build the required docker image.
- run `raspi-run.sh`. This will start the docker image.

### optional raspi setup

- instructions for [setting up raspi as an access point](https://www.raspberrypi.org/documentation/configuration/wireless/access-point.md)
