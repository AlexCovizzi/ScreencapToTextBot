import numpy as np
import cv2
import time
import downloadimage
import pytesseract
from PIL import Image

def find(pil_img):
    cv_img = np.array(pil_img, dtype=np.uint8)
    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)

    prep_img = preprocess(cv_img)
    boxes = find_bounding_boxes(prep_img)
    # sort by y1
    boxes.sort(key=lambda box: box[1])
    
    return boxes

def preprocess(cv_img):
    # preprocess
    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    cv_img = cv2.GaussianBlur(cv_img, (7,7), 0)
    #cv_img = contrast(cv_img, 7, -210)
    cv_img = cv2.Canny(cv_img, 20, 40)

    return cv_img

def find_bounding_boxes(cv_img):
    boxes = []
    _,contours,_ = cv2.findContours(cv_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # close every contour
    for i, cnt in enumerate(contours):
        contours[i] = cv2.convexHull(cnt)

    # build contours hierarchy i.e find outer contours
    # we need this to keep only the contours that have at least
    # one contour inside (probably the contour of text)
    bounding_rects = [cv2.boundingRect(cnt) for cnt in contours]
    hierarchy = build_hierarchy(bounding_rects)
    
    boxes = []
    for member in hierarchy:
        parent_idx = member[0]
        children_idx = member[1]
        cnt = contours[parent_idx]
        x, y, w, h = bounding_rects[parent_idx]
        bounding_rect = np.array([[x, y], [x+w, y], [x+w, y+h], [x, y+h]])
        if w > 28 and h > 28 and is_contour_mostly_rectangular(cnt, bounding_rect):
            #cv2.drawContours(cv_img, [contours[parent]], 0, (0,255,0), 3)
            box = (x, y, x+w, y+h)
            boxes.append(box)

    # TODO: remove duplicates
    boxes = list(set(boxes))

    return boxes

def is_contour_mostly_rectangular(cnt, bounding_rect):
    ret = cv2.matchShapes(cnt, bounding_rect, 1, 0.0)

    vertical = 0
    horizontal = 0
    last_x, last_y = cnt[0][0]
    for pt in cnt[1:]:
        x, y = pt[0]
        if last_x-4 < x < last_x+4:
            v = abs(last_y-y)
            if v > vertical: vertical = v
        if last_y-2 < y < last_y+2:
            h = abs(last_x-x)
            if h > horizontal: horizontal = h
        last_x = x
        last_y = y

    return (ret < 0.15 and vertical > 8 and horizontal > 24)

def build_hierarchy(rects):
    hierarchy = []
    for i, rect_a in enumerate(rects):
        member = (i, [])
        for j, rect_b in enumerate(rects):
            if is_b_inside_a(rect_a, rect_b):
                member[1].append(j)
                [hierarchy.remove(m) for m in hierarchy if m[0] == j]
                    
        if member[1]: hierarchy.append(member)

    return hierarchy

def is_b_inside_a(a, b):
    xa, ya, wa, ha = a
    xb, yb, wb, hb = b
    return (xa < xb < xb+wb < xa+wa and ya < yb < yb+hb < ya+ha)

def contrast(cv_img, alpha=1.5, beta=-60.0):
    array_alpha = np.array([float(alpha)])
    array_beta = np.array([float(beta)])

    cv_img = cv2.add(cv_img, array_beta)
    cv_img = cv2.multiply(cv_img, array_alpha)
    
    return cv_img

if __name__ == '__main__':
    import downloadimage
    import pytesseract

    urls = ["https://i.imgur.com/tQIXpmF.jpg","https://i.imgur.com/ub1JcdD.jpg","https://i.imgur.com/nsuVc9I.jpg","https://i.redd.it/75hvw31dg5o01.jpg"]
    
    for url in urls:
        pil_img = downloadimage.get(url)

        cv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

        boxes = find(pil_img)
        for box in boxes:
            bounding_rect = np.array([[box['x1'], box['y1']], [box['x2'], box['y1']], [box['x2'], box['y2']], [box['x1'], box['y2']]])
            cv2.drawContours(cv_img, [bounding_rect], 0, (0,255,0), 3)
            
        cv2.imshow('img', cv2.resize(cv_img, (0,0), fx=0.5, fy=0.5))
        cv2.waitKey(0)