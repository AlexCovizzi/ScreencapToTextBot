import numpy as np
import cv2
import time
import downloadimage
import pytesseract
from PIL import Image

def find(pil_img):
    cv_img = np.array(pil_img, dtype=np.uint8)
    cv_img = preprocess(cv_img)
    boxes = find_bounding_boxes(cv_img)
    # sort by y
    boxes.sort(key=lambda y: y["y1"])
    
    return boxes

def preprocess(cv_img):
    # preprocess
    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_RGB2GRAY)
    cv_img = cv2.GaussianBlur(cv_img, (7, 7), 0)
    cv_img = contrast(cv_img, 7, -210)
    cv_img = cv2.Canny(cv_img, 40, 60, apertureSize=5)

    return cv_img

def find_bounding_boxes(cv_img):
    boxes = []
    _,contours,_ = cv2.findContours(cv_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        # sometimes the message box contour is open
        cnt = cv2.convexHull(cnt)

        x, y, w, h = cv2.boundingRect(cnt)
        bounding_rect = np.array([[x, y], [x+w, y], [x+w, y+h], [x, y+h]])
        if is_contour_mostly_rectangular(cnt, bounding_rect) and w > 40 and h > 40:
            box = {"x1":x, "y1":y, "x2":x+w, "y2":y+h}
            boxes.append(box)

    return boxes

def is_contour_mostly_rectangular(cnt, bounding_rect):
    ret = cv2.matchShapes(cnt, bounding_rect, 1, 0.0)

    vertical = 0
    horizontal = 0
    last_x, last_y = cnt[0][0]
    for pt in cnt[1:]:
        x, y = pt[0]
        if x == last_x:
            v = abs(last_y-y)
            if v > vertical: vertical = v
        if y == last_y:
            h = abs(last_x-x)
            if h > horizontal: horizontal = h
        last_x = x
        last_y = y

    return (ret < 0.2 and vertical > 8 and horizontal > 24)

def contrast(cv_img, alpha=1.5, beta=-60.0):
    array_alpha = np.array([float(alpha)])
    array_beta = np.array([float(beta)])

    cv_img = cv2.add(cv_img, array_beta)
    cv_img = cv2.multiply(cv_img, array_alpha)
    
    return cv_img

if __name__ == '__main__':
    import downloadimage

    urls = ["https://i.redd.it/cp5rwyl8fco01.jpg"]
    for url in urls:
        pil_img = downloadimage.get(url)

        cv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        
        boxes = find(pil_img)
        for box in boxes:
            cv2.rectangle(cv_img, (box["x1"], box["y1"]), (box["x2"], box["y2"]), (0, 0, 255), 3)

        cv2.imshow('img', cv2.resize(cv_img, (0,0), fx=0.5, fy=0.5))
        cv2.waitKey(0)