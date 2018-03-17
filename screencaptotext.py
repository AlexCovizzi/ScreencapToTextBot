import downloadimage
import messagebox
import ocr
import time

URLS = ["https://i.imgur.com/UNTeANY.png","https://i.imgur.com/jT3MmwZ.jpg", "https://i.redd.it/9pdz4ycgj5m01.jpg", "https://i.imgur.com/Mps09BH.jpg", "https://i.redd.it/wejqbl3on4m01.png", "https://i.redd.it/mxghh2c5q1m01.jpg"]


def analyze(img):
    rects = messagebox.find(img)
    for rect in rects:
        img_bounds = (rect["left"], rect["top"], rect["left"]+rect["w"], rect["top"]+rect["h"])
        text = ocr.analyze(img, img_bounds)
        rect["text"] = text

    rects.sort(key=lambda rect: int(rect["top"]))

    return rects

if __name__ == "__main__":
    #for url in URLS:
    img = downloadimage.get(URLS[0])
    rects = analyze(img)
    for rect in rects:
        print(rect)