

# import the necessary packages
from colordescriptor import ColorDescriptor
from searcher import Searcher



import glob
import cv2
import os

import face_recognition




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
