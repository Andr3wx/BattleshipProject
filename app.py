import pygame
import numpy as np
from battleshipNetwork import Network
from spriteClasses import Hit_Miss, Sprite
import ai
import time
import threading


# import battleship
# import battleshipNetwork
# import battleshipServer

# Screen Size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Color Values
black = (0, 0, 0)
white = (255, 255, 255)
lightBlue = (173, 216, 230)
grey = (64, 64, 64)
red = (139, 0, 0)


# functions
def block():
    # Gets total area of the screen and divides it by number of
    blockSize = (SCREEN_WIDTH * SCREEN_HEIGHT) / 64
    # squares in grid
    # Square roots the total area of a single grid to get the base and width
    blockSize = blockSize ** (1 / 2)
    # Shrinks the block size 1.5x of the previously calculated result
    blockSize = blockSize / 1.5
    return blockSize


def drawGrid():
    rowVals = "123456789"
    colVals = "ABCDEFGH"
    blockSize = block()
    # Creates font size of grid coordinates based on block size
    font = pygame.font.SysFont('arial', int(blockSize * .4330127))
    incrementY = blockSize / 2  # Used to set location of where row coordinates should be
    # Used to set location of where column coordinates should be
    incrementX = blockSize / 2
    screenValX = SCREEN_WIDTH * .08
    screenValY = SCREEN_HEIGHT * .11
    counter2 = 0  # Makes sure there is only N number of rows
    gridLocation = {}
    for x in np.arange(screenValX, SCREEN_WIDTH, blockSize):  # x represents row number
        counter1 = 0  # Makes sure there is only N number of Columns
        gridLocation[str(x)] = []
        # y represents column number
        for y in np.arange(screenValY, SCREEN_HEIGHT, blockSize):
            # Adds grid coordinates to grid
            if counter2 == 0 and counter1 == 0:
                for z in range(len(colVals)):
                    # Print values left of rows
                    text = font.render(rowVals[z], True, lightBlue)
                    screen.blit(text, (screenValX - (blockSize * .34641016),
                                       y + incrementY - (blockSize * .25980762)))
                    # Print values above columns
                    text = font.render(colVals[z], True, lightBlue)
                    screen.blit(text, (x + incrementX - (blockSize * .12124356),
                                       screenValY - (blockSize * .51961524)))
                    incrementX += blockSize
                    incrementY += blockSize

            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, lightBlue, rect)  # Fills rectangle
            pygame.draw.rect(screen, black, rect, 1)  # Rectangle border
            counter1 = counter1 + 1
            if len(gridLocation[str(x)]) > 0:
                gridLocation[str(x)].append(y)
            else:
                gridLocation[str(x)] = [y]
            if counter1 == 8:
                # Needed to include area of final block
                gridLocation[str(x)].append(y + blockSize)
                break

        counter2 = counter2 + 1
        if counter2 == 8:
            # Needed to include area of final block
            gridLocation[str(x + blockSize)] = gridLocation[str(x)]
            break
    return gridLocation


def checkIfGrid(position, locationGrid):
    gridKeys = []
    row = -1
    column = -1
    # Puts the row coordinates in a list
    for x in locationGrid:
        gridKeys.append(float(x))
    # Sorts the rows from least to greatest
    gridKeys.sort()
    # Checks to see whether is within grid area
    if gridKeys[0] <= position[0] <= gridKeys[-1]:
        for x in range(len(gridKeys)):
            if gridKeys[x] > position[0]:
                temp = locationGrid[str(gridKeys[x - 1])]
                column = x - 1
                if temp[0] <= position[1] <= temp[-1]:
                    for y in range(len(temp)):
                        if temp[y] > position[1]:
                            row = y - 1
                            break
                if row != -1:
                    break

    return [row, column]


