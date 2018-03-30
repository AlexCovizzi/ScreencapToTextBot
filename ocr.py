from PIL import Image
import cv2
import numpy as np
import pytesseract
from statistics import mode
import time
import downloadimage
import messagebox

# img PIL Image
# bounds (X1, Y1, X2, Y2)
def process(pil_img, bounds = None):
    if bounds: pil_img = pil_img.crop(bounds)
    
    prep_img = preprocess(pil_img)
    string = pytesseract.image_to_string(prep_img, lang="eng", config='-psm 6 tessconfig')
    prep_img.close()

    return string

def preprocess(pil_img):
    cv_img = np.array(pil_img, dtype=np.uint8)
    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_RGB2GRAY)
    bordersize=10
    cv_img = cv2.copyMakeBorder(cv_img,top=bordersize,bottom=bordersize,left=bordersize,right=bordersize,borderType=cv2.BORDER_CONSTANT,value=255 )
    cv_img = contrast(cv_img)
    return Image.fromarray(cv_img)

def contrast(cv_img, alpha=1.5, beta=-60.0):
    array_alpha = np.array([float(alpha)])
    array_beta = np.array([float(beta)])

    cv_img = cv2.add(cv_img, array_beta)
    cv_img = cv2.multiply(cv_img, array_alpha)
    
    return cv_img

if __name__ == '__main__':
    url = "https://i.redd.it/75hvw31dg5o01.jpg"
    pil_img = downloadimage.get(url)

    cv_img = np.array(pil_img, dtype=np.uint8)
    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)

    boxes = messagebox.find(pil_img)
    for box in boxes:
        x1, y1, x2, y2 = box
        bounding_rect = np.array([[x1, y1], [x2, y1], [x2, y2], [x1, y2]])
        cv2.drawContours(cv_img, [bounding_rect], 0, (0,255,0), 3)
        text = process(pil_img, (x1, y1, x2, y2))
        print(text)

    cv2.imshow('img', cv2.resize(cv_img, (0,0), fx=0.5, fy=0.5))
    cv2.waitKey(0)