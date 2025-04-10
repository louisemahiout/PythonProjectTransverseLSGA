
import pygame

# Initialisation de Pygame
pygame.init()

# Définition des constantes
LARGEUR, HAUTEUR = 800, 600
BLANC = (255, 255, 255)
ROUGE = (255, 0, 0)
BLEU = (0, 0, 255)

# Création de la fenêtre
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Déplacement du personnage")

# Définition des personnages (joueur et bot)
personnage = pygame.Rect(375, 500, 50, 60)
bot = pygame.Rect(400, 550, 40, 30)

# Variables de mouvement
gravite = 0.8
saut_force = -10
y_momentum = 0
au_sol = False

# Vitesses
personnage_speed = 7
bot_speed = 3

# Boucle principale
running = True
while running:
    pygame.time.delay(30)

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Gestion des touches
    touches = pygame.key.get_pressed()
    # Gestion des touches avec vérification de collision avec le bot
    if touches[pygame.K_LEFT] and personnage.x > 0:
        personnage_temp = personnage.move(-personnage_speed, 0)  # Temporaire pour vérifier la collision
        if not personnage_temp.colliderect(bot):  # Empêche le chevauchement avec le bot
            personnage.x -= personnage_speed
    if touches[pygame.K_RIGHT] and personnage.x < LARGEUR - personnage.width:
        personnage_temp = personnage.move(personnage_speed, 0)  # Temporaire pour vérifier la collision
        if not personnage_temp.colliderect(bot):
            personnage.x += personnage_speed
    if touches[pygame.K_UP] and au_sol:
        y_momentum = saut_force
        au_sol = False  # Lancer le saut


    # Application de la gravité
    y_momentum += gravite
    personnage.y += y_momentum

    if personnage.colliderect(bot):  # Si le joueur entre en collision avec le bot
        if y_momentum > 0:  # Si le joueur tombe (momentum positif)
            personnage.y = bot.top - personnage.height  # Arrêter le joueur juste avant le bot
            au_sol = True  # Il touche le bot donc il est au sol
            y_momentum = 0  # Annuler la gravité pendant le contact avec le bot

    # Empêcher le personnage de tomber sous le sol
    if personnage.y >= HAUTEUR - personnage.height:
        personnage.y = HAUTEUR - personnage.height
        au_sol = True
        y_momentum = 0
    # Empêcher le personnage de tomber sous le sol
    if personnage.y >= HAUTEUR - personnage.height:
        personnage.y = HAUTEUR - personnage.height
        au_sol = True
        y_momentum = 0

    # Calcul de la distance bot-joueur
    distance_x = abs(bot.x - personnage.x)
    distance_y = abs(bot.y - personnage.y)

    # Si le bot est à 200 pixels ou moins, il suit le joueur sans chevauchement
    if distance_x <= 200:
        if bot.x < personnage.x:
            bot_temp = bot.move(bot_speed, 0)  # Temporaire pour vérifier la collision
            if not bot_temp.colliderect(personnage):  # Empêche le chevauchement avec le joueur
                bot.x += bot_speed
        elif bot.x > personnage.x:
            bot_temp = bot.move(-bot_speed, 0)  # Temporaire pour vérifier la collision
            if not bot_temp.colliderect(personnage):
                bot.x -= bot_speed

    # Dessin des éléments
    fenetre.fill(BLANC)
    pygame.draw.rect(fenetre, ROUGE, personnage)  # Dessine le joueur
    pygame.draw.rect(fenetre, BLEU, bot)  # Dessine le bot
    pygame.display.update()

pygame.quit()
