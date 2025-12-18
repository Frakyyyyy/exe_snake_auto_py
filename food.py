import random
import pygame
from settings import *

class Food:
    def __init__(self):
        self.width = RECT_WIDTH
        self.height = RECT_HEIGHT
        self.respawn()

    def respawn(self):
        max_x = (WIDTH - RECT_WIDTH) // RECT_WIDTH
        max_y = (HEIGHT - RECT_HEIGHT) // RECT_HEIGHT
        self.x = random.randint(0, max_x) * RECT_WIDTH
        self.y = random.randint(0, max_y) * RECT_HEIGHT

    def draw(self, screen):
        pygame.draw.rect(screen, FOOD_COLOR, 
                        (self.x, self.y, self.width, self.height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)