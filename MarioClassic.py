#ADD: POW! Block, Fireball Behavior, Solid Pipes! Bonus Level, High Scores, Animations!
#ORGANIZE!
#FIX TURTLE IMAGE TRANSITIONS
import pygame
from pygame.locals import *
from pygame.sprite import *
from sys import exit
from random import randint
###############################VECTOR MATH######################################
class Vector(object):
    def __init__(self,x=0.0,y=0.0):
        self.x=x
        self.y=y
    def __str__(self):
        return "(%s,%s)"%(self.x,self.y)
    @staticmethod
    def from_points(p1,p2):
        return Vector(p2[0]-p1[0],p2[1]-p1[1])
    def get_magnitude(self):
        return math.sqrt(self.x**2+self.y**2)
    def __mul__(self,scalar):
        return Vector(self.x*scalar,self.y*scalar)
##########################OBJECT GROUPS#########################################
class Alive(Group):
    def __init__(self,player):
        Group.__init__(self,player)
class Obstacle(Group):
    def __init__(self):
        Group.__init__(self)
class Enemy(Group):
    def __init__(self):
        Group.__init__(self)
class Pipe(Group):
    def __init__(self):
        Group.__init__(self)
class CoinGroup(Group):
    def __init__(self):
        Group.__init__(self)
class FireballGroup(Group):
    def __init__(self):
        Group.__init__(self)
##########################GAME OBJECTS##########################################
class gameObject(Sprite):
    def __init__(self,screen,image_file):
        Sprite.__init__(self) 
        self.screen=screen
        self.x=175
        self.y=300
        self.image=image_file
        self.image_w,self.image_h=self.image.get_size()
        self.rect=pygame.Rect(self.x,self.y,self.image_w,self.image_h)
    def blitObject(self):
        screen.blit(self.image,(self.x,self.y))
    def changePos(self,x,y):
        self.x=x
        self.y=y
        self.rect=pygame.Rect(self.x,self.y,self.image_w,self.image_h)
class Brick(gameObject):
    def __init__(self,screen,image_file):
        gameObject.__init__(self,screen,image_file)
        self.move_y=0
        self.hitframe=0
        self.hit=0
        self.rect=pygame.Rect(self.x,self.y,self.image_w,self.image_h)
    def logic(self,time_passed):
        if self.hit==1:
            self.hitframe+=1
            if self.hitframe<9:
                self.y-=1
            else:
                self.y+=1
            if self.hitframe==16:
                self.hit=0
                self.hitframe=0
            for sprite in spritecollide(self,enemies,0):
                sprite.hit()
            for coin in spritecollide(self,coins,1):
                mario.score+=800
        for sprite in spritecollide(self,living,0):
            if self.rect.collidepoint(sprite.x+(sprite.image_w/2),sprite.rect.top) or self.rect.collidepoint(sprite.x+sprite.image_w,sprite.rect.top) or self.rect.collidepoint(sprite.x,sprite.rect.top):
                self.hit=1
class PowBlock(gameObject):##################################################
    def __init__(self,screen,image_file):
        gameObject.__init__(self,screen,image_file[0])
        self.move_y=0
        self.hit=0
        self.hitcount=0
        self.hitframe=0
        self.imagelist=image_file
        self.currentimage=self.imagelist[0]
        self.rect=pygame.Rect(self.x,self.y,self.image_w,self.image_h)
    def blitObject(self):
        screen.blit(self.currentimage,(self.x,self.y))
    def logic(self,time_passed):
        if self.hit==1:
            self.hitframe+=1
            if self.hitframe<9:
                self.y-=1
            else:
                self.y+=1
            if self.hitframe==16:
                self.hit=0
                self.hitframe=0
            self.rect=pygame.Rect(self.x,self.y,self.image_w,self.image_h)
        for sprite in spritecollide(self,living,0):
            if self.rect.collidepoint(sprite.x+(sprite.image_w/2),sprite.rect.top) or self.rect.collidepoint(sprite.x+sprite.image_w,sprite.rect.top) or self.rect.collidepoint(sprite.x,sprite.rect.top):
                for enemy in enemies:
                    enemy.hit()
                self.hit=1
                self.hitcount+=1
                if self.hitcount==3:
                    self.kill()
                else:
                    self.currentimage=self.imagelist[self.hitcount]
