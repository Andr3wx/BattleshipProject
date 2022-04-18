import random

class Player:
    def __int__(self, grid):
        self.grid = grid
        self.keys = grid.getkeys()
        self.values
        self.rand_x = 0
        self.rand_y = 0
        self.count = 0


    def place_ships(self):
        return

    def set_hit(self, is_hit):
        if is_hit:
            self.grid[self.rand_x] = 'H'


    def make_decision(self):
        self.rand_x = random.randint(0, 7)
        self.values = self.grid[self.rand_x]

        while(True):
            self.rand_y = random.randint(0, 7)
            self.count += 1

            if self.values[self.rand_y] != 'S' and self.values[self.rand_y] != 'H':
                self.grid[self.rand_x] = 'S'
                return (self.keys[self.rand_x], self.grid[self.rand_x])

            elif self.count == 7:
                self.rand_x = random.randint(0, 7)
                self.values = self.grid[self.rand_x]