def getRectCoord(cord, locationGrid):
    tempKey = float(-1)
    tempCol = float(-1)
    for x in locationGrid:  # Loops through keys ( Row values )
        if float(x) > cord[0]:  # Once finds key value greater than mouse position
            break  # Ends loop and temp key has previous position
        tempKey = float(x)
    if tempKey != -1:  # Make sure it finds valid location
        temp = locationGrid[str(tempKey)]
        for x in temp:  # Loops through columns in similar fashion as keys above
            if x > cord[1]:
                break
            tempCol = x
    return [tempKey, tempCol]


def mouseHighlight(position, locationGrid, needShips):
    # Checks to see whether mouse is over grid
    gridLoc = checkIfGrid(position, locationGrid)
    if gridLoc[0] != -1 and gridLoc[1] != -1:  # If it is over grid
        # Get the coordinates of which rectangle the mouse is in
        recLoc = getRectCoord(position, locationGrid)
        if recLoc[0] != -1 and recLoc[1] != -1:  # If in a valid box
            drawGrid()
            rect = pygame.Rect(recLoc[0], recLoc[1], block(), block())
            pygame.draw.rect(screen, white, rect)  # Highlights given box
            pygame.draw.rect(screen, black, rect, 1)
            if needShips:
                ship_group_layered.draw(screen)
            pygame.display.update()  # Updates display

    else:  # If mouse not over grid, returns grid to original state and updates display
        drawGrid()
        if needShips:
            ship_group_layered.draw(screen)
        pygame.display.update()


def shipSize(ship):
    if ship == corvette:
        return 2
    elif ship == sub:
        return 3
    elif ship == destroyer:
        return 4
    elif ship == carrier:
        return 5


def checkSpot(shipLoc, ship, recLoc, color):
    for i in shipLoc:  # Loops through ships
        if i == ship:  # If current key is current ship, skip
            continue
        else:
            # Other ship than currents rectangular coordinates
            temp = shipLoc[i]
            otherShipBeg = temp[0]  # Other ship begin coordinates
            otherShipEnd = temp[-1]  # Other ship end coordinates
            curShipBeg = recLoc[0]
            # Takes first and last coordinates of current ship
            curShipEnd = recLoc[-1]
            # Only comparing x coordinates right now
            if otherShipBeg != -1 or otherShipEnd != -1:
                if otherShipBeg[0] <= curShipBeg[0] <= otherShipEnd[0] \
                        and otherShipBeg[1] == curShipBeg[1] == otherShipEnd[1]:
                    color = red
                    break
                elif otherShipBeg[0] <= curShipEnd[0] <= otherShipEnd[0] \
                        and otherShipBeg[1] == curShipEnd[1] == otherShipEnd[1]:
                    color = red
                    break
                elif curShipBeg[0] <= otherShipBeg[0] <= curShipEnd[0] \
                        and curShipBeg[1] == otherShipBeg[1] == curShipEnd[1]:
                    color = red
                    break
    return color, shipLoc


def highlightedBoxes(ship, recLoc, locationGrid, color):
    for i in range(shipSize(ship)):
        # Goes through all coordinates to know which blocks to highlight if part of ship is off grid
        gridLoc = checkIfGrid(recLoc[i], locationGrid)
        curLoc = recLoc[i]  # Current location of block being looked at
        # If block is on the grid, highlights box on grid
        if gridLoc[0] != -1 and gridLoc[1] != -1:
            rect = pygame.Rect(curLoc[0], curLoc[1], block(), block())
            pygame.draw.rect(screen, color, rect)  # Highlights given box
            pygame.draw.rect(screen, black, rect, 1)


