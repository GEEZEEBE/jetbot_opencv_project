import cv2 as cv
import numpy as np

width, height = 224, 224

src = "snapshots/12.jpg"
img_color = cv.imread(src)

img_gray = cv.cvtColor(img_color, cv.COLOR_BGR2GRAY)
img_blur = cv.GaussianBlur(img_gray, (7, 7), 2)
# ret, img_thresh = cv.threshold(img_blur, 127, 255, cv.THRESH_TOZERO_INV)
img_thresh = cv.adaptiveThreshold(img_blur, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 4)
img_canny = cv.Canny(img_thresh, 50, 50)


contours, _ = cv.findContours(img_canny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
i = 0
for contour in contours:
    area = cv.contourArea(contour)
    epsilon = 0.02 * cv.arcLength(contour, True)
    approx = cv.approxPolyDP(contour, epsilon, True)

    if area > 50 and len(approx) == 4:
        cv.drawContours(img_color, [contour], 0, (255, 0, 0), 2)

        # moments
        M = cv.moments(contour)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        cv.circle(img_color, (cx, cy), 5, (0, 0, 255), -1)

cv.imshow("color", img_color)
cv.imshow("binary", img_canny)

cv.waitKey(0)