import cv2
import numpy as np
from adafruit_pca9685 import PCA9685

# For I2C setup
# PCA9685 communicates over I2C
from board import SCL, SDA
import busio

# Setup PCA9685 for Servo control
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)

# Create the I2C bus interface
# and connect it to the PCA9685
i2c_bus = busio.I2C(SCL, SDA)
pca = PCA9685(i2c_bus)

# Set the PWM frequency
# Specific to servo
pca.frequency = 50

# Setup the first webcam found
cap = cv2.VideoCapture(0)

# Get an initial size for frame
_, frame = cap.read()
rows, cols, _ = frame.shape

# Start position of the servo
position = 90
# Set the servo to the start position
kit.servo[0].angle = position

# Determine what is the center of the screen
center = int(cols/2)
x_midpoint = int(cols/2)

while True:
    # Capture a frame from the webcam
    _, frame = cap.read()
    
    # Create a display mask
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Red colors
    # We will search for red mask color
    low_red = np.array([161, 155, 84])
    high_red = np.array([179, 255, 255])
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    
    # A contour is an area that has the mask color
    # This will segragate the frame to only display black and white
    # where white is the color we selected to look for
    contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Sort the contours and put biggest white spot as first
    contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)
    
    # Create a rectangle around the first largest contour found
    for cnt in contours:
        # Get the dimensions of the contour
        (x,y,w,h) = cv2.boundingRect(cnt)
    
        # Rectangle created around the contour
        # frame, top right corner, bottom left corner, color or rectangle, thickness
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Mid point of the contour
        # This is used to point the servo to the mid point of the contour
        x_midpoint = int((x + x + w) / 2)
        
        # Stop on the first (largest) 
        break
    
    # Draw a line down the center of the object
    cv2.line(frame, (x_midpoint, 0), (x_midpoint, 480), (0, 255, 0), 2)
    
    # Display the frame with the rectangle and line
    cv2.imshow("Frame", frame)
    
    # Debug to view the segragated area
    #cv2.imshow("contour", red_mask)
    
    # Stop when ESC is pressed
    key = cv2.waitKey(1)
    if key == 27:
        break
    
    # Move servo to keep object in the center
    # Give a buffer around the center
    # so it does not continously try to correct
    if x_midpoint < center - 30:
        position += 1.5
    elif x_midpoint > center + 30:
        position -= 1.5
    
    # Ensure to not exceeds min and max
    if position > 180:
        position = 180
    if position < 0:
        position = 0
    
    # Move the servo to the new position
    kit.servo[0].angle = position

# Cleanup
cap.release()
cv2.destroyAllWindows()
