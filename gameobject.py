import pygame
from pygame.locals import *
from pygame.sprite import *
 
class AnimalGroup(Group):   #Initializes each group.  Declaring a new class for each group isn't necessary, except to
    def __init__(self,animal): #have varying numbers of elements initialized in the constructor, which will be useful.
        Group.__init__(self,animal)
class PlantGroup(Group):
    def __init__(self,plant):
        Group.__init__(self,plant)
class ButtonGroup(Group):
    def __init__(self,button):
        Group.__init__(self,button) 
class GameObject(Sprite):
    def __init__(self,screen,image_file):
        Sprite.__init__(self) 
        self.screen=screen
        self.x=0
        self.y=0
        self.image=pygame.image.load(image_file).convert_alpha() # You just pass in a file location and it does the conversion here
        self.image_w,self.image_h=self.image.get_size()
        self.rect=pygame.Rect(self.x,self.y,self.image_w,self.image_h) # Not sure if this is necessary so I'll leaveit here
    def blitObject(self):
        self.screen.blit(self.image,(self.x*40,self.y*40))
    def moveUp(self):
        self.y -= 1
    def moveDown(self):
        self.y += 1
    def moveLeft(self):
        self.x -= 1
    def moveRight(self):
        self.x += 1
    # Not sure if this function is necessary so I'll leave it here
    def changePos(self,x,y):
        self.x=x
        self.y=y
        self.rect=pygame.Rect(self.x*40,self.y*40,self.image_w,self.image_h)
    def logic(self):
        pass
    
class Food(GameObject):
    def __init__(self, screen, image_file):
        GameObject.__init__(self,screen,image_file)
        self.growth_rate = 0 # Arbitrary constant
        self.health = 0 # Arbitrary constant
    def info(self):
        rep=[]
        rep.append("Plant")
        rep.append("Health:"+str(self.health))
        return(rep)
    def moveUp(self):
        pass
    def moveDown(self):
        pass
    def moveLeft(self):
        pass
    def moveRight(self):
        pass
    def logic(self):
        pass
 
class Creature(GameObject):
    def __init__(self, screen, image_file):
        GameObject.__init__(self,screen,image_file)
        # All of the creature-specific stuff goes here
        self.hunger = 0 # Arbitrary constant for right now
        self.speed = 0 # Arbirtary constant
        self.num_offpsring=0 # Arbitrary constant
        self.reproduction_rate=0 # Arbitrary constant
    def info(self):
        rep=[]
        rep.append("Animal")
        rep.append("Hunger:"+str(self.hunger))
        rep.append("Speed:"+str(self.speed))
        return rep
    # Every creature changes its position using a logic function? 
    # By default it should either do nothing or choose a random direction to move in (as to not repeat code in subclasses)    
    def logic(self):
        pass
        # Here's an idea of how this should work (can get more advanced, change priorities, etc)
        # Basically, the creature should check all 8 (or less if its on the border) adjacent squares. 
        # The first priority is food. If the creature can eat at an adjacent square, it should go to that square and eat.
            # There should be a function for the carnivores that's like "if rabbit.can_be_eaten_by(self)" (where self is the wolf object)
            # because of the speed/probability it runs away.
        # Second priority is if it can be eaten. If something that can eat it is in an adjacent square, it should move in the opposite direction, if possible.
        # If it can't eat or be eaten, it should pick a random direction and move.
        # The thing we haven't implemented is how we abstract all of this. Like a two dimensional array representing the map?
            # Like 1 means grass, 2 means rabbit, 3 means wolf or something. The creature looks at the array (passed as a variable
            # in the logic function) and decides what to do.
            # A possible alternative is to get the pixel in a certain direction at a certain and judge what it is by the pixel color.
            # But that doesn't seem as future-proof as the 2D solution. But it's up to you guys.
        
    # Defines how it should eat. Maybe we need to implement a can_eat or something for when it checks to move?
    def eat(self, other_creature):
        pass
 
class Button(GameObject):
    def __init__(self,screen,image_file):
        self.x=310
        self.y=540
        GameObject.__init__(self,screen,image_file)
        self.rect=pygame.Rect(self.x,self.y,40,40)
    def logic(self):
        print "Clicked!"
