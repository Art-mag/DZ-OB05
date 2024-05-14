import pygame
import random

# Инициализация Pygame
pygame.init()

# Параметры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Игра на выживание')

# Цвета
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# Параметры игрока
player_size = 50
player_pos = [SCREEN_WIDTH//2, SCREEN_HEIGHT-2*player_size]
player_speed = 10

# Параметры снаряда
bullet_size = 20
bullet_speed = 20  # Добавлена скорость снаряда
bullet_list = []

# Параметры врага
enemy_size = 50
enemy_list = [[random.randint(0, SCREEN_WIDTH-enemy_size), 0]]  # Исправлено создание списка врагов
enemy_speed = 10

# Счетчик сбитых врагов
score = 0

# Шрифт для отображения счета
font = pygame.font.SysFont("monospace", 35)

# Функция для добавления новых врагов
def add_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 10 and delay < 0.1:
        x_pos = random.randint(0, SCREEN_WIDTH-enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])

# Функция для отрисовки врагов
def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, BLUE, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

# Функция для обновления позиции врагов
def update_enemy_positions(enemy_list, score):
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < SCREEN_HEIGHT:
            enemy_pos[1] += enemy_speed
        else:
            enemy_list.pop(idx)
            score += 1
    return score

# Функция для отрисовки снарядов
def draw_bullets(bullet_list):
    for bullet_pos in bullet_list:
        pygame.draw.rect(screen, GREEN, (bullet_pos[0], bullet_pos[1], bullet_size, bullet_size))

# Функция для обновления позиции снарядов
def update_bullet_positions(bullet_list):
    for idx, bullet_pos in enumerate(bullet_list):
        if bullet_pos[1] > 0:
            bullet_pos[1] -= bullet_speed
        else:
            bullet_list.pop(idx)

# Функция для проверки столкновений
def collision_check(enemy_list, bullet_list, score):
    for enemy_pos in enemy_list[:]:
        for bullet_pos in bullet_list[:]:
            if detect_collision(enemy_pos, bullet_pos):
                enemy_list.remove(enemy_pos)
                bullet_list.remove(bullet_pos)
                score += 1
    return score

# Функция для обнаружения столкновений
def detect_collision(enemy_pos, bullet_pos):
    e_x, e_y = enemy_pos
    b_x, b_y = bullet_pos

    if (e_x < b_x + bullet_size) and (e_x + enemy_size > b_x) and (e_y < b_y + bullet_size) and (e_y + enemy_size > b_y):
        return True
    return False

# Игровой цикл
game_over = False
clock = pygame.time.Clock()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Создаем снаряд в текущем положении игрока, а не в начальном
                bullet_pos = [player_pos[0] + player_size//2 - bullet_size//2, player_pos[1] - bullet_size]
                bullet_list.append(list(bullet_pos))  # Исправлено добавление копии позиции снаряда

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_d] and player_pos[0] < SCREEN_WIDTH - player_size:
        player_pos[0] += player_speed

    screen.fill(BLACK)

    add_enemies(enemy_list)
    score = update_enemy_positions(enemy_list, score)
    update_bullet_positions(bullet_list)
    score = collision_check(enemy_list, bullet_list, score)

    draw_enemies(enemy_list)
    draw_bullets(bullet_list)

    pygame.draw.rect(screen, BLUE, (player_pos[0], player_pos[1], player_size, player_size))

    # Отображение счета
    text = font.render("Счет: {}".format(score), True, WHITE)
    screen.blit(text, (SCREEN_WIDTH - 200, 10))

    clock.tick(30)
    pygame.display.update()

pygame.quit()
