import numpy as np
import cv2
import time
import downloadimage
import pytesseract
from PIL import Image

def find(pil_img):
    cv_img = cv2.cvtColor(np.array(pil_img, dtype=np.uint8), cv2.COLOR_RGB2GRAY)

    wsize = cv_img.shape[1]

    contours = findContours(cv_img)
    rects = getBoundingRects(contours, int(wsize/24), int(wsize/20), wsize)

    for rect in rects:
        #print(rect)
        cv2.rectangle(cv_img, (rect["left"], rect["top"]), (rect["left"]+rect["w"], rect["top"]+rect["h"]), (0, 0, 255), 3)
        
    cv2.imshow('dst_rt', cv2.resize(cv_img, (0,0), fx=0.5, fy=0.5))
    cv2.waitKey(0)

    return rects

def findContours(cv_img):
    contours = []

    ret, upper_thresh = cv2.threshold(cv_img,244,255,cv2.THRESH_BINARY_INV)
    ret, lower_thresh = cv2.threshold(cv_img,140,255,cv2.THRESH_BINARY)
    cv_img = cv2.bitwise_and(lower_thresh, upper_thresh)

    cv_img = cv2.medianBlur(cv_img, 11)

    kernel = np.ones((7,7),np.uint8)
    cv_img = cv2.erode(cv_img, kernel)

    _,cnts,_ = cv2.findContours(cv_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in cnts:
        if is_contour_mostly_rectangular(cnt):
            contours.append(cnt)

    cv2.imshow('dst_rt', cv2.resize(cv_img, (0,0), fx=0.4, fy=0.4))
    cv2.waitKey(0)

    return contours

def is_contour_mostly_rectangular(contour):
    return True

def getBoundingRects(contours, min_w, min_h, max_w):
    rects = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > min_w and h > min_h and w < max_w-max_w/32:
            rects.append( {"left":x, "top":y, "w":w, "h":h} )
    return rects


if __name__ == '__main__':
    url = "https://i.imgur.com/Mps09BH.jpg"
    pil_img = downloadimage.get(url)
    cv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    
    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    ret, cv_img = cv2.threshold(cv_img,180,255,cv2.THRESH_BINARY)
    pil_img = Image.fromarray(cv_img)
    text = pytesseract.image_to_boxes(pil_img, lang="eng")
    lines = text.split('\n')
    boxes = []
    for line in lines:
        char = line.split(' ')
        box = {'text':char[0], 'x1':char[1], 'y1':char[2], 'x2':char[3], 'y2':char[4]}
        boxes.append(box)

    for box in boxes:
        print(box)
    cv2.imshow('dst_rt', cv2.resize(cv_img, (0,0), fx=0.4, fy=0.4))
    cv2.waitKey(0)
    