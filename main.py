# Author: Mark Peng
# Amazeing Algorithms

#####################
#      Imports      #
#####################

import pygame
import random
import colorsys
from mazelib import Maze
from mazelib.generate.Kruskal import Kruskal
from mazelib.generate.BacktrackingGenerator import BacktrackingGenerator



#####################
#  Initializations  #
#####################

### Files ###

scores = []  # easy, med, hard, respectively 

# Opens files in append mode; functions as a way
# to either do nothing if a file exists,
# or create a file if it does not already exist.

temp = open("scores.txt", "a+")
temp.close()

scoreFile = open("scores.txt", "r")
for line in scoreFile:
    scores.append(float(line.strip("\n")))
scoreFile.close()

### PyGame ###

# Intialize PyGame
pygame.init() 

# Window Settings
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Amazeing Algorithms")
clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)
fontLarge = pygame.font.Font(None, 100)

pygame.mixer.music.set_volume(0.8)

### Color Variables ###
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (105, 105, 105)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

### Game Variables ###

onIntro = True
easyMode = False
mediumMode = False
hardMode = False
helpMode = False
winScreen = False
DFSwin = False
time = 0

### Misc. Variables ###

muted = False
runOnce = True

#####################
#      Classes      #
#####################

class Intro:
    
    ### Class Variables ###

    # Buttons
    easyButton = pygame.Rect(250, 200, 300, 60)
    mediumButton = pygame.Rect(250, 300, 300, 60)
    hardButton = pygame.Rect(250, 400, 300, 60)
    helpButton = pygame.Rect(250, 500, 300, 60)
    buttonColors = [BLACK, BLACK, BLACK, BLACK]  # easyButton = idx#0, and so on

    # Images
    intro = pygame.image.load("text.png")
    background = pygame.image.load("bg.jpg")

    # Sounds
    buttonClick = pygame.mixer.Sound("clicked.wav")

    def start(self):
        # Only play sound when called 
        pygame.mixer.music.load("introBGM.mp3")
        pygame.mixer.music.play(-1)

    def handleEvent(self, event, mouse_pos):
        global onIntro
        global easyMode
        global mediumMode
        global hardMode
        global helpMode
        global runOnce

        if Intro.easyButton.collidepoint(mouse_pos):
            if(event.type == pygame.MOUSEBUTTONDOWN):
                onIntro = False
                easyMode = True
                runOnce = True
                # Handle sounds
                pygame.mixer.music.stop()
                pygame.mixer.music.load("gameBGM.mp3")
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.2)
                Intro.buttonClick.play()
            else:
                Intro.buttonColors[0] = GREY
        else:
            Intro.buttonColors[0] = BLACK

        if Intro.mediumButton.collidepoint(mouse_pos):
            if(event.type == pygame.MOUSEBUTTONDOWN):
                onIntro = False
                mediumMode = True
                runOnce = True
                # Handle sounds
                pygame.mixer.music.stop()
                pygame.mixer.music.load("gameBGM.mp3")
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.2)
                Intro.buttonClick.play()
            else:
                Intro.buttonColors[1] = GREY
        else:
            Intro.buttonColors[1] = BLACK
        
        if Intro.hardButton.collidepoint(mouse_pos):
            if(event.type == pygame.MOUSEBUTTONDOWN):
                onIntro = False
                hardMode = True
                runOnce = True
                # Handle sounds
                pygame.mixer.music.stop()
                pygame.mixer.music.load("gameBGM.mp3")
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.2)
                Intro.buttonClick.play()
            else:
                Intro.buttonColors[2] = GREY
        else:
            Intro.buttonColors[2] = BLACK

        if Intro.helpButton.collidepoint(mouse_pos):
            if(event.type == pygame.MOUSEBUTTONDOWN):
                onIntro = False
                helpMode = True
                runOnce = True
                # Handle sounds
                Intro.buttonClick.play()
            else:
                Intro.buttonColors[3] = GREY
        else:
            Intro.buttonColors[3] = BLACK


    def draw(self):    
        screen.blit(Intro.background, (0,0))
        screen.blit(Intro.intro, (35, 100))

        pygame.draw.rect(surface=screen, color=Intro.buttonColors[0], rect=Intro.easyButton, border_radius=8)
        text = font.render("Easy Mode", True, WHITE)
        text_rect = text.get_rect(center=Intro.easyButton.center)
        screen.blit(text, text_rect)

        pygame.draw.rect(surface=screen, color=Intro.buttonColors[1], rect=Intro.mediumButton, border_radius=8)
        text = font.render("Medium Mode", True, WHITE)
        text_rect = text.get_rect(center=Intro.mediumButton.center)
        screen.blit(text, text_rect)
        
        pygame.draw.rect(surface=screen, color=Intro.buttonColors[2], rect=Intro.hardButton, border_radius=8)
        text = font.render("Hard Mode", True, WHITE)
        text_rect = text.get_rect(center=Intro.hardButton.center)
        screen.blit(text, text_rect)

        pygame.draw.rect(surface=screen, color=Intro.buttonColors[3], rect=Intro.helpButton, border_radius=8)
        text = font.render("Game Instructions", True, WHITE)
        text_rect = text.get_rect(center=Intro.helpButton.center)
        screen.blit(text, text_rect)

