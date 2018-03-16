import downloadimage
import messagebox
import ocr
import time

URLS = ["https://i.redd.it/9pdz4ycgj5m01.jpg", "https://i.imgur.com/Mps09BH.jpg", "https://i.redd.it/wejqbl3on4m01.png", "https://i.redd.it/mxghh2c5q1m01.jpg"]
URL = URLS[0]

def analyze(img):
    rects = messagebox.find(img)
    for rect in rects:
        img_bounds = (rect["left"], rect["top"], rect["left"]+rect["w"], rect["top"]+rect["h"])
        text = ocr.analyze(img, img_bounds)
        rect["text"] = text

    return rects
    
if __name__ == "__main__":
    img = downloadimage.get(URL)
    rects = analyze(img)
    for rect in rects:
        print(rect["text"])