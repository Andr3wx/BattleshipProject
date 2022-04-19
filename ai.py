import random

class Player:
    def __init__(self):
        self.grid = {}
        self.shipLocations = {}
        self.values = {}
        self.rand_x = 0
        self.rand_y = 0
        self.count = 0

    def get_ship_locations(self):
        return self.shipLocations

    def set_grid(self, grid):
        self.grid = grid

    def place_ships(self, block):
        ships = ['corvette', 'sub', 'carrier', 'destroyer']
        rows = list(self.grid.keys())  # Gets row coordinates
        cols = self.grid[rows[0]]  # Gets column coordinates
        while len(ships) > 0:
            index = random.randint(0, len(ships) - 1)  # Gets a random ship from ships list
            rowIndex = random.randint(0, len(rows) - 1)  # Gets a random row value
            if ships[index] == 'corvette':
                # Corvette size is two so can only be placed two blocks away from right edge
                colIndex = random.randint(0, 5)
                # Beginning coordinates are the given row and given column
                # End coordinates is just the column value plus how many blocks the ship takes up
                self.shipLocations['corvette'] = [[cols[colIndex],float(rows[rowIndex])],
                                                  [2 * block + cols[colIndex],float(rows[rowIndex])]]
            elif ships[index] == 'sub':
                colIndex = random.randint(0, 4)
                self.shipLocations['sub'] = [[cols[colIndex],float(rows[rowIndex])],
                                             [3 * block + cols[colIndex],float(rows[rowIndex])]]
            elif ships[index] == 'destroyer':
                colIndex = random.randint(0, 3)
                self.shipLocations['destroyer'] = [[cols[colIndex],float(rows[rowIndex])],
                                                   [4 * block + cols[colIndex],float(rows[rowIndex])]]
            elif ships[index] == 'carrier':
                colIndex = random.randint(0, 2)
                self.shipLocations['carrier'] = [[cols[colIndex],float(rows[rowIndex])],
                                                 [5 * block + cols[colIndex],float(rows[rowIndex])]]
            ships.pop(index)  # Ships get placed once so removes ship from list
            rows.pop(rowIndex)  # Only allowing one ship per row, so pops the row index so not accessed again

    def set_hit(self, is_hit):
        if is_hit:
            self.grid[self.rand_x] = 'H'

    def make_decision(self):
        self.rand_x = random.randint(0, 7)
        getKeys = list(self.grid.keys())
        self.values = self.grid[getKeys[self.rand_x]]

        self.rand_y = random.randint(0, 7)
        self.count = self.rand_y
        while (True):
            if self.values[self.count] != 'S' and self.values[self.count] != 'H':
                yReturnVal = self.values[self.count]
                self.values[self.count] = 'S'
                self.grid[getKeys[self.rand_x]] = self.values
                return [getKeys[self.rand_x], yReturnVal]

            elif self.count == 7:
                self.rand_x = random.randint(0, 7)
                self.values = self.grid[getKeys[self.rand_x]]
                self.rand_y = random.randint(0, 7)
                self.count = self.rand_y-1
            self.count += 1