def shipHighlight(position, locationGrid, ship, shipLoc):
    recLoc = []
    color = white
    drawGrid()
    for i in range(shipSize(ship)):  # Determines how many boxes it needs to highlight
        # ! Need to modify once allow ship rotation
        # Gets rectangular coordinates
        recLoc.append(getRectCoord(position, locationGrid))
        gridLoc = checkIfGrid(position, locationGrid)
        # If orientation is horizontal, gets the block positions in the x direction
        position = (position[0] + block(), position[1])
        # If ship goes off the grid then blocks will highlight red
        if gridLoc[0] == -1 or gridLoc[1] == -1:
            color = red
    if color == white:
        # Checks whether another ship occupies spot
        color, shipLoc = checkSpot(shipLoc, ship, recLoc, color)

    highlightedBoxes(ship, recLoc, locationGrid, color)

    ship_group_layered.draw(screen)
    pygame.display.update()

    if color == red:
        shipLoc[ship] = [-1, -1]
        return False, shipLoc
    shipLoc[ship] = recLoc
    tempCord = shipLoc[ship]
    endCord = tempCord[1]
    if ship == sub:
        endCord[0] = endCord[0] + block()
    elif ship == destroyer:
        endCord[0] = endCord[0] + (2*block())
    elif ship == carrier:
        endCord[0] = endCord[0] + (3*block())
    tempCord[1] = endCord
    shipLoc[ship] = tempCord

    return True, shipLoc


def placingShips(position):
    if corvette.rect.collidepoint(position):
        corvette.set_location(position)
        return corvette
    elif sub.rect.collidepoint(position):
        sub.set_location(position)
        return sub
    elif destroyer.rect.collidepoint(position):
        destroyer.set_location(position)
        return destroyer
    elif carrier.rect.collidepoint(position):
        carrier.set_location(position)
        return carrier
    else:
        return None


# When user releases mouse and stops dragging ship, places ship into proper location
def placingShipsRelease(position, locationGrid, sprite, onGrid):
    positionShip = getRectCoord(position, locationGrid)
    if sprite == corvette:
        positionShip[0] = positionShip[0] + block()
    elif sprite == sub:
        positionShip[0] = positionShip[0] + (block() * 1.5)
    elif sprite == destroyer:
        positionShip[0] = positionShip[0] + (2 * block())
    elif sprite == carrier:
        positionShip[0] = positionShip[0] + (2.4 * block())

    positionShip[1] = positionShip[1] + (block() * .485)

    if onGrid:
        sprite.set_location(positionShip)
    else:
        sprite.set_location(sprite.getStartLoc())


# When user clicks and drags ship to location
def shipIsHeld(position, sprite):
    drawGrid()
    sprite.set_location(position)
    ship_group_layered.draw(screen)
    pygame.display.update()


def moveShipScreen(placing, run, grid, curSprite, shipLoc, network, screenN, otherPlayerShips, gameType):
    pos = pygame.mouse.get_pos()
    if placing:
        shipIsHeld(pos, curSprite)
        allowToPlace, shipLoc = shipHighlight(pos, grid, curSprite, shipLoc)

    allPlaced = True
    # print(shipLoc)
    for x in shipLoc:
        temp = shipLoc[x]
        if temp[0] == -1 or temp[1] == -1:
            allPlaced = False
            break
    if allPlaced and not placing:
        if gameType == False:

            network.send(convertShipToStr(shipLoc))
        # time.sleep(1)
            screenN = network.receive()
            otherPlayerShips = network.receive()
            print(otherPlayerShips)
            otherPlayerShips = convertStrToShip(otherPlayerShips)
            print(otherPlayerShips)
            return placing, run, grid, curSprite, shipLoc, screenN, otherPlayerShips
        else:
            screenN = "Taking Shot"
            return placing, run, grid, curSprite, shipLoc, screenN, otherPlayerShips

        print(screenN)

        # print(screenN)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # press ESC to quit
                run = False
        elif event.type == pygame.MOUSEBUTTONUP:
            if placing:
                placingShipsRelease(pos, grid, curSprite, allowToPlace)
                placing = False
            # print(checkIfGrid(pos, grid)[0], checkIfGrid(pos, grid)[1])
        elif event.type == pygame.MOUSEBUTTONDOWN:
            curSprite = placingShips(pos)
            if curSprite is not None:
                placing = True

    # Any mouse movement
    if len(grid.keys()) != 0:
        if not placing:
            mouseHighlight(pos, grid, True)

    # RGB background
    screen.fill(black)
    if len(grid.keys()) <= 0:
        grid = drawGrid()
        ship_group_layered.draw(screen)
        pygame.display.update()

    return placing, run, grid, curSprite, shipLoc, screenN, otherPlayerShips


