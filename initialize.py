import pygame

# ---------------------------------------------------------------
# Initialise tous les modules nécessaires de Pygame :
# - Crée la fenêtre du jeu avec les dimensions définies
# - Définit le titre de la fenêtre
# - Initialise le système audio
# - Tente de charger et de jouer la musique de fond en boucle
# En cas d'erreur de chargement audio, un message est affiché
# Retourne l'objet screen (surface principale d'affichage)
# ---------------------------------------------------------------
def initialize_pygame(SCREEN_WIDTH, SCREEN_HEIGHT,MUSIC_PATH):
    # Initialise tous les modules de base de Pygame (affichage, événements, etc.)
    pygame.init()

    # Initialise le module de mixage audio (sons et musique)
    pygame.mixer.init()  # Important pour pouvoir jouer de la musique ou des effets sonores

    # Crée la fenêtre principale du jeu avec la taille définie
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Définit le titre de la fenêtre du jeu
    pygame.display.set_caption('Crabinator')

    try:
        # Tente de charger la musique de fond depuis le chemin défini
        pygame.mixer.music.load(MUSIC_PATH)

        # Joue la musique en boucle infinie
        pygame.mixer.music.play(-1)

        # Réduit le volume de la musique à 20% pour ne pas couvrir les effets sonores
        pygame.mixer.music.set_volume(0.2)
    except pygame.error as e:
        # En cas d'erreur (fichier manquant, format invalide...), affiche un message d'avertissement
        print(f"Attention : Impossible de charger ou jouer la musique : {e}")

    # Retourne la surface principale de l'écran pour l'utiliser ailleurs dans le jeu
    return screen