class Platform(gameObject):
    def __init__(self,screen,image_file):
        gameObject.__init__(self,screen,image_file)
        self.x=200
        self.y=50
        self.rect=pygame.Rect(self.x,self.y,self.image_w,self.image_h)
    def logic(self,time_passed):
        if mario.y>50:
            self.kill()           
class Coin(gameObject):
    def __init__(self,screen,image_file):
        gameObject.__init__(self,screen,image_file)
        self.move_x=.1
        self.move_y=0
        self.fallframe=0
        self.fall=1
        self.rect=pygame.Rect(self.x,self.y,self.image_w,self.image_h)
    def collDetect(self):
        for sprite in spritecollide(self,obstacles,0):
            #print "collision!"
            if self.rect.collidepoint(sprite.rect.left,sprite.y+(sprite.image_h/2)):
                #print "left side!"
                self.x=sprite.rect.left-self.image_w
                if self.fall==0:
                    self.move_x=-.1
            if self.rect.collidepoint(sprite.rect.right,sprite.y+(sprite.image_h/2)):
                #print "right side!"
                self.x=sprite.rect.right
                if self.fall==0:
                    self.move_x=.1
            if self.rect.collidepoint(sprite.x+(sprite.image_w/2),sprite.rect.top) or self.rect.collidepoint(sprite.x+sprite.image_w,sprite.rect.top) or self.rect.collidepoint(sprite.x,sprite.rect.top):
                #print "top!"
                self.y=sprite.rect.top-self.image_h
                self.move_y=0
                self.fallframe=0
                self.fall=0
            if self.rect.collidepoint(sprite.x+(sprite.image_w/2),sprite.rect.bottom):
                #print "bottom!"
                self.y=sprite.rect.bottom
                self.move_y=0
                self.fallframe=0
        for sprite in spritecollide(self,pipes,0):
            if self.rect.collidepoint(sprite.x+(sprite.image_w/2),sprite.y+(sprite.image_h/2)):
                self.kill()
        self.rect=pygame.Rect(self.x,self.y,self.image_w,self.image_h)
        if self.x<0:
            self.x=SCREEN_WIDTH-self.image_w
        elif self.x>SCREEN_WIDTH-self.image_w:
            self.x=0
        if self.y<0:
            self.y=0
        elif self.y>SCREEN_HEIGHT-38:
            self.y=SCREEN_HEIGHT-38
    def logic(self,time_passed):
        if self.fallframe<8:
            self.fallframe+=1
        self.fall=1
        self.move_y=.03*self.fallframe
        self.x+=self.move_x*time_passed
        self.y+=self.move_y*time_passed
        self.collDetect()
class Fireball(gameObject):
    def __init__(self,screen,image_file):
        gameObject.__init__(self,screen,image_file)
        self.move_x=.1
        self.move_y=.1
        self.fallframe=0
        self.rect=pygame.Rect(self.x,self.y,self.image_w,self.image_h)
    def collDetect(self):
        for sprite in spritecollide(self,obstacles,0):
            #print "collision!"
            if self.rect.collidepoint(sprite.rect.left,sprite.y+(sprite.image_h/2)):
                #print "left side!"
                self.x=sprite.rect.left-self.image_w
                if self.fall==0:
                    self.move_x=-.1
            if self.rect.collidepoint(sprite.rect.right,sprite.y+(sprite.image_h/2)):
                #print "right side!"
                self.x=sprite.rect.right
                if self.fall==0:
                    self.move_x=.1
            if self.rect.collidepoint(sprite.x+(sprite.image_w/2),sprite.rect.top):
                #print "top!"
                self.y=sprite.rect.top-self.image_h
                self.move_y*=-1
                self.fallframe=0
                self.fall=0
            if self.rect.collidepoint(sprite.x+(sprite.image_w/2),sprite.rect.bottom):
                #print "bottom!"
                self.y=sprite.rect.bottom
                self.move_y*=-1
                self.move_y=0
                self.fallframe=0
            self.rect=pygame.Rect(self.x,self.y,self.image_w,self.image_h)
        for sprite in spritecollide(self,living,1):
            self.kill()
            sprite.lives-=1
            sprite.changePos(200,1)
            obstacles.add(platform)
            if sprite.lives<0:
                sprite.kill()
        if self.x<0:
            self.move_x*=-1
        elif self.x>SCREEN_WIDTH-self.image_w:
            self.move_x*=-1
        if self.y<0:
            self.move_y*=-1
        elif self.y>SCREEN_HEIGHT- self.image_h:
            self.move_y*=-1
    def logic(self,time_passed):
        self.x+=self.move_x*time_passed
        self.y+=self.move_y*time_passed
        self.rect=pygame.Rect(self.x,self.y,self.image_w,self.image_h)
        #if screen.get_at((x+move_x,y+move_y))==(0,0,0):
        self.collDetect()    
