# import the necessary packages
import numpy as np
import cv2
import imutils
from sklearn.svm import LinearSVC
from skimage import feature
import argparse
import glob
import cv2
import os
from skimage.io import imread
import face_recognition

class ColorDescriptor:
	def __init__(self, bins):
		# store the number of bins for the 3D histogram
		self.bins = bins

	def describe(self, image):
		# convert the image to the HSV color space and initialize
		# the features used to quantify the image
		image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		features = []

		# grab the dimensions and compute the center of the image
		(h, w) = image.shape[:2]
		(cX, cY) = (int(w * 0.5), int(h * 0.5))

		# divide the image into four rectangles/segments (top-left,
		# top-right, bottom-right, bottom-left)
		segments = [(0, cX, 0, cY), (cX, w, 0, cY), (cX, w, cY, h),
			(0, cX, cY, h)]

		# construct an elliptical mask representing the center of the
		# image
		(axesX, axesY) = (int(w * 0.75) // 2, int(h * 0.75) // 2)
		ellipMask = np.zeros(image.shape[:2], dtype = "uint8")
		cv2.ellipse(ellipMask, (cX, cY), (axesX, axesY), 0, 0, 360, 255, -1)

		# loop over the segments
		for (startX, endX, startY, endY) in segments:
			# construct a mask for each corner of the image, subtracting
			# the elliptical center from it
			cornerMask = np.zeros(image.shape[:2], dtype = "uint8")
			cv2.rectangle(cornerMask, (startX, startY), (endX, endY), 255, -1)
			cornerMask = cv2.subtract(cornerMask, ellipMask)

			# extract a color histogram from the image, then update the
			# feature vector
			hist = self.histogram(image, cornerMask)
			features.extend(hist)

		# extract a color histogram from the elliptical region and
		# update the feature vector
		hist = self.histogram(image, ellipMask)
		features.extend(hist)

		# return the feature vector
		return features

	def histogram(self, image, mask):
		# extract a 3D color histogram from the masked region of the
		# image, using the supplied number of bins per channel
		hist = cv2.calcHist([image], [0, 1, 2], mask, self.bins,
			[0, 180, 0, 256, 0, 256])

		# normalize the histogram if we are using OpenCV 2.4
		if imutils.is_cv2():
			hist = cv2.normalize(hist).flatten()

		# otherwise handle for OpenCV 3+
		else:
			hist = cv2.normalize(hist, hist).flatten()

		# return the histogram
		return hist
	def build_filters(self):
		filters = []
		ksize = 31
		for theta in np.arange(0, np.pi, np.pi / 16):
		    kern = cv2.getGaborKernel((ksize, ksize), 4.0, theta, 10.0, 0.5, 0, ktype=cv2.CV_32F)
		    kern /= 1.5*kern.sum()
		    filters.append(kern)
		return filters

	def process(sef,img, filters):
		accum = np.zeros_like(img)
		for kern in filters:
		    fimg = cv2.filter2D(img, cv2.CV_8UC3, kern)
		    np.maximum(accum, fimg, accum)
		return accum

	def gabour(self, image):
		# convertimage = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
		image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		image = cv2.resize(image,(128,256))
		filters=self.build_filters()
		Result=self.process( image,filters)
		#cv2.imshow('result',Result)
		#cv2.write('test.csv')
		#cv2.waitKey(0)
		Result = cv2.normalize(Result, Result, 0, 1, cv2.NORM_MINMAX,dtype=cv2.CV_32F).flatten()
		#Result = cv2.normalize(Result, Result, 0, 1, cv2.NORM_MINMAX,dtype=cv2.CV_32F).flatten()
		return Result

	def HOG(self, image):
		image =cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
	
		hog_desc = face_recognition.face_encodings(image)[0]
		return hog_desc
    
        
        
