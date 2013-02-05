import pygame,sys
from pygame.locals import *
from PIL import Image

imagenPath = 'kristen.jpg'#ruta de la imagen
umbralNegro = 99#Umbral para cambiar pixeles a negro
umbralBlanco = 100#Umbral para cambiar pixeles a blanco

#obtiene las medidas de la imagen para ajustar la ventana a la imagen
def medidas():
    im = Image.open(imagenPath)
    (ancho, alto) = im.size
    return ancho,alto,im

#cambia imagen a escala de grises
def grises(im,ancho,alto):
    x = 0
    y = 0
    
    pixeles = im.load()

    for x in range(ancho):
        for y in range(alto):
            rgb = pixeles[x,y]
            r = rgb[0]
            g = rgb[1]
            b = rgb[2]
            
            promedio = int((r+g+b)/3)
            #print promedio
            gris = (promedio,promedio,promedio)
            im.putpixel((x,y),gris)

    im.save('gris.png')#guarda la imagen


def umbrales(im,ancho,alto):
    x = 0
    y = 0
    
    pixeles = im.load()

    for x in range(ancho):
        for y in range(alto):
            rgb = pixeles[x,y]
            r = rgb[0]
            g = rgb[1]
            b = rgb[2]
            
            promedio = int((r+g+b)/3)
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

    im.save('umbrales.png')

#actualiza la ventana cuando se cambia la imagen a grises o al utilizar la funcion umbrales
def actualizarPantalla(ventana, cargar):
    if cargar == 'gris':
        fondo = pygame.image.load('gris.png').convert()
    elif cargar == 'umbrales':
        fondo = pygame.image.load('umbrales.png').convert()
    ventana.blit(fondo,(0,0))
    pygame.display.flip()

def main():
    ancho,alto,im = medidas()#toma medidas de la imagen
    pygame.init()
    ventana = pygame.display.set_mode([ancho,alto])#crea ventana de acuerdo a medidas de la imagen
    pygame.display.set_caption('Laboratorio 1')
    fondo = pygame.image.load(imagenPath).convert()#carga fondo
    ventana.blit(fondo,(0,0))#agrega imagen a ventana
    pygame.display.flip()#actualiza pantalla

    while True:
        evento = pygame.event.poll()
        if evento.type == pygame.QUIT:
            break
        if evento.type == pygame.KEYDOWN:
            if evento.key == K_SPACE:
                cargar = 'gris'
                grises(im,ancho,alto)
                actualizarPantalla(ventana,cargar)
            elif evento.key == K_l:
                cargar = 'umbrales'
                umbrales(im,ancho,alto)
                actualizarPantalla(ventana,cargar)
                

print 'Presiona la barra espaciadora para cambiar la imagen a escala de grises o la tecla L para jugar con los umbrales'
main()
