import pygame
import pymunk
import pymunk.pygame_util
import math

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lancer de crâbe")

# Couleurs
WHITE = (255, 255, 255)
RED = (200, 50, 50)
BLUE = (50, 50, 255)
GREEN = (50, 200, 50)
BLACK = (0, 0, 0)

# Création de l'espace Pymunk
space = pymunk.Space()
space.gravity = (0, 900)  # Gravité vers le bas

# Position initiale du crabe (au sol)
crabe_start_x, crabe_start_y = 100, HEIGHT - 70

# Variable pour stocker le crabe
current_crabe = None


# Fonction pour créer le crabe (et supprimer l'ancien)
def create_crabe(impulse_x, impulse_y):
    global current_crabe

    # Supprimer l'ancien crabe s'il existe
    if current_crabe:
        space.remove(current_crabe, current_crabe.shape)

    # Création du nouvel crabe
    mass = 5
    radius = 20
    inertia = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, inertia, pymunk.Body.DYNAMIC)
    body.position = crabe_start_x, crabe_start_y
    shape = pymunk.Circle(body, radius)
    shape.elasticity = 0.5
    shape.friction = 0.5
    space.add(body, shape)

    # Appliquer une impulsion pour un tir parabolique
    body.apply_impulse_at_local_point((impulse_x, impulse_y))

    # Stocker l'oiseau actuel
    body.shape = shape  # Pour pouvoir le supprimer
    current_bird = body


# Ajout du sol
def add_static_ground():
    static_body = space.static_body
    floor = pymunk.Segment(static_body, (0, HEIGHT - 50), (WIDTH, HEIGHT - 50), 5)
    floor.elasticity = 0.6
    floor.friction = 1.0
    space.add(floor)


# Fonction pour dessiner une flèche indiquant la trajectoire
def draw_trajectory_arrow(start_x, start_y, vel_x, vel_y):
    """Dessine une flèche indiquant la direction et la force du tir"""
    arrow_length = min(150, math.sqrt(vel_x ** 2 + vel_y ** 2) / 5)  # Augmenter la longueur de la flèche pour plus de portée
    angle = math.atan2(vel_y, vel_x)  # Angle de la flèche

    # Calculer la position de la pointe de la flèche
    arrow_end_x = start_x + arrow_length * math.cos(angle)
    arrow_end_y = start_y + arrow_length * math.sin(angle)

    # Dessiner la ligne principale de la flèche
    pygame.draw.line(screen, GREEN, (start_x, start_y), (arrow_end_x, arrow_end_y), 5)

    # Dessiner les petites ailes de la flèche
    arrow_size = 15  # Taille des ailes plus grande pour refléter la puissance
    left_wing_x = arrow_end_x - arrow_size * math.cos(angle - math.pi / 6)
    left_wing_y = arrow_end_y - arrow_size * math.sin(angle - math.pi / 6)

    right_wing_x = arrow_end_x - arrow_size * math.cos(angle + math.pi / 6)
    right_wing_y = arrow_end_y - arrow_size * math.sin(angle + math.pi / 6)

    pygame.draw.line(screen, GREEN, (arrow_end_x, arrow_end_y), (left_wing_x, left_wing_y), 5)
    pygame.draw.line(screen, GREEN, (arrow_end_x, arrow_end_y), (right_wing_x, right_wing_y), 5)


# Initialisation
add_static_ground()
running = True
clock = pygame.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(screen)

# Variables pour la sélection de tir
start_pos = (crabe_start_x, crabe_start_y)
current_pos = None
launching = False

# Boucle du jeu
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Début du clic : choisir l'angle et la puissance
        if event.type == pygame.MOUSEBUTTONDOWN:
            launching = True

        # Fin du clic : lancer le crabe
        if event.type == pygame.MOUSEBUTTONUP:
            if launching and current_pos:
                end_pos = pygame.mouse.get_pos()

                # Calcul du vecteur de tir (impulsion)
                dx = start_pos[0] - end_pos[0]
                dy = start_pos[1] - end_pos[1]

                # Limiter la puissance max
                power_factor = 10000 # Augmenter le facteur de puissance pour permettre un tir plus fort
                impulse_x = max(min(dx * power_factor, 3000), -3000)  # Plus de portée horizontale
                impulse_y = max(min(dy * power_factor, 3000), -3000)  # Plus de hauteur verticale

                create_crabe(impulse_x, impulse_y)

            launching = False

    # Afficher l’oiseau s’il n’a pas encore été lancé
    if not current_crabe:
        pygame.draw.circle(screen, BLUE, (crabe_start_x, crabe_start_y), 20)

    # Mettre à jour la position du pointeur
    if launching:
        current_pos = pygame.mouse.get_pos()

        # Calcul du vecteur d'impulsion
        dx = start_pos[0] - current_pos[0]
        dy = start_pos[1] - current_pos[1]
        impulse_x = dx * 5  # Augmenter la puissance horizontale
        impulse_y = dy * 5 # Augmenter la puissance verticale

        # Dessiner la flèche de trajectoire
        draw_trajectory_arrow(crabe_start_x, crabe_start_y, impulse_x, impulse_y)

    # Mettre à jour la physique
    space.step(1 / 60.0)

    # Dessiner les objets
    space.debug_draw(draw_options)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
