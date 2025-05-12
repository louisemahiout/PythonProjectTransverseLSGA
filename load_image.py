import pygame

# Fonctions pour le chargement d'images
def load_image(path, alpha=False):
    try:
        # Tente de charger l'image depuis le fichier donné
        image = pygame.image.load(path)
        # Si alpha est True, conserve la transparence ; sinon, conversion normale pour optimisation
        return image.convert_alpha() if alpha else image.convert()
    except pygame.error as e:
        # En cas d'erreur (fichier manquant, format invalide...), afficher un message d'erreur
        print(f"Erreur de chargement de l'image {path}: {e}")
        # Crée une surface par défaut pour éviter un crash
        default_surface = pygame.Surface((50, 50))
        default_surface.fill(RED)
        return default_surface  # Alternative : lever une erreur fatale avec SystemExit

# Fonction chargement de la police
def load_font(path, size):
    try:
        # Tente de charger une police depuis le fichier spécifié
        return pygame.font.Font(path, size)
    except pygame.error as e:
        # Si une erreur survient (fichier introuvable, corrompu, etc.), afficher une erreur
        print(f"Erreur de chargement de la police {path}: {e}")
        # Utilise la police par défaut de Pygame pour éviter que le jeu plante
        return pygame.font.Font(None, size)
