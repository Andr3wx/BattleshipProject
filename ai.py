import random

class Player:
    def __int__(self, grid):
        self.grid = grid
        self.keys = grid.getkeys()
        self.shipLocations = {}
        self.values
        self.rand_x = 0
        self.rand_y = 0
        self.count = 0

    def get_ship_locations(self):
        return self.shipLocations

    def place_ships(self, block):
        ships = ['corvette', 'sub', 'carrier', 'destroyer']
        rows = self.keys  # Gets row coordinates
        col = self.grid[self.keys[0]]  # Gets column coordinates
        while len(ships) > 0:
            index = random.randint(0, len(ships) - 1)  # Gets a random ship from ships list
            rowIndex = random.randint(0, len(rows) - 1)  # Gets a random row value
            if ships[index] == 'corvette':
                # Corvette size is two so can only be placed two blocks away from right edge
                colIndex = random.randint(0, 5)
                # Beginning coordinates are the given row and given column
                # End coordinates is just the column value plus how many blocks the ship takes up
                self.shipLocations['corvette'] = [[rows[rowIndex], col[colIndex]],
                                                  [rows[rowIndex], 2 * block + col[colIndex]]]
            elif ships[index] == 'sub':
                colIndex = random.randint(0, 4)
                self.shipLocations['sub'] = [[rows[rowIndex], col[colIndex]],
                                             [rows[rowIndex], 3 * block + col[colIndex]]]
            elif ships[index] == 'destroyer':
                colIndex = random.randint(0, 3)
                self.shipLocations['destroyer'] = [[rows[rowIndex], col[colIndex]],
                                                   [rows[rowIndex], 4 * block + col[colIndex]]]
            elif ships[index] == 'carrier':
                colIndex = random.randint(0, 2)
                self.shipLocations['carrier'] = [[rows[rowIndex], col[colIndex]],
                                                 [rows[rowIndex], 5 * block + col[colIndex]]]
            ships.pop(index)  # Ships get placed once so removes ship from list
            rows.pop(rowIndex)  # Only allowing one ship per row, so pops the row index so not accessed again

    def set_hit(self, is_hit):
        if is_hit:
            self.grid[self.rand_x] = 'H'

    def make_decision(self):
        self.rand_x = random.randint(0, 7)
        self.values = self.grid[self.rand_x]

        while (True):
            self.rand_y = random.randint(0, 7)
            self.count += 1

            if self.values[self.rand_y] != 'S' and self.values[self.rand_y] != 'H':
                self.grid[self.rand_x] = 'S'
                return (self.keys[self.rand_x], self.grid[self.rand_x])

            elif self.count == 7:
                self.rand_x = random.randint(0, 7)
                self.values = self.grid[self.rand_x]
