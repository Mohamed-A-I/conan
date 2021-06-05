# import the necessary packages
import numpy as np
import cv2
import imutils
#from skimage import feature
from skimage.io import imread
from skimage.transform import resize
from skimage.feature import hog



import os

import argparse

from sklearn.svm import LinearSVC

import argparse
import glob




class videoDescriptor:
	def __init__(self, bins):
		# store the number of bins for the 3D histogram
		self.bins = bins

	def HOG(self, image):
		image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		
		image =resize(image, (128, 256))
		
		

		
		Hog= hog(image, orientations=9, pixels_per_cell=(8, 8),
            cells_per_block=(2, 2), transform_sqrt=True, block_norm='L2-Hys')
        
		

		# return the feature vector
		return Hog

	
