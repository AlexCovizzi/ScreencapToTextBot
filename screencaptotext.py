import downloadimage
import messagebox
import ocr
import time
import re

URLS = ["https://i.imgur.com/n3U3Afj.jpg"]


def analyze(pil_img):
    messages = []
    rects = messagebox.find(pil_img)
    for rect in rects:
        img_bounds = (rect["left"], rect["top"], rect["left"]+rect["w"], rect["top"]+rect["h"])
        text = ocr.analyze(pil_img, img_bounds)
        rect["text"] = text
        if text: messages.append(rect)

    messages.sort(key=lambda msg: int(msg["top"]))

    return messages

def extract_dst_name(pil_img, bounds):
    text = ocr.analyze(pil_img, bounds)
    lines = text.split('\n')
    for line in lines:
        print(line)
        match = re.match(r'^[A-Z][a-z]+$', line)
        if match:
            return line
    return "Other"

if __name__ == "__main__":
    #for url in URLS:
    img = downloadimage.get(URLS[0])
    #img.show()
    rects = analyze(img)
    
    dst_name = extract_dst_name(img, (0, 0, img.size[0], rects[0]['top']+1))
    print("dst: "+dst_name)

    for rect in rects:
        print(rect)