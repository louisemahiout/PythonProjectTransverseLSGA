import pygame
import sys
import math

# Initialisation
pygame.init()
WIDTH, HEIGHT = 725, 550
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lancement de crâbes")

# Couleurs
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Sol
sol_rect = pygame.Rect(0, HEIGHT - 30, WIDTH, 30)

# Personnages
girl_img = pygame.image.load(f'Hero/Idle (1).png')
girl_img = pygame.transform.scale(girl_img, (64, 64))
girl_rect = girl_img.get_rect()
girl_rect.midbottom = (100, sol_rect.top)

ennemie_img = pygame.image.load('ennemi1/poisson.png')
ennemie_img = pygame.transform.scale(ennemie_img, (80, 80))
ennemie_rect = ennemie_img.get_rect()
ennemie_rect.midbottom = (650, sol_rect.top)
ennemie_alive = True

# Création crâbe boule rouge
ball_radius = 10
ball_pos = None
ball_vel = None
gravity = 0.5

# État
selecting_trajectory = False
arrow_end = None

def draw_arrow(start, end):
    # Dessine une vraie flèche entre deux points
    pygame.draw.line(win, BLACK, start, end, 3)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    arrow_size = 10
    # Pointe de flèche
    left = (end[0] - arrow_size * math.cos(angle - math.pi / 6),
            end[1] - arrow_size * math.sin(angle - math.pi / 6))
    right = (end[0] - arrow_size * math.cos(angle + math.pi / 6),
             end[1] - arrow_size * math.sin(angle + math.pi / 6))

    pygame.draw.polygon(win, BLACK, [end, left, right])

def draw():
    win.fill(WHITE)

    # Sol
    pygame.draw.rect(win, GREEN, sol_rect)
    pygame.draw.rect(win, BROWN, sol_rect.inflate(-4, -4))

    # Personnages
    win.blit(girl_img, girl_rect)
    if ennemie_alive:
        win.blit(ennemie_img, ennemie_rect)

    # Flèche de visée (pendant que le joueur vise)
    if selecting_trajectory and arrow_end:
        draw_arrow(girl_rect.center, arrow_end)

    # Boule
    if ball_pos:
        pygame.draw.circle(win, RED, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)

    pygame.display.update()

def check_collision_with_ennemy():
    if not ennemie_alive or not ball_pos:
        return False
    ball_rect = pygame.Rect(ball_pos[0] - ball_radius, ball_pos[1] - ball_radius,
                            ball_radius * 2, ball_radius * 2)
    return ball_rect.colliderect(ennemie_rect)

def main():
    global selecting_trajectory, arrow_end, ball_pos, ball_vel, ennemie_alive

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
                    arrow_end = None  # On efface la flèche une fois la boule lancée

        if selecting_trajectory:
            arrow_end = pygame.mouse.get_pos()

        # Mise à jour de la boule
        if ball_pos and ball_vel:
            ball_vel[1] += gravity
            ball_pos[0] += ball_vel[0]
            ball_pos[1] += ball_vel[1]

            # Collision avec le sol
            if ball_pos[1] > sol_rect.top - ball_radius:
                ball_pos = None
                ball_vel = None

            # Collision avec l’ennemi
            elif check_collision_with_ennemy():
                ennemie_alive = False
                ball_pos = None
                ball_vel = None

        draw()

    pygame.quit()
    sys.exit()
#main
if __name__ == "__main__":
    main()