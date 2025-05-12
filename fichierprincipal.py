import pygame
import math
import sys
from load_image import *
from initialize import *
from menu_et_niveau import *
from gagner_perdu import *
from contextualisation import *
from jeu_principal import *
# === Constantes globales ===
SCREEN_WIDTH = 725
SCREEN_HEIGHT = 550
FPS = 60

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
SAND_COLOR = (237, 201, 175)
GREEN_BORDER = (0, 100, 0)
BLUE_ENEMY = (0, 0, 255)
INVINCIBLE_COLOR_DEBUG = (255, 165, 0)  # Orange pour le debug de l'invincibilité
PLAYER_DEBUG_COLOR = (255, 0, 0)  # Rouge pour le debug hitbox joueur

# Dimensions joueur
PLAYER_WIDTH, PLAYER_HEIGHT = 64, 64

# Chemins des ressources
FONT_PATH = "assetsaffichage/PressStart2P.ttf"
MUSIC_PATH = "assetsaffichage/musique.mp3"
BACKGROUND_IMG_PATH_MENU = "assetsaffichage/fond1.jpg"
BACKGROUND_IMG_PATH_GAME = "assetsaffichage/fond2.jpg"
BACKGROUND_IMG_PATH_GAME2= "assetsaffichage/palmier2.jpg"
PLAY_BUTTON_IMG_PATH = 'assetsaffichage/boutonplay.png'
MENU_BUTTON_IMG_PATH = "assetsaffichage/boutonmenu.png"
CRAB_COLLECTIBLE_IMG_PATH = "assetsaffichage/crabe.png"
ENEMY_IMG_PATH = "assetsaffichage/ennemi.png"


# Préfixes pour les animations du héros
HERO_RUN_IMG_PATH_PREFIX = "Hero/Run ("
HERO_IDLE_IMG_PATH_PREFIX = "Hero/Idle ("
HERO_JUMP_IMG_PATH_PREFIX = "Hero/Jump ("


