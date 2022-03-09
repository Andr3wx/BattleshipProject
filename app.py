import pygame
# import battleship
# import battleshipNetwork
# import battleshipServer


# functions

if __name__ == "__main__":
    pygame.init()   # initialize pygame
    screen = pygame.display.set_mode((800, 600))    # create screen
    pygame.display.set_caption("Battleship")    # set caption
    icon = pygame.image.load('battleship.png')  # set game icon
    pygame.display.set_icon(icon)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:    # press ESC to quit
                    running = False
        # RGB background
        screen.fill((255, 255, 255))
        pygame.display.update()
