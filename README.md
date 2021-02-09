# R2D2 Eyes
Track an object and move the head.  This will use OpenCV to track an object.  It will then turn the head to track the object.  If no specific object is found, it will do some random looking around.

The head is moved with a motor without an encoder, so at initialization, the head will need to determine where forward is.  It will then track any object.  The head position will not be the same the direction the body will move.  This is to ensure the robot will not run away.

Right now the object it tries to detect is a red object.  In the future it will be a specific color or infrared. I prefer not infrared so the camera can be used for other purposes.

# object_cap.py
Testing is being done right now with a Raspberry PI 3 B, a Adafruit PCA9685 and a servo to test the detection code.

This is the verify the code can detect and move to the correct position. Then the motor controller will be used to take servo input to move the R2D2 head.

# Install OpenCV 4.1.2 on Raspbian Buster

## Increase the swap space size
```bash
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile
```

Change the size to 2048
```bash
CONF_SWAPSIZE=2048
```

Reset the swap space
```bash
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
sudo reboot
```

## Build and Install

```bash
cd opencv
chmod +x *.sh
./download-opencv.sh
./install-deps.sh
./build-opencv.sh
cd ~/opencv/opencv-4.1.2/build
sudo make install
```

https://gist.github.com/willprice/abe456f5f74aa95d7e0bb81d5a710b60


You can monitor the build with Top to see if you are running out of memory.
