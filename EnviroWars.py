import pygame
from pygame.locals import *
from sys import exit
#Initialization#################################################################
SCREEN_WIDTH=640
SCREEN_HEIGHT=640
screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),0,32)
SPRITE_IMAGE=pygame.image.load("F:\Python\Graphics\FighterFly.png").convert_alpha()
pygame.init()
linex=40
liney=40
spritex=0
spritey=0
#Main Loop######################################################################
while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            exit()
        elif event.type==KEYDOWN:
            if event.key==K_a:
                if spritex>0:
                    spritex-=1
            elif event.key==K_d:
                if spritex<15:
                    spritex+=1
            elif event.key==K_w:
                if spritey>0:
                    spritey-=1
            elif event.key==K_s:
                if spritey<11:
                    spritey+=1
        elif event.type==MOUSEBUTTONDOWN:
            if event.button==1:
                if event.pos[1]<=480:
                    print event.pos
                    spritex=event.pos[0]/40
                    print spritex
                    spritey=event.pos[1]/40
                    print spritey
    screen.fill((255,255,255))
    for x in xrange(16):
        pygame.draw.line(screen,(0,0,0),(linex,0),(linex,480))
        linex+=40
    linex=40
    for x in xrange(12):
        pygame.draw.line(screen,(0,0,0),(0,liney),(SCREEN_WIDTH,liney))
        liney+=40
    liney=40
    screen.blit(SPRITE_IMAGE,(spritex*40,spritey*40))
    pygame.display.update()
                         
        
            