class Help:
    def draw(self):
        screen.fill((255,255,255))
        textWidth = 500  # maximum width of text in px.
        y = 100
        text = """
        Welcome to aMAZEing algorithms! This game is about traversing through mazes as fast as possible.
        Depending on the mode, the complexity of each maze will change accordingly. Heres the twist, through! You are not alone.
        What do you mean? Well, you have to complete each maze faster than the common graph theory algorithm, DFS!

        Controls are very simple in this game. ARROW KEYS to move the CHARACTER. That's it.

        Press escape to leave this screen, and all screens. Good luck!
        """
        words = text.split()
        textLines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= textWidth:
                current_line = test_line
            else:
                textLines.append(current_line)
                current_line = word + " "
        textLines.append(current_line)

        for line in textLines:
            text_surface = font.render(line, True, BLACK)
            screen.blit(text_surface, (150, y))
            y += font.get_height()+5

class Game:

    # maze
    squareSize = (100, 100)
    rows = 0
    columns = 0
    grid = []

    # DFS
    visited = []
    r = 0
    c = 0
    cnt = 0

    visitedDisplay = {}
    idx = 0

    def __init__(self, mode, playerX, playerY, time):
        self.mode = mode
        self.playerX = playerX
        self.playerY = playerY
        Game.r = playerX
        Game.c = playerY
        self.time = time
    
    def dfs(self, r, c):
        if (Game.visited[r][c] != True):
            Game.visitedDisplay[(r,c)] = Game.cnt
            Game.cnt += 1
        Game.visited[r][c] = True
        if(Game.grid[r-1][c] == 0 and not Game.visited[r-1][c] and r != 0):
            self.dfs(r-1, c)
        if(Game.grid[r][c-1] == 0 and not Game.visited[r][c-1] and c != 0):
            self.dfs(r, c-1)
        if(r+1 != Game.rows):
            if(Game.grid[r+1][c] == 0 and not Game.visited[r+1][c]):
                self.dfs(r+1, c)
        if(c+1 != Game.columns):
            if(Game.grid[r][c+1] == 0 and not Game.visited[r][c+1]):
                self.dfs(r, c+1)

    def genGrid(self):
        mode = self.mode
        if mode == "easy":
            Game.squareSize = (100, 100)
            Game.rows = 6
            Game.columns = 8

            # generate an 8x6 grid
            selection = random.randint(1, 3)
            if selection == 1:
                Game.grid = [
                    [0,1,0,0,0,0,0,0],
                    [0,1,0,1,1,0,1,0],
                    [0,1,0,1,0,1,0,0],
                    [0,1,0,1,0,1,0,1],
                    [0,0,0,0,0,1,0,0],
                    [0,1,0,1,0,0,1,0],
                    ]
            elif selection == 2:
                Game.grid = [
                    [0,0,0,0,0,0,0,0],
                    [1,0,1,1,1,1,1,1],
                    [1,0,0,0,1,0,0,0],
                    [1,1,1,0,1,0,1,0],
                    [1,0,0,0,0,0,1,0],
                    [1,1,1,1,1,1,1,0],
                    ]
            elif selection == 3:
                Game.grid = [
                    [0,0,0,0,1,0,0,0],
                    [0,1,1,0,1,0,1,0],
                    [0,0,1,0,1,0,1,0],
                    [0,1,1,0,0,0,1,0],
                    [0,0,1,0,1,1,1,0],
                    [0,0,0,0,1,0,0,0],
                    ]
        if mode == "medium":
            Game.squareSize = (25, 25)
            Game.rows = 24
            Game.columns = 32
            m = Maze()
            m.generator = Kruskal(12, 16)
            m.generate()
            m.generate_entrances(False, False)
            maze = m.grid.tolist()
            Game.grid = []
            for i in range(0, 24):
                Game.grid.append(maze[i][0:32])
        if mode == "hard":
            Game.squareSize = (12.5, 12.5)
            Game.rows = 36
            Game.columns = 64
            m = Maze()
            m.generator = BacktrackingGenerator(18, 32)
            m.generate()
            m.generate_entrances(False, False)
            maze = m.grid.tolist()
            Game.grid = []
            for i in range(0, 36):
                Game.grid.append(maze[i][0:64])
        
        Game.visited = [[0 for x in range(Game.columns)] for y in range(Game.rows)]
        Game.visitedDisplay.clear()
        Game.idx = 0
        Game.cnt = 0
        self.dfs(Game.r, Game.c)
    
    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                if self.playerY+1 < Game.rows:
                    if not Game.grid[self.playerY+1][self.playerX]:
                        self.playerY += 1
            elif event.key == pygame.K_UP:
                if self.playerY-1 >= 0:
                    if not Game.grid[self.playerY-1][self.playerX]:
                        self.playerY -= 1
            elif event.key == pygame.K_RIGHT:
                if self.playerX+1 < Game.columns:
                    if not Game.grid[self.playerY][self.playerX+1]:
                        self.playerX += 1
            elif event.key == pygame.K_LEFT:
                if self.playerX-1 >= 0:
                    if not Game.grid[self.playerY][self.playerX-1]:
                        self.playerX -= 1


    def drawGrid(self):
        global winScreen
        global easyMode
        global mediumMode
        global hardMode
        global DFSwin
        global time
        screen.fill(WHITE)
        x, y = 0, 0
        for i in range(0, Game.rows):
            for j in range(0, Game.columns):
                if i == self.playerY and j == self.playerX:
                    if i+1 == Game.rows and j+1 == Game.columns:
                        winScreen = True
                        time = self.time
                        self.playerX = 0
                        self.playerY = 0
                    else:
                        square = pygame.Rect(x, y, Game.squareSize[0], Game.squareSize[1])
                        pygame.draw.rect(surface=screen, color=BLUE, rect=square)
                elif i == 0 and j == 0: # start square
                    square = pygame.Rect(x, y, Game.squareSize[0], Game.squareSize[1])
                    pygame.draw.rect(surface=screen, color=GREEN, rect=square)
                elif Game.grid[i][j]: # wall
                    square = pygame.Rect(x,y, Game.squareSize[0], Game.squareSize[1])
                    pygame.draw.rect(surface=screen, color=BLACK, rect=square)
                elif Game.visited[i][j]:
                    if((i,j) in Game.visitedDisplay):
                        if(Game.visitedDisplay[(i,j)] <= Game.idx):
                            if (i+1 == Game.rows and j+1 == Game.columns):
                                winScreen = True
                                DFSwin = True
                                time = self.time
                                self.playerX = 0
                                self.playerY = 0
                            square = pygame.Rect(x,y, Game.squareSize[0], Game.squareSize[1])
                            pygame.draw.rect(surface=screen, color=GREY, rect=square)
                if i+1 == Game.rows and j+1 == Game.columns: # end square
                    square = pygame.Rect(x, y, Game.squareSize[0], Game.squareSize[1])
                    pygame.draw.rect(surface=screen, color=GREEN, rect=square)

                x += Game.squareSize[0]
            y += Game.squareSize[1]
            x = 0
        
        if hardMode:
            square = pygame.Rect(0, 450, 800, 200)
            pygame.draw.rect(surface=screen, color=BLACK, rect=square)

        self.time += 1
        if easyMode and self.time%40 == 0:
                Game.idx += 1
        if mediumMode and self.time%4 == 0:
            Game.idx += 1
        if hardMode and self.time % 7 == 0:
            Game.idx += 1
        text_surface = font.render(str(round(self.time/60, 2)), True, RED) 
        screen.blit(text_surface, (0, 0))

