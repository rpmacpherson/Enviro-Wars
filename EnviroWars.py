import pygame
from pygame.locals import *
from gameobject import GameObject, Food,AnimalGroup,PlantGroup
from sys import exit
#Initialization#################################################################
SCREEN_WIDTH=640
SCREEN_HEIGHT=640
screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),0,32)
creature = GameObject(screen,"/Users/clayallsopp/Desktop/Projects/Python/Pygame/Enviro-Wars/images/Rabbit.jpg")
grass = Food(screen,"/Users/clayallsopp/Desktop/Projects/Python/Pygame/Enviro-Wars/images/Grass.jpg")
grass.x = 5
grass.y = 5
animals=AnimalGroup(creature)
plants=PlantGroup(grass)

pygame.init()
linex=40
liney=40

#Main Loop######################################################################
while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            exit()
        elif event.type==KEYDOWN:
            if event.key==K_a:
                if creature.x>0:
                    creature.moveLeft()
            elif event.key==K_d:
                if creature.x<15:
                    creature.moveRight()
            elif event.key==K_w:
                if creature.y>0:
                    creature.moveUp()
            elif event.key==K_s:
                if creature.y<11:
                    creature.moveDown()
        elif event.type==MOUSEBUTTONDOWN: 
            if event.button==1:
                if event.pos[1]<=480:
                    print event.pos
                    creature.x=event.pos[0]/40
                    print creature.x
                    creature.y=event.pos[1]/40
                    print creature.y
    screen.fill((255,255,255))
    for x in xrange(16):
        pygame.draw.line(screen,(0,0,0),(linex,0),(linex,480))
        linex+=40
    linex=40
    for x in xrange(12):
        pygame.draw.line(screen,(0,0,0),(0,liney),(SCREEN_WIDTH,liney))
        liney+=40
    liney=40
    for plant in plants:
        plant.logic()
        plant.blitObject()
    for animal in animals:
        creature.logic()
        creature.blitObject()
    pygame.display.update()
                         
        
            
