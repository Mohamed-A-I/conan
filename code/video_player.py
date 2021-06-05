import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
from PIL import ImageTk, Image
 
class vid_player:
     def __init__(self,canvas, video_source="/home/ahmed/trials/video.mp4"):
         
         self.video_source = video_source 
         self.vid = MyVideoCapture(self.video_source)
 
         # Create a canvas that can fit the above video source size
      
         self.canvas=canvas
         # After it is called once, the update method will be automatically called every delay milliseconds
         self.delay = 15
         self.update()
 
         
 
    
 
     def update(self):
         # Get a frame from the video source
         ret, frame = self.vid.get_frame()
         if ret:
             frame= cv2.resize(frame, dsize=(800, 800), interpolation=cv2.INTER_AREA)
             self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
             self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
 
         self.canvas.after(self.delay, self.update)
 
 
class MyVideoCapture:
     def __init__(self, video_source=0):
         # Open the video source
         self.vid = cv2.VideoCapture(video_source)
         if not self.vid.isOpened():
             raise ValueError("Unable to open video source", video_source)
 
         # Get video source width and height
         self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
         self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
 
     def get_frame(self):
         if self.vid.isOpened():
             ret, frame = self.vid.read()
             if ret:
                 # Return a boolean success flag and the current frame converted to BGR
                 return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
             else:
                 return (ret, None)
         else:
             return (ret, None)
 
     # Release the video source when the object is destroyed
     def __del__(self):
         if self.vid.isOpened():
             self.vid.release()
 
