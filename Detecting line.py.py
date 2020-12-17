# Detecting line.py
import cv2 as cv 
import numpy as np
import os
def make_canny(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray,(3,3),0)
    canny = cv.Canny(blur,50,150) ## 
    return canny 

dir = "./snapshots_road"
roads = os.listdir(dir)
for road in roads:

    image = cv.imread(dir + '/' + road)
    canny = make_canny(image)
    # cv.imshow("canny", canny)
    # cv.waitKey(0)
  
    contours, hierarchy = cv.findContours(canny, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE) 
    for contour in contours:
        
        area = cv.contourArea(contour)
        epsilon = 0.025*cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, epsilon, True)
        if len(approx) == 4 and area > 50:
            cv.drawContours(image, [approx], 0, (0,0,255), -1)
            cv.imshow("image", image)
            cv.waitKey(0)

            #https://github.com/NVIDIA-AI-IOT/jetbot/tree/master/notebooks