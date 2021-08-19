import pygame
import random
import os

pygame.init()


# paths to files - CHANGE THEM IF WORKING WITH THE CODE
fontpath = os.path.join('/Users/eliska/Downloads/joystix/joystixmonospace.ttf')
bgpath = os.path.join('/Users/eliska/Documents/youlost/design', 'bg.png')
charpath = os.path.join('/Users/eliska/Documents/youlost/code/cloudodge', 'char.png')
cloudpath = os.path.join('/Users/eliska/Documents/youlost/design', 'goodcloud.png')
badcloudpath = os.path.join('/Users/eliska/Documents/youlost/design', 'badcloud.png')
endpath = os.path.join('/Users/eliska/Documents/youlost/design', 'endscreen.png')

# setting the screen
sizeinfo = pygame.display.Info()
screenWidth = sizeinfo.current_w
screenHeight = int(screenWidth*768/1366)
screen = pygame.display.set_mode([screenWidth,screenHeight])

ratio = screenHeight/900  # used for adjusting sizes according to screen size
font = pygame.font.Font(fontpath, int(40 * ratio))

highscore = 0
attempts = 1



def gamerunning():
    #display
    bgimg = pygame.image.load(bgpath)
    bg = pygame.transform.smoothscale(bgimg, [screenWidth, screenHeight])

    #character
    charWidth = 60*ratio
    charHeight = 110*ratio
    charX = screenWidth/2
    charY = screenHeight-(150*ratio)-charHeight
    movement = (screenWidth/90) * ratio
    char = pygame.image.load(charpath)
    char = pygame.transform.smoothscale(char, [int(ratio*60), int(ratio*110)])

    #clouds
    cloudWidth = ratio * 180
    cloudHeight = ratio * 80
    speed = (screenHeight/70) * ratio
    cloudMovement = ratio*speed
    cloudimg = pygame.image.load(cloudpath)
    cloudimg = pygame.transform.smoothscale(cloudimg, [int(cloudWidth), int(cloudHeight)])

    badCloudWidth = 220 * ratio
    badCloudHeight = 100 * ratio
    badcloudimg = pygame.image.load(badcloudpath)
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

    # declaring fields
    clouds = []
    badClouds = []

    # min and max for generating random amounts of time between clouds spawning
    timemin = 800
    timemax = 4000
    timestamp = (random.randint(timemin,timemax))
    timechangingstamp = 10000
    n=2   # later used for multiplying to set timechangingstamp
    badProbability = 5

    score = 0
    gameover = False

    clock=pygame.time.Clock()
    time = 0

    font = pygame.font.Font(fontpath, int(30 * ratio))

    while True:
        clock.tick()
        k = pygame.key.get_pressed()
        # changing the character's coordinates
        if k[pygame.K_LEFT] and (charX > 0):
            charX = charX-movement
        if k[pygame.K_RIGHT] and (charX + charWidth < screenWidth):
            charX = charX+movement

        # how the fuck does this work?
        # generates a cloud once per a random amount of time
        if time >= timestamp:
            r = random.randrange(0, badProbability)  # decides if the cloud will be bad or good
            if r == 0:
                badClouds.append(BadCloud(random.randint(0, int(screenWidth - cloudWidth)), 0))
            else:
                clouds.append(Cloud(random.randint(0, int(screenWidth - cloudWidth)), 0))
            timestamp = time+(random.randint(timemin,timemax))

        # every 10 seconds narrowing the range of rng for time between generating clouds
        # does the sentence even make sense? idk anymore
        if time >= timechangingstamp:
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
                    gameover = True

        #as the player gets more points, the probability of spawning a bad cloud increases
        if score % 100 == 0 and badProbability > 1 and score != 0:
            badProbability -= 1

        #drawing stuff on screen
        screen.blit(bg, (0, 0))  # drawing background
        screen.blit(char, (charX, charY))

        # changing coordinates of clouds and drawing them on screen
        for cloud in clouds:
            cloud.y += cloudMovement
            cloud.draw()
        for badcloud in badClouds:
            badcloud.y += cloudMovement
            badcloud.draw()

        scorecounter = font.render("Score: " + str(score), True, (255,255,255), (60,160,145))
        screen.blit(scorecounter, ((1600-300)*ratio, 50*ratio))

        attemptcounter = font.render("Attempt: " + str(attempts), True, (255, 255, 255), (70, 200, 125))
        screen.blit(attemptcounter, ((1600 - 625) * ratio, 50 * ratio))

        pygame.event.pump()
        pygame.display.flip()

        time += clock.get_time()

        # temporary escape way, will do a better one later
        if pygame.key.get_pressed()[pygame.K_q]:
            break

        if gameover == True:
            break

    return score



def endscreen():
    newhighscore = False
    gameended = False
    endimg = pygame.image.load(endpath)
    endimg = pygame.transform.smoothscale(endimg, [screenWidth, screenHeight])

    # creating text
    scoretxt = font.render("Score: " + str(score), True, [200, 100, 0])
    scoreY = 350 * ratio
    scoreX = 0.5 * screenWidth - 0.5 * (font.size("Score: " + str(score))[0])

    if score > highscore:
        newhighscore = True
        highscoretxt = "New highscore!"
    else:
        highscoretxt = "Highscore: " + str(highscore)

    highscoreX = 0.5 * screenWidth - 0.5 * (font.size(highscoretxt))[0]
    highscoretxt = font.render(highscoretxt, True, [100, 255, 0])
    highscoreY = 420*ratio
    instructions = font.render("Press F to play again, esc to end", True, [255,240,100])

    #draws stuff on screen, every frame is the same so its kinda useless but it does weird things when i do it different
    while True:
        screen.blit(endimg, (0, 0))
        screen.blit(scoretxt, (scoreX, scoreY))
        screen.blit(highscoretxt, (highscoreX,highscoreY))
        screen.blit(instructions, (0.5 * screenWidth - 0.5 * (font.size("Press F to play again, esc to end"))[0], 800*ratio))
        pygame.event.pump()
        pygame.display.flip()

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            gameended = True
            break
        if pygame.key.get_pressed()[pygame.K_f]:
            gameended = False
            if newhighscore == True:
                global highscoreNEW
                highscoreNEW = score
            break

    return gameended


# here it finally runs haha
score = gamerunning() # first it runs the game
while True:
    gameended = endscreen()
    if gameended == True:
        break
    else:
        try:
            highscore = highscoreNEW
        except:
            highscore = highscore
        attempts += 1
        score = gamerunning()

"""
To do:
done everything yay

To do later or something:
- lives
- some fancy sidebar showing score, highscore and number of attempts
- time, maybe?
- redesign the bad cloud
"""