def takeShotScreen(run, grid, clicked, network, screenN, otherPlayerShips, hitWinCount, gameType):
    is_hit = True
    pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # press ESC to quit
                run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if checkIfGrid(pos, grid)[0] != -1 and checkIfGrid(pos, grid)[1] != -1:
                exactSpot = str(getRectCoord(pos, grid)[
                                0]) + ',' + str(getRectCoord(pos, grid)[1])
                # print(otherPlayerShips)
                is_hit = checkIfHitOther(
                    otherPlayerShips, getRectCoord(pos, grid))
                if gameType == True:
                    # Pai.set_hit(is_hit)
                    screenN = 'Other Player'
                else:

                    network.send(exactSpot)
                    screenN = 'Other Player'

                #   screenN = #! Set to idle screen
            # send to other player to see if hit or miss

            if is_hit:
                drawGrid()
                hit = Hit_Miss("hit")
                hitWinCount += 1
                if checkIfMultWin(hitWinCount):
                    if gameType == False:
                        print("Player: ", network.getP(), " Wins!")
                        run = False
                    else:
                        print("You Win!")
                        run = False
                positionHit = getRectCoord(pos, grid)
                hit.set_location(positionHit)
                hit_miss_group_layered.add(hit)
                hit_miss_group_layered.draw(screen)
                clicked = True
                pygame.display.update()

            else:
                drawGrid()
                miss = Hit_Miss("miss")
                positionMiss = getRectCoord(pos, grid)
                miss.set_location(positionMiss)
                hit_miss_group_layered.add(miss)
                hit_miss_group_layered.draw(screen)
                clicked = True
                pygame.display.update()

    # Any mouse movement
    if len(grid.keys()) != 0 and not clicked:
        mouseHighlight(pos, grid, False)

    if screenN == 'Other Player':
        time.sleep(3)

    # RGB background
    screen.fill(black)
    grid = drawGrid()
    hit_miss_group_layered.draw(screen)
    pygame.display.update()

    return run, grid, clicked, screenN, hitWinCount


def otherPlayerTurnScreen(screenN, shipLoc, network, gridLoc, run, gameType):
    drawGrid()
    ship_group_layered.draw(screen)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # press ESC to quit
                run = False
    shotSpot = []
    if not gameType:
        getShot = network.receive()
        # print(getShot)
        getShot = getShot.split(',')
        shotSpot.append(float(getShot[0]))
        shotSpot.append(float(getShot[1]))
        print(shotSpot[0], "     ", shotSpot[1])
    else:
        getShot = Pai.make_decision()
        print(getShot)
        shotSpot.append(float(getShot[0]))
        shotSpot.append(float(getShot[1]))
    rect = pygame.Rect(shotSpot[0], shotSpot[1], block(), block())
    pygame.draw.rect(screen, red, rect)  # Highlights given box
    pygame.draw.rect(screen, black, rect, 1)
    pygame.display.update()
    time.sleep(3)
    screenN = 'Taking Shot'
    # print(screenN)

    # counter += 1
    # if counter == 20:
    #     screenN = 'Placing Ships'
    return screenN, run


def convertShipToStr(shipLoc):
    toString = ""
    for x in shipLoc:
        if x == corvette:
            toString += 'corvette'
        elif x == sub:
            toString += 'sub'
        elif x == destroyer:
            toString += 'destroyer'
        elif x == carrier:
            toString += 'carrier'

        toString += '/'
        temp = shipLoc[x]
        toString += str(temp[0])
        toString += '/'
        toString += str(temp[1])
        toString += '/'
    return toString


