#ADD: POW! Block, Fireball Behavior, Solid Pipes! Bonus Level, High Scores, Animations!
#ORGANIZE!
#FIX TURTLE IMAGE TRANSITIONS
import pygame
from pygame.locals import *
from pygame.sprite import *
from sys import exit
from random import randint


##########################GAME OBJECTS##########################################

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
             
        
