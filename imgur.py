from bs4 import BeautifulSoup
import requests
import re

def imageUrlFromSingle(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")
    # temporary
    try:
        imageUrl = soup.select('.post-image a img')[0]['src']
    except Exception:
        return None

    return 'https:'+imageUrl

def imageUrlFromAlbum(url):
    pass
