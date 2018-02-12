import pygame


class Inputs():
    def __init__(self):
        self.Exit = False

    def process(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.Exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    pass
                if event.key == pygame.K_LEFT:
                    pass
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    pass
                if event.key == pygame.K_LEFT:
                    pass
