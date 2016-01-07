import cv2,math
import time
import numpy as np



class ColourTracker:
    def __init__(self):
        cv2.namedWindow("colourTrackerWindow",cv2.CV_WINDOW_AUTOSIZE)
        cv2.namedWindow("alternateWindow",cv2.CV_WINDOW_AUTOSIZE)
        self.capture=cv2.VideoCapture(0)
        self.scale_down=1
        time.sleep(5)
    def getColorUpper(self):
        return [255,255,255] # [5,255,255]
    def getColorLower(self):
        return [0,150,255]
    def run(self):
        f = True
        while True and f:
            f,orig_img=self.capture.read()
            orig_img2=cv2.flip(orig_img,1)
            img=cv2.GaussianBlur(orig_img,(5,5),0)
            img=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
            red_lower=np.array(self.getColorLower(),np.uint8)             # getColorUpper() and getColorLower() returns a list of 3 numbers in HSV for the upperbound and lower bound for caliberated color
            red_upper=np.array(self.getColorUpper(),np.uint8)              
            red_binary=cv2.inRange(img,red_lower,red_upper)
            dilation=np.ones((15,15),"uint8")
            red_binary=cv2.dilate(red_binary,dilation)
            contours,hierarchy=cv2.findContours(red_binary,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
            max_area=0
            largest_contour=None
            for idx,contour in enumerate(contours):
                area=cv2.contourArea(contour.astype('int'))
                if area>max_area:
                    largest_contour=contour
                if not largest_contour==None:
                    moment=cv2.moments(largest_contour)
                    if moment["m00"]>1000/self.scale_down:
                        (x,y),radius=cv2.minEnclosingCircle(largest_contour)
                        center=(int(x),int(y))
                        center_x=center[0]
                        center_y=center[1]
                        radius=int(radius)
                        cv2.circle(orig_img,(center[0]*self.scale_down,center[1]*self.scale_down),radius*self.scale_down,(0,255,0),2)
                        self.mouse_scale_x=1376/orig_img.shape[0]
                        self.mouse_scale_y=1376/orig_img.shape[1]
                        print orig_img.shape[0],orig_img.shape[1]
            cv2.imshow('colourTrackerWindow',orig_img)
            cv2.imshow('alternateWindow',red_binary)
            
            if cv2.waitKey(2)==27:
                break


colour_tracker=ColourTracker()
colour_tracker.run()