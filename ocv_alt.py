import numpy as np
import cv2 as cv
import dimage

IMAGES = ['https://i.redd.it/vt4n7trojqk01.jpg']
def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

def analyze(imgBuf):
    x = np.fromstring(imgBuf, dtype='uint8')
    image = cv.imdecode(x, 1)

    img = cv.GaussianBlur(image, (5, 5), 0)
    squares = []


    lower = np.array([30,130,0], dtype = "uint8")
    upper = np.array([255,246,255], dtype = "uint8")

    # find the colors within the specified boundaries and apply the mask
    mask = cv.inRange(img, lower, upper)
    img = cv.bitwise_and(img, img, mask = mask)

    # convert to grayscale
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # erosion
    kernel = np.ones((5,5),np.uint8)
    gray = cv.erode(gray,kernel,iterations = 1)

    gray = cv.Canny(gray, 0, 50, apertureSize=5)
    gray = cv.dilate(gray, None)

    #cv.imshow('squares', cv.resize(gray, (0,0), fx=0.5, fy=0.5))
    #cv.waitKey(0)

    ret, thresh = cv.threshold(gray, 180, 255, cv.THRESH_TRUNC)
    bin, contours, _hierarchy = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        cnt_len = cv.arcLength(cnt, True)
        cnt = cv.approxPolyDP(cnt, 0.005*cnt_len, True)
        if cv.contourArea(cnt) > 2000 and len(cnt) > 4:
            squares.append(cnt)

    rects = getBoundingRects(contours, 36, 36)
    
    for rect in rects:
        cv.rectangle(image, (rect["left"], rect["top"]), (rect["left"]+rect["w"], rect["top"]+rect["h"]), (0, 0, 255), 3)
    
    #cv.imshow('squares', cv.resize(image, (0,0), fx=0.5, fy=0.5))
    #cv.waitKey(0)

    '''
        cnt_len = cv.arcLength(cnt, True)
        #cnt = cv.convexHull(cnt)
        if cv.contourArea(cnt) > 5000 and len(cnt) > 4:
            cnt = cv.approxPolyDP(cnt, 0.005*cnt_len, True)
            if cv.isContourConvex(cnt):
                squares.append(cnt)
    for gray in cv.split(img):
        print("split: "+str(gray))
        for thrs in range(0, 255, 26):
            print("thrs: "+str(thrs))
            if thrs == 0:
                bin = cv.Canny(gray, 0, 50, apertureSize=5)
                bin = cv.dilate(bin, None)
            else:
                _retval, bin = cv.threshold(gray, thrs, 255, cv.THRESH_BINARY)
            bin, contours, _hierarchy = cv.findContours(bin, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                cnt_len = cv.arcLength(cnt, True)
                #cnt = cv.convexHull(cnt)
                if cv.contourArea(cnt) > 5000 and len(cnt) > 4:
                    cnt = cv.approxPolyDP(cnt, 0.005*cnt_len, True)
                    if cv.isContourConvex(cnt):
                        squares.append(cnt)
                cnt = cv.approxPolyDP(cnt, 0.001*cnt_len, True)
                if len(cnt) == 4 and cv.contourArea(cnt) > 1000 and cv.isContourConvex(cnt):
                    cnt = cnt.reshape(-1, 2)
                    max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in range(4)])
                    if max_cos < 0.1:
                        squares.append(cnt)
                        '''
    return squares


def getBoundingRects(contours, min_w, min_h):
    rects = []
    for cnt in contours:
        x, y, w, h = cv.boundingRect(cnt)
        if w > min_w and h > min_h and w < 720-720/24:
            rects.append( {"left":x, "top":y, "w":w, "h":h} )
    return rects

if __name__ == '__main__':
    for url in IMAGES:
        imgBuf = dimage.get(url)
        x = np.fromstring(imgBuf, dtype='uint8')
        img = cv.imdecode(x, 1)
        squares = analyze(img)
        #cv.drawContours( img, squares, -1, (0, 255, 0), 3 )
        #cv.imshow('squares', cv.resize(img, (0,0), fx=0.5, fy=0.5))
        #cv.waitKey()