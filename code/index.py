# USAGE
# python index.py --dataset dataset --index index.csv

# import the necessary packages
from colordescriptor import ColorDescriptor




import glob
import cv2
import os

import face_recognition

# initialize the color descriptor
class Indexer:
    def __init__(self,ColorDesc=(8, 12, 3)):
        self.ColorDesc=ColorDesc

    def WriteDB(self,IndexOption,Outputfile):

        cd = ColorDescriptor(self.ColorDesc)
        # open the output index file for writing
        if os.path.exists(Outputfile):
            os.remove(Outputfile)
        output = open(Outputfile, "w")
        # use glob to grab the image paths and loop over them
        for imagePath in glob.glob("dataset" + ("/*.*g")  ):
            print(imagePath)
            # extract the image ID (i.e. the unique filename) from the image
            # path and load the image itself
            imageID = imagePath[imagePath.rfind("/") + 1:]
            image = cv2.imread(imagePath)
            # describe the image
            if IndexOption == 1:
                features = cd.HOG(image)

            # write the features to file
            features = [str(f) for f in features]
            output.write("%s,%s\n" % (imagePath, ",".join(features)))
        # close the index file
        output.close()

    def IndexHog(self):
        # Write the database and save it in .csv file
        self.WriteDB(1,"IndexHog.csv")
        pass

