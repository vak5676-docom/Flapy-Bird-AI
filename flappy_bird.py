from ~/Desktop/Python1/My Games/Collect_data import *
import random
import pygame
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Частота кадрів
clock = pygame.time.Clock()
FPS = 60

# Кольори
BG_COLOR = (135, 206, 235)  # Блакитний (небо)
GROUND_COLOR = (222, 184, 135)  # Пісочний
BIRD_COLOR = (255, 255, 0)  # Жовтий
PIPE_COLOR = (0, 200, 0)  # Зелений
TEXT_COLOR = (255, 255, 255)

# Шрифт
font = pygame.font.SysFont("Arial", 30)


class Bird:

  def __init__(self):
    self.x = 100
    self.y = SCREEN_HEIGHT // 2
    self.width = 30
    self.height = 30
    self.gravity = 0.5
    self.lift = -9
    self.velocity = 0

  def update(self):
    self.velocity += self.gravity
    self.y += self.velocity

    # Обмеження екраном верх/низ
    if self.y >= SCREEN_HEIGHT - 100:
      self.y = SCREEN_HEIGHT - 100
      self.velocity = 0
    if self.y <= 0:
      self.y = 0
      self.velocity = 0

  def jump(self):
    self.velocity = self.lift

  def draw(self):
    pygame.draw.rect(
        screen,
        BIRD_COLOR,
        (self.x, self.y, self.width, self.height),
        border_radius=5,
    )

  def get_rect(self):
    return pygame.Rect(self.x, self.y, self.width, self.height)


class Pipe:

  def __init__(self):
    self.x = SCREEN_WIDTH
    self.width = 60
    self.gap = 150
    self.top_height = random.randint(50, 300)
    self.bottom_y = self.top_height + self.gap
    self.speed = 4
    self.passed = False

  def update(self):
    self.x -= self.speed

  def draw(self):
    # Верхня труба
    pygame.draw.rect(
        screen, PIPE_COLOR, (self.x, 0, self.width, self.top_height)
    )
    # Нижня труба
    pygame.draw.rect(
        screen,
        PIPE_COLOR,
        (self.x, self.bottom_y, self.width, SCREEN_HEIGHT - self.bottom_y),
    )

  def get_rects(self):
    top_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
    bottom_rect = pygame.Rect(
        self.x, self.bottom_y, self.width, SCREEN_HEIGHT - self.bottom_y
    )
    return top_rect, bottom_rect


def reset_game():
  return Bird(), [Pipe()], 0, 0


# Ініціалізація гри
bird, pipes, score, spawn_timer = reset_game()
game_over = False

# Головний ігровий цикл
running = True
while running:
  screen.fill(BG_COLOR)

  # Обробка подій
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE:
        if game_over:
          bird, pipes, score, spawn_timer = reset_game()
          game_over = False
        else:
          bird.jump()
          eve = "jump"
          collect(bird, pipes ,eve)
  if not game_over:
    # Оновлення пташки
    bird.update()
    eve = "wait"
    if spawn_timer % 10 == 0:
      collect(bird, pipes ,eve)

    # Генерація труб
    spawn_timer += 1
    if spawn_timer >= 90:  # Кожні 90 кадрів з'являється нова труба
      pipes.append(Pipe())
      spawn_timer = 0

    # Оновлення труб
    for pipe in pipes[:]:
      pipe.update()
      if pipe.x + pipe.width < 0:
        pipes.remove(pipe)

      # Перевірка нарахування очок
      if not pipe.passed and pipe.x < bird.x:
        score += 1
        pipe.passed = True

      # Перевірка зіткнень
      top_rect, bottom_rect = pipe.get_rects()
      bird_rect = bird.get_rect()
      if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
        game_over = True

    # Зіткнення з землею
    if bird.y >= SCREEN_HEIGHT - 100:
      game_over = True

  # Малювання елементів гри
  for pipe in pipes:
    pipe.draw()

  # Малювання землі
  pygame.draw.rect(
      screen,
      GROUND_COLOR,
      (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100),
  )

  bird.draw()

  # Виведення рахунку
  score_surface = font.render(f"Рахунок: {score}", True, TEXT_COLOR)
  screen.blit(score_surface, (15, 15))

  # Повідомлення про кінець гри
  if game_over:
    over_surface = font.render("Гра закінчена!", True, (255, 0, 0))
    restart_surface = font.render("Натисніть ПРОБІЛ", True, TEXT_COLOR)
    screen.blit(
        over_surface,
        (SCREEN_WIDTH // 2 - over_surface.get_width() // 2, SCREEN_HEIGHT // 2 - 40),
    )
    screen.blit(
        restart_surface,
        (
            SCREEN_WIDTH // 2 - restart_surface.get_width() // 2,
            SCREEN_HEIGHT // 2 + 10,
        ),
    )

  pygame.display.flip()
  clock.tick(FPS)

pygame.quit()