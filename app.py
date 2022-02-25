import pygame
import socket
import random


# functions

if __name__ == "__main__":
    pygame.init()   # initialize pygame
    screen = pygame.display.set_mode((800, 600))    # create screen
    pygame.display.set_caption("Battleship")    # set caption

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:    # press ESC to quit
                    running = False
