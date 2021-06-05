
import cv2
import operator
import numpy as np
import matplotlib.pyplot as plt
import sys
from scipy.signal import argrelextrema
import argparse
import glob
"""
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required = True,
    help = "Path to the directory that contains the images to be indexed")
#ap.add_argument("-i", "--index", required = True,
 #   help = "Path to where the computed index will be stored")
args = vars(ap.parse_args()) 

"""



def smooth(x, window_len=13, window='hanning'):
    
    print(len(x), window_len)

 
    s = np.r_[2 * x[0] - x[window_len:1:-1],
              x, 2 * x[-1] - x[-1:-window_len:-1]]
    #print(len(s))
 
    if window == 'flat':  # moving average
        w = np.ones(window_len, 'd')
    else:
        w = getattr(np, window)(window_len)
    y = np.convolve(w / w.sum(), s, mode='same')
    return y[window_len - 1:-window_len + 1]
 

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
 
class video_indexer:
         
  def index(self):
    args={'dataset': '..\dataset\V\ ','index':"video.csv"}

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
    
     
    #Video path of the source file
    #videopath = 'D:/college/4th year computer and systems/2nd Term/Multimedia Systems/CBIR/CBIR_conan/dataset/V/surfer.mp4'
    #Directory to store the processed frames
    #dir = 'D:/college/4th year computer and systems/2nd Term/Multimedia Systems/CBIR/CBIR_conan/dataset/V/extract_result/'
    #smoothing window size
    #dir='/media/ahmed/8816F62D16F61BBE/downtor/college/recovered_CBIR_conan-main/CBIR_conan-main/code/V'

    len_window = int(50)
    output = open(args["index"], "w")

    
    for videopath in glob.glob("../dataset/V" + "/*mp4"):
        dir = args["dataset"] + '/extract_result/'
        print("target video :" + videopath)
        print("frame save directory: " + args["index"])
        # load video and compute diff between frames
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
        if USE_LOCAL_MAXIMA:
            print("Using Local Maxima")
            diff_array = np.array(frame_diffs)
            sm_diff_array = smooth(diff_array, len_window)
            frame_indexes = np.asarray(argrelextrema(sm_diff_array, np.greater))[0]
            for i in frame_indexes:
                keyframe_id_set.add(frames[i - 1].id)
            
            plt.figure(figsize=(40, 20))
            #plt.locator_params(numticks=300)
            plt.stem(sm_diff_array)
            plt.savefig(dir + 'plot.png')
        
    
        # save all keyframes as image
        '''
        cap = cv2.VideoCapture(str(videopath))
        curr_frame = None
        success, frame = cap.read()
        idx = 0
        #Result = ""
        keyframes = list(keyframe_id_set)
        while(success):
             if idx in keyframe_id_set:
                name = str(videopath) +"keyframe_" + str(idx) + ".jpg"
                cv2.imwrite(dir + name, frame)
                keyframe_id_set.remove(idx)
                features = frame.copy()
                features = cv2.resize(features,(128,256))
                features = cv2.normalize(features, features, 0, 1, cv2.NORM_MINMAX,dtype=cv2.CV_32F).flatten()
                features = [str(f) for f in features]
                Result += ",".join(features)
             idx = idx + 1
             success, frame = cap.read()
             '''
        frame_diffs = [str(f) for f in frame_diffs]
        output.write("%s,%s\n" % (str(videopath), ",".join(frame_diffs)))
    output.close()
        #cap.release()
