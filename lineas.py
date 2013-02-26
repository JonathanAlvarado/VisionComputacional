from PIL import Image
import sys 
from math import sqrt,fabs,sin,cos,floor,atan, ceil

def escalaDeGrises(im):
    imGris = im.copy()
    w,h = imGris.size
    pixeles = imGris.load()

    for x in range(w):
        for y in range(h):
            promedio = sum(pixeles[x,y])/3
            pixeles[x,y] = (promedio, promedio,promedio)
    imGris.save('grises.png')
    return imGris
    
def difuminar(im):
    pixeles = im.load()
    w,h = im.size
    imDif = Image.new('RGB',(w,h))
    difPix = imDif.load()

    for x in range(w):
        for y in range(h):
            pix = []
            pix.append(list(pixeles[x,y]))

            if x > 0:
                pix.append(list(pixeles[x-1, y]))
            if y > 0:
                pix.append(list(pixeles[x, y-1]))
            if x < w-1:
                pix.append(list(pixeles[x+1, y]))
            if y < h-1:
                pix.append(list(pixeles[x, y+1]))
            
            filtro = [sum(i) for i in zip(*pix)]
            total = len(pix)
            difPix[x,y] = filtro[0]/total, filtro[1]/total, filtro[2]/total
    imDif.save('difuminada.png')
    return imDif

def binarizar(im):
    imBinaria = im.copy()
    w,h = im.size
    pixeles = imBinaria.load()

    for x in range(w):
        for y in range(h):
            if pixeles[x,y][0] >= 30:
                    pixeles[x,y] = (255,255,255)
            else:
                    pixeles[x,y] = (0,0,0)
    imBinaria.save('binaria.png')
    return imBinaria

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

def euclides(gx,gy):
    w, h = gx.size
    g = Image.new('RGB', (w,h))
    pixeles = g.load()
    dx = gx.load()
    dy = gy.load()
    for x in range(w):
        for y in range(h):
            c = int(sqrt( (dx[x,y][0])**2 + (dy[x,y][0])**2 ))
            pixeles[x,y] = (c,c,c)
    return g

def normalizar(im):
    w,h = im.size
    imNorm = im.copy()
    pixeles = imNorm.load()
    maximo = 0
    minimo = 0
    for x in range(w):
        for y in range(h):
            if pixeles[x,y] > maximo:
                maximo = pixeles[x,y][0]
            if pixeles[x,y] < minimo:
                minimo = pixeles[x,y][0]
    prop = 256.0/(maximo - minimo)
    for x in range(w):
        for y in range(h):
            n = int(floor((pixeles[x,y][0] - minimo)* prop))
            pixeles[x,y] = (n,n,n)
    imNorm.save('normalizada.png')
    return imNorm

def bfs(im, origen, color):
    pixeles = im.load()
    cola = []
    coordenadas = []
    cola.append(origen)
    inicio = pixeles[origen]

    while len(cola) > 0:
        x,y = cola.pop(0)
        actual = pixeles[x,y]

        if actual == inicio or actual == color:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    fila, colum = x+dx, y+dy
                    try:
                        candidato = pixeles[fila,colum]
                        if candidato == inicio:
                            pixeles[fila,colum] = color
                            cola.append((fila,colum))
                            coordenadas.append((fila,colum))
                    except:
                        pass
    return coordenadas

def frecuentes(histo, cantidad):
    frec = list()
    for valor in histo:
        if valor is None:
            continue
        frecuencia = histo[valor]
        acepta = False
        if len(frec) <= cantidad:
            acepta = True
        if not acepta:
            for (v, f) in frec:
                if frecuencia > f:
                    acepta = True
                    break
        if acepta:
            frec.append((valor, frecuencia))
            frec = sorted(frec, key = lambda tupla: tupla[1])
            if len(frec) > cantidad:
                frec.pop(0)
    incluidos = list()
    for (valor, frecuencia) in frec:
        incluidos.append(valor)
        #print frecuencia
    return incluidos

def deteccionDeLineas(im,umbral):
    '''Transformada de Hough
    umbral = lineas a considerar'''
    sobelx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    sobely = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]
    imx = convolucion(im, sobelx)
    imy = convolucion(im, sobely)
    gx = imx.load()
    gy = imy.load()
    m = binarizar(normalizar(euclides(imx,imy)))
    w,h = im.size
    #coords = bfs(m,(0,0),(255,255,255))
    angulos = []
    comb = {}
    pixeles = m.load()
    resultado = list()

    for x in range(w):
        datos = list()
        for y in range(h):
            hor = gx[x,y][0]
            ver = gy[x,y][0]

            if fabs(hor) + fabs(ver) <= 0.0:#nada en ninguna direccion
                theta = None
            elif hor == 0 and ver == 255:
                theta = 90
            elif fabs(hor) > 0.0:
                theta = atan(fabs(ver/hor))
            if theta is not None:
                rho = fabs( x * cos(theta) + y * sin(theta))
                
                if x > 0 and x < w-1 and y > 0 and y < h-1:
                    if (rho, theta) in comb:
                        comb[ (rho, theta) ] += 1
                    else:
                        comb[ (rho, theta) ] = 1
                datos.append( (rho, theta) )
            else:
                datos.append((None,None))
        resultado.append(datos)

    incluir = int(ceil (len(comb) * umbral))
    
    frec = frecuentes(comb, incluir)
    '''for i in range(incluir):
        rho, theta = comb[i][0]
        frec[ (rho,theta) ] = comb[1]'''

    for x in range(w):
        for y in range(h):
            if x > 0 and x< w-1 and y > 0 and y < h-1:
                rho, theta = resultado[x][y]
                    
                if (rho, theta) in frec:
                    if theta == 0:
                        pixeles[x,y] = (255,0,0)
                    elif theta == 90:
                        pixeles [x,y] = (0,0,255)
    m.save('lineas.png')

if __name__=="__main__":
    imPath = sys.argv[1]
    im = Image.open(imPath)
    gris = escalaDeGrises(im)
    dif = difuminar(gris)
    lineas = deteccionDeLineas(dif,.05)
