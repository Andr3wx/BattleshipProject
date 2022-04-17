from app import *
import random
from spriteClasses import Sprite
import pygame

class AI:
    def __int__(self, id):
        self.p1Went = False
        self.p2Went = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0, 0]
        self.ties = 0
        self.img_X = SCREEN_WIDTH * .65
        self.corvette = Sprite('corvette', self.img_X, SCREEN_HEIGHT * .1)
        self.sub = Sprite('sub', self.img_X, SCREEN_HEIGHT * .3)
        self.destroyer = Sprite('destroyer', self.img_X, SCREEN_HEIGHT * .5)
        self.carrier = Sprite('carrier', self.img_X, SCREEN_HEIGHT * .7)

        # Ship group
        self.ship_group_layered = pygame.sprite.LayeredUpdates(
            [self.corvette, self.sub, self.destroyer, self.carrier])
        # Group of Hit and Miss instances
        self.hit_miss_group_layered = pygame.sprite.LayeredUpdates([])

    def get_player_move(self, p):
        return self.moves[p]

    def player(self, player, move):
        if player == 0:
            self.moves[player] = move
            if player == 0:
                self.p1Went = True
            else:
                self.p2Went = True

    def bothWent(self):
        return self.p1Went and self.p2Went

    def winner(self):
        p1 = self.moves[0].upper()[0]

    def resetWent(self):
        self.p1Went = False
        self.p2Went = False

    def make_decision(self, current_grid):
        self.open = False
        while(not self.open):
            rand_x = random(1, 10)
            rand_y = random(1, 10)
        self.canPlace, self.running, self.gridCord, self.currentSprite, self.shipPos = moveShipScreen(
            canPlace, running, gridCord, currentSprite, (rand_x, rand_y))


