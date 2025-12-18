import pygame
from settings import *
from snake import Snake
from food import Food
import numpy as np

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Змейка")
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)
        self.move_timer = 0
        self.move_delay = 150
        self.running = True
        self.game_over = False
        self.eat_sound = self.create_beep_sound()

    def run(self):
        while self.running:
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if self.game_over:
                        if event.key == pygame.K_r:
                            self.restart()
                        elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                            self.running = False
                    else:
                        self.handle_input(event.key)

            if not self.game_over and current_time - self.move_timer > self.move_delay:
                self.snake.update()
                self.move_timer = current_time

                if self.snake.get_head_rect().colliderect(self.food.get_rect()):
                    self.snake.grow()
                    self.score += 10
                    self.food.respawn()
                    self.eat_sound.play()
                    # Проверка, чтобы еда не появлялась на змейке
                    while any(self.food.x == seg[0] and self.food.y == seg[1] 
                             for seg in self.snake.body):
                        self.food.respawn()

                if self.snake.check_collision():
                    self.game_over = True

            self.screen.fill(BACKGROUND)
            self.snake.draw(self.screen)
            self.food.draw(self.screen)
            self.draw_score()

            if self.game_over:
                self.draw_game_over()

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

    def draw_score(self):
        score_text = self.font.render(f"Счёт: {self.score}", True, SCORE_COLOR)
        self.screen.blit(score_text, (10, 10))

    def draw_game_over(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill(GAME_OVER_BG)
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font.render("ИГРА ОКОНЧЕНА", True, (255, 50, 50))
        text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        self.screen.blit(game_over_text, text_rect)
        
        final_score = self.small_font.render(f"Ваш счёт: {self.score}", True, SCORE_COLOR)
        score_rect = final_score.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(final_score, score_rect)
        
        restart_text = self.small_font.render("R - Новая игра", True, (50, 255, 50))
        quit_text = self.small_font.render("Q - Выход", True, (255, 50, 50))
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
        quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
        
        self.screen.blit(restart_text, restart_rect)
        self.screen.blit(quit_text, quit_rect)

    def handle_input(self, key):
        if key == pygame.K_LEFT and self.snake.dx == 0:
            self.snake.dx = -RECT_WIDTH
            self.snake.dy = 0
        elif key == pygame.K_RIGHT and self.snake.dx == 0:
            self.snake.dx = RECT_WIDTH
            self.snake.dy = 0
        elif key == pygame.K_UP and self.snake.dy == 0:
            self.snake.dx = 0
            self.snake.dy = -RECT_HEIGHT
        elif key == pygame.K_DOWN and self.snake.dy == 0:
            self.snake.dx = 0
            self.snake.dy = RECT_HEIGHT

    def restart(self):
        self.snake.reset()
        self.food.respawn()
        self.score = 0
        self.game_over = False

    def create_beep_sound(self):
        # Создаем простой звуковой сигнал (бип)
       
        
        frequency = 440  # Герц (нота Ля)
        duration = 100   # миллисекунд
        sample_rate = 44100
        
        samples = np.array([32767 * np.sin(2 * np.pi * frequency * i / sample_rate) 
                        for i in range(int(duration * sample_rate / 1000))]).astype(np.int16)
        samples = np.repeat(samples.reshape(len(samples), 1), 2, axis=1)  # Стерео
        
        sound = pygame.sndarray.make_sound(samples)
        return sound

if __name__ == "__main__":
    game = Game()
    game.run()