import io
import requests
from PIL import Image
import logging
log = logging.getLogger(__name__)

# download image from url
def get(url):
    response = requests.get(url)

    response.raise_for_status()

    img = Image.open(io.BytesIO(response.content))
    img = resize(img, 720)
    img = img.convert('RGB')

    return img

def resize(img, wsize):
    wpercent = (wsize/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    return img.resize((wsize,hsize), Image.ANTIALIAS)