class NPC(gameObject):
    def __init__(self,screen,image_file):
        gameObject.__init__(self,screen,image_file[0])
        self.move_x=.1
        self.move_y=0
        self.fallframe=0
        self.fall=1
        self.direction=1
        self.flip=False
        self.flipcount=0
        self.fliptime=0
        self.rect=pygame.Rect(self.x,self.y,self.image_w,self.image_h)
        self.imagelist=image_file ####MOVE TO GAMEOBJECT WHEN IMPLEMENTING FOR ALL SPRITES
        self.currentimage=self.imagelist[0]
    def blitObject(self): #########OVERWRITTEN TO TEST ANIMATIONS!!!!!!!
        screen.blit(self.currentimage,(self.x,self.y))
    def collDetect(self):
        selfGroup=GroupSingle()
        selfGroup.add(self)
        enemies.remove(self)
        for sprite in spritecollide(self,enemies,0):
            if (self.move_x>0 and sprite.move_x<0) or (self.move_x<0 and sprite.move_x>0):
                self.move_x*=-1
                self.currentimage=pygame.transform.flip(self.currentimage,True,False)
                sprite.move_x*=-1
                sprite.currentimage=pygame.transform.flip(sprite.currentimage,True,False)
            if self.rect.collidepoint(sprite.rect.left,sprite.y+(sprite.image_h/2)):
                #print "left side!"
                self.x=sprite.rect.left-self.image_w
                if self.fall==0:
                    self.move_x*=-1
                    self.image=pygame.transform.flip(self.image,True,False)
            if self.rect.collidepoint(sprite.rect.right,sprite.y+(sprite.image_h/2)):
                #print "right side!"
                self.x=sprite.rect.right
                if self.fall==0:
                    self.move_x*=-1
                    self.image=pygame.transform.flip(self.image,True,False)
            self.rect=pygame.Rect(self.x,self.y,self.image_w,self.image_h)
        enemies.add(self)
        selfGroup.empty()
        for sprite in spritecollide(self,pipes,0):
            if self.rect.collidepoint(sprite.x+(sprite.image_w/2),sprite.y+(sprite.image_h/2)):
                if sprite.x+sprite.image_w==SCREEN_WIDTH:
                    xpos=150
                else:
                    xpos=SCREEN_WIDTH-self.image_w-150
                self.changePos(xpos,(SCREEN_HEIGHT/4)-self.image_h-1)
        for sprite in spritecollide(self,obstacles,0):
            #print "collision!"
            if self.rect.collidepoint(sprite.rect.left,sprite.y+(sprite.image_h/2)):
                #print "left side!"
                self.x=sprite.rect.left-self.image_w
                if self.fall==0:
                    self.move_x=-.1
            if self.rect.collidepoint(sprite.rect.right,sprite.y+(sprite.image_h/2)):
                #print "right side!"
                self.x=sprite.rect.right
                if self.fall==0:
                    self.move_x=.1
            if self.rect.collidepoint(sprite.x+(sprite.image_w/2),sprite.rect.top):
                #print "top!"
                self.y=sprite.rect.top-self.image_h
                self.move_y=0
                self.fallframe=0
                self.fall=0
            if self.rect.collidepoint(sprite.x+(sprite.image_w/2),sprite.rect.bottom):
                #print "bottom!"
                self.y=sprite.rect.bottom
                self.move_y=0
                self.fallframe=0
            self.rect=pygame.Rect(self.x,self.y,self.image_w,self.image_h)
        if self.x<0:
            self.x=SCREEN_WIDTH-self.image_w
        elif self.x>SCREEN_WIDTH-self.image_w:
            self.x=0
        if self.y<0:
            self.y=0
        elif self.y>SCREEN_HEIGHT-self.image_h:
            self.y=SCREEN_HEIGHT-self.image_h
    def hit(self):
        self.flip=not self.flip
        self.currentimage=pygame.transform.flip(self.currentimage,True,True)
        self.y-=2
        self.rect=pygame.Rect(self.x,self.y,self.image_w,self.image_h)
    def logic(self,time_passed):
        if self.flip==True:
            self.flipcount+=1
            self.fliptime+=time_passed
            if self.flipcount<12:
                self.y-=2
                self.rect=pygame.Rect(self.x,self.y,self.image_w,self.image_h)
            elif self.flipcount<24:
                self.y+=2
                self.rect=pygame.Rect(self.x,self.y,self.image_w,self.image_h)
            if self.fliptime>=20000:
                self.flip=False
                self.flipcount=0
                self.fliptime=0
                direction=randint(0,1)
                if direction==1:
                    self.move_x=.15
                    self.currentimage=pygame.transform.flip(self.imagelist[1],True,False)
                else:
                    self.move_x=-.15
                    self.currentimage=self.imagelist[1]
            else:
                for sprite in spritecollide(self,living,0):
                    self.kill()
                    mario.killcount+=1
                    sprite.score+=800
                    temp=Coin(screen,coin_image)
                    side=randint(1,2)
                    if side==1:
                        xpos=150
                    else:
                        xpos=SCREEN_WIDTH-temp.image_w-150
                        temp.move_x=-.1
                    temp.changePos(xpos,SCREEN_HEIGHT/4-temp.image_h-1)
                    coins.add(temp)
        else:
            if self.fallframe<8:
                self.fallframe+=1
            self.fall=1
            self.move_y=.03*self.fallframe*time_passed
            self.x+=self.move_x*time_passed
            self.y+=self.move_y
            self.rect=pygame.Rect(self.x,self.y,self.image_w,self.image_h)
            #if screen.get_at((x+move_x,y+move_y))==(0,0,0):
            self.collDetect()
