# coding: utf-8
# Melanie Huston
# download all health topic images from English health topic page index of all topics
# August 2017

from os.path import basename
from bs4 import BeautifulSoup
import requests
import re
import urllib.request
import io
from PIL import Image
import csv

HTindex = 'https://medlineplus.gov/all_healthtopics.html'

imagenames = []
nonstandardimages = []
processedimages = []

# Get and parse HTML from the URL
page = requests.get(HTindex)
soup = BeautifulSoup(page.content, 'html.parser')

# find all list items containing a link to a health topic
HTcrawl = soup.find_all('li', class_='item')

for li in HTcrawl:
    # get the link to the health topic and follow it
    HTurl = li.find('a', href=True)
    link_text = HTurl['href']
    htpage = requests.get(link_text)
    htsoup = BeautifulSoup(htpage.content, 'html.parser')

    # find the section on the health topic page containing the health topic image
    # and get the image url
    imagesection = htsoup.find('section', id='ht-img-section')
    link = imagesection.find("img", src=True)
    lnk = link['src']

    # if we haven't already downloaded this image, record the image name and download it
    if not basename(lnk) in imagenames:
        print(lnk)
        imagenames.append(basename(lnk))
        fd = urllib.request.urlopen(lnk)
        image_file = io.BytesIO(fd.read())
        siteimage = Image.open(image_file)
        #fd = urllib.request.urlretrieve(lnk, basename(lnk))
        #siteimage = Image.open(lnk)
        width, height = siteimage.size
        nameparts = re.match("(?P<fn>.*)\.(?P<ext>.*)$", basename(lnk))
        filename = nameparts.group('fn')
        extension = nameparts.group('ext')
        exttype = extension
        if exttype in ['jpg', 'JPG']:
            exttype = 'jpeg'

        if width == height:
            processedimages.append(basename(lnk))
            siteimage.thumbnail((100, 100), Image.LANCZOS)
            siteimage.save('images/' + filename + '_thumb.' + extension, format=exttype, subsampling=0, quality=100)
        else:
            nonstandardimages.append(basename(lnk))
            #siteimage.save('bigtest/problems/' + basename(lnk), format=exttype, subsampling=0, quality=100)
        siteimage.close()

# print the number of unique images downloaded
print("\nNumber of images converted:", len(processedimages))
print("\nNumber of non-standard images:", len(nonstandardimages))

processedimages.sort()
nonstandardimages.sort()

if len(nonstandardimages):
    for problem in nonstandardimages:
        print(problem)

with open('Images_thumbnaillist.txt', 'w') as f_new:
    for item in processedimages:
        f_new.write("%s\n" % item)
f_new.close()

with open('Images_problemlist.txt', 'w') as f_prob:
    for item in nonstandardimages:
        f_prob.write("%s\n" % item)
f_prob.close()

print('\nTwo csv files written')