def convertStrToShip(strShips):
    otherPlayer = {}
    listShips = strShips.split('/')
    count = 0
    for x in listShips:
        if count == 0:
            tempKey = x
            otherPlayer[tempKey] = []
            count += 1
        elif count == 1:
            cord = x.split(',')
            otherPlayer[tempKey].append(
                [float(cord[0][1:]), float(cord[1][:-1])])
            count += 1
        elif count == 2:
            cord = x.split(',')
            otherPlayer[tempKey].append(
                [float(cord[0][1:]), float(cord[1][:-1])])
            count = 0
    return otherPlayer


# Parameter is the other player ship location dict
def checkIfHitOther(shipDic, shotPos):
    # print(shipDic)
    for x in shipDic:
        temp = shipDic[x]
        # print(temp)
        if len(temp) > 1:
            temp1 = temp[0]     # Beginning ship coordinates
            temp2 = temp[1]     # End ships coordinates
            # If y coordinates are the same for ship location and shot location
            print('Ship beginning row coordinate: ', temp1[1])
            print('Shot row coordinate: ', shotPos[1])
            print('Ship end row coordinate: ', )
            if temp1[1] == shotPos[1]:
                print('in')
                if x == 'corvette':
                    if temp1[0] <= shotPos[0] <= temp2[0]:
                        return True
                elif x == 'sub':
                    if temp1[0] <= shotPos[0] <= temp2[0]:
                        return True
                elif x == 'destroyer':
                    if temp1[0] <= shotPos[0] <= temp2[0]:
                        return True
                elif x == 'carrier':
                    if temp1[0] <= shotPos[0] <= temp2[0]:
                        return True
    return False


def checkIfMultWin(hitCount):
    if hitCount == 14:
        return True
    else:
        return False


def mainMenu():

    # defining a font
    smallfont = pygame.font.SysFont('Corbel', 35)

    # rendering a text written in
    # this font
    quitText = smallfont.render('quit', True, black)
    playSingle = smallfont.render('single player', True, black)
    playMulti = smallfont.render('multiplayer', True, black)

    while True:

        screen.fill((60, 25, 60))

        # stores the (x,y) coordinates into
        # the variable as a tuple
        mouse = pygame.mouse.get_pos()

        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                pygame.quit()

            # checks if a mouse is clicked
            if ev.type == pygame.MOUSEBUTTONDOWN:

                # if the mouse is clicked on the
                # button the game is terminated
                if SCREEN_WIDTH / 2 <= mouse[0] <= SCREEN_WIDTH / 2 + 140 and SCREEN_HEIGHT / 2 <= mouse[1] <= SCREEN_HEIGHT / 2 + 40:
                    run = False
                    screenName = "Placing Ships"
                    single = True
                    return screenName, single, run

                elif SCREEN_WIDTH / 2 <= mouse[0] <= SCREEN_WIDTH / 2 + 140 and SCREEN_HEIGHT / 2 - 80 <= mouse[1] <= SCREEN_HEIGHT / 2 - 40:
                    screenName = "Placing Ships"
                    single = True
                    run = True
                    return screenName, single, run

                elif SCREEN_WIDTH / 2 <= mouse[0] <= SCREEN_WIDTH / 2 + 140 and SCREEN_HEIGHT / 2 - 40 <= mouse[1] <= SCREEN_HEIGHT / 2:
                    screenName = "Placing Ships"
                    single = False
                    run = True
                    #start = multiplayerSubOptions()

                    return screenName, single, run

                # fills the screen with a color

        # if mouse is hovered on a button it
        # changes to lighter shade
        if SCREEN_WIDTH / 2 <= mouse[0] <= SCREEN_WIDTH / 2 + 140 and SCREEN_HEIGHT / 2 <= mouse[1] <= SCREEN_HEIGHT / 2 + 40:
            pygame.draw.rect(screen, white, [
                             SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 180, 40])

        else:
            pygame.draw.rect(screen, lightBlue, [
                             SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 180, 40])

        if SCREEN_WIDTH / 2 <= mouse[0] <= SCREEN_WIDTH / 2 + 140 and SCREEN_HEIGHT / 2 - 80 <= mouse[1] <= SCREEN_HEIGHT / 2 - 40:
            pygame.draw.rect(screen, white, [
                             SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 80, 180, 40])

        else:
            pygame.draw.rect(screen, lightBlue, [
                             SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 80, 180, 40])

        if SCREEN_WIDTH / 2 <= mouse[0] <= SCREEN_WIDTH / 2 + 140 and SCREEN_HEIGHT / 2 - 40 <= mouse[1] <= SCREEN_HEIGHT / 2:
            pygame.draw.rect(screen, white, [
                             SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 40, 180, 40])

        else:
            pygame.draw.rect(screen, lightBlue, [
                             SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 40, 180, 40])

            # superimposing the text onto our button
        screen.blit(quitText, (SCREEN_WIDTH / 2 + 20, SCREEN_HEIGHT / 2))
        screen.blit(playSingle, (SCREEN_WIDTH /
                    2 + 20, SCREEN_HEIGHT / 2 - 80))
        screen.blit(playMulti, (SCREEN_WIDTH / 2 + 20, SCREEN_HEIGHT / 2 - 40))

        # updates the frames of the game
        pygame.display.update()