class Crab(NPC):
    def __init__(self,screen,image_file):
        NPC.__init__(self,screen,image_file)
        self.angry=0
        self.angrycount=0
        self.imagelist=image_file ####MOVE TO GAMEOBJECT WHEN IMPLEMENTING FOR ALL SPRITES
        self.currentimage=self.imagelist[0]
    def blitObject(self): #########OVERWRITTEN TO TEST ANIMATIONS!!!!!!!
        screen.blit(self.currentimage,(self.x,self.y))
    def hit(self):
        if self.angry==0:
            print 'Angry!'
            self.angry=1
            self.move_x*=2
            self.currentimage=self.imagelist[1]
        else:
            self.flip=not self.flip
            self.currentimage=pygame.transform.flip(self.currentimage,True,True)
        self.y-=2
        self.rect=pygame.Rect(self.x,self.y,self.image_w,self.image_h)
    def logic(self,time_passed):
        if self.flip==True:
            self.flipcount+=1
            self.fliptime+=time_passed
            if self.flipcount<12:
                self.y-=2
                self.rect=pygame.Rect(self.x,self.y,self.image_w,self.image_h)
            elif self.flipcount<24:
                self.y+=2
                self.rect=pygame.Rect(self.x,self.y,self.image_w,self.image_h)
            if self.fliptime>=20000:
                self.flip=False
                self.flipcount=0
                self.fliptime=0
                direction=randint(0,1)
                if direction==1:
                    self.move_x=.15
                    if self.angry==0:
                        self.currentimage=self.imagelist[2]
                    else:
                        self.currentimage=self.imagelist[3]
                else:
                    self.move_x=-.15
                    if self.angry==0:
                        self.currentimage=pygame.transform.flip(self.imagelist[2],True,False)
                    else:
                        self.currentimage=pygame.transform.flip(self.imagelist[3],True,False)
            else:
                for sprite in spritecollide(self,living,0):
                    self.kill()
                    mario.killcount+=1
                    sprite.score+=800
                    temp=Coin(screen,coin_image)
                    side=randint(1,2)
                    if side==1:
                        xpos=150
                    else:
                        xpos=SCREEN_WIDTH-temp.image_w-150
                        temp.move_x=-.1
                    temp.changePos(xpos,SCREEN_HEIGHT/4-temp.image_h-1)
                    coins.add(temp)
        elif self.angry==1 and self.angrycount<24:
            self.angrycount+=1
            if self.angrycount<12:
                self.y-=2
                self.rect=pygame.Rect(self.x,self.y,self.image_w,self.image_h)
            elif self.angrycount<24:
                self.y+=2
                self.rect=pygame.Rect(self.x,self.y,self.image_w,self.image_h)
        else:
            if self.fallframe<8:
                self.fallframe+=1
            self.fall=1
            self.move_y=.03*self.fallframe*time_passed
            self.x+=self.move_x*time_passed
            self.y+=self.move_y
            self.rect=pygame.Rect(self.x,self.y,self.image_w,self.image_h)
            #if screen.get_at((x+move_x,y+move_y))==(0,0,0):
            self.collDetect()
