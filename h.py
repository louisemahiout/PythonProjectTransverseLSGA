import pygame
import sys
import os
import math

pygame.init()

# Fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mon jeu de plateforme")

# Musique
pygame.mixer.music.load("assetsaffichage/musique.mp3")
pygame.mixer.music.play(-1)

# Images menu
background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
button_image = pygame.image.load("button.png")
button_rect = button_image.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

font = pygame.font.SysFont(None, 48)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def show_menu():
    while True:
        screen.blit(background, (0, 0))
        screen.blit(button_image, button_rect)
        draw_text("Niveau 1", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2 + 50)
        draw_text("Niveau 2", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2 + 130)

        # Deuxième bouton
        button2_rect = button_image.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 130))
        screen.blit(button_image, button2_rect)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return "level1"
                elif button2_rect.collidepoint(event.pos):
                    return "level2"

# ============ NIVEAU 1 =============
def run_level1():
    print("Lancement du niveau 1...")
    # (insère ici tout ton code de jeu de plateforme)

# ============ NIVEAU 2 =============
def run_level2():
    print("Lancement du niveau 2... (jeu de lancement de crâbes)")
    # Re-déclaration locale
    WHITE = (255, 255, 255)
    BROWN = (139, 69, 19)
    GREEN = (0, 200, 0)
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)
    gravity = 0.5
    ball_radius = 10

    sol_rect = pygame.Rect(0, HEIGHT - 30, WIDTH, 30)
    girl_img = pygame.image.load(f'Hero/Idle (1).png')
    girl_img = pygame.transform.scale(girl_img, (64, 64))
    girl_rect = girl_img.get_rect()
    girl_rect.midbottom = (100, sol_rect.top)

    ennemie_img = pygame.image.load('ennemi1/poisson.png')
    ennemie_img = pygame.transform.scale(ennemie_img, (80, 80))
    ennemie_rect = ennemie_img.get_rect()
    ennemie_rect.midbottom = (650, sol_rect.top)
    ennemie_alive = True

    ball_pos = None
    ball_vel = None
    selecting_trajectory = False
    arrow_end = None

    def draw_arrow(start, end):
        pygame.draw.line(screen, BLACK, start, end, 3)
        angle = math.atan2(end[1] - start[1], end[0] - start[0])
        arrow_size = 10
        left = (end[0] - arrow_size * math.cos(angle - math.pi / 6),
                end[1] - arrow_size * math.sin(angle - math.pi / 6))
        right = (end[0] - arrow_size * math.cos(angle + math.pi / 6),
                 end[1] - arrow_size * math.sin(angle + math.pi / 6))
        pygame.draw.polygon(screen, BLACK, [end, left, right])

    def draw():
        screen.fill(WHITE)
        pygame.draw.rect(screen, GREEN, sol_rect)
        pygame.draw.rect(screen, BROWN, sol_rect.inflate(-4, -4))
        screen.blit(girl_img, girl_rect)
        if ennemie_alive:
            screen.blit(ennemie_img, ennemie_rect)
        if selecting_trajectory and arrow_end:
            draw_arrow(girl_rect.center, arrow_end)
        if ball_pos:
            pygame.draw.circle(screen, RED, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)
        pygame.display.update()

    def check_collision_with_enemy():
        if not ennemie_alive or not ball_pos:
            return False
        ball_rect = pygame.Rect(ball_pos[0] - ball_radius, ball_pos[1] - ball_radius, ball_radius * 2, ball_radius * 2)
        return ball_rect.colliderect(ennemie_rect)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if girl_rect.collidepoint(event.pos):
                    selecting_trajectory = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if selecting_trajectory:
                    arrow_end = event.pos
                    dx = arrow_end[0] - girl_rect.centerx
                    dy = arrow_end[1] - girl_rect.centery
                    power = 0.2
                    ball_pos = list(girl_rect.center)
                    ball_vel = [dx * power, dy * power]
                    selecting_trajectory = False
                    arrow_end = None
        if selecting_trajectory:
            arrow_end = pygame.mouse.get_pos()
        if ball_pos and ball_vel:
            ball_vel[1] += gravity
            ball_pos[0] += ball_vel[0]
            ball_pos[1] += ball_vel[1]
            if ball_pos[1] > sol_rect.top - ball_radius:
                ball_pos = None
                ball_vel = None
            elif check_collision_with_enemy():
                ennemie_alive = False
                ball_pos = None
                ball_vel = None
        draw()

# ========= Lancement du jeu =========
def main():
    while True:
        choice = show_menu()
        if choice == "level1":
            run_level1()
        elif choice == "level2":
            run_level2()

if __name__ == "__main__":
    main()
