# USAGE
# python search.py --index index.csv --query queries/103100.png --result-path dataset

# import the necessary packages
from colordescriptor import ColorDescriptor
from searcher import Searcher
import argparse
import cv2
from sklearn.svm import LinearSVC
from skimage import feature
import argparse
import glob
import cv2
import os
from skimage.io import imread
import face_recognition

"""# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--index", required = True,
	help = "Path to where the computed index will be stored")
ap.add_argument("-q", "--query", required = True,
	help = "Path to the query image")
ap.add_argument("-r", "--result-path", required = True,
	help = "Path to the result path")
args = vars(ap.parse_args())"""


class Retriever:
    def __init__(self,  Query,ColorDesc=(8, 12, 3)):
        self.cd = ColorDescriptor(ColorDesc)
        self.ResultList = list()
        self.results=list()
        # load the query image
        self.Query=cv2.imread(Query)
        self.features=list()
    def GetSearchResult(self, IndexFile):
        # perform the search
        searcher = Searcher(IndexFile)
        self.results = searcher.search(self.features)
        self.ResultList.clear()
        # loop over the results
    def HogSearch(self):
        # load the query image and describe it
        self.features=self.cd.HOG(self.Query)
        self.GetSearchResult("IndexHog.csv")
        pass

    def GetImageList(self):
        for (score, resultID) in self.results:
            # load the result image and display it
            self.ResultList.append(resultID)
            result = cv2.imread(resultID)
            # print("-------->",result)
            # if (not result):continue
            # cv2.imshow("Result", result)
            # cv2.waitKey(5000)
        return self.ResultList
