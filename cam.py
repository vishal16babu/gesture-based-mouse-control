import cv2
import numpy as np
import os
cap = cv2.VideoCapture(0)
while( cap.isOpened() ) :
    ret,img = cap.read()
    img = cv2.flip(img,1)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    ret,thresh1 = cv2.threshold(blur,70,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
  
    contours, hierarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    drawing = np.zeros(img.shape,np.uint8)

    max_area=0
   
    for i in range(len(contours)):
            cnt=contours[i]
            area = cv2.contourArea(cnt)
            if(area>max_area):
                max_area=area
                ci=i
    cnt=contours[ci]
    hull = cv2.convexHull(cnt)
    moments = cv2.moments(cnt)
    if moments['m00']!=0:
                cx = int(moments['m10']/moments['m00']) # cx = M10/M00
                cy = int(moments['m01']/moments['m00']) # cy = M01/M00
              
    centr=(cx,cy)       
    #cv2.circle(img,centr,5,[0,0,255],2)       
    cv2.drawContours(drawing,[cnt],0,(0,255,0),2) 
    cv2.drawContours(drawing,[hull],0,(0,0,255),2) 
          
    cnt = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
    hull = cv2.convexHull(cnt,returnPoints = False)
    
    if(1):
               defects = cv2.convexityDefects(cnt,hull)
               mind=0
               maxd=0
               p_x =0
               p_y =0
               os.system("xdotool mousemove_relative -- 0 0")

               for i in range(defects.shape[0]):
                    s,e,f,d = defects[i,0]
                    start = tuple(cnt[s][0])
                    end = tuple(cnt[e][0])
                    far = tuple(cnt[f][0])
                    mouse_x = str((far[0]-p_x)/10)
                    mouse_y = str((far[1]-p_y)/10)
                    #print(str(far[0])+" "+str(far[1]))
                    dist = cv2.pointPolygonTest(cnt,centr,True)
                    #cv2.line(img,start,end,[0,255,0],2)
                    p_x = far[0]
                    p_y = far[1]
                    cv2.circle(img,far,i,[0,0,255],-1)

               print(i)
               if(i>3):
                    os.system("xdotool mousemove_relative -- "+mouse_x+" "+mouse_y)

               i=0
    cv2.imshow('output',drawing)
    cv2.imshow('input',img)
                
    k = cv2.waitKey(10)
    if k == 27:
        break