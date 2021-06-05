import cv2
import operator
import numpy as np
import matplotlib.pyplot as plt
import sys
from scipy.signal import argrelextrema
import argparse
import glob
from pyimagesearch.searcher import Searcher

# construct the argument parser and parse the arguments
"""ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required = True,
    help = "Path to the video")
#ap.add_argument("-i", "--index", required = True,
args = vars(ap.parse_args()) 

 """

class Frame:
    """class to hold information about each frame
    
    """
    def __init__(self, id, diff):
        self.id = id
        self.diff = diff
 
    def __lt__(self, other):
        if self.id == other.id:
            return self.id < other.id
        return self.id < other.id
 
    def __gt__(self, other):
        return other.__lt__(self)
 
    def __eq__(self, other):
        return self.id == other.id and self.id == other.id
 
    def __ne__(self, other):
        return not self.__eq__(other)
 
 
def rel_change(a, b):
   x = (b - a) / max(a, b)
   #print(x)
   return x

class vid_search:

  def search(self,args):
    videopath = args["dataset"]

    #Setting fixed threshold criteria
    USE_THRESH = True
    #fixed threshold value
    THRESH = 0.2
    #Setting fixed threshold criteria
    USE_TOP_ORDER = False
    #Number of top sorted frames
    NUM_TOP_FRAMES = 50
    #Setting local maxima criteria
    USE_LOCAL_MAXIMA = False
    len_window = int(50)
    cap = cv2.VideoCapture(str(videopath)) 
    curr_frame = None
    prev_frame = None 
    frame_diffs = []
    frames = []
    success, frame = cap.read()
    i = 0 
    while(success):
        luv = cv2.cvtColor(frame, cv2.COLOR_BGR2LUV)
        curr_frame = luv
        if curr_frame is not None and prev_frame is not None:
           #logic here
           diff = cv2.absdiff(curr_frame, prev_frame)
           diff_sum = np.sum(diff)
           diff_sum_mean = diff_sum / (diff.shape[0] * diff.shape[1])
           frame_diffs.append(diff_sum_mean)
           frame = Frame(i, diff_sum_mean)
           frames.append(frame)
        prev_frame = curr_frame
        i = i + 1
        success, frame = cap.read()   
    cap.release()
    
    # compute keyframe
    keyframe_id_set = set()
    if USE_TOP_ORDER:
        print("Using Top Order")
        # sort the list in descending order
        frames.sort(key=operator.attrgetter("diff"), reverse=True)
        for keyframe in frames[:NUM_TOP_FRAMES]:
            keyframe_id_set.add(keyframe.id) 
    
    if USE_THRESH:
        print("Using Threshold")
        for i in range(1, len(frames)):
            if (rel_change(float(frames[i - 1].diff), float(frames[i].diff)) >= THRESH):
                #Diff.append(rel_change(float(frames[i - 1].diff), float(frames[i].diff)))
                keyframe_id_set.add(frames[i].id) 
    '''
    if USE_LOCAL_MAXIMA:
        print("Using Local Maxima")
        diff_array = np.array(frame_diffs)
        #sm_diff_array = smooth(diff_array, len_window)
        #frame_indexes = np.asarray(argrelextrema(sm_diff_array, np.greater))[0]
        for i in frame_indexes:
            keyframe_id_set.add(frames[i - 1].id)
        
        plt.figure(figsize=(40, 20))
        #plt.locator_params(numticks=300)
        plt.stem(sm_diff_array)
        plt.savefig(dir + 'plot.png')
    '''
    #frame_diffs = [str(f) for f in frame_diffs]
    #features = str(videopath)+",".join(frame_diffs)
    searcher = Searcher("video.csv")
    results = searcher.search(frame_diffs,1)

    return(results[0][1])
    
