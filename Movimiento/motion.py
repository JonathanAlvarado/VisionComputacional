import cv2.cv as cv
import sys
import numpy
import os

def toarray(im):
    '''Converts opencv image into a numpy array '''
    array = cv.GetMat(im)
    array = numpy.asarray(array)
    return array

def grayScale(im):
    '''Converts image into gray scale using numpy arrays.
    gets an average of every row of the matrix'''
    #print im.dtype
    out = numpy.sum(im.astype(numpy.int), axis=2, dtype=im.dtype)/3 
    #print out.dtype
    #out = numpy.array(out, dtype = im.dtype)
    #print out.dtype
    return out

def difference(im1, im2):
    '''Subtract two images, to get the objects that are moving'''
    x = im1.astype(numpy.int)#converts into int type
    y = im2.astype(numpy.int)
    #out = out.astype(numpy.uint8)
    out = numpy.subtract(x,y)
    return out

def binarize(im, tresh):
    '''Binarize the image usig numpy arrays'''
    tresh = numpy.array([15], dtype = im.dtype)#threshold array
    color = numpy.array([255], dtype = im.dtype)#White color array
    im[numpy.where(im > [tresh])] = color#compare the elements, every element that is higher than the threshold gets a white color
    return im

def paint_motion(frame, im):
    '''The objects that are moving are painted with a blue tone in the original frame '''
    white = numpy.array([255], dtype = im.dtype)
    color = numpy.array([255,0,0], dtype = im.dtype)
    frame[numpy.where(im == [white])] = color
    return frame

def detect(frame, motion, w,h):
    size = 45
    color = numpy.array([255], dtype = motion.dtype)
    w = w/size
    h = h/size
    area = w*h
    for x in range(w):
        for y in range(h):
            p1 = x * size , y * size
            p2 = (x+1) * size, (y+1) * size
            region = motion[p1[1]:p2[1] , p1[0]:p2[0]]
            n = numpy.where(region == color)
            n = len(n[0])/10
            if n > area*0.001:
                cv.Rectangle(frame, p1, p2, cv.CV_RGB(0, 255, 0), 2)
    return frame

def capture(video):
    video = cv.CaptureFromFile(video)
    cv.SetCaptureProperty( video, cv.CV_CAP_PROP_FRAME_WIDTH, 280 )
    cv.SetCaptureProperty( video, cv.CV_CAP_PROP_FRAME_HEIGHT, 160 )
    width = int(cv.GetCaptureProperty(video, cv.CV_CAP_PROP_FRAME_WIDTH))
    height = int(cv.GetCaptureProperty(video, cv.CV_CAP_PROP_FRAME_HEIGHT))
    n = cv.GetCaptureProperty(video, cv.CV_CAP_PROP_FRAME_COUNT)
    curr = 0
    while True:
        cv.SetCaptureProperty(video, cv.CV_CAP_PROP_POS_FRAMES, curr)
        frame1 = cv.QueryFrame(video)
        frame1 = cv.CloneImage(frame1)
        
        #if frame1 == None:
            #break
        frame2 = cv.QueryFrame(video)
        frame2 = cv.CloneImage(frame2)
        array1 = toarray(frame1)
        array2 = toarray(frame2)
        out = difference(array1, array2)
        
        out = grayScale(out)
        out = binarize(out, 10)
        paint = paint_motion(array1, out)
        detection = detect(frame1, out, width, height)
        im = cv.fromarray(paint)
        #im = cv.fromarray(out)
        cv.SaveImage('motion/prueba%s.png'%curr,detection)
        #cv.SaveImage('motion/prueba%s.png'%curr,im)
        curr+=1
        if curr >= n - 1: 
            break
        

if __name__ == '__main__':
    video = sys.argv[1]
    capture(video)
    os.system('rm motion.mp4')
    os.system('ffmpeg -qscale 5 -r 20 -b 9600 -i motion/prueba%01d.png motion.mp4')
