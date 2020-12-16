import cv2 as cv
import numpy as np

width, height = 224, 224

color_list, binary_list = [], []
for i in range(1, 11):
    src = "snapshots/"+ str(i) +".jpg"
    img_color = cv.imread(src)

    color_list.append(img_color)

    img_gray = cv.cvtColor(img_color, cv.COLOR_BGR2GRAY)
    img_blur = cv.GaussianBlur(img_gray, (7, 7), 2)
    # ret, img_thresh = cv.threshold(img_blur, 127, 255, cv.THRESH_TOZERO_INV)
    img_thresh = cv.adaptiveThreshold(img_blur, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 4)
    img_canny = cv.Canny(img_thresh, 50, 50)

    binary_list.append(img_canny)

    contours, _ = cv.findContours(img_canny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    i = 0
    for contour in contours:
        area = cv.contourArea(contour)
        epsilon = 0.02 * cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, epsilon, True)

        if area > 50 and len(approx) == 4:
            cv.drawContours(img_color, [contour], 0, (255, 0, 0), 2)


c_hstack1 = color_list[0].copy()
b_hstack1 = binary_list[0].copy()
for i in range(1, 5):
    c_hstack1 = np.hstack((c_hstack1, color_list[i]))
    b_hstack1 = np.hstack((b_hstack1, binary_list[i]))

c_hstack2 = color_list[5].copy()
b_hstack2 = binary_list[5].copy()
for i in range(6, 10):
    c_hstack2 = np.hstack((c_hstack2, color_list[i]))
    b_hstack2 = np.hstack((b_hstack2, binary_list[i]))

c_vstack = np.vstack((c_hstack1, c_hstack2))
b_vstack = np.vstack((b_hstack1, b_hstack2))
cv.imshow("color", c_vstack)
cv.imshow("binary", b_vstack)





# for contour in contours:
#     area = cv.contourArea(contour)
#     cv.drawContours(img_color, [contour], 0, (255, 0, 0), 2)
#     x, y, w, h = cv.boundingRect(contour)
#     cv.rectangle(img_color, (x, y), (x+w, y+h), (0, 0, 255), 2)

#     epsilon = 0.02 * cv.arcLength(contour, True)
#     approx = cv.approxPolyDP(contour, epsilon, True)
#     print(len(approx))
#     if len(approx) == 3: text = "Tri"
#     elif len(approx) == 4:
#         ratio = w/h
#         if ratio > 0.98 and ratio < 1.03:
#             text = "Square"
#         else:
#             text = "Rectangle"
#     elif len(approx) > 4: text = "Circle"
#     else: text = "None"
#     cv.putText(img_color, text, (x+20, y+30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

# cv.imshow("result", img_color)

cv.waitKey(0)