import cv
import os

os.system('rm video.mp4')
os.system('rm -r frames')
os.system('mkdir frames')
#cv.NamedWindow("Video",cv.CV_WINDOW_AUTOSIZE)
cam = cv.CreateCameraCapture(0)
cv.SetCaptureProperty(cam,cv.CV_CAP_PROP_FRAME_WIDTH, 640)
cv.SetCaptureProperty(cam,cv.CV_CAP_PROP_FRAME_HEIGHT, 480)
cont = 0
while True:
    frame = cv.QueryFrame(cam)
    cv.ShowImage('Video', frame)
    cv.SaveImage("frames/out%s.png"%cont,frame)
    cont +=1
    k = cv.WaitKey(10)
    if cont >=50:
        break
os.system('ffmpeg -qscale 5 -r 20 -b 9600 -i frames/out%01d.png video.mp4')
