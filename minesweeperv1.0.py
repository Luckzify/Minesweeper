#Gavin Brady
#Oct 26 2023
#Minesweeper

#Version Number
VERSION_NUMBER = "V1.0"

#modules
import pygame as pg
import random
import numpy as np
pg.init()

#functions
def drawGameScreen(swidth, sheight, gwidth, gheight):
    pg.display.set_caption('Minesweeper Game')
    #draws grid
    for x in range(0, gwidth, blockSize):
        for y in range(0, gheight, blockSize):
            rect = pg.Rect(x, y+GRID_MENU_HEIGHT, blockSize, blockSize)
            pg.draw.rect(SCREEN, "black", rect, 1)

    #draws grid menu
    global MENU_BUTTON
    font = pg.font.SysFont('Arial', 40, bold=True)
    menu_text = font.render('MENU', True, 'white')
    menu_textbox = menu_text.get_rect()
    MENU_BUTTON = pg.Rect(0,0,150,75)
    menu_textbox.center = (((swidth // 2) + 160), (GRID_MENU_HEIGHT // 2))
    MENU_BUTTON.center = (((swidth // 2) + 160), (GRID_MENU_HEIGHT // 2))
    pg.draw.rect(SCREEN, (255, 00, 00), menu_textbox)
    pg.draw.rect(SCREEN, (255, 00, 00), MENU_BUTTON)
    SCREEN.blit(menu_text, menu_textbox)

    #Draws bomb counter
    #Bombs remaining text and textbox
    font = pg.font.SysFont('Arial', 25, bold=True)
    counter_text = font.render('Bombs remaining:', True, 'red')
    counter_textbox = counter_text.get_rect()
    counter_outertextbox = pg.Rect(0,0,225, 50)
    counter_textbox.center = (((swidth // 2) - 125), (GRID_MENU_HEIGHT // 2))
    counter_outertextbox.center = counter_textbox.center
    pg.draw.rect(SCREEN, (255, 255, 255), counter_outertextbox)
    pg.draw.rect(SCREEN, (255, 255, 255), counter_textbox, width=-1)
    SCREEN.blit(counter_text, counter_textbox)

    #bombs remaining value
    global counter_box
    global bombs_remaining
    counter_box = pg.Rect(0,0,50,50)
    counter_box.topleft = (counter_outertextbox.topright[0]-7, counter_outertextbox.topright[1])
    pg.draw.rect(SCREEN, (255, 255, 255), counter_box)
    font = pg.font.SysFont('Arial', 30, bold=True)
    bomb_remainder_text = font.render(str(bombs_remaining), True, 'red')
    bomb_remainder_textbox = bomb_remainder_text.get_rect()
    bomb_remainder_textbox.center = counter_box.center
    pg.draw.rect(SCREEN, (255, 255, 255), bomb_remainder_textbox, width=-1)
    SCREEN.blit(bomb_remainder_text, bomb_remainder_textbox)

def updateNumberTiles(x, y):
##adds +1 to all 9 sides, assuming no bomb present at location
    if y > 0 and x > 0 and gridArr[y-1][x-1] != 'BOMB': #upper-left corner
    	gridArr[y-1][x-1] = str(int(gridArr[y-1][x-1]) + 1)
    if y > 0 and gridArr[y-1][x] != 'BOMB': #upper end
    	gridArr[y-1][x] = str(int(gridArr[y-1][x]) + 1)
    if y > 0 and x < (xDimension-1) and gridArr[y-1][x+1] != 'BOMB': #upper-right corner
    	gridArr[y-1][x+1] = str(int(gridArr[y-1][x+1]) + 1)
    if x < (xDimension-1) and gridArr[y][x+1] != 'BOMB': #right side
    	gridArr[y][x+1] = str(int(gridArr[y][x+1]) + 1)
    if y < (yDimension-1) and x < (xDimension-1) and gridArr[y+1][x+1] != 'BOMB': #lower-right corner
    	gridArr[y+1][x+1] = str(int(gridArr[y+1][x+1]) + 1)
    if y < (yDimension-1) and gridArr[y+1][x] != 'BOMB': #lower end
    	gridArr[y+1][x] = str(int(gridArr[y+1][x]) + 1)
    if y < (yDimension-1) and x > 0 and gridArr[y+1][x-1] != 'BOMB': #lower-left corner
    	gridArr[y+1][x-1] = str(int(gridArr[y+1][x-1]) + 1)
    if x > 0 and gridArr[y][x-1] != 'BOMB': #left side
    	gridArr[y][x-1] = str(int(gridArr[y][x-1]) + 1)

def flagSquare(xc, yc):
    global bombs_remaining
    bombs_remaining -= 1
    
    leftBorder = blockSize * xc
    upperBorder = blockSize * yc + GRID_MENU_HEIGHT

    flagRect = pg.Rect(leftBorder, upperBorder, blockSize, blockSize)
    pg.draw.rect(SCREEN, (255, 0, 255), flagRect, 0)

def unflagSquare(xc, yc):
    global bombs_remaining
    bombs_remaining += 1
    
    leftBorder = blockSize * xc
    upperBorder = blockSize * yc + GRID_MENU_HEIGHT
    
    flagRect = pg.Rect(leftBorder, upperBorder, blockSize, blockSize)
    pg.draw.rect(SCREEN, (128, 128, 128), flagRect, 0)
                          
def revealSquare(x, y, value):
    if y >= 0:
        #finds tile dimensions
        leftBorder = x * blockSize
        upperBorder = y * blockSize + GRID_MENU_HEIGHT
        tileRect = pg.Rect(leftBorder, upperBorder, blockSize, blockSize)
        global alive
        
        #reveals all further bombs if already dead
        if alive == False and value == 'BOMB':
            pg.draw.rect(SCREEN, (255, 0, 0), tileRect, 0)

        #ensures player is alive and clicked on unrevealed tile
        #also checks to see it could be a flag, as if was clicked it already
        #checked tile was not flagged, but if revealing adjacents this allows
        #it to be revealed
        if alive == True and (SCREEN.get_at((leftBorder + 25, upperBorder + 25))[:3] == (128, 128, 128) or SCREEN.get_at((leftBorder + 25, upperBorder + 25))[:3] == (255, 0, 255)):   
            global unrevealedTiles
            unrevealedTiles -= 1
            if value == 'BOMB': #colors tile red if holds bomb
                pg.draw.rect(SCREEN, (255, 0, 0), tileRect, 0)
                alive = False
                loss()

            elif value =='0': #colors tile white
                pg.draw.rect(SCREEN, (255, 255, 255), tileRect, 0)
                revealAdjacents(x, y)
                
            else: #colors tile white with text showing bombs touching value
                pg.draw.rect(SCREEN, (255, 255, 255), tileRect, 0)
                pg.font.init()
                font = pg.font.SysFont(None, 60)
                numberIcon = font.render(value, True, (0, 0, 255), (255, 255, 255))
                pg.Surface.blit(SCREEN, numberIcon, (leftBorder, upperBorder))

def revealAdjacents(x,y):
    if y != 0:
        revealSquare(x, y-1, gridArr[y-1][x])
        if x != 0:
            revealSquare(x-1, y-1, gridArr[y-1][x-1])
        if x != (xDimension-1):
            revealSquare(x+1, y-1, gridArr[y-1][x+1])
    if y != (yDimension-1):
        revealSquare(x, y+1, gridArr[y+1][x])
        if x != 0:
            revealSquare(x-1, y+1, gridArr[y+1][x-1])
        if x != (xDimension-1):
            revealSquare(x+1, y+1, gridArr[y+1][x+1])
    if x != 0:
            revealSquare(x-1, y, gridArr[y][x-1])
    if x != (xDimension-1):
            revealSquare(x+1, y, gridArr[y][x+1])

def getTileCoords(x, y):
    xCoord = x // blockSize
    yCoord = y // blockSize

    return [xCoord, yCoord]

#generates bombs and tile values
def generateBombs(x,y,bc, tc):
    #LEA MODE BOMB POS: 19, 20, 21, 25, 26, 27, 33, 37, 39, 43, 47, 53, 59, 62, 74, 77, 89, 93, 103, 109, 117, 125, 131, 141, 145, 157, 159, 173
    bombPosList = []
    ###NOTE: gridArr[0][0] = tile 1###
    firstClickTile = {(y * yDimension) + x + 1}
### print(set([a for a in range(1, tc+1)]) - firstClickTile)
    while len(bombPosList) != bc:
        bombTile = random.choice(list(set([a for a in range(1, tc)]) - set(firstClickTile)))
        if not(bombTile in bombPosList):
            bombPosList.append(bombTile)

    if LEA_MODE == True:
        bombPosList = [19, 20, 21, 25, 26, 27, 33, 37, 39, 43, 47, 53, 59, 62, 74, 77, 89, 93, 103, 109, 117, 125, 131, 141, 145, 157, 159, 173]

### print(f"Bomb positions: {bombPosList}")
    #creates list of all tiles, to have thier values (bomb and bombTouchCount added)
    tileList = []
    for i in range(tc):
        tileList.append(str(0))

    #replaces bomb position names with BOMB
    for bombPos in bombPosList:
        tileList[bombPos-1] = "BOMB"

    #converts list into array, with each element corresponding to tile position
    listCount = xDimension
    global gridArr
    gridArr = np.empty((0,listCount))
    rangeStart = 0
    rangeStop = xDimension
    for listNum in range(yDimension):
        arrayRow = np.array(tileList[rangeStart:rangeStop])#builds slice of list into 1D array)
        rangeStart = rangeStop
        rangeStop += xDimension
        gridArr = np.vstack((gridArr, arrayRow)) #appends 1D row array onto 2D full grid array

    #updates total bombs adjacent values
    bombXPos = np.where(gridArr == "BOMB")[1]
    bombYPos = np.where(gridArr == "BOMB")[0]

    for bomb in range(BOMB_COUNT):
            updateNumberTiles(bombXPos[bomb], bombYPos[bomb])

### print(gridArr)

def loss():
    #reveals all bombs
    bombXPos = np.where(gridArr == 'BOMB')[1]
    bombYPos = np.where(gridArr == 'BOMB')[0]
    for bomb in range(BOMB_COUNT):
        xPos = bombXPos[bomb]
        yPos = bombYPos[bomb]
        revealSquare(xPos, yPos, gridArr[yPos][xPos])

def win(gwidth, gheight):
    font = pg.font.SysFont('Arial', 100, bold=True)
    win_text = font.render('YOU WIN!', True, 'Green')
    win_textbox = win_text.get_rect()
    win_textbox.center = ((gwidth // 2), (gheight // 2 + GRID_MENU_HEIGHT))
    pg.draw.rect(SCREEN, (00, 00, 00), win_textbox, width=-1)
    SCREEN.blit(win_text, win_textbox)

def drawMenu(xd, yd):
    #creates menu screen
    global MENU
    MENU = pg.display.set_mode((xd, yd))
    MENU.fill((128,128,128))
    pg.display.set_caption('Minesweeper Menu')

    #creates text
    #title
    font = pg.font.SysFont('Arial', 65, bold=True)
    title_text = font.render('Minesweeper', True, 'red')
    title_textbox = title_text.get_rect()
    title_textbox.center = (250, 50)
    pg.draw.rect(MENU, (00, 00, 00), title_textbox, width=-1)
    MENU.blit(title_text, title_textbox)

    #version
    font = pg.font.SysFont('Arial', 25, bold=True)
    version_text = font.render(VERSION_NUMBER, True, 'black')
    version_textbox = version_text.get_rect()
    version_textbox.topleft = title_textbox.bottomleft
    pg.draw.rect(MENU, (00, 00, 00), version_textbox, width=-1)
    MENU.blit(version_text, version_textbox)

    #signature
    font = pg.font.SysFont('Arial', 25, bold=True)
    sig_text = font.render("By: Gavin Brady", True, 'black')
    sig_textbox = sig_text.get_rect()
    sig_textbox.topright = title_textbox.bottomright
    pg.draw.rect(MENU, (00, 00, 00), sig_textbox, width=-1)
    MENU.blit(sig_text, sig_textbox)

    #difficulty heading
    font = pg.font.SysFont('Arial', 50, bold=True)
    difficulty_text = font.render("Difficulty", True, 'black')
    difficulty_textbox = difficulty_text.get_rect()
    difficulty_textbox.center = (150, 180)
    pg.draw.rect(MENU, (00, 00, 00), difficulty_textbox, width=-1)
    MENU.blit(difficulty_text, difficulty_textbox)

    #Creates buttons
    #beginner
    global BEGINNER_BUTTON
    font = pg.font.SysFont('Arial', 45, bold=True)
    beginner_text = font.render('Beginner', True, 'white')
    beginner_textbox = beginner_text.get_rect()
    BEGINNER_BUTTON = pg.Rect(0,0,275,60)
    beginner_textbox.center = (150, 250)
    BEGINNER_BUTTON.center = beginner_textbox.center
    pg.draw.rect(MENU, (255, 00, 00), beginner_textbox)
    pg.draw.rect(MENU, (255, 00, 00), BEGINNER_BUTTON)
    MENU.blit(beginner_text, beginner_textbox)
    #intermediate
    global INTERMEDIATE_BUTTON
    intermediate_text = font.render('Intermediate', True, 'white')
    intermediate_textbox = intermediate_text.get_rect()
    INTERMEDIATE_BUTTON = pg.Rect(0,0,275,60)
    intermediate_textbox.center = (150, 320)
    INTERMEDIATE_BUTTON.center = intermediate_textbox.center
    pg.draw.rect(MENU, (255, 00, 00), intermediate_textbox)
    pg.draw.rect(MENU, (255, 00, 00), INTERMEDIATE_BUTTON)
    MENU.blit(intermediate_text, intermediate_textbox)
    #hard
    global EXPERT_BUTTON
    expert_text = font.render('Expert', True, 'white')
    expert_textbox = expert_text.get_rect()
    EXPERT_BUTTON = pg.Rect(0,0,275,60)
    expert_textbox.center = (150, 390)
    EXPERT_BUTTON.center = expert_textbox.center
    pg.draw.rect(MENU, (255, 00, 00), expert_textbox)
    pg.draw.rect(MENU, (255, 00, 00), EXPERT_BUTTON)
    MENU.blit(expert_text, expert_textbox)

    #custom button
    global CUSTOM_BUTTON
    custom_text = font.render('Custom', True, "white")
    custom_textbox = custom_text.get_rect()
    CUSTOM_BUTTON = pg.Rect(0,0,275,60)
    custom_textbox.center = (150, 460)
    CUSTOM_BUTTON.center = custom_textbox.center
    pg.draw.rect(MENU, (255, 00, 00), custom_textbox)
    pg.draw.rect(MENU, (255, 00, 00), CUSTOM_BUTTON)
    MENU.blit(custom_text, custom_textbox)

    #custom input buttons
    font = pg.font.SysFont('Arial', 22, bold=True)
    #xdimension button
    global XDIMENSION_BUTTON
    xdimension_text = font.render('X-Dimension', True, "black")
    xdimension_textbox = xdimension_text.get_rect()
    XDIMENSION_BUTTON = pg.Rect(0,0,100,50)
    xdimension_textbox.center = (90, 515)
    XDIMENSION_BUTTON.midtop = xdimension_textbox.midbottom
    pg.draw.rect(MENU, (00, 00, 00), xdimension_textbox,width=-1)
    pg.draw.rect(MENU, (255, 255, 255), XDIMENSION_BUTTON)
    MENU.blit(xdimension_text, xdimension_textbox)

    #ydimension button
    global YDIMENSION_BUTTON
    ydimension_text = font.render('Y-Dimension', True, "black")
    ydimension_textbox = ydimension_text.get_rect()
    YDIMENSION_BUTTON = pg.Rect(0,0,100,50)
    ydimension_textbox.center = (250, 515)
    YDIMENSION_BUTTON.midtop = ydimension_textbox.midbottom
    pg.draw.rect(MENU, (00, 00, 00), ydimension_textbox,width=-1)
    pg.draw.rect(MENU, (255, 255, 255), YDIMENSION_BUTTON)
    MENU.blit(ydimension_text, ydimension_textbox)

    #bomb count button
    global BOMB_COUNT_BUTTON
    bomb_count_text = font.render('Bomb Count', True, "black")
    bomb_count_textbox = bomb_count_text.get_rect()
    BOMB_COUNT_BUTTON = pg.Rect(0,0,100,50)
    bomb_count_textbox.center = (410, 515)
    BOMB_COUNT_BUTTON.midtop = bomb_count_textbox.midbottom
    pg.draw.rect(MENU, (00, 00, 00), bomb_count_textbox,width=-1)
    pg.draw.rect(MENU, (255, 255, 255), BOMB_COUNT_BUTTON)
    MENU.blit(bomb_count_text, bomb_count_textbox)

def typeInputs(button):
    #sets initial variables
    typing = True
    font = pg.font.SysFont('Arial', 30, bold=True)
    text = ''
    global POSSIBLE_DIMENSION
    POSSIBLE_DIMENSION = False

    while typing:
        for event in pg.event.get():
            #allows for quit while typing
            if event.type == pg.QUIT:  
                running = False
                menu_open = False
                typing = False
            if event.type == pg.KEYDOWN:
                #removes final character if backspace pressed
                if event.key == pg.K_BACKSPACE:
                    if text != '':
                        text = text[:-1]
                #ends typing on return keypress
                elif event.key == pg.K_RETURN:
                    typing = False
                #updates text if enterred integer between 0 and 9 inclusive
                elif 0 <= int(event.unicode) <= 9:
                    text += event.unicode

                #redraws input box to hide shown text
                pg.draw.rect(MENU, (255, 255, 255), button)
                if text != '':
                    if (button == XDIMENSION_BUTTON or button == YDIMENSION_BUTTON) and int(text) > 30:
                        shown_text = font.render(text, True, 'red')
                        POSSIBLE_DIMENSION = False
                    else: 
                        shown_text = font.render(text, True, "black")
                        POSSIBLE_DIMENSION = True
                    MENU.blit(shown_text, button)
                pg.display.update()
    if text == '':
        text = 0
    return(int(text))
  
                
#menu settings
MENU_X_DIMENSION = 500
MENU_Y_DIMENSION = 600

#boolean setup
running = True
game_open = False
game_started = False
menu_open = True

#changing block size may mess up some ways the grid is drawn/if fits on screen
blockSize = 50
                 
while running:
    #menu usage
    drawMenu(MENU_X_DIMENSION, MENU_Y_DIMENSION)
    CUSTOM_OPEN = False
    LEA_MODE = False
    POSSIBLE_DIMENSION = False
    while menu_open == True:
        for event in pg.event.get():
            if event.type == pg.QUIT:  
                running = False
                menu_open = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if BEGINNER_BUTTON.collidepoint(pg.mouse.get_pos()):
                    #grid setup
                    GRID_HEIGHT = 500
                    GRID_WIDTH = 500
                    yDimension = GRID_HEIGHT // blockSize
                    xDimension = GRID_WIDTH // blockSize
                    tileCount = xDimension * yDimension
                    BOMB_COUNT = 10
                    game_open = True
                    menu_open = False
                elif INTERMEDIATE_BUTTON.collidepoint(pg.mouse.get_pos()):
                    #grid setup
                    GRID_HEIGHT = 800
                    GRID_WIDTH = 800
                    yDimension = GRID_HEIGHT // blockSize
                    xDimension = GRID_WIDTH // blockSize
                    tileCount = xDimension * yDimension
                    BOMB_COUNT = 40
                    game_open = True
                    menu_open = False
                elif EXPERT_BUTTON.collidepoint(pg.mouse.get_pos()):
                    #grid setup
                    GRID_HEIGHT = 800
                    GRID_WIDTH = 1500
                    yDimension = GRID_HEIGHT // blockSize
                    xDimension = GRID_WIDTH // blockSize
                    tileCount = xDimension * yDimension
                    BOMB_COUNT = 99
                    game_open = True
                    menu_open = False
                elif CUSTOM_BUTTON.collidepoint(pg.mouse.get_pos()):
                    tileCount = xDimension * yDimension
                    if xDimension == 9 and yDimension == 17 and BOMB_COUNT == 22:
                        LEA_MODE = True
                        xDimension = 15
                        yDimension = 13
                        BOMB_COUNT = 28
                        tileCount = xDimension * yDimension
                        GRID_WIDTH = xDimension * blockSize
                        GRID_HEIGHT = yDimension * blockSize
                    if POSSIBLE_DIMENSION == True and BOMB_COUNT < tileCount:
                        game_open = True
                        menu_open = False
                    else:
                        print('Invalid input')
                #checks for typing in inputs
                elif XDIMENSION_BUTTON.collidepoint(pg.mouse.get_pos()):
                    xDimension = typeInputs(XDIMENSION_BUTTON)
                    GRID_WIDTH = xDimension * blockSize
                elif YDIMENSION_BUTTON.collidepoint(pg.mouse.get_pos()):
                    yDimension = typeInputs(YDIMENSION_BUTTON)
                    GRID_HEIGHT = yDimension * blockSize
                elif BOMB_COUNT_BUTTON.collidepoint(pg.mouse.get_pos()):
                    BOMB_COUNT = typeInputs(BOMB_COUNT_BUTTON)                        
                    
        pg.display.update()
    if game_open == True:
        #setup game screen 
        SCREEN_WIDTH = GRID_WIDTH
        GRID_MENU_HEIGHT = 100
        SCREEN_HEIGHT = GRID_HEIGHT + GRID_MENU_HEIGHT
        SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        SCREEN.fill((128,128,128))

        #sets variables
        bombs_remaining = BOMB_COUNT
        unrevealedTiles = tileCount - BOMB_COUNT
    
    #gameplay
    while game_open == True:
        drawGameScreen(SCREEN_WIDTH, SCREEN_HEIGHT, GRID_WIDTH, GRID_HEIGHT)
        for event in pg.event.get():
            if event.type == pg.QUIT:  
                game_open = False
                running = False
                
            if event.type == pg.MOUSEBUTTONDOWN:
                #posX and posY are literal pixel positions (including GRID_MENU_HEIGHT)
                posX, posY = pg.mouse.get_pos()
                #checks if click was on grid
                if posY > GRID_MENU_HEIGHT:
                    #xCoord and yCoord are coordinates of tile on grid
                    xCoord, yCoord = getTileCoords(posX, posY-GRID_MENU_HEIGHT)
###                 print(f"Tile coord pressed: ({xCoord}, {yCoord})")
                    
                    if pg.key.get_pressed()[pg.K_LSHIFT]:
                        if SCREEN.get_at((posX, posY))[:3] == (128, 128, 128):
                            flagSquare(xCoord, yCoord)
                        elif SCREEN.get_at((posX, posY))[:3] == (255, 0, 255):
                            unflagSquare(xCoord, yCoord)
                    
                    elif SCREEN.get_at((posX, posY))[:3] == (128, 128, 128):  
                        #ensures do not start on bomb by generating after click
                        if game_started == False:
                            generateBombs(xCoord, yCoord, BOMB_COUNT, tileCount)
                            game_started = True
                            alive = True  
                        revealSquare(xCoord, yCoord, gridArr[yCoord][xCoord])
                if posY < GRID_MENU_HEIGHT:
                    if MENU_BUTTON.collidepoint(pg.mouse.get_pos()):
                        menu_open = True
                        game_open = False
                        game_started = False
        if unrevealedTiles == 0 and bombs_remaining == 0:
            win(GRID_WIDTH, GRID_HEIGHT)
        pg.display.update()

pg.quit()
print("Program Quit")