def startServer():
    import battleshipServer


def multiplayerSubOptions():
    # defining a font
    smallfont = pygame.font.SysFont('Corbel', 35)

    # rendering a text written in
    # this font
    startGame = smallfont.render('Start Game', True, black)
    joinGame = smallfont.render('Join game', True, black)
    while True:
        # stores the (x,y) coordinates into
        # the variable as a tuple
        mouse = pygame.mouse.get_pos()
        # fills the screen with a color
        screen.fill((60, 25, 60))

        for ev in pygame.event.get():
            # checks if a mouse is clicked
            if ev.type == pygame.MOUSEBUTTONDOWN:

                # if the mouse is clicked on the
                # button the game is terminated
                # Start game
                if SCREEN_WIDTH / 2 <= mouse[0] <= SCREEN_WIDTH / 2 + 140 and SCREEN_HEIGHT / 2 <= mouse[1] <= SCREEN_HEIGHT / 2 + 40:
                    start = False
                    return start

                # Join game
                elif SCREEN_WIDTH / 2 <= mouse[0] <= SCREEN_WIDTH / 2 + 140 and SCREEN_HEIGHT / 2 - 80 <= mouse[1] <= SCREEN_HEIGHT / 2 - 40:
                    start = True
                    return start
                    # fills the screen with a color
                screen.fill((60, 25, 60))

                # if mouse is hovered on a button it
                # changes to lighter shade
                # Start game
                if SCREEN_WIDTH / 2 <= mouse[0] <= SCREEN_WIDTH / 2 + 140 and SCREEN_HEIGHT / 2 <= mouse[1] <= SCREEN_HEIGHT / 2 + 40:
                    pygame.draw.rect(
                        screen, white, [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 180, 40])

                else:
                    pygame.draw.rect(
                        screen, lightBlue, [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 180, 40])

                # Join game
                if SCREEN_WIDTH / 2 <= mouse[0] <= SCREEN_WIDTH / 2 + 140 and SCREEN_HEIGHT / 2 - 80 <= mouse[1] <= SCREEN_HEIGHT / 2 - 40:
                    pygame.draw.rect(
                        screen, white, [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 80, 180, 40])

                else:
                    pygame.draw.rect(
                        screen, lightBlue, [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 80, 180, 40])

                    # superimposing the text onto our button
                screen.blit(joinGame, (SCREEN_WIDTH /
                            2 + 20, SCREEN_HEIGHT / 2))
                screen.blit(startGame, (SCREEN_WIDTH / 2 +
                            20, SCREEN_HEIGHT / 2 - 80))
                # updates the frames of the game
                pygame.display.update()


