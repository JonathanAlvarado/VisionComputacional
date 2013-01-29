import pygame,sys
from pygame.locals import *
from PIL import Image

imagenPath = 'kristen.jpg'

def medidas():
    im = Image.open(imagenPath)
    (ancho, alto) = im.size
    return ancho,alto

def main():
    ancho,alto = medidas()
    pygame.init()
    ventana = pygame.display.set_mode([ancho,alto])
    pygame.display.set_caption('Grises')
    fondo = pygame.image.load(imagenPath)#carga fondo
    ventana.blit(fondo,(0,0))#agrega imagen a ventana
    pygame.display.flip()#actualiza pantalla
    
    while True:
        evento = pygame.event.poll()
        if evento.type == pygame.QUIT:
            break

    

main()
