#-----------------------------------------------------------------------------
# Name:        Chrome Dino (Chrome Dino.py)
# Purpose:     It a game to see how far you can go, last, and highest score without hitting an obstacle
#
# Author:      Dylan Bellamy
# Created:     22-Oct-2021
# Updated:     15-Nov-2021
#-----------------------------------------------------------------------------
#I think this project deserves a level 4+ because it covers the whole rubric and has buttons to swap from screens, a restart ability and has a moving background for added features. 
#
#Features Added:
#   Restart 
#   Moving Background (Clouds)
#   Buttons
#-----------------------------------------------------------------------------

import pygame
import random
import time


# Screen Setup
screenHeight = 600 # Screen Height
screenWidth = 1100 # Screen Width
screen = pygame.display.set_mode((screenWidth, screenHeight))  # Initializing screen for display
    
    
clock = pygame.time.Clock()  #Force frame rate to be slower

# Loading images from files into variables
RUNNING = [pygame.image.load(("images//DinoRun1.png")),
           pygame.image.load(("images//DinoRun2.png"))]
JUMPING = pygame.image.load(("images//DinoJump.png"))
DUCKING = [pygame.image.load(("images//DinoDuck1.png")),
           pygame.image.load(("images//DinoDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(("images//SmallCactus1.png")),
                pygame.image.load(("images//SmallCactus2.png")),
                pygame.image.load(("images//SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(("images//LargeCactus1.png")),
                pygame.image.load(("images//LargeCactus2.png")),
                pygame.image.load(("images//LargeCactus3.png"))]

BIRD = [pygame.image.load(("images//Bird1.png")),
        pygame.image.load(("images//Bird2.png"))]

CLOUD = pygame.image.load(("images//Cloud.png"))

BG = pygame.image.load(("images//Track.png"))

controlPanel = pygame.image.load(("images//ControlsPanel.png"))


# Setting Up Class Dinosaur
class dinosaur:
    xPos = 80                               # X positon of dinosaur
    yPos = 310                              # Y Position of dinosaur
    yPosDuck = 340                          # Y Positon of dinosaur in duck mode
    JUMP_VEL = 8.5                          # Jumping velocity of dinosaur, pixle per while loop iteration 
    userInput = pygame.key.get_pressed()    # Gets the state of all keyboard buttons

    # __init__ - Initializing attributes of class
    # self - Accesses the attritbutes of class
    def __init__(self):
        self.duck_img = DUCKING  
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False  # Doesn't use ducking images
        self.dino_run = True    # Uses running images
        self.dino_jump = False  # Doesn't use jumping images

        self.step_index = 0                    # step_index starts at 0 and used to help animate dinosuar
        self.jumpVel = self.JUMP_VEL           #
        self.image = self.run_img[0]           # Initializing first image of dinosaur
        self.dino_rect = self.image.get_rect() # Takes the rectangle of the dinosaur
        self.dino_rect.x = self.xPos           # Sets the x-cord of rectangle to the x-position
        self.dino_rect.y = self.yPos           # Sets the y-cord of rectangle to the y-position

    # Update Function
    def update(self, userInput):
        if self.dino_duck:       # If dinosaur is ducking, it calls duck function
            self.duck()
        if self.dino_run:        # If dinosaur is running, it calls run function
            self.run()
        if self.dino_jump:       # If dinosaur is jumping, it calls jump function
            self.jump()

        if self.step_index >= 10:  # If step_index is greater or equal to 10
            self.step_index = 0    # Then reset step_index's value to 0

        # If user pressed up key and dino is not jumping
        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False     
            self.dino_run = False
            self.dino_jump = True
            
        # If user pressed down key and dino is not ducking
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
            
        # If user hasn't pressed any up or down key
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    # duck function
    def duck(self):
        self.image = self.duck_img[self.step_index // 5] # Cycles through DUCKING list of images every 5 steps
        self.dino_rect = self.image.get_rect()           # Gets the rectangles area of surface
        self.dino_rect.x = self.xPos                     # Sets dinosaur rectangle x-cord to x-positon
        self.dino_rect.y = self.yPosDuck                 # Sets dinosaur rectangle y-cord to y-positon-duck
        self.step_index += 1                             # Adds one to or makes step_index equal to one 

    # run function
    def run(self):
        self.image = self.run_img[self.step_index // 5]  # Cycles through RUNNING list of images every 5 steps
        self.dino_rect = self.image.get_rect()           # Gets the rectangles area of surface
        self.dino_rect.x = self.xPos                     # Sets dinosaur rectangle x-cord to x-positon
        self.dino_rect.y = self.yPos                     # Sets dinosaur rectangle y-cord to y-positon
        self.step_index += 1                             # Adds one to or makes step_index equal to one 

    # jump function
    def jump(self):
        self.image = self.jump_img                       # Sets image of dinosaur to jump image
        if self.dino_jump:                               # If dinosaur is set to jumping
            self.dino_rect.y -= self.jumpVel * 4         # Decrease the y-position of the dinosaur
            self.jumpVel -= 0.8                          # Decrease the velocity of dinosaur jumping
        if self.jumpVel < - self.JUMP_VEL:               # If dinosaur jumping velocity is equal to -8.5
            self.dino_jump = False                       # Stop jump function 
            self.jumpVel = self.JUMP_VEL                 # Reset JUMP_VEL of dinosaur

    # Blits image on to screen
    def draw(self, screen):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
    
    # Initializing attributes of class
    def __init__(self):
        self.x = screenWidth + random.randint(800, 1000) # X-Cordinates of Cloud when created
        self.y = random.randint(50, 100)                 # Y-Cordinates of Cloud when created
        self.image = CLOUD                               # Sets image of class
        self.width = self.image.get_width()              # Gets and Sets width of image
        
    # Update Function
    def update(self):
        self.x -= gameSpeed                                   # Cloud x-cord is being subtracted by the value of gameSpeed
        if self.x < -self.width:                              # If the cloud moves off the screen
            self.x = screenWidth + random.randint(2500, 3000) # X-Cordinates of Cloud when created again
            self.y = random.randint(50, 100)                  # Y-Cordinates of Cloud when created again

    # Blits image on to screen
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


class obstacle:
    
    # Initializing attributes of class
    def __init__(self, image, type):
        self.image = image                           # First Arguement
        self.type = type                             # Second Arguement
        self.rect = self.image[self.type].get_rect() # Gets rectangle of image that going to be displayed
        self.rect.x = screenWidth                    # Obstacles are created on the right hand of the screen

    # Update Function
    def update(self):
        self.rect.x -= gameSpeed            # Obstacle x-cord is being subtracted by the value of gameSpeed
        if self.rect.x < -self.rect.width:  # If the obstacle moves off the screen
            obstacles.pop()                 # Removes obstacle 

    # Blits image on to screen
    def draw(self, screen):
        screen.blit(self.image[self.type], self.rect)


class smallCactus(obstacle):
    
    # Initializing attributes of class
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class largeCactus(obstacle):
    
    # Initializing attributes of class
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300


class bird(obstacle):
    
    # Initializing attributes of class
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    # Blits image on to screen
    def draw(self, screen):
        if self.index >= 9:
            self.index = 0
        screen.blit(self.image[self.index//5], self.rect)
        self.index += 1
        
        

def endscreen(deathCount):
    #-----------------------------Setup------------------------------------------------------#    
    pygame.init()
    
    #-----------------------------Program Variable Initialization----------------------------#  
    # Setting up fonts size
    font = pygame.font.Font('freesansbold.ttf', 30)
    
    screen.fill((255, 255, 255))  # Fills the screen with white
    #-----------------------------Event Handling-----------------------------------------#
    ev = pygame.event.poll()     # Look for any event
    if ev.type == pygame.QUIT:   # Window close button clicked?        
        pygame.quit()            # Exit for program
    if ev.type == pygame.KEYDOWN:
        main()
    #-----------------------------End Screen Logic---------------------------------------------# 
    # Rendering written font
    text = font.render("Press any Key to Restart", True, (0, 0, 0))  
    finalscore = font.render("Your Score: " + str(points), True, (0, 0, 0))
    
    finalscoreRect = finalscore.get_rect()                                    # Takes Rectangle of "finalscore"
    finalscoreRect.center = (screenWidth // 2, screenHeight // 2 + 50)   # Centers Rectangle of the screen and changes the height 
    textRect = text.get_rect()                                      # Takes Rectangle of "text"
    textRect.center = (screenWidth // 2, screenHeight // 2)         # Centers Rectangle of the screen 
    
    #-----------------------------Drawing Everything-------------------------------------#
    screen.blit(text, textRect)  # Draws text 
    screen.blit(RUNNING[0], (screenWidth // 2 - 20, screenHeight // 2 - 140))  # Draws Image of dino on screen
    screen.blit(finalscore, finalscoreRect) # Draws finalscore
    pygame.display.update() # Updates display
   
            
def controls():
    #-----------------------------Setup------------------------------------------------------#    
    pygame.init()
    
    #-----------------------------Program Variable Initialization----------------------------#
    # Setting up Colours
    border = (100,100,100) # Border Colour
    white = (255,255,255)  # Colour white
  
    # Setting up fonts size
    smallFont = pygame.font.SysFont('Corbel',35)
    bigFont = pygame.font.SysFont('Corbel',65)
  
    # Rendering written font
    text5 = smallFont.render('Jump: Up Arrow' , True , white)
    text6 = smallFont.render('Duck: Down Arrow' , True , white)
    text7 = bigFont.render('Controls' , True , white)
    text8 = smallFont.render('Back' , True , white)
    
    #-----------------------------Control Loop---------------------------------------------#  
    while True:
        
        #-----------------------------Event Handling-----------------------------------------#                  
        ev = pygame.event.poll()     # Look for any event
        if ev.type == pygame.QUIT:   # Window close button clicked?
            pygame.quit()            # Exit from program
              
        # Checks if the mouse has been clicked
        if ev.type == pygame.MOUSEBUTTONDOWN: 
              
                # If the button is clicked, then it will bring back the start screen (start())
            if screenWidth-250 <= mouse[0] <= screenWidth+200 and screenHeight-125 <= mouse[1] <= screenHeight+75:
                
                start()   

        #-----------------------------Controls Screen Logic---------------------------------------------#                    
        screen.fill((0,0,0))  # Fills the screen with black
      
        
        mouse = pygame.mouse.get_pos()  # Stores the (x,y) coordinates of the mouse into the variable
        
        #-----------------------------Drawing Everything-------------------------------------#    
        # Draws rectangles for borders of the buttons
        pygame.draw.rect(screen,border,[screenWidth-250,screenHeight-125,200,75])
        
        # Putting text onto the buttons
        screen.blit(text5 , (screenWidth/3+70,screenHeight/3+19))
        screen.blit(text6 , (screenWidth/3+50,screenHeight/2+19))
        screen.blit(text7 , (screenWidth/3+74,screenHeight/8+19))
        screen.blit(text8 , (screenWidth-185,screenHeight-105))
       
        # Updates frames
        pygame.display.update()
        
    
def start():
    #-----------------------------Setup------------------------------------------------------#    
    pygame.init()
    #-----------------------------Program Variable Initialization----------------------------#  
    # Setting up Colours
    border = (100,100,100) # Border Colour
    white = (255,255,255)  # Colour white
  
    # Setting up fonts size
    smallFont = pygame.font.SysFont('Corbel',35)
    bigFont = pygame.font.SysFont('Corbel',65)
  
    # Rendering written font
    text2 = smallFont.render('Start' , True , white)
    text3 = smallFont.render('Controls' , True , white)
    text4 = bigFont.render('Chrome Dino' , True , white)
    #-----------------------------Start Loop---------------------------------------------#  
    while True:
        
        #-----------------------------Event Handling-----------------------------------------#                  
            ev = pygame.event.poll()     # Look for any event
            if ev.type == pygame.QUIT:   # Window close button clicked?
                pygame.quit()            # Exit from program
              
            # Checks if the mouse has been clicked
            if ev.type == pygame.MOUSEBUTTONDOWN: 
              
                # If the button is clicked, then it will start the game (main())
                if screenWidth/3 <= mouse[0] <= screenWidth/3+366 and screenHeight/3 <= mouse[1] <= screenHeight/3+75:
                    time.sleep(0.25)
                    main()
                    
                # If the button is clicked, then it will bring up the controls screen (controls())
                if screenWidth/3 <= mouse[0] <= screenWidth/3+366 and screenHeight/2 <= mouse[1] <= screenHeight/2+75:
                    controls()
            
        #-----------------------------Start Screen Logic---------------------------------------------#                    
            screen.fill((0,0,0))  # Fills the screen with black
      
        
            mouse = pygame.mouse.get_pos()  # Stores the (x,y) coordinates of the mouse into the variable
            
            #-----------------------------Drawing Everything-------------------------------------#
            # Draws rectangles for borders of the buttons
            pygame.draw.rect(screen,border,[screenWidth/3,screenHeight/3,366,75])
            pygame.draw.rect(screen,border,[screenWidth/3,screenHeight/2,366,75])
      
            # Putting text onto the buttons
            screen.blit(text2 , (screenWidth/3+146,screenHeight/3+19))
            screen.blit(text3 , (screenWidth/3+124,screenHeight/2+19))
            screen.blit(text4 , (screenWidth/3+10,screenHeight/8+19))
      
            # Updates frames
            pygame.display.update()
        
    
    
def main():
    #-----------------------------Setup------------------------------------------------------#
    """ Set up the game and run the main game loop """
    pygame.init()      # Prepare the pygame module for use

    #-----------------------------Program Variable Initialization----------------------------#
    global gameSpeed, xPosBackground, yPosBackground, points, obstacles
    clock = pygame.time.Clock()
    playable = dinosaur()
    cloud = Cloud()
    gameSpeed = 20
    xPosBackground = 0
    yPosBackground = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    deathCount = 0
    #-----------------------------Main Game Loop---------------------------------------------#
    def score():
        global points, gameSpeed
        points += 1              # Everytime the function is called add one to or make points equal to one
        if points % 100 == 0:    # Every 100 points 
            gameSpeed += 1       # gameSpeed is increased by 1

        text = font.render("Score: " + str(points), True, (0, 0, 0)) # Display "Score" and number of points on screen
        textRect = text.get_rect()                                   # Gets cooridinates of text
        textRect.center = (1000, 45)                                 # Sets text rectangle to the top corner of the screen
        screen.blit(text, textRect)                                  # Blits score on screen

    def background():
        global xPosBackground, yPosBackground
        image_width = BG.get_width()                                        # Gets and Sets width of Image
        screen.blit(BG, (xPosBackground, yPosBackground))                   # Blits Image on screen
        screen.blit(BG, (image_width + xPosBackground, yPosBackground))     # Behind that Image we blit another one, becuase with out it there would be a gab after running out of background
        if xPosBackground <= -image_width:                                  # If Background moves off screen
            screen.blit(BG, (image_width + xPosBackground, yPosBackground)) # Another background is made
            xPosBackground = 0                                              # xPosBackground is reset to 0
        xPosBackground -= gameSpeed                                         # Background x-cord is being subtracted by the value of gameSpeed


    while True:
        
        #-----------------------------Event Handling-----------------------------------------#
        ev = pygame.event.poll()    # Look for any event
        if ev.type == pygame.QUIT:  # Window close button clicked?
            break                   #   ... leave game loop 
        #-----------------------------Game Logic---------------------------------------------#
        # Update your game objects and data structures here...
        
        screen.fill((255, 255, 255))   # Fills the screen with white
        
        # If amount obstacles is equal to 0 then it randomly picks a smallCactus, largeCactus, or bird and appends them to the obstactles list
        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(smallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(largeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(bird(BIRD))

        
        for obstacle in obstacles:
            obstacle.draw(screen) # Draws Obstacles
            obstacle.update() # Updates Obstacle
            if playable.dino_rect.colliderect(obstacle.rect):  # If the rectangle of the obstacle collides with the dinosaur's rectangle
                pygame.time.delay(3000)                        # Stops game for 3 seconds
                deathCount += 1        # Adds or equals one to deathCount
                endscreen(deathCount)  # Starts Endscreen
                
                
        userInput = pygame.key.get_pressed() # Gets the state of all keyboard buttons
        
        
        


        #-----------------------------Drawing Everything-------------------------------------#
        # We draw everything from scratch on each frame.
        # So first fill everything with the background color
        
        background() # Calls background function

        cloud.draw(screen) # Calls cloud function 
        cloud.update() # Updates cloud function

        score() # Calls score function

        clock.tick(30)  #Force frame rate to be slower
        pygame.display.update() 
        
        playable.draw(screen) # Draws dinosaur on screen
        playable.update(userInput) # Updates dinosaur on screen when needed
               
        

        # Now the screen is ready, tell pygame to display it!
        pygame.display.flip()





    pygame.quit()     # Once we leave the loop, close the window.

start()