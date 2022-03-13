import pygame
import numpy as np


# import battleship
# import battleshipNetwork
# import battleshipServer

# ! Make screen size global constants

# functions
def block():
    blockSize = (800 * 600) / 64  # Gets total area of the screen and divides it by number of squares in grid
    blockSize = blockSize ** (1 / 2)  # Square roots the total area of a single grid to get the base and width
    blockSize = blockSize / 1.5  # Shrinks the block size 1.5x of the previously calculated result
    return blockSize


def drawGrid():
    blockSize = block()
    counter2 = 0  # Makes sure there is only N number of rows
    gridLocation = {}
    for x in np.arange(140, 800, blockSize):    # x represents row number
        counter1 = 0  # Makes sure there is only N number of Columns
        gridLocation[str(x)] = []
        for y in np.arange(75, 600, blockSize): # y represents column number
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)
            counter1 = counter1 + 1
            if len(gridLocation[str(x)]) > 0:
                gridLocation[str(x)].append(y)
            else:
                gridLocation[str(x)] = [y]
            if counter1 == 8:
                gridLocation[str(x)].append(y + blockSize)  # Needed to include area of final block
                break
        counter2 = counter2 + 1
        if counter2 == 8:
            gridLocation[str(x + blockSize)] = gridLocation[str(x)]     # Needed to include area of final block
            break
    return gridLocation


def checkIfGrid(position, gridLocation):
    gridKeys = []
    row = -1
    column = -1
    # Puts the row coordinates in a list
    for x in gridLocation:
        gridKeys.append(float(x))
    # Sorts the rows from least to greatest
    gridKeys.sort()
    # Checks to see whether is within grid area
    if gridKeys[0] <= position[0] <= gridKeys[-1]:
        for x in range(len(gridKeys)):
            if gridKeys[x] > position[0]:
                temp = gridLocation[str(gridKeys[x - 1])]
                column = x - 1
                if temp[0] <= position[1] <= temp[-1]:
                    for y in range(len(temp)):
                        if temp[y] > position[1]:
                            row = y - 1
                            break
                if row != -1:
                    break

    return [row, column]


def getRectCoord(cord, gridLocation):
    tempKey = float(-1)
    tempCol = float(-1)
    for x in gridLocation:  # Loops through keys ( Row values )
        if float(x) > cord[0]:  # Once finds key value greater than mouse position
            break   # Ends loop and temp key has previous position
        tempKey = float(x)
    if tempKey != -1:   # Make sure it finds valid location
        temp = gridLocation[str(tempKey)]
        for x in temp:  # Loops through columns in similar fashion as keys above
            if x > cord[1]:
                break
            tempCol = x
    return [tempKey, tempCol]


def mouseHighlight(position, gridLocation):
    # Checks to see whether mouse is over grid
    gridLoc = checkIfGrid(pos, grid)
    if gridLoc[0] != -1 and gridLoc[1] != -1:  # If it is over grid
        recLoc = getRectCoord(pos, grid)  # Get the coordinates of which rectangle the mouse is in
        if recLoc[0] != -1 and recLoc[1] != -1:  # If in a valid box
            drawGrid()
            rect = pygame.Rect(recLoc[0], recLoc[1], block(), block())
            pygame.draw.rect(screen, (255, 255, 255), rect)  # Highlights given box
            pygame.display.update()  # Updates display

    else:  # If mouse not over grid, returns grid to original state and updates display
        drawGrid()
        pygame.display.update()


if __name__ == "__main__":
    pygame.init()  # initialize pygame
    screen = pygame.display.set_mode((800, 600))  # create screen
    pygame.display.set_caption("Battleship")  # set caption
    icon = pygame.image.load('battleship.png')  # set game icon
    pygame.display.set_icon(icon)

    running = True
    grid = {}
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # press ESC to quit
                    running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                # ! Change this later to specific screen where grid shows
                pos = pygame.mouse.get_pos()
                print(checkIfGrid(pos, grid)[0], checkIfGrid(pos, grid)[1])
        # Any mouse movement
        # ! Later make this only on grid screen
        if len(grid.keys()) != 0:
            pos = pygame.mouse.get_pos()
            mouseHighlight(pos, grid)

        # RGB background
        screen.fill((173, 216, 230))
        if len(grid.keys()) <= 0:
            grid = drawGrid()
            pygame.display.update()
