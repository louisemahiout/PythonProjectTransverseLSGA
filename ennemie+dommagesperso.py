import pygame
import time

# Initialisation de Pygame
pygame.init()
import pygame


# Partie MENU

def show_menu():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("assetsaffichage/musique.mp3")
    pygame.mixer.music.play(-1)  # -1 = jouer en boucle
    pygame.mixer.music.set_volume(0.2)  # Volume initial (entre 0.0 et 1.0)
    pygame.display.set_caption('Crabinator')
    screen = pygame.display.set_mode((725, 550))

    # Charger les images
    background = pygame.image.load("assetsaffichage/fond1.jpg").convert()
    play_button = pygame.image.load('assetsaffichage/boutonplay.png').convert_alpha()
    play_button = pygame.transform.scale(play_button, (300, 200))
    play_button_rect = play_button.get_rect()
    play_button_rect.topleft = (200, 300)

    running = True
    while running:
        screen.blit(background, (0, 0))
        screen.blit(play_button, play_button_rect)

        # Création de la police et du texte
        font = pygame.font.Font("assetsaffichage/PressStart2P.ttf", 48)
        title_text = font.render("CRABINATOR", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(725 // 2, 300))

        # Affichage du menu
        screen.blit(background, (0, 0))
        screen.blit(title_text, title_rect)
        screen.blit(play_button, play_button_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    return True


def choose_level():
    screen = pygame.display.set_mode((725, 550))
    background = pygame.image.load("assetsaffichage/fond1.jpg").convert()

    # Charger les boutons
    level1_button = pygame.image.load("assetsaffichage/boutonplay.png").convert_alpha()
    level1_button = pygame.transform.scale(level1_button, (300, 100))
    level1_rect = level1_button.get_rect(center=(725 // 2, 250))

    level2_button = pygame.image.load("assetsaffichage/boutonplay.png").convert_alpha()
    level2_button = pygame.transform.scale(level2_button, (300, 100))
    level2_rect = level2_button.get_rect(center=(725 // 2, 400))

    font = pygame.font.Font("assetsaffichage/PressStart2P.ttf", 24)
    title_text = font.render("CHOISIS TON NIVEAU", True, (0, 0, 0))
    title_rect = title_text.get_rect(center=(725 // 2, 100))

    running = True
    while running:
        screen.blit(background, (0, 0))
        screen.blit(title_text, title_rect)
        screen.blit(level1_button, level1_rect)
        screen.blit(level2_button, level2_rect)

        # Affichage des labels
        label1 = font.render("NIVEAU 1", True, (255, 255, 255))
        label2 = font.render("NIVEAU 2", True, (255, 255, 255))
        screen.blit(label1, (level1_rect.centerx - label1.get_width() // 2, level1_rect.centery - 10))
        screen.blit(label2, (level2_rect.centerx - label2.get_width() // 2, level2_rect.centery - 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if level1_rect.collidepoint(event.pos):
                    return 1
                elif level2_rect.collidepoint(event.pos):
                    return 2


# Définition des constantes
LARGEUR, HAUTEUR = 800, 600
BLANC = (255, 255, 255)
ROUGE = (255, 0, 0)
BLEU = (0, 0, 255)

# Création de la fenêtre
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Déplacement du personnage")

# Définition des personnages (joueur et bots)
personnage = pygame.Rect(200, 500, 50, 60)
bot = pygame.Rect(400, 575, 40, 30)
bot1 = pygame.Rect(500, 400, 40, 30)
bot2 = pygame.Rect(300, 380, 40, 30)

# Variables de mouvement
gravite = 0.8
saut_force = -10
y_momentum = 0
au_sol = False

# Vitesses
personnage_speed = 7
bot_speed = 3

# Système de vies et d'invincibilité
vies = 3
invincible = False
invincible_time = 0

# Boucle principale
running = True
while running:
    pygame.time.delay(30)

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Vérification de l'invincibilité
    if invincible and time.time() - invincible_time >= 3:
        invincible = False  # Fin de l'invincibilité

    # Gestion des touches
    touches = pygame.key.get_pressed()
    if touches[pygame.K_LEFT] and personnage.x > 0:
        personnage.x -= personnage_speed
    if touches[pygame.K_RIGHT] and personnage.x < LARGEUR - personnage.width:
        personnage.x += personnage_speed
    if touches[pygame.K_UP] and au_sol:
        y_momentum = saut_force
        au_sol = False

    # Application de la gravité
    y_momentum += gravite
    personnage.y += y_momentum

    # Vérification des collisions avec le sol
    if personnage.y >= HAUTEUR - personnage.height:
        personnage.y = HAUTEUR - personnage.height
        au_sol = True
        y_momentum = 0

    # Vérification des collisions avec les bots
    if any(personnage.colliderect(b) and not invincible for b in [bot, bot1, bot2]):
        vies -= 1
        invincible = True
        invincible_time = time.time()
        print(f"Collision ! Vies restantes : {vies}")
        if vies <= 0:
            print("Game Over!")
            running = False

    # Déplacement des bots
    for b in [bot, bot1, bot2]:
        distance_x = abs(b.x - personnage.x)
        if distance_x <= 200:
            if b.x < personnage.x:
                b.x += bot_speed
            elif b.x > personnage.x:
                b.x -= bot_speed

    # Dessin des éléments
    fenetre.fill(BLANC)
    pygame.draw.rect(fenetre, ROUGE if not invincible else (255, 165, 0), personnage)  # Devient orange si invincible
    pygame.draw.rect(fenetre, BLEU, bot)
    pygame.draw.rect(fenetre, BLEU, bot1)  # Affichage du deuxième bot
    pygame.draw.rect(fenetre, BLEU, bot2)  # Affichage du troisième bot
    pygame.display.update()

pygame.quit()
