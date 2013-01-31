import pygame,sys
from pygame.locals import *
from PIL import Image

imagenPath = 'kristen.jpg'

def medidas():
    im = Image.open(imagenPath)
    (ancho, alto) = im.size
    return ancho,alto,im

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
            gris = (promedio,promedio,promedio)

            im.putpixel((x,y),gris)

        im.save('gris.jpg')

def actualizarPantalla(ventana):
    fondo = pygame.image.load('gris.jpg').convert()
    ventana.blit(fondo,(0,0))
    pygame.display.flip()

def main():
    ancho,alto,im = medidas()
    pygame.init()
    ventana = pygame.display.set_mode([ancho,alto])
    pygame.display.set_caption('Grises')
    fondo = pygame.image.load(imagenPath).convert()#carga fondo
    ventana.blit(fondo,(0,0))#agrega imagen a ventana
    pygame.display.flip()#actualiza pantalla
    
    grises(im,ancho,alto)

    while True:
        evento = pygame.event.poll()
        if evento.type == pygame.QUIT:
            break
        if evento.type == pygame.KEYDOWN:
            if evento.key == K_SPACE:
                actualizarPantalla(ventana)

main()
