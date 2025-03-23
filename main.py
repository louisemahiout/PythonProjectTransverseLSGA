import pygame

# Initialisation de Pygame
pygame.init()

# Définition des constantes
LARGEUR, HAUTEUR = 800, 600
BLANC = (255, 255, 255)
ROUGE = (255, 0, 0)

# Création de la fenêtre
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Déplacement du personnage")

# Définition du personnage
personnage = pygame.Rect(375, 500, 50, 50)

# Variables de mouvement
vitesse_x = 5
gravite = 0.8
saut_force = -10
y_momentum = 0
au_sol = False

# Boucle princpale
running = True
while running:
    pygame.time.delay(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Gestion des touches
    touches = pygame.key.get_pressed()
    if touches[pygame.K_LEFT]:
        personnage.x -= vitesse_x
    if touches[pygame.K_RIGHT]:
        personnage.x += vitesse_x
    if touches[pygame.K_UP] and au_sol:
        y_momentum = saut_force
        au_sol = False

    # Application de la gravité
    y_momentum += gravite
    personnage.y += y_momentum

    # Empêcher le personnage de tomber sous le sol
    if personnage.y >= HAUTEUR - personnage.height:
        personnage.y = HAUTEUR - personnage.height
        au_sol = True
        y_momentum = 0

    # Dessin des éléments
    fenetre.fill(BLANC)
    pygame.draw.rect(fenetre, ROUGE, personnage)
    pygame.display.update()

pygame.quit()