class Winner:
    frame = 0
    exitButton = pygame.Rect(250, 270, 300, 60)
    buttonClick = pygame.mixer.Sound("clicked.wav")

    def __init__(self, mode):
        self.mode = mode

    def handleEvent(self, event, mouse_pos):
        global onIntro
        global winScreen
        global easyMode
        global mediumMode
        global hardMode
        global DFSwin
        if (event.type == pygame.MOUSEBUTTONDOWN) and Winner.exitButton.collidepoint(mouse_pos):
            onIntro = True
            easyMode = False
            mediumMode = False
            hardMode = False
            winScreen = False
            DFSwin = False
            Winner.buttonClick.play()
            pygame.mixer.music.load("introBGM.mp3")
            pygame.mixer.music.set_volume(0.8)
            pygame.mixer.music.play(-1)

    def draw(self):
        if Winner.frame == 360:
            Winner.frame = 0

        
        # colors
        colorTup = colorsys.hsv_to_rgb(Winner.frame/360, 1, 1)
        colors = (colorTup[0] * 255, colorTup[1] * 255, colorTup[2] * 255)
        colors2 = (abs(1-colorTup[0])*255, abs(1-colorTup[1])*255, abs(1-colorTup[2])*255) # offset num. 1
        colors3 = (abs(0.8-colorTup[0])*255, abs(0.8-colorTup[1])*255, abs(0.8-colorTup[2])*255) # offset num. 2
        screen.fill(colors)

        if(self.mode == "dfs"):
            screen.fill(BLACK)
            pygame.draw.rect(surface=screen, color=GREY, rect=Winner.exitButton, border_radius=8)        
            text = font.render("Exit!", True, WHITE)
            text_rect = text.get_rect(center=Winner.exitButton.center)
            screen.blit(text, text_rect)
            text_surface = fontLarge.render("You have lost to DFS :(", True, WHITE) 
            screen.blit(text_surface, (35, 30))
        else:
            # gamemode text handlers
            if(self.mode == "easy"):
                text_surface = fontLarge.render("You have won in easy!", True, colors2) 
                screen.blit(text_surface, (35, 30))
                if scores[0] != 9999999999999.0:
                    text_surface = font.render("High score: " + str(scores[0]), True, colors2)
                    screen.blit(text_surface, (260, 150))

            if(self.mode == "medium"):
                text_surface = fontLarge.render("Medium mode winner!", True, colors2) 
                screen.blit(text_surface, (35, 30))

                if scores[1] != 9999999999999.0:
                    text_surface = font.render("High score: " + str(scores[1]), True, colors2)
                    screen.blit(text_surface, (260, 150))
            if(self.mode == "hard"):
                text_surface = fontLarge.render("You have won in hard!", True, colors2) 
                screen.blit(text_surface, (35, 30))
                
                if scores[2] != 9999999999999.0:
                    text_surface = font.render("High score: " + str(scores[2]), True, colors2)
                    screen.blit(text_surface, (260, 150))
                
            # time text
            text_surface = font.render("You have won in " + str(round(time/60, 2)) + " seconds!", True, colors2)
            screen.blit(text_surface, (215, 100))

            

            # exit button
            pygame.draw.rect(surface=screen, color=colors3, rect=Winner.exitButton, border_radius=8)        
            text = font.render("Exit!", True, WHITE)
            text_rect = text.get_rect(center=Winner.exitButton.center)
            screen.blit(text, text_rect)
            
            # circle animation
            movement = Winner.frame
            if Winner.frame > 180:
                movement = 180 - abs(Winner.frame - 180)
            pygame.draw.circle(screen, colors3, (400, 300-movement/1.5), 30)  # up
            pygame.draw.circle(screen, colors3, (400, 300+movement/1.5), 30)  # down
            pygame.draw.circle(screen, colors3, (400+movement*2, 300), 30)  # right
            pygame.draw.circle(screen, colors3, (400-movement*2, 300), 30)  # left

        Winner.frame += 1

                          
