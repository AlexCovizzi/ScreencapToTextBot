# download image and resize

import io
import requests
from PIL import Image
import constants as c
import exceptions
import logging
log = logging.getLogger(__name__)

# download the image from url
# returns the image as a buffer
def get(url):
    log.info("Downloading image from: "+url)
    response = requests.get(url)

    response.raise_for_status()

    img = Image.open(io.BytesIO(response.content))
    img = resize(img)

    if not isImageValid(img):
        return None

    img = img.convert('RGB')
    output = io.BytesIO()
    img.save(output, format='JPEG')
    imgBuf = output.getvalue()
    
    img.close()
    output.close()

    return imgBuf

def resize(img):
    wpercent = (c.IMG_WIDTH/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    return img.resize((c.IMG_WIDTH,hsize), Image.ANTIALIAS)

def isImageValid(img):
    return img.size[1] < 4000
