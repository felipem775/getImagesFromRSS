#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import urllib
import os
#import datetime
import json

json_data=open(os.path.dirname(__file__) + '/getImagesFromRSS.config')
data = json.load(json_data)
json_data.close()

path = data["path"]
rss = data["rss"]
images = ['.jpg','jpeg','.png','.gif']

# Ficheros antiguos
oldPics = []
if not os.path.isfile(path + '.descargado.log'):
  open(path + '.descargado.log','w').close()
fo = open(path + '.descargado.log','r+')
for line in fo:
  oldPics.append(line.strip())
fo.close()

# Ficheros que descargamos en esta sesión
newPics = []

for rs in rss:
  urllib.urlretrieve(rs["value"], "rss.tmp")
  fxml = open("rss.tmp",'r')
  for line in fxml:
    line = line.split('"')
    for l in line:
      l = l.replace('_m.jpg','_b.jpg')
      if "_400." in l:
        continue
      if l[0:4] == "http" and l[len(l)-4:len(l)] in images and l not in oldPics:
        newPics.append(l)
        name = l.split('/')
        urllib.urlretrieve(l, path + rs["name"] + name[len(name) -1])
  fxml.close()
  os.remove("rss.tmp")

fw = open(path + '.descargado.log','a')
fw.write("\n".join(newPics))
fw.close()
