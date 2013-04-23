import sys
from PIL import Image, ImageDraw, ImageFont
#from math import sqrt
from random import randint

def grayScale(im):
    w,h = im.size
    gray = im.copy()
    pix = gray.load()
    for x in range(w):
        for y in range(h):
            curr = pix[x,y]
            prom = max(curr)
            pix[x,y] = prom, prom, prom
    return gray

def blur(im):
    w,h = im.size
    blurred = im.copy()
    pix = blurred.load()
    for x in range(w):
        for y in range(h):
            ngbs = []
            ngbs.append(list(pix[x,y]))
            for i in range(x-1, x+2):
                for j in range(y-1, y+2):
                    try:
                        ngbs.append(list(pix[i,j]))
                    except IndexError:
                        pass
            total = [ sum(z) for z in zip(*ngbs) ]
            pix[x,y] = total[0]/len(ngbs), total[1]/len(ngbs), total[2]/len(ngbs)
    return blurred

def binarized(im, thresh):
    w,h = im.size
    binarized = im.copy()
    pix = binarized.load()
    for x in range(w):
        for y in range(h):
            if pix[x,y][0] >= thresh:
                pix[x,y] = (255,255,255)
            else:
                pix[x,y] = (0,0,0)
    return binarized

def bfs(im, root, color, out):
    '''q = queue '''
    pix = im.load()
    output = out.load()
    w, h = im.size
    q = []
    q.append(root)
    coords = []
    original = pix[root]
    tot = 0
    while len(q) > 0:
        (x, y) = q.pop(0)
        curr = pix[x, y]
        if curr == original or curr == color:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    i, j = (x + dx, y + dy)
                    if i >= 0 and i < w and j >= 0 and j < h:
                        rgb = pix[i, j]
                        if rgb == original:
                            tot+=1
                            pix[i, j] = color
                            output[i,j] = color
                            coords.append((i, j))
                            q.append((i, j))
    return coords, out

def horizontalHistogram(im):
    w,h = im.size
    pix = im.load()
    file_ = open('horizontal.txt', 'w')
    hist = []
    prom = 0
    for x in range(w):
        temp = 0
        for y in range(h):
            temp += pix[x,y][0]
        file_.write(str(x)+ ' ' + str(temp) + '\n')
        hist.append(temp)
    file_.close()
    for i in hist:
        prom += i
    prom = float(prom)/ len(hist)
    return hist, prom

def verticalHistogram(im):
    w,h = im.size
    pix = im.load()
    file_ = open('vertical.txt', 'w')
    hist = []
    prom = 0
    for y in range(h):
        temp = 0
        for x in range(w):
            temp += pix[x,y][0]
        file_.write(str(x)+ ' ' + str(temp) + '\n')
        hist.append(temp)
    for i in hist:
        prom +=i
    prom = float(prom)/len(hist)
    file_.close()
    return hist, prom

'''
def possibleHoles(hist):
    coord = []
    for i in range(1, len(hist) - 1):
        if hist[i] < hist[i-1] and hist[i+1] > hist[i]:
            coord.append(i)
    return coord
'''

def possibleHoles(histx, histy, im):
    '''inter = intersections '''
    pix = im.load()
    inter = []
    for i in range(1, len(histx)-1):
        if histx[i-1] > histx[i] < histx[i+1]:
            for j in range(1, len(histy) -1):
                if histy[j-1] > histy[j] < histy[j+1]:
                    inter.append((i,j))
    return inter

def purple():
    return (randint(85,255), randint(0, 150), randint(128, 255))

def findCenters(coords, im, original):
    centers = []
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMonoOblique.ttf", 14)
    r = 2
    t = 1
    for c in coords:
        id_ = 'a'+str(t)
        c.sort()
        max_ = c[-1]
        min_ = c[0]
        promx = (max_[0] + min_[0])/2
        promy = (max_[1] + min_[1])/2
        centers.append((promx, promy))
        draw.ellipse((promx-r,promy-r, promx+r, promy+r), fill='blue')
        draw.text((promx,promy),id_, fill='red', font=font)
        t += 1
    return im

def holeDetection(im):
    size = 128,128
    original = im.copy()
    output = im.copy()
    output.thumbnail(size, Image.ANTIALIAS)
    im.thumbnail(size, Image.ANTIALIAS)
    im = grayScale(im)
    im = blur(im)
    histx, promx = horizontalHistogram(im)
    histy, promy = verticalHistogram(im)
    
    inter = possibleHoles(histx, histy, im)

    prop = im.size
    prop = float(original.size[0])/prop[0] , float(original.size[1]/prop[1])
    w, h = original.size
    
    im = binarized(im,60)
    pix = im.load()
    coords = []

    for i in inter:
        if pix[i] == (0,0,0):
            c, out = bfs(im, (i), purple(), output)
            coords.append(c)

    im = findCenters(coords, out, original)
    im = im.resize((original.size), Image.ANTIALIAS)
    im.save('agujeros.png')
    im.show()


if __name__ == '__main__':
    path = sys.argv[1]
    image = Image.open(path).convert('RGB')
    holeDetection(image)