class Fly(NPC):
    def __init__(self,screen,image_file):
        NPC.__init__(self,screen,image_file)
        self.hopframe=0
    def hit(self):
        print "Hit!"
        self.flip=not self.flip
        self.image=pygame.transform.flip(self.image,True,True)
        self.y-=2
        self.rect=pygame.Rect(self.x,self.y,self.image_w,self.image_h)
    def collDetect(self):
        selfGroup=GroupSingle()
        selfGroup.add(self)
        enemies.remove(self)
        for sprite in spritecollide(self,enemies,0):
            if (self.move_x>0 and sprite.move_x<0) or (self.move_x<0 and sprite.move_x>0):
                self.move_x*=-1
                sprite.move_x*=-1
            if self.rect.collidepoint(sprite.rect.left,sprite.y+(sprite.image_h/2)):
                #print "left side!"
                self.x=sprite.rect.left-self.image_w
                if self.fall==0:
                    self.move_x=-.1
            if self.rect.collidepoint(sprite.rect.right,sprite.y+(sprite.image_h/2)):
                #print "right side!"
                self.x=sprite.rect.right
                if self.fall==0:
                    self.move_x=.1
            self.rect=pygame.Rect(self.x,self.y,self.image_w,self.image_h)
        enemies.add(self)
        selfGroup.empty()
        for sprite in spritecollide(self,pipes,0):
            if self.rect.collidepoint(sprite.x+(sprite.image_w/2),sprite.y+(sprite.image_h/2)):
                if sprite.x+sprite.image_w==SCREEN_WIDTH:
                    xpos=150
                else:
                    xpos=SCREEN_WIDTH-self.image_w-150
                self.changePos(xpos,(SCREEN_HEIGHT/4)-self.image_h-1)
        for sprite in spritecollide(self,obstacles,0):
            #print "collision!"
            if self.rect.collidepoint(sprite.rect.left,sprite.y+(sprite.image_h/2)):
                #print "left side!"
                self.x=sprite.rect.left-self.image_w
                if self.fall==0:
                    self.move_x=-.1
            if self.rect.collidepoint(sprite.rect.right,sprite.y+(sprite.image_h/2)):
                #print "right side!"
                self.x=sprite.rect.right
                if self.fall==0:
                    self.move_x=.1
            if self.rect.collidepoint(sprite.x+(sprite.image_w/2),sprite.rect.top):
                #print "top!"
                self.y=sprite.rect.top-self.image_h
                self.move_y=0
                if self.hopframe>40:
                    self.hopframe=0
                self.fallframe=0
                self.fall=0
            if self.rect.collidepoint(sprite.x+(sprite.image_w/2),sprite.rect.bottom):
                #print "bottom!"
                self.y=sprite.rect.bottom
                self.move_y=0
                self.fallframe=0
            if sprite.hit==1:
                self.hit()
            self.rect=pygame.Rect(self.x,self.y,self.image_w,self.image_h)
        if self.x<0:
            self.x=SCREEN_WIDTH-self.image_w
        elif self.x>SCREEN_WIDTH-self.image_w:
            self.x=0
        if self.y<0:
            self.y=0
        elif self.y>SCREEN_HEIGHT- self.image_h:
            self.y=SCREEN_HEIGHT- self.image_h
    def logic(self,time_passed):
        if self.flip==True:
            self.flipcount+=1
            self.fliptime+=time_passed
            if self.flipcount<12:
                self.y-=2
                self.rect=pygame.Rect(self.x,self.y,self.image_w,self.image_h)
            elif self.flipcount<24:
                self.y+=2
                self.rect=pygame.Rect(self.x,self.y,self.image_w,self.image_h)
            if self.fliptime>=20000:
                self.flip=False
                self.flipcount=0
                self.fliptime=0
                self.image=pygame.transform.flip(self.image,True,True)
                direction=randint(0,1)
                if direction==1:
                    self.move_x=.15
                else:
                    self.move_x=-.15
            else:
                for sprite in spritecollide(self,living,0):
                    self.kill()
                    mario.killcount+=1
                    sprite.score+=800
                    temp=Coin(screen,coin_image)
                    side=randint(1,2)
                    if side==1:
                        xpos=150
                    else:
                        xpos=SCREEN_WIDTH-temp.image_w-150
                        temp.move_x=-.1
                    temp.changePos(xpos,SCREEN_HEIGHT/4-temp.image_h-1)
                    coins.add(temp)
        else:
            if self.fallframe<8:
                self.fallframe+=1
            self.hopframe+=1
            self.fall=1
            if self.hopframe>40 and self.hopframe<50:
                self.y-=.05*(self.hopframe-40)*time_passed
                self.x+=self.move_x*time_passed*3+2
            else:
                self.move_y=.03*self.fallframe*time_passed
                self.y+=self.move_y
            self.rect=pygame.Rect(self.x,self.y,self.image_w,self.image_h)
            #if screen.get_at((x+move_x,y+move_y))==(0,0,0):
            self.collDetect()