if __name__ == "__main__":
    counter = 0
    running = True
    canPlace = False  # Indicates whether player is in the process of choosing a ship position
    gridCord = {}  # Indicates the row rectangle coordinates and stores the column coordinates within the key
    currentSprite = None
    click = False
    hitCount = 0
    screenName = "Placing Ships"

    pygame.init()  # initialize pygame
    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT))  # create screen
    pygame.display.set_caption("Battleship")  # set caption
    icon = pygame.image.load('images/battleship.png')  # set game icon
    pygame.display.set_icon(icon)
    screenName, gameType, running = mainMenu()

    if gameType:
        Pai = ai.Player()
        n = False
        gridCord = drawGrid()
        # print(gridCord)
        Pai.set_grid(gridCord)
    else:
        server = multiplayerSubOptions()
        if server:

            t1 = threading.Thread(target=startServer, name='t1')
            t1.start()
        n = Network()
    # n.send("Check")
        player = n.getP()
        print("you are player: ", player)
        screenName = n.receive()

    #n = False
    # print(screenName)
    # n.send("Test")

    # create ship objects
    img_X = SCREEN_WIDTH * .65
    corvette = Sprite('corvette', img_X, SCREEN_HEIGHT * .1)
    sub = Sprite('sub', img_X, SCREEN_HEIGHT * .3)
    destroyer = Sprite('destroyer', img_X, SCREEN_HEIGHT * .5)
    carrier = Sprite('carrier', img_X, SCREEN_HEIGHT * .7)

    # Ship group
    ship_group_layered = pygame.sprite.LayeredUpdates(
        [corvette, sub, destroyer, carrier])
    # Group of Hit and Miss instances
    hit_miss_group_layered = pygame.sprite.LayeredUpdates([])

    shipPos = {corvette: [-1, -1], sub: [-1, -1],
               destroyer: [-1, -1], carrier: [-1, -1]}
    opposingShipPos = {}

    # if ai:
    #     Pai = ai.Player()
    # else:
    #     is_ai = False
    if gameType:
        Pai.place_ships(block())
        opposingShipPos = Pai.get_ship_locations()

    while running:
       # print('Player Ships: ', shipPos)
        #  Placing ships
        if screenName == "Placing Ships":
            if gameType == False:
                canPlace, running, gridCord, currentSprite, shipPos, screenName, opposingShipPos = moveShipScreen(
                    canPlace, running, gridCord, currentSprite, shipPos, n, screenName, opposingShipPos, gameType)
            if gameType == True:

                canPlace, running, gridCord, currentSprite, shipPos, screenName, opposingShipPos = moveShipScreen(
                    canPlace, running, gridCord, currentSprite, shipPos, n, screenName, opposingShipPos, gameType)
                # Pai.set_grid(gridCord)
                # Pai.place_ships(block())
                # opposingShipPos = Pai.get_ship_locations()

        elif screenName == "Taking Shot":
            print(shipPos)
            # break
            if gameType == True:

                running, gridCord, click, screenName, hitCount = takeShotScreen(running, gridCord, click, n, screenName,
                                                                                opposingShipPos, hitCount, gameType)
                #gridCord = Pai.make_decision()
            else:
                running, gridCord, click, screenName, hitCount = takeShotScreen(running, gridCord, click, n, screenName,
                                                                                opposingShipPos, hitCount, gameType)
        elif screenName == "Other Player":
            screenName, running = otherPlayerTurnScreen(
                screenName, shipPos, n, gridCord, running, gameType)

        # screenName = n.receive()
