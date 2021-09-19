import drv6470
import time
import RPi.GPIO as GPIO

import cv2
import numpy as np

if __name__ == '__main__':
    def callback(*arg):
        print (arg)

LASERLED = 22
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(LASERLED, GPIO.OUT, initial=GPIO.HIGH)
#GPIO.output(LASERLED, GPIO.HIGH)

drvH = drv6470.L6470(0, 1)
drvV = drv6470.L6470(0, 0)

drvH.SetParam(drv6470.REGADR_KVAL_RUN, 180)
drvH.SetParam(drv6470.REGADR_KVAL_ACC, 200)
drvH.SetParam(drv6470.REGADR_KVAL_DEC, 200)
drvV.SetParam(drv6470.REGADR_KVAL_RUN, 180)
drvV.SetParam(drv6470.REGADR_KVAL_ACC, 200)
drvV.SetParam(drv6470.REGADR_KVAL_DEC, 200)

        

cv2.namedWindow( "result" )

cap = cv2.VideoCapture(0)

hsv_min = np.array((30, 130, 80), np.uint8)
hsv_max = np.array((50, 255, 255), np.uint8)

while True:
    flag, img = cap.read()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV )
    thresh = cv2.inRange(hsv, hsv_min, hsv_max)

    moments = cv2.moments(thresh, 1)
    dM01 = moments['m01']
    dM10 = moments['m10']
    dArea = moments['m00']

    if dArea > 100:
        x = int(dM10 / dArea)
        y = int(dM01 / dArea)
        cv2.circle(img, (x, y), 12, (255,255,255), 2)

        if (x > 400):
            drvV.HardStop()
            drvH.Run(200)
                
        if (x < 200):
            drvV.HardStop()
            drvH.Run(-200)
                
        if (y > 315):
            drvH.HardStop()
            drvV.Run(100)
        
        if (y < 150):
            drvH.HardStop()
            drvV.Run(-100)

    cv2.imshow('result', img) 
 
    ch = cv2.waitKey(5)
    if ch == 27:
        break

#GPIO.output(LASERLED, GPIO.LOW)

GPIO.cleanup()
drvH.HardHiZ()
drvV.HardHiZ()
