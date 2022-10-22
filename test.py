import pygame

from pygame.locals import *
pygame.init()

screen = pygame.display.set_mode((400,500))

while True:
    screen.fill((200,1,1))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
        
         pygame.quit()
         quit()
        pygame.display.update