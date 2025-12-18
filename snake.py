import pygame
from settings import *

class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        start_x = (WIDTH // 2 // RECT_WIDTH) * RECT_WIDTH
        start_y = (HEIGHT // 2 // RECT_HEIGHT) * RECT_HEIGHT
        self.body = [(start_x, start_y)]
        self.dx = 0
        self.dy = 0
        self.should_grow = False

    def update(self):
        if self.dx == 0 and self.dy == 0:
            return

        head_x, head_y = self.body[0]
        new_head = (head_x + self.dx, head_y + self.dy)
        self.body.insert(0, new_head)

        if not self.should_grow:
            self.body.pop()
        else:
            self.should_grow = False

    def grow(self):
        self.should_grow = True

    def draw(self, screen):
        for x, y in self.body:
            pygame.draw.rect(screen, SNAKE_COLOR, 
                           (x, y, RECT_WIDTH, RECT_HEIGHT))

    def get_head_rect(self):
        head = self.body[0]
        return pygame.Rect(head[0], head[1], RECT_WIDTH, RECT_HEIGHT)

    def check_collision(self):
        head = self.body[0]
        # Столкновение с собой
        if head in self.body[1:]:
            return True
        # Столкновение со стенами
        head_x, head_y = head
        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
            return True
        return False