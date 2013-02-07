import pygame,sys
from pygame.locals import *
from PIL import Image
import numpy

imagenPath = 'kristen.jpg'#ruta de la imagen
umbralNegro = 99#Umbral para cambiar pixeles a negro
umbralBlanco = 100#Umbral para cambiar pixeles a blanco
imFiltro = 'filtro.png'

#obtiene las medidas de la imagen para ajustar la ventana a la imagen
def medidas():
    im = Image.open(imagenPath)
    #print im.mode
    (ancho, alto) = im.size
    return ancho,alto,im

#cambia imagen a escala de grises
def grises(im,ancho,alto):
    pixeles = im.load()

    for x in range(ancho):
        for y in range(alto):
            #rgb = pixeles[x,y]
            #r = rgb[0]
            #g = rgb[1]
            #b = rgb[2]
            
            #promedio = int((r+g+b)/3)
            promedio = sum(pixeles[x,y])/3
            #print promedio
            gris = (promedio,promedio,promedio)
            im.putpixel((x,y),gris)
    print '\nEscala de grises'
    im.save('gris.png')#guarda la imagen


def umbrales(im,ancho,alto):
    pixeles = im.load()

    for x in range(ancho):
        for y in range(alto):
            promedio = sum(pixeles[x,y])/3
            #print promedio
            
            if promedio < umbralNegro:
                gris = (0, 0, 0)
                #print "Negro= ",gris
            elif promedio > umbralBlanco:
                gris = (255, 255, 255)
                #print "Blanco= ",gris
            else:
                gris = (promedio,promedio,promedio)

            im.putpixel((x,y),gris)
    print '\nUmbrales'
    im.save('umbrales.png')


'''
def conv(im):
    f = im.load()
    F=...
    h = np.array([0,0.2,0], [0.2,0.2,0.2], [0, 0.2,0])
    for x in xrange(ancho):
        for y in xrange(alto):
            suma = 0.0
            for i in xrange(3):
                for j in xrange(3):
                    try si hay pixel
                        suma +=f(x+i,y+i) * h(i,j)
                    except
            F(x,y) = suma
    return F
'''

def filtros(im,ancho,alto):
    imPixeles = im.load()

    for x in range(ancho):
        for y in range(alto):
            pix = []
            pix.append(list(imPixeles[x, y]))
            
            if x > 0:
                pix.append(list(imPixeles[x-1, y]))
            if y > 0:
                pix.append(list(imPixeles[x, y-1]))
            if x < ancho-1:
                pix.append(list(imPixeles[x+1, y]))
            if y < alto-1:
                pix.append(list(imPixeles[x, y+1]))
            
            filtro = [sum(i) for i in zip(*pix)]
            total = len(pix)
            imPixeles[x,y] = filtro[0]/total, filtro[1]/total, filtro[2]/total
    print '\nFiltro aplicado'
    im.save(imFiltro)


#actualiza la ventana cuando se cambia la imagen a grises o al utilizar la funcion umbrales
def actualizar(ventana, cargar):
    if cargar == 1:
        fondo = pygame.image.load('gris.png').convert()
    elif cargar == 2:
        fondo = pygame.image.load('umbrales.png').convert()
    elif cargar == 3:
        fondo = pygame.image.load('filtro.png').convert()
    ventana.blit(fondo,(0,0))
    pygame.display.flip()


def main():
    ancho,alto,im = medidas()#toma medidas de la imagen
    pygame.init()
    ventana = pygame.display.set_mode([ancho,alto])#crea ventana de acuerdo a medidas de la imagen
    pygame.display.set_caption('Laboratorio 1')
    fondo = pygame.image.load(imagenPath).convert()#carga fondo
    ventana.blit(fondo,(0,0))#agrega imagen a ventana
    #pygame.display.flip()#actualiza pantalla
    pygame.display.update()

    while True:
        evento = pygame.event.poll()
        if evento.type == pygame.QUIT:
            break
        if evento.type == pygame.KEYDOWN:
            if evento.key == K_SPACE:
                grises(im,ancho,alto)
                actualizar(ventana,1)
            elif evento.key == K_l:
                umbrales(im,ancho,alto)
                actualizar(ventana,2)
            elif evento.key == K_f:
                imagen = filtros(im,ancho,alto)
                actualizar(ventana,3)
                
                
print 'Presiona\n\nBarra espaciadora -> para cambiar la imagen a escala de grises\nTecla L -> para jugar con los umbrales\nTecla f -> para aplicar filtro'
main()