class Player(gameObject):
    def __init__(self,screen,image_file):
        gameObject.__init__(self,screen,image_file[0])
        self.x=200
        self.y=30
        self.imagelist=image_file ####MOVE TO GAMEOBJECT WHEN IMPLEMENTING FOR ALL SPRITES
        self.currentimage=self.imagelist[0]
        self.move_x=0
        self.move_y=0
        self.direction=1
        self.jump=0      
        self.jumpframe=0
        self.fallframe=0
        self.fall=1
        self.score=0
        self.killcount=0
        self.lives=3
        self.rect=pygame.Rect(self.x,self.y,self.image_w,self.image_h)
    def blitObject(self): #########OVERWRITTEN TO TEST ANIMATIONS!!!!!!!
        screen.blit(self.currentimage,(self.x,self.y))
    def collDetect(self):
        if self.x<0:
            self.x=SCREEN_WIDTH-45
        elif self.x>SCREEN_WIDTH-45:
            self.x=0
        if self.y<0:
            self.y=0
            self.move_y=0
            self.jump=0
            self.jumpframe=0
            self.fallframe=0
        elif self.y>SCREEN_HEIGHT- self.image_h:
            self.y=SCREEN_HEIGHT- self.image_h
        self.rect=pygame.Rect(self.x,self.y,self.image_w,self.image_h)
        #if screen.get_at((x+move_x,y+move_y))==(0,0,0):
        for sprite in spritecollide(self,obstacles,0):
            #print "collision!"
            if self.rect.collidepoint(sprite.rect.left,sprite.y+(sprite.image_h/2)):
                #print "left side!"
                self.x=sprite.rect.left-self.image_w
            if self.rect.collidepoint(sprite.rect.right,sprite.y+(sprite.image_h/2)):
                #print "right side!"
                self.x=sprite.rect.right
            if self.rect.collidepoint(sprite.x+(sprite.image_w/2),sprite.rect.top) or self.rect.collidepoint(sprite.x+sprite.image_w,sprite.rect.top) or self.rect.collidepoint(sprite.x,sprite.rect.top):
                #print "top!"
                self.y=sprite.rect.top-self.image_h
                self.move_y=0
                if self.fallframe>1:
                    if self.direction==1:
                        self.currentimage=self.imagelist[0]
                    else:
                        self.currentimage=pygame.transform.flip(self.imagelist[0],True,False)
                self.fallframe=0
                jumpframe=0
                self.fall=0
            if self.rect.collidepoint(sprite.x+(sprite.image_w/2),sprite.rect.bottom) or self.rect.collidepoint(sprite.x+(sprite.image_w),sprite.rect.bottom) or self.rect.collidepoint(sprite.x,sprite.rect.bottom):
                #print "bottom!"
                self.y=sprite.rect.bottom
                self.move_y=0
                self.jump=0
                self.jumpframe=0
                self.fallframe=0
        for sprite in spritecollide(self,pipes,0):
            #print "collision!"
            if self.rect.collidepoint(sprite.rect.left,sprite.y+(sprite.image_h/2)):
                #print "left side!"
                self.x=sprite.rect.left-self.image_w
            if self.rect.collidepoint(sprite.rect.right,sprite.y+(sprite.image_h/2)):
                #print "right side!"
                self.x=sprite.rect.right
        for sprite in spritecollide(self,enemies,0):
            if sprite.flip==False:
                self.lives-=1
                self.changePos(200,1)
                obstacles.add(platform)
                if self.lives==-1:
                    self.kill()
        for coin in spritecollide(self,coins,1):
            self.score+=800
    def control(self,time_passed):
        for event in pygame.event.get():
            if event.type==QUIT:
                exit()
            elif event.type==KEYDOWN:
                if event.key==K_a:
                    self.move_x=-.15*time_passed
                    if self.direction==1:
                        self.direction=0
                        self.currentimage=pygame.transform.flip(self.currentimage,True,False)
                elif event.key==K_d:
                    self.move_x=.15*time_passed
                    if self.direction==0:
                        self.direction=1
                        self.currentimage=pygame.transform.flip(self.currentimage,True,False)
                elif event.key==K_w: 
                    if self.fall==0:
                        self.jump=1
                        if self.direction==1:
                            self.currentimage=self.imagelist[1]
                        else:
                            self.currentimage=pygame.transform.flip(self.imagelist[1],True,False)
                elif event.key==K_q:
                    self.kill()
            elif event.type==KEYUP:
                if event.key==K_w or event.key==K_s:
                    self.move_y=0
                elif event.key==K_a or event.key==K_d:
                    self.move_x=0
                elif event.key==K_w:
                    self.jump=0
                    self.jumpframe=0
    def logic(self,time_passed):
        self.control(time_passed)
        if self.fallframe<8:
            self.fallframe+=1
        self.fall=1
        self.move_y=.03*self.fallframe*time_passed
        if self.jump==1:
            if self.jumpframe<21:
                self.jumpframe+=1
                self.move_y=-.04*self.jumpframe*time_passed
            else:
                self.jump=0
                self.jumpframe=0
        self.x+=self.move_x
        self.y+=self.move_y
        self.collDetect()
