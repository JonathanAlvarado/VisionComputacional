import sys
from PIL import Image, ImageDraw, ImageOps

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
                        #ngbs.append(pix[i,j])
                        ngbs.append(list(pix[i,j]))
                    except IndexError:
                        pass
            #ngbs.sort()
            #p = ngbs[len(ngbs)/2][0]
            total = [ sum(z) for z in zip(*ngbs) ]
            #pix[x,y] = p,p,p
            pix[x,y] = total[0]/len(ngbs), total[1]/len(ngbs), total[2]/len(ngbs)
    return blurred

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

def possibleHoles(hist):
    coord = []
    for i in range(1, len(hist) - 1):
        if hist[i-1] > hist[i] and hist[i+1] > hist[i]:
            coord.append(i)
    return coord

def holeDetection(im):
    size = 128,128
    original = im.copy()
    im.thumbnail(size, Image.ANTIALIAS)
    im = grayScale(im)
    im = blur(im)
    im.save('gray.png')
    histx, promx = horizontalHistogram(im)
    histy, promy = verticalHistogram(im)
    
    holesx = possibleHoles(histx)
    holesy = possibleHoles(histy)
    draw = ImageDraw.Draw(original)

    prop = im.size
    prop = float(original.size[0])/prop[0] , float(original.size[1]/prop[1])
    w, h = original.size
    '''
    for i in range (len(histx)):
        if histx[i] < promx:
            x = int(i*prop[0])
            draw.line((x,0,x,h), fill='yellow')
            '''
    for i in holesx:
        x = int(i*prop[0])
        draw.line((x,0,x,h), fill='yellow')
    '''
    for i in histy:
        if i > promy:
            y = int(i*prop[1])
            draw.line((0,y,w,y), fill='skyblue')
    '''
    for i in holesy:
        y = int(i*prop[1])
        draw.line((0,y,w,y), fill='skyblue')
    original.save('lineas.png')
    original.show()
    

if __name__ == '__main__':
    path = sys.argv[1]
    image = Image.open(path).convert('RGB')
    holeDetection(image)
