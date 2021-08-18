import pygame
import random
import time
import os

pygame.init()

#display
screenWidth = 1000
screenHeight = int(screenWidth*768/1366)
screen = pygame.display.set_mode([screenWidth, screenHeight])
ratio = screenHeight/900
bgimg = pygame.image.load(os.path.join('/Users/eliska/Documents/youlost/code/cloudodge', 'bg.png'))
bg = pygame.transform.smoothscale(bgimg, [screenWidth, screenHeight])

#character
charWidth = 60*ratio
charHeight = 110*ratio
charX = screenWidth/2
charY = screenHeight-(150*ratio)-charHeight
movement = ratio*10
char = pygame.image.load(os.path.join('/Users/eliska/Documents/youlost/code/cloudodge', 'char.png'))
char = pygame.transform.smoothscale(char, [int(ratio*60), int(ratio*110)])

#clouds
cloudWidth = ratio * 180
cloudHeight = ratio * 80
speed = 8
cloudMovement = ratio*speed
cloudimg = pygame.image.load(os.path.join('/Users/eliska/Documents/youlost/design', 'goodcloud.png'))
cloudimg = pygame.transform.smoothscale(cloudimg, [int(cloudWidth), int(cloudHeight)])

badCloudWidth = 220 * ratio
badCloudHeight = 100 * ratio
badcloudimg = pygame.image.load(os.path.join('/Users/eliska/Documents/youlost/design', 'badcloud.png'))
badcloudimg = pygame.transform.smoothscale(badcloudimg, [int(badCloudWidth), int(badCloudHeight)])

class Cloud():
    def __init__(self,cloudX,cloudY):
        self.x=cloudX
        self.y=cloudY

    def draw(self):
        screen.blit(cloudimg, [self.x, self.y])

class BadCloud():
    def __init__(self, cloudX, cloudY):
        self.x = cloudX
        self.y = cloudY

    def draw(self):
        screen.blit(badcloudimg, [self.x, self.y])

# odtud by to asi mohla byt funkce ?? ja doprdele nevim
# a kde si jako resetnes veci a co budes delat s casem lol <- KOUKEJ TO VYRESIT IDIOTE, TOHLE JE PROBLEM
# kaslu na to, proste tohle nebudou pouzivat  l i d i   a ja budu moct jit spinkat


clouds = [] # field for clouds
badClouds = [] # field for bad clouds
timemin = 800 # min and max for generating random amounts of time between clouds spawning
timemax = 4000
timestamp = (pygame.time.get_ticks())+(random.randint(timemin,timemax))
timechangingstamp = 10000
n=2   # later used for multiplying to set timechangingstamp
badProbability = 5

score = 0
gameover = False

# pygame.time.set_timer(pygame.USEREVENT+2, generatingtime)  #timer for generating new clouds - NOT USED
# pygame.time.get_ticks()  using this only for copying lol

while True:
    k = pygame.key.get_pressed()
    # changing the character's coordinates
    if k[pygame.K_LEFT] and (charX > 0):
        charX = charX-movement
    if k[pygame.K_RIGHT] and (charX + charWidth < screenWidth):
        charX = charX+movement

    # generating new clouds
    # how the fuck does this work?
    """
    # this generates a cloud after the same amount of time every time, not using this but keeping it here just because i can
    if pygame.event.get(pygame.USEREVENT+2):
        r = random.randrange(0, 5)
        if r == 0:
            badClouds.append(BadCloud(random.randint(0,int(screenWidth-cloudWidth)),0))
        else:
            clouds.append(Cloud(random.randint(0,int(screenWidth-cloudWidth)),0))

        generatingtime = random.randint(1000, 4000) #aaaaaa no this is so wrong omg
    """
    # generates a cloud once per a random amount of time
    if pygame.time.get_ticks() >= timestamp:
        r = random.randrange(0, badProbability)  # decides if the cloud will be bad or good
        if r == 0:
            badClouds.append(BadCloud(random.randint(0, int(screenWidth - cloudWidth)), 0))
        else:
            clouds.append(Cloud(random.randint(0, int(screenWidth - cloudWidth)), 0))
        timestamp = (pygame.time.get_ticks())+(random.randint(timemin,timemax))

    # every 10 seconds narrowing the range of rng for time between generating clouds
    # does the sentence even make sense? idk anymore
    if pygame.time.get_ticks() >= timechangingstamp:
        if timemin >= 40:
            timemin -=40

        if timemax >=400:
            timemax -=200

        timechangingstamp = n * 10000
        n += 1


    # checking whether the clouds have reached the ground
    for cloud in clouds:  # checking the good ones and deleting those on ground from the array
        if cloud.y >= screenHeight-(150*ratio)-cloudHeight:
            clouds.pop(clouds.index(cloud))
    for badcloud in badClouds:  # checking the bad ones
        if badcloud.y >= screenHeight-(150*ratio)-badCloudHeight:
            badClouds.pop(badClouds.index(badcloud))

    # checks if the player's catched the good cloud and eventually increases the score
    for cloud in clouds:
        if ( cloud.x < charX and cloud.x+cloudWidth < charX ) or ( cloud.x > charX+charWidth and cloud.x+cloudWidth > charX+charWidth ):
            clouds = clouds
        else:
            if (cloud.y + cloudHeight) >= charY:
                clouds.pop(clouds.index(cloud))
                score +=1

    #checking if the player hit the bad one
    for badcloud in badClouds:
        if (badcloud.x < charX and badcloud.x+badCloudWidth < charX) or (badcloud.x > charX+charWidth and badcloud.x+badCloudWidth > charX+charWidth):
            badClouds = badClouds
        else:
            if (badcloud.y + badCloudHeight) >= charY:
                print("you lost")
                gameover = True
    #drawing stuff on screen
    screen.fill([200, 150, 100])  # bg color - basically useless but it's there
    screen.blit(bg, (0, 0))  # drawing background
    #pygame.draw.rect(screen, [255, 0, 0], [charX, charY, charWidth, charHeight])  # useless already but keeping it here just in case i'd forget
    screen.blit(char, (charX, charY))

    # changing coordinates of clouds and drawing them on screen
    for cloud in clouds:
        cloud.y += cloudMovement
        cloud.draw()
    for badcloud in badClouds:
        badcloud.y += cloudMovement
        badcloud.draw()

    pygame.event.pump()
    pygame.display.flip()
    print(score)

    # temporary escape way, will do a better one later
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        break

    if gameover == True:
        break

"""
To do:
- probability of spawning bad clouds (based on points)
- play again function (and the 'you lose' screen in general)
- showing highscore

To do later or something:
- lives
- some fancy sidebar showing score, highscore and number of attempts
- time, maybe?
- redesign the bad cloud
"""