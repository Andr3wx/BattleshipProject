"""
'.' represents empty space on board
'X' represents part of ship occupies location
'H' indicates part of ship is hit

"""


class Battleships:
    # The number of ships every player will have
    numOfShips = 4
    # Ship positions
    shipPositions = dict()
    # Counts how many times a ship has been hit
    shipHit = dict()
    # Key List for ship names
    keyList = ['A', 'B', 'C', 'D']
    # Row and Column amount
    rowColumn = 8
    # Creates board of players ships
    playerGrid = []

    def __init__(self):
        # Add keys to dictionary
        for x in self.keyList:
            self.shipPositions[x] = []
            self.shipHit[x] = []
        # Creates empty game board
        for x in range(self.rowColumn):
            self.playerGrid.append(['.'] * self.rowColumn)

    def getNumShips(self):
        return self.numOfShips

    def getPlayerGrid(self):
        return self.playerGrid

    def placeShip(self, ship, begSpot, endSpot):
        temp = self.playerGrid[begSpot[1]]
        # if x coordinates of begin and end are same creates vertical ship in grid
        if begSpot[0] == endSpot[0]:
            for x in range(begSpot[1], endSpot[1] + 1):
                if temp[begSpot[0]] == '.':
                    temp[begSpot[0]] = 'X'
                    temp = self.playerGrid[x]
                else:
                    return False
        # if beginning and ending y coordinates are the same creates horizontal ship in grid
        elif begSpot[1] == endSpot[1]:
            for x in range(begSpot[0], endSpot[0]):
                if temp[x] == '.':
                    temp[x] = 'X'
                else:
                    return False
        self.shipPositions[ship].append(begSpot)
        self.shipPositions[ship].append(endSpot)
        print(self.shipPositions[ship])
        return True

    def isShipHit(self, cord):
        # If a ship is at given coordinates, places an H to indicate a hit and returns True
        temp = self.playerGrid[cord[1]]
        if temp[cord[0]] == 'X':
            temp[cord[0]] = 'H'
            for x in self.shipPositions:
                temp1 = self.shipPositions[x]
                # Gets end ship coordinates
                temp2 = temp1[1]
                # Gets beginning of ship coordinates
                temp1 = temp1[0]
                # Checks to see which ship is hit by looking at what ship is at given coordinates
                if temp1[0] == temp2[0] and temp1[0] == cord[0]:
                    if temp1[1] <= cord[1] <= temp2[1]:
                        self.shipHit[x].append(cord)
                elif temp1[1] == temp2[1] and temp1[1] == cord[1]:
                    if temp1[0] <= cord[0] <= temp2[0]:
                        self.shipHit[x].append(cord)
            return True

        return False


player1 = Battleships()
player1.placeShip('A', [0, 0], [3, 0])
player1.placeShip('B', [7, 0], [7, 5])
check = player1.getPlayerGrid()
for x in check:
    print(x)
