import base64
import time #delay
import gzip
import sys
import pygame
import random
from pygame.locals import *
import json
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
""" variables globales"""
ancho = 1000
alto = 650
listaEnemigo = []
habilitador = False
lalo = True
listaDeDisparo = []

class jugador(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagenCarro = pygame.image.load("sprites_gold.png")
        self.imagenCarro.set_clip(pygame.Rect(99,26,90,140))
        self.image = self.imagenCarro.subsurface(self.imagenCarro.get_clip())
        self.inv_imagencarro = pygame.transform.flip(self.imagenCarro,True,False)
        self.inv_imagencarro.set_clip(pygame.Rect(50,26,90,70))
        self.Rimage = self.inv_imagencarro.subsurface(self.inv_imagencarro.get_clip())



        self.rect = self.image.get_rect()
        self.rect.centerx = ancho-830
        self.rect.centery = alto-65

        self.vida = True
        self.velocidad = 50

        self.frame = 0
        """ animacion """
        self.right_states = {0: (41,26,90,134),1:(200,26,80,140),2:(140,26,70,138)}
        self.Rright_states = {0: (41,26,90,134),1:(500,26,200,140),2:(140,26,70,138)}

        self.direct = True
        self.salto = True
        self.salto_par = True
        self.contadorfun = 0

        




        """ mover a la derecha """


    def movimientoDerecha(self):
        """ que se pueda mover a la derecha en el eje x """

        self.rect.right += self.velocidad
        self.movimiento()


    def movimientoIzquierda(self):
        """ que se pueda mover a la izquierda """
        self.rect.left -= self.velocidad
        self.movimiento()


    def movimiento(self):
        if self.vida == True:
            """ crear hasta donde se puede mover"""
            if self.rect.left <= 10 :
                self.rect.left = 11

    def disparar(self,x,y):

        miProyectil = Proyectil(x,y,"zonahoria.png",True)

        listaDeDisparo.append(miProyectil)


    """ animacion"""

    def get_frame(self,frame_set):
        self.frame += 1
        if self.frame > (len(frame_set)-1):
            self.frame = 0

        return frame_set[self.frame]

    def clip(self,clipped_rect):
        if type(clipped_rect) is dict:
            self.imagenCarro.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            self.imagenCarro.set_clip(pygame.Rect(clipped_rect))
        return clipped_rect

    def Rclip (self, Rclipped_rect):
        if type (Rclipped_rect) is dict:
            self.inv_imagencarro.set_clip(pygame.Rect(self.get_frame(Rclipped_rect)))
        else:
            self.inv_imagencarro.set_clip(pygame.Rect(Rclipped_rect))
        return Rclipped_rect

    def update(self,direction):
        if direction == 'right':
            self.clip(self.right_states)
            self.rect.centerx += 5

        elif direction == "left":
            self.Rclip(self.Rright_states)
            self.rect.centerx -= 5


        self.Rimage = self.inv_imagencarro.subsurface(self.inv_imagencarro.get_clip())
        self.image = self.imagenCarro.subsurface(self.imagenCarro.get_clip())

    def dibujar(self,superficie):
        superficie.blit(self.image,self.rect)
    def rdibujar(self,superficie):
        superficie.blit(self.Rimage,self.rect)


class Proyectil(pygame.sprite.Sprite):
    def __init__(self,posx,posy,ruta,personaje):
        pygame.sprite.Sprite.__init__(self)

        self.imagenProyectil = pygame.image.load(ruta)
        self.peque = pygame.transform.scale(self.imagenProyectil,(100,100))

        self.rect = self.imagenProyectil.get_rect()
        self.velocidadDisparo = 3

        self.rect.top = posy
        self.rect.left = posx
        self.disparoPersonaje = personaje

    def trayectoria(self):
        if self.disparoPersonaje == True:
            self.rect.top = self.rect.top - self.velocidadDisparo
        else:
            self.rect.top = self.rect.top + self.velocidadDisparo

    def dibujar(self,superficie):
        superficie.blit(self.peque,self.rect)

class Enemigos(pygame.sprite.Sprite):
    def __init__(self,posx,posy,distancia,imagenUno,imagenDos):
        pygame.sprite.Sprite.__init__(self)
        """ enemigo de tierra"""
        self.imagenA = pygame.image.load(imagenUno)
        self.imagenA =  pygame.transform.scale(self.imagenA,(50,50))

        """ enemigo de aire"""
        self.imagenB = pygame.image.load(imagenDos)
        self.imagenB = pygame.transform.scale(self.imagenB,(25,25))



        self.listaImagenes=[self.imagenA]
        self.imagenPos = 0
        self.imagenDepredador = self.listaImagenes[self.imagenPos]
        self.rect= self.imagenDepredador.get_rect()

        self.listaDeDisparos =[]
        self.velocidad = 5
        self.rect.top = posy
        self.rect.left = posx

        self.rangoDisparo = 5
        self.tiempoCambio =1

        self.derecha = True
        self.Contador = 0
        self.maxDescenso = self.rect.top + 40

        self.limiteDerecha = posx+ distancia
        self.limiteIzquierda = posx-distancia


        """ atributos del enemigo"""
    def comportamiento(self,tiempo):
        self.movimientos()

        self.ataque()
        if self.tiempoCambio == tiempo:
            self.imagenPos += 1
            self.tiempoCambio +=1

            if self.imagenPos > len(self.listaImagenes)-1:
                self.imagenPos = 0

    def ataque(self):
        if (random.randint(0,100) < self.rangoDisparo ):
            self.disparo()

    def disparo(self):
        x,y = self.rect.center
        miProyectil = Proyectil(x,y,"disparob.jpg",False)
        self.listaDeDisparos.append(miProyectil)


    def dibujar(self,superficie):
        self.imagenDepredador = self.listaImagenes[self.imagenPos]
        superficie.blit(self.imagenDepredador,self.rect)


def CargarEnemigos():
        posx = 100
        for x in range(1):
            enemigo = Enemigos(posx, 300, 100,'aguila.png','veneno.png')
            listaEnemigo.append(enemigo)
            posx += 300






def goldTraver():
    pygame.init()
    ventana = pygame.display.set_mode((ancho,alto))
    pygame.display.set_caption("Gold Traver")
    #imagenFondo = pygame.image.load("desierto.png").convert_alpha()
    """ me permite configurar la imagen el ancho y el alto de la imagen"""
    #imagenFondo = pygame.transform.scale(imagenFondo, (900, 500))

    #imagenFondo = pygame.image.load("fondo.png").convert_alpha()
    #imagenFondo = pygame.transform.scale(imagenFondo, (ancho, alto))

    """ creacion del jugador"""
    player = jugador()

    enJuego = True

    """ creacion del enemigo"""
    CargarEnemigos()

    reloj = pygame.time.Clock()


    while True:
        global lalo
        global habilitador
        global listaDeDisparo

        """cuantos frames se ejecutan por segundo"""
        reloj.tick(60)
        """ movimiento """
        tiempo = pygame.time.get_ticks()/1000


        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            """ crear eventos cuando se oprime una telca"""

            #if enJuego == True: #se usa para saber si el jugador no ha perdido


            """ hacer mover al enemigo mientras que el jugador no alla perdido"""



            if evento.type == pygame.KEYDOWN:
                key = evento.dict["key"]
                print(key)


                if evento.key == 276:#izquierda
                    player.movimientoIzquierda()
                    player.update("left")

                    player.direct = False


                if evento.key == 275:#derecha
                    player.movimientoDerecha()
                    player.update('right')


                    player.direct = True
                if evento.key == 273:
                    player.salto = True
                    if player.contadorfun == 0:
                        player.rect.y -= 250
                        player.contadorfun += 1

                        """ jugador dispara"""

                elif evento.key == 32:
                    x,y=player.rect.center
                    player.disparar(x,y)
                elif evento.key == 13:
                    imagenFondo = pygame.image.load("fondo.png").convert_alpha()
                    imagenFondo = pygame.transform.scale(imagenFondo, (ancho, alto))
                    ventana.blit(imagenFondo,(0,0))
                    enJuego = True
                    habilitador = True
                elif evento.key == 105:
                    imagenFondo = pygame.image.load("INSTRUCCIONES.png").convert_alpha()
                    imagenFondo = pygame.transform.scale(imagenFondo, (ancho, alto))
                    ventana.blit(imagenFondo,(0,0))
                    enJuego = False
                    habilitador = True
                elif evento.key ==101:
                    habilitador = False



            if evento.type ==pygame.KEYUP:
                if evento.key == 273:
                    player.contadorfun -= 1
                    player.rect.y += 250
                elif evento.key == 13:
                    imagenFondo = pygame.image.load("fondo.png").convert_alpha()
                    imagenFondo = pygame.transform.scale(imagenFondo, (ancho, alto))
                    ventana.blit(imagenFondo,(0,0))
                    enJuego = True
                    habilitador = True

        if  habilitador == False:
            imagenFondo = pygame.image.load("PRINCIPAL.png").convert_alpha()
            imagenFondo = pygame.transform.scale(imagenFondo, (ancho, alto))
            ventana.blit(imagenFondo, (0,0))
            enJuego = False

        """creando las colisiones """
        """ pinta el jugador en la ventana y la dibuja """
        if habilitador == True:
            if enJuego == False:
                imagenFondo = pygame.image.load("INSTRUCCIONES.png").convert_alpha()
                imagenFondo = pygame.transform.scale(imagenFondo, (ancho, alto))
                ventana.blit(imagenFondo,(0,0))
                if lalo == False:
                    imagenFondo = pygame.image.load("GAMEOVER.png").convert_alpha()
                    imagenFondo = pygame.transform.scale(imagenFondo, (ancho, alto))
                    ventana.blit(imagenFondo,(0,0))

            if enJuego == True:
                imagenFondo = pygame.image.load("fondo.png").convert_alpha()
                imagenFondo = pygame.transform.scale(imagenFondo, (ancho, alto))
                ventana.blit(imagenFondo,(0,0))
                if player.direct == True:
                    player.dibujar(ventana)
                elif player.direct == False:
                    player.rdibujar(ventana)


                if len(listaDeDisparo) >0:
                    for l in listaDeDisparo:
                        l.dibujar(ventana)
                        l.trayectoria()
                    if l.rect.top < -10:
                        listaDeDisparo.remove(l) #si el proyectil salio de nuesra visa entonces
                        #lo eliminamos

                    else:
                        #colision
                        for enemigo  in listaEnemigo:
                            for m in listaDeDisparo:
                                if m.rect.colliderect(enemigo.rect):
                                    listaEnemigo.remove(enemigo)
                                    
                                    listaDeDisparo.remove(m)

                                    if len(listaEnemigo) == 0:
                                        CargarEnemigos()
                                    if enemigo.rect.left > 460 :
                                        del m



                if len(listaEnemigo) > 0:

                    for enemigo in listaEnemigo:#coge cada enemigo
                        
                        if enemigo.rect.top > 500 or enemigo.rect.top < 300:
                             enemigo.rect.top = random.randrange(50, 500)

                        enemigo.rect.left -= 5#se mueve a la izquierda

                        if enemigo.rect.left == 0:#los limites
                            enemigo.rect.left = 1000
                            enemigo.rect.top += random.randrange(-300 ,300)

                        enemigo.dibujar(ventana)

                        if enemigo.rect.colliderect(player.rect):
                            enJuego = False

                        if len(enemigo.listaDeDisparos) >0:
                            for x in enemigo.listaDeDisparos:
                                x.dibujar(ventana)
                                x.trayectoria()
                            if x.rect.colliderect(player.rect):
                                enJuego = False
                            if x.rect.top > 900:
                                enemigo.listaDeDisparos.remove(x)#si el proyectil salio de nuesra visa entonces
                            #lo eliminamos
                            else:
                                for disparo in listaDeDisparo:
                                    if x.rect.colliderect(disparo.rect):
                                        listaDeDisparo.remove(disparo)
                                        listaDeDisparos.remove(x)
                        if enemigo.rect.colliderect(player.rect):
                            lalo = False
                        if lalo == False:
                            imagenFondo = pygame.image.load("GAMEOVER.png").convert_alpha()
                            imagenFondo = pygame.transform.scale(imagenFondo, (ancho, alto))
                            ventana.blit(imagenFondo,(0,0))





















        pygame.display.update()

goldTraver()
