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