###############################INITIALIZATION###################################
SCREEN_WIDTH=850
SCREEN_HEIGHT=600
pygame.init()
font=pygame.font.SysFont("Courier New",16)
font_height=font.get_linesize()
screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),0,32)
character=[pygame.image.load("E:\Python\Graphics\Mario.png").convert_alpha(),pygame.image.load("E:\Python\Graphics\Mariojump.png").convert_alpha()]
turtle_image=[pygame.image.load("E:\Python\Graphics\Turtle.png").convert_alpha(),pygame.image.load("E:\Python\Graphics\Turtleblue.png").convert_alpha()]
brick_image=pygame.image.load("E:\Python\Graphics\Brick.jpg").convert_alpha()
platform_image=pygame.image.load("E:\Python\Graphics\Brick2.jpg").convert_alpha()
block_image=[pygame.image.load("E:\Python\Graphics\Powblock.png").convert_alpha(),pygame.image.load("E:\Python\Graphics\Powblock2.png").convert_alpha(),pygame.image.load("E:\Python\Graphics\Powblock3.png").convert_alpha()]
crab_image=[pygame.image.load("E:\Python\Graphics\Crab.png").convert_alpha(),pygame.image.load("E:\Python\Graphics\Crabangry.png").convert_alpha(),pygame.image.load("E:\Python\Graphics\Crabblue.png").convert_alpha(),pygame.image.load("E:\Python\Graphics\Crabblueangry.png").convert_alpha()]
pipe_image=pygame.image.load("E:\Python\Graphics\Pipes.png").convert_alpha()
coin_image=pygame.image.load("E:\Python\Graphics\Coin.png").convert_alpha()
fly_image=pygame.image.load("E:\Python\Graphics\Fighterfly.png").convert_alpha()
fire_image=pygame.image.load("E:\Python\Graphics\Fireball.png").convert_alpha()
clock=pygame.time.Clock()
mario=Player(screen,character)
platform=Platform(screen,platform_image)
pipe1=gameObject(screen,pipe_image)
pipe1.changePos(0,SCREEN_HEIGHT-55-pipe1.image_h)
pipe1.image=pygame.transform.flip(pipe1.image,True,False)
pipe2=gameObject(screen,pipe_image)
pipe2.changePos(SCREEN_WIDTH-pipe2.image_w,SCREEN_HEIGHT-55-pipe2.image_h)
pipe3=gameObject(screen,pipe_image)
pipe3.changePos(0,pipe3.image_h*1.4)
pipe3.image=pygame.transform.flip(pipe3.image,True,False)
pipe4=gameObject(screen,pipe_image)
pipe4.changePos(SCREEN_WIDTH-pipe2.image_w,pipe4.image_h*1.4)
tempx=0
tempy=SCREEN_HEIGHT-54.
obstacles=Obstacle()
enemies=Enemy()
fireballs=FireballGroup()
pipes=Pipe()
pipes.add(pipe1,pipe2,pipe3,pipe4)
level=1
for x in xrange(20):
    temp=Brick(screen,brick_image)
    temp.changePos(tempx,tempy)
    tempx+=temp.image_w
    obstacles.add(temp)
