# Cropping_tool.py

import cv2 as cv
import os

cwd = os.getcwd()
output_dir = cwd + "/crop" #잘라낸 이미지 저장 폴더
if not os.path.exists(output_dir):
    os.mkdir(output_dir)
    
isDragging = False
x0, y0, w, h = -1, -1, -1, -1
blue, red = (255, 0, 0), (0, 0, 255)
 
def Crop(event, x, y, flags, param):
    global isDragging, x0, y0, image, dir
    if event == cv.EVENT_LBUTTONDOWN:
        isDragging = True
        x0 = x
        y0 = y
    elif event == cv.EVENT_MOUSEMOVE:
        if isDragging:
            drawing = image.copy()
            cv.rectangle(drawing, (x0, y0), (x, y), blue, 2)
            cv.imshow('image', drawing)
    elif event == cv.EVENT_LBUTTONUP:
        if isDragging:
            isDragging = False
            w = x - x0
            h = y - y0
            if w > 0 and h > 0:
                drawing = image.copy()
                cv.rectangle(drawing, (x0, y0), (x, y), red, 2)
                cv.imshow('image', drawing)
                crop = image[y0:y0+h, x0:x0+w]
                cv.imshow('cropped', crop)
                cv.imwrite(output_dir + f'/{file_name}cropped.png', crop)
            else:
                cv.imshow('image', image)
                print('drag should start from left-top side')

input_dir = cwd + "/circle red sign/" ## input dir
files = os.listdir(input_dir)
for file in files:
    print(file)
    file_name = file.split(".")[0]
    image = cv.imread(input_dir + file)
    cv.imshow('image', image)
    cv.setMouseCallback('image', Crop)
    cv.waitKey()
    cv.destroyAllWindows()

           