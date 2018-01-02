import matplotlib.pyplot as plt
import cv2
import numpy as np
import math
import os
import time
import random


def edgeDetection(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_red = np.array([30, 150, 50])
    upper_red = np.array([255, 255, 180])

    mask = cv2.inRange(hsv, lower_red, upper_red)
    res = cv2.bitwise_and(img, img, mask=mask)
    img = cv2.Canny(img, 50, 150)
    return img


def getSrcPoint(img):
    h, w = img.shape[:2]
    for row in range(0, h)[::-1]:
        for col in range(0, w):
            if (50 < img[row][col][0] < 60) and (53 < img[row][col][1] < 63) and (95 < img[row][col][2] < 110):
                m = row
                n = col + 8
                break
        else:
            continue
        break
    print(m, n)
    return m, n


def getDestPoint(img, m, n):
    k = math.tan(math.pi / 6)
    count = 0
    w = img.shape[1]
    if(n < w / 2):
        print("left")
        col = w - 1
        row = int(m - (w - 1 - n) * k)
        while(img[row][col] < 10):
            img[row][col] = 255
            if count == 0:
                row = row + 1
            else:
                col = col - 1
            count = (count + 1) % 3
        dest_n = col
        dest_m = row
    else:
        print("right")
        col = 0
        row = int(m - (n + 1) * k)
        while(img[row][col] < 10):
            img[row][col] = 255
            if count == 0:
                row = row + 1
            else:
                col = col + 1
            count = (count + 1) % 3
        dest_n = col
        dest_m = row
    print(dest_m, dest_n)
    return img, dest_m, dest_n


def getDistance(filename):
    img = plt.imread(filename)
    img = img.copy()
    m, n = getSrcPoint(img)
    img = img[0:m, :]
    img = edgeDetection(img)
    img, dest_m, dest_n = getDestPoint(img, m, n)

    currenttime = time.strftime("%H%M%S", time.localtime())
    filename = 'result_' + currenttime + '.jpg'
    cv2.imwrite(filename, img)
    distance = math.sqrt(abs((dest_m - m)**2) + abs((dest_n - n)**2))
    print(distance)
    return distance


def getScreenshot():
    os.system('adb shell screencap -p /sdcard/screenshot.jpg')
    os.system('adb pull /sdcard/screenshot.jpg')


def jump(distance):
    press_coefficient = 1.765
    press_time = distance * press_coefficient
    press_time = int(press_time)
    cmd = 'adb shell input swipe 10 10 10 10 {duration}'.format(
        duration=press_time
    )
    os.system(cmd)


def main():
    # for i in range(100):
    #     print(i)
    while True:
        getScreenshot()
        distance = getDistance("screenshot.jpg")
        jump(distance)
        time.sleep(random.uniform(1, 1.1))
        print('\n')


if __name__ == '__main__':
    main()
