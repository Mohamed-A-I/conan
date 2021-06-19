# import the necessary packages
import numpy as np
import cv2
import os

import face_recognition

class ColorDescriptor:
	def __init__(self, bins):
		# store the number of bins for the 3D histogram
		self.bins = bins

	

	
	
        # Return the features of the object (face)
        # that is recognized using the hog algorithm
	def HOG(self, image):
		image =cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
	
		hog_desc = face_recognition.face_encodings(image)[0]
		return hog_desc
    
        
        
