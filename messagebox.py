import numpy as np
import cv2
import time
import downloadimage
import pytesseract
from PIL import Image

def find(pil_img):
    cv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    wsize = cv_img.shape[1]

    contours = findContours(cv_img)
    rects = getBoundingRects(contours, int(wsize/24), int(wsize/20), wsize)

    for rect in rects:
        #print(rect)
        cv2.rectangle(cv_img, (rect["left"], rect["top"]), (rect["left"]+rect["w"], rect["top"]+rect["h"]), (0, 0, 255), 3)
        
    #cv2.imshow('dst_rt', cv2.resize(cv_img, (0,0), fx=0.4, fy=0.4))
    #cv2.waitKey(0)

    return rects


def findContours(cv_img):
    contours = []

    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    cv_img = cv2.medianBlur(cv_img, 5)
    #cv_img = cv2.GaussianBlur(cv_img, (5, 5), 0)

    ret, upper_thresh = cv2.threshold(cv_img,242,255,cv2.THRESH_BINARY_INV)
    ret, lower_thresh = cv2.threshold(cv_img,120,255,cv2.THRESH_BINARY)
    cv_img = cv2.bitwise_and(lower_thresh, upper_thresh)

    kernel = np.ones((5,5),np.uint8)
    cv_img = cv2.erode(cv_img, kernel)

    _,contours,_ = cv2.findContours(cv_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cv2.imshow('dst_rt', cv2.resize(cv_img, (0,0), fx=0.4, fy=0.4))
    cv2.waitKey(0)
    '''
    #blue_mask = cv2.inRange(cv_img, (190, 160, 0), (255, 212, 110))
    blue_mask = cv2.inRange(cv_img, (10, 120, 200), (80, 200, 250))
    blue = cv2.bitwise_and(cv_img, cv_img, mask = blue_mask)
    blue = cv2.cvtColor(blue, cv2.COLOR_BGR2GRAY)
    blue = cv2.erode(blue,None,iterations = 2)
    ret, blue = cv2.threshold(blue, 127, 255, cv2.THRESH_TRUNC)
    _,blue_contours,_ = cv2.findContours(blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    gray_mask = cv2.inRange(cv_img, (220, 220, 220), (245, 245, 245))
    gray = cv2.bitwise_and(cv_img, cv_img, mask = gray_mask)
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    gray = cv2.erode(gray,None,iterations = 2)
    ret, gray = cv2.threshold(gray, 200, 255, cv2.THRESH_TRUNC)
    _,gray_contours,_ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contours.extend(blue_contours)
    contours.extend(gray_contours)
    '''

    return contours

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
    text = pytesseract.image_to_string(pil_img, lang="eng")
    print(text)
    cv2.imshow('dst_rt', cv2.resize(cv_img, (0,0), fx=0.4, fy=0.4))
    cv2.waitKey(0)
    