tempx,tempy=0,SCREEN_HEIGHT/1.75
for x in xrange(6):
    temp=Brick(screen,brick_image)
    temp.changePos(tempx,tempy)
    tempx+=temp.image_w
    obstacles.add(temp)
tempx,tempy=SCREEN_WIDTH-temp.image_w,SCREEN_HEIGHT/1.75
for x in xrange(6):
    temp=Brick(screen,brick_image)
    temp.changePos(tempx,tempy)
    tempx-=temp.image_w
    obstacles.add(temp)
tempx,tempy=0,SCREEN_HEIGHT/4
for x in xrange(6):
    temp=Brick(screen,brick_image)
    temp.changePos(tempx,tempy)
    tempx+=temp.image_w
    obstacles.add(temp)
tempx,tempy=SCREEN_WIDTH-temp.image_w,SCREEN_HEIGHT/4
for x in xrange(6):              
    temp=Brick(screen,brick_image)
    temp.changePos(tempx,tempy)
    tempx-=temp.image_w
    obstacles.add(temp)
tempx,tempy=SCREEN_WIDTH-(temp.image_w*10),SCREEN_HEIGHT/2.5
for x in xrange(3):
    temp=Brick(screen,brick_image)
    temp.changePos(tempx,tempy)
    tempx+=temp.image_w
    obstacles.add(temp)
living=Alive(mario)
coins=CoinGroup()
powblock=PowBlock(screen,block_image)
powblock.changePos(425-powblock.image_w,SCREEN_HEIGHT-300)
obstacles.add(powblock)
spawntimer=0
spawncount=0
fireballmax=0
fireballtimer=0
##########################MAIN LOOP#############################################
while mario.alive():
    time_passed=clock.tick(30)
    enemymax=4*level
    fireballmax=40000*level
    fireballtimer+=time_passed
    if fireballtimer>fireballmax:
        fireballtimer=0
        temp=Fireball(screen,fire_image)
        fireballs.add(temp)
    if mario.killcount==enemymax:
        level+=1
        mario.killcount=0
        spawncount=0
        spawntimer=0
        fireballtimer=0
        fireballs.empty()
    if spawncount<enemymax:
        spawntimer+=1
        if spawntimer==200:
            if level==1:
                temp=NPC(screen,turtle_image)
            elif level==2:
                enemy=randint(1,2)
                if enemy==1:
                    temp=NPC(screen,turtle_image)
                else:
                    temp=Crab(screen,crab_image)
            else:
                enemy=randint(1,3)
                if enemy==1:
                    temp=NPC(screen,turtle_image)
                elif enemy==2:
                    temp=Crab(screen,crab_image)
                else:
                    temp=Fly(screen,fly_image)
            side=randint(1,2)
            if side==1:
                xpos=150
                temp.image=pygame.transform.flip(temp.image,True,False)
            else:
                xpos=SCREEN_WIDTH-temp.image_w-150
                temp.move_x=-.1
            temp.changePos(xpos,SCREEN_HEIGHT/4-temp.image_h-1)
            enemies.add(temp)
            spawntimer=0
            spawncount+=1
    screen.fill((0,0,0))
    for player in living:
        mario.logic(time_passed)
        player.blitObject()
    for obstacle in obstacles:
        obstacle.logic(time_passed)
        obstacle.blitObject()
    for coin in coins:
        coin.logic(time_passed)
        coin.blitObject()
    for enemy in enemies:
        enemy.logic(time_passed)
        enemy.blitObject()
    for pipe in pipes:
        pipe.blitObject()
    for fireball in fireballs:
        fireball.logic(time_passed)
        fireball.blitObject()
    screen.blit(font.render("Score:"+str(mario.score),True,(255,255,255)),(0,SCREEN_HEIGHT-50))
    screen.blit(font.render("Lives:"+str(mario.lives),True,(255,255,255)),(0,SCREEN_HEIGHT-34))
    screen.blit(font.render("Level:"+str(level),True,(255,255,255)),(0,SCREEN_HEIGHT-18))      
    pygame.display.update()
             
        
