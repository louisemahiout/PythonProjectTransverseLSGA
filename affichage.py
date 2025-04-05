# Importation du module pygame
import pygame
# Initialisation de pygame
pygame.init()

# Création de la fenêtre
pygame.display.set_caption('Crabinator')
screen = pygame.display.set_mode((725, 550))

# Chargement du fond
background = pygame.image.load("assetsaffichage/fond1.jpg").convert()

# Chargement et redimensionnement du bouton PLAY
play_button = pygame.image.load('assetsaffichage/boutonplay.png').convert_alpha()
play_button = pygame.transform.scale(play_button, (300, 200))
play_button_rect = play_button.get_rect()
play_button_rect.x = 200
play_button_rect.y = 300

# Boucle principale
running = True
while running:
    # Affichage fond + bouton
    screen.blit(background, (0, 0))
    screen.blit(play_button, play_button_rect)
    pygame.display.flip()

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            print("Fermeture du jeu")
