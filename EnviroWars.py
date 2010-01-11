import pygame
from pygame.locals import *
from gameobject import *
from sys import exit
#Initialization#################################################################
SCREEN_WIDTH=640
SCREEN_HEIGHT=640
screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),0,32)
creature = Creature(screen,"Rabbit.jpg")
grass = Food(screen,"Grass.jpg")
button=Button(screen,"Grass.jpg")
creature.x=9
grass.x = 5
grass.y = 5
animals=AnimalGroup(creature)
plants=PlantGroup(grass)
buttons=ButtonGroup(button)
selected=None

pygame.init()
font=pygame.font.SysFont("Courier New",16)
font_height=font.get_linesize()
linex=40
liney=40

def Search(searchx,searchy):
    print searchx,searchy
    for animal in animals:
        if animal.x==searchx and animal.y==searchy:
            print "found it!"
            return(animal)
    for plant in plants:
        if plant.x==searchx and plant.y==searchy:
            print "found it!"
            return(plant)
    return ("Nothing")
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
                if button.rect.collidepoint(event.pos):
                    button.logic()
                elif event.pos[1]<=480:
                   selected=Search(event.pos[0]/40,event.pos[1]/40)
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
        plant.logic(animals,plants)
        plant.blitObject()
    for animal in animals:
        creature.logic()
        creature.blitObject()
    for button in buttons:
        button.blitObject()
    linenum=50
    if selected!=None and selected!="Nothing":
        info=selected.info()
        for line in info:
            screen.blit(font.render(line,True,(0,0,0)),(0,SCREEN_HEIGHT-linenum))
            linenum-=18
    elif selected=="Nothing":
        screen.blit(font.render("Nothing Here",True,(0,0,0)),(0,SCREEN_HEIGHT-linenum))
    pygame.display.update()                        
        
            
