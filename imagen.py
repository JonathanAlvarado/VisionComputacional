#!/usr/bin/python

from Tkinter import *
from PIL import Image, ImageTk
import sys
import random

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
        #self.canvas.create_image(self.w/2, self.h/2, self.image=fondo)
        self.label = Label(self.canvas, image=self.fondo)
        self.label.image=self.fondo
        self.label.pack()

        '''Canvas para los botones '''
        self.botones = Canvas(self.root, width=self.w, height = 30)
        self.boton = Button(self.botones, text='Escala de grises', fg='black', command=self.grises)
        self.panel = self.botones.create_window(5,0, anchor='nw', window=self.boton)
        self.boton = Button(self.botones, text='Difuminar', fg='black', command=self.difuminar)
        self.panel = self.botones.create_window(150,0, anchor='nw', window=self.boton)
        self.boton = Button(self.botones, text='Binarizar', fg='black', command=self.binarizar)
        self.panel = self.botones.create_window(250,0, anchor='nw', window=self.boton)
        self.boton = Button(self.botones, text='Ruido', fg='black', command=self.salPimienta)
        self.panel = self.botones.create_window(350,0, anchor='nw', window=self.boton)
        self.boton = Button(self.botones, text='Limpiar', fg='black', command=self.quitarSalPimienta)
        self.panel = self.botones.create_window(400,0, anchor='nw', window=self.boton)
        self.boton = Button(self.botones, text='Convolucion', fg='black', command=self.convolucion)
        self.panel = self.botones.create_window(450,0, anchor='nw', window=self.boton)

        self.canvas.pack(side='top')
        self.botones.pack(side='bottom')

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
        imBinaria = Image.new("L", (self.w, self.h))
        binPix = imBinaria.load()
        
        for x in range(self.w):
            for y in range(self.h):
                if self.im.mode == 'RGB':
                    if max( pixeles[x,y] ) >= 127:
                        binPix[x,y] = 255
                    else:
                        binPix[x,y] = 0
                elif self.im.mode == 'L':
                    if max( pixeles[x,y] ) >= 127:
                        binPix[x,y] = 127
                    else:
                        binPix[x,y] = 0
        imBinaria.save('binaria.png')
        self.imActual = imBinaria
        self.actualizarFondo()

        
    def salPimienta(self):
        '''Aplica ruido sal y pimienta escogiendo pixeles al azar '''
        salPim = self.imActual.copy()
        pixeles = salPim.load()
        area = self.w * self.h
        num = random.uniform(1,area)/2
        tot = int(num * random.uniform(0.1, 0.5))
        print tot
        if salPim.mode == 'RGB':
            for i in range(tot):
                x,y=random.randint(0,self.w-1), random.randint(0,self.h-1)
                cambio = random.randint(0,1)
                if cambio==1:
                    pixeles[x,y] = (255,255,255)
                else:
                    pixeles[x,y] = (0,0,0)
            print 'entre'
        elif salPim.mode == 'L':
            for i in range(tot):
                x,y=random.randint(0,self.w-1), random.randint(0,self.h-1)
                cambio = random.randint(0,1)
                if cambio==1:
                    pixeles[x,y] = 255
                else:
                    pixeles[x,y] = 0

        salPim.save('salPimienta.png')
        self.imActual = salPim
        self.actualizarFondo()

    def quitarSalPimienta(self):
        pixeles = self.imActual.load()
        
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
            
                        sumas = [sum(i) for i in zip(*vecinos)]
                        total = len(vecinos)
                        normPix[x,y] = sumas[0]/total, sumas[1]/total, sumas[2]/total
            normal.save('sinSal.png')
            self.imActual = normal
        
        if self.imActual.mode == 'L':
            normal = Image.new('L', (self.w, self.h))
            normPix = normal.load()
            for x in range(self.w):
                for y in range(self.h):
                    salPimienta = [255,0]
                    vecinos = []
                    if pixeles[x,y] in salPimienta:
                        if x > 0:
                            vecinos.append(pixeles[x-1, y])
                        if y > 0:
                            vecinos.append(pixeles[x, y-1])
                        if x < self.w-1:
                            vecinos.append(pixeles[x+1, y])
                        if y < self.h-1:
                            vecinos.append(pixeles[x, y+1])
                        
                        prom = sum(vecinos)/len(vecinos)
                        print 'actual=',pixeles[x,y],'resta=',pixeles[x,y]-prom
                        if pixeles[x,y] - prom <= -150 or pixeles[x,y]-prom >=150:
                            normPix[x,y] = prom
            normal.save('sinSal.png')
            self.imActual = normal

        self.actualizarFondo()

    def convolucion(self):
        pixeles = self.imActual.load()
        imCon = Image.new("L", (self.w, self.h))
        conPix = imCon.load()
        h = [(0,0.2,0), (0.2,0.2,0.2), (0,0.2,0)]

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
        

def main():
    try:
        imPath = sys.argv[1]
        #print imPath
    except:
        print "Selecciona una imagen"
        return
    
    root = Tk()
    Instagram = Filtros(imPath, root)
    root.title("Filtros")
    root.mainloop()

if __name__ == "__main__":
    main()