#####################
# MAIN CONTROL LOOP #
#####################

intro = Intro()
intro.start()

help = Help()


while True:
    
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            if onIntro:
                intro.handleEvent(event, mouse_pos)
            if winScreen and event.type == pygame.MOUSEBUTTONDOWN:
                winScreenD.handleEvent(event, mouse_pos)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if not onIntro:
                    onIntro = True
                    if helpMode == False:  # only restart intro music if not on help screen previously.
                        intro.start()  
                    pygame.mixer.music.set_volume(0.8)
                    easyMode = False
                    mediumMode = False
                    hardMode = False
                    helpMode = False
                    winScreen = False
            elif event.key == pygame.K_m:
                if muted:
                    muted = False
                    if onIntro or helpMode:
                        pygame.mixer.music.set_volume(0.8)
                    else:
                        pygame.mixer.music.set_volume(0.2)
                else:
                    muted = True
                    pygame.mixer.music.set_volume(0)
            elif onIntro == False and helpMode == False and winScreen == False:
                game.handleEvent(event)

    # Drawing
    if onIntro:
        intro.draw()
        easyMode = False
        mediumMode = False
        hardMode = False
    
    if winScreen:
        if DFSwin:
            winScreenD = Winner("dfs")
            winScreenD.draw()
        else:
            if easyMode:
                winScreenD = Winner("easy")
                scores[0] = min(round(time/60, 2), scores[0])
                winScreenD.draw()
            elif mediumMode:
                winScreenD = Winner("medium")
                scores[1] = min(round(time/60, 2), scores[1])
                winScreenD.draw()
            elif hardMode:
                winScreenD = Winner("hard")
                scores[2] = min(round(time/60, 2), scores[2])
                winScreenD.draw()
            scoreFile = open("scores.txt", "w")
            for i in scores:
                scoreFile.write(str(i) + "\n")
            scoreFile.close()

        
    elif easyMode:
        if runOnce:
            runOnce = False
            game = Game("easy", 0, 0, 0)
            game.genGrid()
        game.drawGrid()  
    elif mediumMode:
        if runOnce:
            runOnce = False
            game = Game("medium", 1, 1, 0)
            game.genGrid()
        game.drawGrid()
    elif hardMode:
        if runOnce:
            runOnce = False
            game = Game("hard", 1, 1, 0)
            game.genGrid()
        game.drawGrid()
    if helpMode:
        help.draw()

    pygame.display.flip()
    clock.tick(60)