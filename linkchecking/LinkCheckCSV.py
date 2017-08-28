
import os
import csv
import json
import urllib

from collections import Counter
from operator import itemgetter
from urllib.request import urlopen


filename = 'Linkchecking08152017.csv'
listofhtml = []
i = 1

with open(filename, newline='', encoding='iso-8859-1') as f:
    stuffreader = csv.reader(f)
    for row in stuffreader:
        teststr= "<a href=" + "\"" + row[1] + "\"" + ">" + row[1] +" | " + row[0] + " | " + row[2] + " | " + row[3] + "</a><br>"
        listofhtml.insert(i,teststr)
        i += 1
f.close()

g = open('html08152017.html','w')

g.write("<!doctype html><html><head><meta charset=\"utf-8\"><title>Link check</title></head><body><p>")
for item in listofhtml:
  g.write("%s\n" % item)
g.write("</p></body></html>")

g.close()
