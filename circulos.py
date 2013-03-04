from PIL import Image, ImageDraw,ImageFont
import sys, random
from math import sqrt,fabs,sin,cos,atan2, pow,radians


def convolucion(im,g):
    w, h = im.size
    pixeles = im.load()
    imCon = Image.new('RGB', (w,h))
    pixCon = imCon.load()

    for x in range(w):
        for y in range(h):
            suma = 0
            for i in range(x-1, x+2):
                for j in range(y-1, y+2):
                    try:
                        suma += g[i - (x-1)][j - (y-1)] * pixeles[i,j][1]
                    except:
                        pass
            pixCon[x,y] = (suma,suma,suma)
    #imCon.save('convolucion.png')
    return imCon

def centroCirculo(imx, imy, im, r):
    w,h = im.size
    freq = dict()
    circulos = dict()
    coordx = imx.load()
    coordy = imy.load()

    for x in range(w):
        for y in range(h):
            (rx,gx,bx) = coordx[x,y]
            (ry,gy,by) = coordy[x,y]
            
            gx = float(rx+gx+bx)/3
            gy = float(ry+gy+by)/3
            g = sqrt(pow(gx,2) + pow(gy,2))

            if fabs(g) > 0:
                #cosTheta = gx/g
                #sinTheta = gy/g
                theta = atan2(gy,gx)
                
                #centro = (int(x-r*cosTheta), int(y-r*sinTheta))
                centro = (int( x - r * cos(theta)), int( y - r * sin(theta)))
                #redondear
                centro = ((centro[0]/10)*10, (centro[1]/10)*10)
                circulos[x,y]=centro

                if not centro in freq:
                    freq[centro] = 1
                else:
                    freq[centro] += 1
            else:
                circulos[x,y]=None
    return circulos, freq

def amarillo():
    amarillo = (random.randint(238,255), random.randint(100,255), random.randint(0,50))
    return amarillo


def etiquetarCirculos(im, freq, circulos,r):
    pixeles = im.load()
    w, h = im.size
    fuente = ImageFont.truetype('/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-LI.ttf',14)
    imagen = ImageDraw.Draw(im)
    cont = 1
    color = dict()
    aux = 1
    for i in freq.keys():
        color[i] = amarillo()
        imagen.ellipse((i[0]-aux, i[1]-aux, i[0]+aux, i[1]+aux), fill=(0,255,0))
        imagen.text((i[0]+aux+3, i[1]), ('Circulo '+str(cont)), fill=(0,255,0), font=fuente)
        cont +=1

    print color
    
    for x in range(w):
        for y in range(h):
            if circulos[x,y] in freq:
                print x,' ',y
                try:
                    pixeles[x,y] = color[circulos[x,y]]
                except:
                    pass
    return im

if __name__ =="__main__":
    imPath = sys.argv[1]
    im = Image.open(imPath)
    w, h = im.size
    mx = [[-1, -1, -1], [2, 2, 2], [-1, -1, -1]]
    my = [[-1, 2, -1], [-1, 2, -1], [-1, 2, -1]]
    imx = convolucion(im, mx)
    imy = convolucion(im, my)
    radio = 55
    
    circulos,freq = centroCirculo(imx, imy, im, radio)
    
    maximo = 0
    suma = 0.0
    for i in freq.keys():
        suma += freq[i]
        if freq[i] > maximo:
            maximo = freq[i]

    prom = suma/len(freq)
    print prom
    print maximo
    umbral = maximo-prom
    print umbral

    for i in freq.keys():
        if freq[i] < umbral:
            freq.pop(i)
        else:
            print freq[i]
        
    etiquetarCirculos(im,freq,circulos,radio)
    im.save('circulos.png')
