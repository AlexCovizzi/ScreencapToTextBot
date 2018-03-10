from bs4 import BeautifulSoup
import requests
import re

def imageUrlFromSingle(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")
    imageUrl = soup.select('.post-image a img')[0]['src']
    return 'https:'+imageUrl

def imageUrlFromAlbum(url):
    pass
