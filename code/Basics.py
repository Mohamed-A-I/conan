import cv2
import face_recognition

import numpy as np
import os
from datetime import datetime
# from PIL import ImageGrab
 
path = 'img'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
	curImg = cv2.imread(f'{path}/{cl}')
	images.append(curImg)
	classNames.append(os.path.splitext(cl)[0])
print(classNames)
 
def findEncodings(images):
	encodeList = []
	for img in images:
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		encode = face_recognition.face_encodings(img)[0]
		encodeList.append(encode)
	return encodeList



 
imgElon = face_recognition.load_image_file('img/h.jpg')
imgElon = cv2.cvtColor(imgElon,cv2.COLOR_BGR2RGB)
imgTest = face_recognition.load_image_file('img/h2.jpg')
imgTest = cv2.cvtColor(imgTest,cv2.COLOR_BGR2RGB)
 

encodeElon = face_recognition.face_encodings(imgElon)[0]

 

encodeTest = face_recognition.face_encodings(imgTest)[0]

 
results = face_recognition.compare_faces([encodeElon],encodeTest)
faceDis = face_recognition.face_distance([encodeElon],encodeTest)
print(results,faceDis)

 

