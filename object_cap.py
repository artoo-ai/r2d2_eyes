import cv2
import numpy as np
#from PCA9685 import PCA9685

cap = cv2.VideoCapture(0)

position = 90 #degrees
x_midpoint = 0

while True:
    _, frame = cap.read()
    
    # Only display mask
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Red colors
    low_red = np.array([161, 155, 84])
    high_red = np.array([179, 255, 255])
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    
    # A contour is an area that has the mask color
    contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Sort the contours and put biggest as first
    contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)
    
    # Create a rectangel around the first largest contour found
    for cnt in contours:
        # Get the dimensions of the contour
        (x,y,w,h) = cv2.boundingRect(cnt)
    
        # Rectangle created around the contour
        # frame, top right corner, bottom left corner, color, thickness
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Mid point of the contour
        x_midpoint = int((x + x + w) / 2)
        
        # Stop on the first (largest) 
        break
    
    cv2.line(frame, (x_midpoint, 0), (x_midpoint, 480), (0, 255, 0), 2)
    cv2.imshow("Frame", frame)
    #cv2.imshow("contour", red_mask)
    
    key = cv2.waitKey(1)
    
    if key == 27:
        break
    
cap.release()
cv2.destroyAllWindows()
