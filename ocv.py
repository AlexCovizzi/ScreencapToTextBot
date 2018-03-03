import numpy as np
import cv2
import dimage
import statistics
import constants as c

MIN_WIDTH = 52
MIN_HEIGHT = 52

DEBUG = False

# imgBuf -> buffered image
# return list of dict (color, rects)
def analyze(imgBuf, debug = False):
    global DEBUG
    DEBUG = debug
    rects = []
    image = loadImage(imgBuf)

    blueRects = analyzeByColor(image, c.BLUE_BOUNDS)
    # if there are no blue rectangles we can assume that the screencap
    # is not a conversation
    if not blueRects:
        return []

    grayRects = analyzeByColor(image, c.GRAY_BOUNDS)

    rects.extend(blueRects)
    rects.extend(grayRects)
    
    if DEBUG:
        for rect in rects:
            print(rect)
            cv2.rectangle(image, (rect["left"], rect["top"]), (rect["left"]+rect["w"], rect["top"]+rect["h"]), (0, 0, 255), 3)
        
        cv2.imshow('dst_rt', cv2.resize(image, (0,0), fx=0.4, fy=0.4))
        cv2.waitKey(0)

    return rects

def loadImage(imgBuf):
    #use numpy to construct an array from the bytes
    x = np.fromstring(imgBuf, dtype='uint8')

    #decode the array into an image
    image = cv2.imdecode(x, 1)

    return image

def analyzeByColor(image, colorBounds):
    contours = findContours(image, colorBounds)
    boundingRects = getBoundingRects(contours, MIN_WIDTH, MIN_HEIGHT)

    return boundingRects

# image -> ocv image
def findContours(image, colBoundaries):
    grayThresh = int(statistics.median(colBoundaries[0]))

    lower = np.array(colBoundaries[0], dtype = "uint8")
    upper = np.array(colBoundaries[1], dtype = "uint8")

    # find the colors within the specified boundaries and apply the mask
    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask = mask)

    # convert to grayscale
    imgray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
    # erosion
    kernel = np.ones((5,5),np.uint8)
    imgray = cv2.erode(imgray,kernel,iterations = 1)

    if DEBUG:
        cv2.imshow('dst_rt', cv2.resize(imgray, (0,0), fx=0.4, fy=0.4))
        cv2.waitKey(0)

    ret, thresh = cv2.threshold(imgray, grayThresh, 255, cv2.THRESH_TRUNC)

    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return contours

def getBoundingRects(contours, min_w, min_h):
    rects = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > min_w and h > min_h and w < c.IMG_WIDTH-c.IMG_WIDTH/12:
            rects.append( {"left":x, "top":y, "w":w, "h":h} )
    return rects
    

