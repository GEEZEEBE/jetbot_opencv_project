import cv2 as cv
import numpy as np
from jetbot import Robot
import time

width, height = 224, 224

speed_gain = 0.1
steering_gain = 0.1
steering_dgain = 0.1
steering_bias = 0.1

angle = 0.0
angle_last = 0.0

robot = Robot()

def gstreamer_pipeline(
    capture_width=224,
    capture_height=224,
    display_width=224,
    display_height=224,
    framerate=20,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


def image_proc(img):
    img = cv.resize(img, (width, height))
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img_blur = cv.GaussianBlur(img_gray, (7, 7), 2)
    img_thresh = cv.adaptiveThreshold(img_blur, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 4)
    img_canny = cv.Canny(img_thresh, 50, 50)

    contours, _ = cv.findContours(img_canny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    for contour in contours:
        area = cv.contourArea(contour)
        epsilon = 0.02 * cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, epsilon, True)

        if area > 50 and len(approx) == 4:
            # moments
            M = cv.moments(contour)
            m_x = int(M['m10']/M['m00'])
            m_y = int(M['m01']/M['m00'])
            return m_x, m_y
    return None, None


def execute(xy):
    global angle, angle_last
    x = np.abs(width - xy[0])/2
    y = height - xy[1]
    # y = (0.5 - xy[1]) / 2.0
    print("x: ", x, "y: ", y)

    speed = speed_gain

    angle = np.arctan2(x, y)
    pid = angle * steering_gain + (angle - angle_last) * steering_dgain
    angle_last = angle

    steering = pid + steering_bias

    left = max(min(speed + steering, 1.0), 0.0)
    right = max(min(speed - steering, 1.0), 0.0)
    robot.left_motor.value = left
    robot.right_motor.value = right


def main():

    gs = gstreamer_pipeline()
    print(gs)
    cap = cv.VideoCapture(gs)

    while cap.isOpened():
        _, img = cap.read()
        x, y = image_proc(img)
        if x == None and y == None:
            x, y = 112, 48
        execute([x, y])

        # Stop the program on the ESC key
        if cv.waitKey(30) == 27:
            break
    else:
        print("Unable to open camera")

    cap.release()
    robot.stop()


if __name__ == "__main__":
    main()
