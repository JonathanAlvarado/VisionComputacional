#!/usr/bin/python

from Tkinter import *
from PIL import Image, ImageTk
import sys
import random
import math
import time

class Filtros:
    
    def __init__(self, path, root):
        self.imPath = path
        self.im = self.imRGB()
        self.w, self.h = self.im.size
        self.imActual = self.im

        self.root = root
        
        '''Canvas imagen '''
        self.fondo = ImageTk.PhotoImage(self.im)
        self.canvas = Canvas(self.root, width=self.w, height = self.h)
        self.label = Label(self.canvas, image=self.fondo)
        self.label.image=self.fondo
        self.label.pack()

        '''Canvas para los botones '''
        self.botones = Canvas(self.root, width=150, height = self.h)
        self.boton = Button(self.botones, text='Escala de grises', fg='black', command=self.grises)
        self.panel = self.botones.create_window(5,0, anchor='nw', window=self.boton)
        self.boton = Button(self.botones, text='Difuminar', fg='black', command=self.difuminar)
        self.panel = self.botones.create_window(5,30, anchor='nw', window=self.boton)
        self.boton = Button(self.botones, text='Binarizar', fg='black', command=self.binarizar)
        self.panel = self.botones.create_window(5,60, anchor='nw', window=self.boton)
        self.boton = Button(self.botones, text='Ruido', fg='black', command=self.salPimienta)
        self.panel = self.botones.create_window(5,90, anchor='nw', window=self.boton)
        self.boton = Button(self.botones, text='Limpiar', fg='black', command=self.quitarSalPimienta)
        self.panel = self.botones.create_window(5,120, anchor='nw', window=self.boton)
        self.boton = Button(self.botones, text='Convolucion', fg='black', command=self.convolucion)
        self.panel = self.botones.create_window(5,150, anchor='nw', window=self.boton)
        self.boton = Button(self.botones, text='Bordes', fg='black', command=self.bordes)
        self.panel = self.botones.create_window(5,180, anchor='nw', window=self.boton)
        self.boton = Button(self.botones, text='Etiquetar', fg='black', command=self.etiquetar)
        self.panel = self.botones.create_window(5,210, anchor='nw', window=self.boton)
        self.boton = Button(self.botones, text='Normalizar', fg='black', command=self.normalizar)
        self.panel = self.botones.create_window(5,250, anchor='nw', window=self.boton)

        self.botones.pack(side=LEFT)
        self.canvas.pack()

    def imRGB(self):
        '''Abre imagen original y convierte a RGB
        '''
        imagen = Image.open(self.imPath)
        imagen = imagen.convert('RGB')
        return imagen

    def actualizarFondo(self):
        '''Actualiza fondo de la ventana'''
        fondo = ImageTk.PhotoImage(self.imActual)
        self.label.config(image=fondo)
        self.label.image = fondo
        
    def grises(self):
        imGris = Image.new('L',(self.w, self.h))
        grisPix = imGris.load()
        pixeles = self.im.load()
        
        for x in range(self.w):
            for y in range(self.h):
                promedio = sum( pixeles[x,y] )/3
                #print promedio
                grisPix[x,y] = promedio
        imGris.save('grises.png')
        self.imActual = imGris
        self.actualizarFondo()

    def difuminar(self):
        '''Toma los vecinos (arriba,abajo,izquierda,derecha) de un pixel
        calcula el promedio y el resultado es el valor de todfos los 
        pixeles'''
        pixeles = self.imActual.load()

        if self.imActual.mode == 'RGB':
            imDifuminada = Image.new('RGB', (self.w, self.h))
            difPix = imDifuminada.load()
            for i in range(5):
                for x in range(self.w):
                    for y in range(self.h):
                        pix = []
                        pix.append(list(pixeles[x, y]))
            
                        if x > 0:
                            pix.append(list(pixeles[x-1, y]))
                        if y > 0:
                            pix.append(list(pixeles[x, y-1]))
                        if x < self.w-1:
                            pix.append(list(pixeles[x+1, y]))
                        if y < self.h-1:
                            pix.append(list(pixeles[x, y+1]))
            
                        filtro = [sum(i) for i in zip(*pix)]
                        total = len(pix)
                        difPix[x,y] = filtro[0]/total, filtro[1]/total, filtro[2]/total

        if self.imActual.mode == 'L':
            imDifuminada = Image.new('L', (self.w, self.h))
            difPix = imDifuminada.load()
            for x in range(self.w):
                for y in range(self.h):
                    pix = []
                    pix.append(pixeles[x, y])
            
                    if x > 0:
                        pix.append(pixeles[x-1, y])
                    if y > 0:
                        pix.append(pixeles[x, y-1])
                    if x < self.w-1:
                        pix.append(pixeles[x+1, y])
                    if y < self.h-1:
                        pix.append(pixeles[x, y+1])
            
                    filtro = sum(pix)
                    difPix[x,y] = filtro/len(pix)
        
        imDifuminada.save('difuminada.png')
        self.imActual = imDifuminada
        self.actualizarFondo()
        
    def binarizar(self):
        pixeles = self.imActual.load()
        imBinaria = Image.new('RGB', (self.w, self.h))
        binPix = imBinaria.load()
        
        for x in range(self.w):
            for y in range(self.h):
                if pixeles[x,y] >= 30:
                    binPix[x,y] = (255,255,255)
                else:
                    binPix[x,y] = (0,0,0)
        imBinaria.save('binaria.png')
        self.imActual = imBinaria
        self.actualizarFondo()

        
    def salPimienta(self):
        '''Aplica ruido sal y pimienta escogiendo pixeles al azar '''
        salPim = self.imActual.copy()
        pixeles = salPim.load()
        frec = 0.02

        if salPim.mode == 'RGB':
            for x in range(self.w):
                for y in range(self.h):
                    cambio = random.uniform(0,1)
                    if cambio < frec:
                        if cambio>0:
                            pixeles[x,y] = (255,255,255)
                        else:
                            pixeles[x,y] = (0,0,0)
            
        elif salPim.mode == 'L':
            for x in range(self.w):
                for y in range(self.h):
                    cambio = random.uniform(0,1.0)
                    if cambio < frec:
                        if cambio > 0:
                            pixeles[x,y] = 255
                        else:
                            pixeles[x,y] = 0

        salPim.save('salPimienta.png')
        self.imActual = salPim
        self.actualizarFondo()


    def quitarSalPimienta(self):
        '''Quita el ruido sal y pimienta
        '''
        pixeles = self.imActual.load()
        umbral = 30
        
        if self.imActual.mode == 'RGB':
            normal = Image.new('RGB', (self.w, self.h))
            normPix = normal.load()
            
            for x in range(self.w):
                for y in range(self.h):
                    salPimienta = [(255,255,255),(0,0,0)]
                    vecinos = []
                    if pixeles[x,y] in salPimienta:
                        if x > 0:
                            vecinos.append(list(pixeles[x-1, y]))
                        if y > 0:
                            vecinos.append(list(pixeles[x, y-1]))
                        if x < self.w-1:
                            vecinos.append(list(pixeles[x+1, y]))
                        if y < self.h-1:
                            vecinos.append(list(pixeles[x, y+1]))
            
                        suma = [sum(i) for i in zip(*vecinos)]
                        total = len(vecinos)
                        normPix[x,y] = sumas[0]/total, sumas[1]/total, sumas[2]/total
            normal.save('sinSal.png')
            self.imActual = normal
        
        if self.imActual.mode == 'L':
            normal = Image.new('L', (self.w, self.h))
            normPix = normal.load()
            for x in range(self.w):
                for y in range(self.h):
                    vecinos = []
                    if x > 0:
                        vecinos.append(pixeles[x-1, y])
                    if y > 0:
                        vecinos.append(pixeles[x, y-1])
                    if x < self.w-1:
                        vecinos.append(pixeles[x+1, y])
                    if y < self.h-1:
                        vecinos.append(pixeles[x, y+1])

                    prom = sum(vecinos)/len(vecinos)
                    if abs(prom - pixeles[x,y]) > 60:
                        normPix[x,y] = prom
                    else:
                        normPix[x,y] = pixeles[x,y]

            normal.save('sinSal.png')
            self.imActual = normal
        self.actualizarFondo()

    def convolucion(self):
        pixeles = self.imActual.load()
        imCon = Image.new("L", (self.w, self.h))
        conPix = imCon.load()
        h = [(0,0.2,0), (0.2,0.2,0.2), (0,0.2,0)]

        if self.imActual.mode == 'RGB':
            for x in range(self.w):
                for y in range(self.h):
                    suma = 0
                    for i in range(3):
                        for j in range (3):
                            try:
                                if x < self.w or y < self.h:
                                    suma += int(max(pixeles[(x-1)+i,(y-1)+j]) * h[j][i])
                            except IndexError:
                                suma += 0
                    #print suma
                    conPix[x,y] = suma


        if self.imActual.mode == 'L':
            for x in range(self.w):
                for y in range(self.h):
                    suma = 0
                    for i in range(3):
                        for j in range (3):
                            try:
                                if x < self.w or y < self.h:
                                    suma += int(pixeles[(x-1)+i,(y-1)+j] * h[j][i])
                            except IndexError:
                                suma += 0
                    #print suma
                    conPix[x,y] = suma

        imCon.save('convolusion.png')
        self.imActual = imCon
        self.actualizarFondo()


    def bordes(self):
        '''Aplica mascara para obtener los bordes de una imagen '''
        tiempoIn = time.time()
        
        pixeles = self.imActual.load()
        imBor = Image.new("L", (self.w, self.h))
        borPix = imBor.load()

        g = ([0,1,0], [1,-4,1], [0,1,0])

        for y in range(self.h):
            for x in range(self.w):
                suma = 0
                for i in range( x-1, x+2):
                    for j in range(y-1, y+2):
                        try:
                            suma += g[i-(x-1)] [j-(y-1)] * pixeles[i,j]
                        except:
                            pass
                        
                        
                borPix[x,y]=suma
        imBor.save('bordes.png')
        tiempoFin = time.time()
        print 'Mascara tardo: ', tiempoFin - tiempoIn, ' segundos'
        self.imActual = imBor
        self.actualizarFondo()


    def normalizar(self):
        imNorm = Image.new('L',(self.w,self.h))
        normPix = imNorm.load()
        pixeles = self.imActual.load()

        pix = []
        for x in range(self.w):
            for y in range(self.h):
                pix.append( pixeles[x,y])

        maximo = max(pix)
        minimo = min(pix)
        prop = 256.0 / (maximo - minimo)

        for x in range(self.w):
            for y in range(self.h):
                normPix[x,y]= int(math.floor((pixeles[x,y]-minimo )*prop))
        imNorm.save('Normalizada.png')
        self.imActual = imNorm
        self.actualizarFondo()


    def bfs(self,im,color,origen):
        '''actual = pixel actual
        total = cuenta el total de pixeles de la figura
        '''
        pixeles = im.load()
        cola = []
        coordX = []
        coordY = []
        cola.append(origen)
        inicio = pixeles[origen]
        total = 0

        while len(cola) > 0:
            x, y = cola.pop(0)
            actual = pixeles[x,y]

            if actual == inicio or actual == color:
                for dx in [-1,0,1]:
                    for dy in [-1,0,1]:
                        fila,colum = x+dx, y+dy
                        try:
                            candidato = pixeles[fila,colum]
                            if candidato == inicio:
                                pixeles[fila,colum] = color
                                total +=1
                                cola.append((fila,colum))
                                coordX.append(fila)
                                coordY.append(colum)
                        except:
                            pass
        return total, coordX, coordY


    def etiquetar(self):
        im = self.imActual.copy()
        pixeles = im.load()
        totPix = self.w * self.h
        porcentajes = []
        centros = []
        
        for x in range(self.w):
            for y in range(self.h):
                if pixeles[x,y] == (0,0,0):
                    r,g,b = random.randint(0,255), random.randint(0,255), random.randint(0,255)
                    color = (r,g,b)
                    pixFigura,cX, cY = self.bfs(im, color, (x,y))
                    porciento = float(pixFigura)/totPix
                    if porciento > .001:
                        porcentajes.append([porciento,color])
                        c = sum(cX)/len(cX), sum(cY)/len(cY)
                        centros.append(c)

        fondo = porcentajes.index(max(porcentajes))
        colorFondo = porcentajes[fondo][1]

        fig = 1
        for i in porcentajes:
            print 'Figura %s porcentaje de la imagen: %.4f'%(fig,i[0])
            fig+=1

        #cambia fondo a color gris
        for x in range(self.w):
            for y in range(self.h):
                if pixeles[x,y] == colorFondo:
                    pixeles[x,y] = (190,190,190)

        #centros de masa
        for i in centros:
            pixeles[i]=(0,255,0)

        im.save('final.png')
        self.imActual = im
        self.actualizarFondo()
        
        #etiqueta centros
        etiqueta=1
        for c in centros:
            i,j = c[0],c[1]
            Label(self.canvas, text='Obj %d'%etiqueta).place(x=i, y=j)
            etiqueta+=1

def main():
    try:
        imPath = sys.argv[1]
    except:
        print "Selecciona una imagen"
        return
    
    root = Tk()
    Instagram = Filtros(imPath, root)
    root.title("Filtros")
    root.mainloop()

if __name__ == "__main__":
    main()
