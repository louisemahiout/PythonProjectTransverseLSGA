import pygame
import math
import sys

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
BACKGROUND_IMG_PATH_GAME2= "assetsaffichage/fond 5.jpg"
PLAY_BUTTON_IMG_PATH = 'assetsaffichage/boutonplay.png'
MENU_BUTTON_IMG_PATH = "assetsaffichage/boutonmenu.png"
CRAB_COLLECTIBLE_IMG_PATH = "assetsaffichage/crabe.png"

# Préfixes pour les animations du héros
HERO_RUN_IMG_PATH_PREFIX = "Hero/Run ("
HERO_IDLE_IMG_PATH_PREFIX = "Hero/Idle ("
HERO_JUMP_IMG_PATH_PREFIX = "Hero/Jump ("


# === Fonctions utilitaires pour le chargement ===
def load_image(path, alpha=False):
    try:
        image = pygame.image.load(path)
        return image.convert_alpha() if alpha else image.convert()
    except pygame.error as e:
        print(f"Erreur de chargement de l'image {path}: {e}")
        # Retourner une surface par défaut pour éviter un crash, ou quitter
        default_surface = pygame.Surface((50, 50))
        default_surface.fill(RED)
        return default_surface  # Ou `raise SystemExit(f"Impossible de charger: {path}")`


def load_font(path, size):
    try:
        return pygame.font.Font(path, size)
    except pygame.error as e:
        print(f"Erreur de chargement de la police {path}: {e}")
        return pygame.font.Font(None, size)  # Police système par défaut


# === Initialisation de Pygame (une seule fois) ===
def initialize_pygame():
    pygame.init()
    pygame.mixer.init()  # Pour les sons et la musique
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Crabinator')
    try:
        pygame.mixer.music.load(MUSIC_PATH)
        pygame.mixer.music.play(-1)  # Jouer en boucle
        pygame.mixer.music.set_volume(0.2)
    except pygame.error as e:
        print(f"Attention : Impossible de charger ou jouer la musique : {e}")
    return screen


# === Fonctions MENU & NIVEAUX (adaptées) ===

def show_menu(screen):
    background = load_image(BACKGROUND_IMG_PATH_MENU)
    play_button_img = load_image(PLAY_BUTTON_IMG_PATH, alpha=True)
    play_button_img = pygame.transform.scale(play_button_img, (300, 200))
    play_button_rect = play_button_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5))  # Centré et plus bas

    font_title = load_font(FONT_PATH, 48)
    title_text = font_title.render("CRABINATOR", True, BLACK)
    # Positionnement du titre au-dessus du bouton play
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, play_button_rect.top + 30))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"  # Indique de quitter le jeu
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    return "play"  # Indique de passer au choix de niveau

        screen.blit(background, (0, 0))
        screen.blit(title_text, title_rect)
        screen.blit(play_button_img, play_button_rect)
        pygame.display.flip()


def choose_level(screen):
    background = load_image(BACKGROUND_IMG_PATH_MENU)
    button_width, button_height = 350, 80  # Boutons un peu plus larges
    font_title = load_font(FONT_PATH, 30)  # Taille ajustée
    font_button = load_font(FONT_PATH, 20)  # Taille ajustée

    title_text = font_title.render("CHOISIS TON NIVEAU", True, BLACK)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))

    # Calcul des positions des rectangles pour les boutons
    level1_rect = pygame.Rect(0, 0, button_width, button_height)
    level1_rect.center = (SCREEN_WIDTH // 2, 250)
    level2_rect = pygame.Rect(0, 0, button_width, button_height)
    level2_rect.center = (SCREEN_WIDTH // 2, 370)  # Plus d'espace entre les boutons

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if level1_rect.collidepoint(event.pos):
                    return 1  # Retourne le numéro du niveau
                elif level2_rect.collidepoint(event.pos):
                    return 2

        screen.blit(background, (0, 0))

        # Fond semi-transparent pour le titre
        title_bg_surface = pygame.Surface((title_rect.width + 20, title_rect.height + 20), pygame.SRCALPHA)
        title_bg_surface.fill((255, 255, 255, 180))
        screen.blit(title_bg_surface, (title_rect.x - 10, title_rect.y - 10))
        screen.blit(title_text, title_rect)

        # Fonction pour dessiner les boutons de niveau
        def draw_level_button(rect, text):
            # Fond du bouton
            btn_bg_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            btn_bg_surface.fill((220, 220, 220, 200))  # Gris clair semi-transparent
            screen.blit(btn_bg_surface, rect.topleft)
            pygame.draw.rect(screen, BLACK, rect, 2, border_radius=10)  # Bordure

            label = font_button.render(text, True, BLACK)
            label_rect = label.get_rect(center=rect.center)
            screen.blit(label, label_rect)

        draw_level_button(level1_rect, "NIVEAU 1 (Facile)")
        draw_level_button(level2_rect, "NIVEAU 2 (Moyen)")

        pygame.display.flip()


def show_game_over_screen(screen):
    background = load_image(BACKGROUND_IMG_PATH_MENU)  # Peut être un fond spécifique "game over"
    title_font = load_font(FONT_PATH, 36)
    button_font = load_font(FONT_PATH, 18)

    # Assombrir l'écran
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # Noir semi-transparent

    button_width = 400  # Boutons un peu moins larges que dans le code original
    button_height = 60
    restart_button_rect = pygame.Rect((SCREEN_WIDTH - button_width) // 2, 300, button_width, button_height)
    menu_button_rect = pygame.Rect((SCREEN_WIDTH - button_width) // 2, 380, button_width, button_height)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button_rect.collidepoint(event.pos):
                    return "restart"
                elif menu_button_rect.collidepoint(event.pos):
                    return "menu"

        screen.blit(background, (0, 0))
        screen.blit(overlay, (0, 0))  # Appliquer l'assombrissement

        title_text = title_font.render("PERDU", True, RED)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 225))
        screen.blit(title_text, title_rect)

        # Dessin des boutons
        pygame.draw.rect(screen, WHITE, restart_button_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, menu_button_rect, border_radius=10)

        restart_text = button_font.render("Relancer le niveau", True, BLACK)
        restart_text_rect = restart_text.get_rect(center=restart_button_rect.center)
        screen.blit(restart_text, restart_text_rect)

        menu_text = button_font.render("Retour au menu", True, BLACK)
        menu_text_rect = menu_text.get_rect(center=menu_button_rect.center)
        screen.blit(menu_text, menu_text_rect)

        pygame.display.flip()

def show_win_screen(screen):
    background = load_image(BACKGROUND_IMG_PATH_MENU)
    font = load_font(FONT_PATH, 36)
    button_font = load_font(FONT_PATH, 20)

    button_rect = pygame.Rect((SCREEN_WIDTH - 300) // 2, 350, 300, 60)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(event.pos):
                return "menu"

        screen.blit(background, (0, 0))
        win_text = font.render("TU T'ES ENFUI!", True, BLACK)
        screen.blit(win_text, win_text.get_rect(center=(SCREEN_WIDTH // 1.85, 290)))

        pygame.draw.rect(screen, WHITE, button_rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, button_rect, 2, border_radius=10)
        label = button_font.render("Retour au menu", True, BLACK)
        screen.blit(label, label.get_rect(center=button_rect.center))

        pygame.display.flip()


def show_context(screen):
    # Charger l'image de fond
    background = pygame.image.load("assetsaffichage/transverse.png").convert()
    font = pygame.font.Font(FONT_PATH, 11)

    # Liste de textes à afficher progressivement
    text_lines = [
        "Bienvenue dans l’univers de Crabinator !",
        "La plage est envahie par des créatures terrifiantes qui menacent",
        "tout sur leur passage. Mais elles ont une faiblesse : elles",
        "détestent les crabes! Alors attrape-en, vise bien… et bombarde",
        "-les pour te défendre et t'enfuire!"
    ]

    # Affichage initial de l'image de fond
    screen.blit(background, (0, 0))

    # Zone noire sous l'image si l'image ne couvre pas tout l'écran
    image_height = background.get_height()
    screen.fill((0, 0, 0), pygame.Rect(0, image_height, screen.get_width(), screen.get_height() - image_height))
    pygame.display.flip()

    y_offset = 425  # Position initiale pour afficher le texte
    line_delay = 50
    skip = False

    # === BOUTON PASSER ===
    skip_button_font = load_font(FONT_PATH, 18)
    skip_button_text = skip_button_font.render("Passer", True, BLACK)
    skip_button_rect = pygame.Rect(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 60, 120, 40)

    # Dessiner une fois au début
    pygame.draw.rect(screen, (255, 255, 255), skip_button_rect, border_radius=10)
    pygame.draw.rect(screen, BLACK, skip_button_rect, 2, border_radius=10)
    screen.blit(skip_button_text, skip_button_text.get_rect(center=skip_button_rect.center))
    pygame.display.flip()


    for line in text_lines:
        rendered_line = ""
        for char in line:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if skip_button_rect.collidepoint(event.pos):
                        skip = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    skip = True

            if skip:
                break

            rendered_line += char

            # Redessiner le fond + fond noir
            screen.blit(background, (0, 0))
            screen.fill((0, 0, 0), pygame.Rect(0, image_height, screen.get_width(), screen.get_height() - image_height))
            # Réafficher le bouton "Passer"
            pygame.draw.rect(screen, (255, 255, 255), skip_button_rect, border_radius=10)
            pygame.draw.rect(screen, BLACK, skip_button_rect, 2, border_radius=10)
            screen.blit(skip_button_text, skip_button_text.get_rect(center=skip_button_rect.center))

            # Afficher les lignes précédentes
            for i in range(len(text_lines)):
                if i < text_lines.index(line):
                    text_surface = font.render(text_lines[i], True, (255, 255, 255))
                    screen.blit(text_surface, (20, 425 + i * 20))

            # Afficher la ligne en cours
            text_surface = font.render(rendered_line, True, (255, 255, 255))
            screen.blit(text_surface, (20, y_offset))

            pygame.display.flip()
            pygame.time.delay(line_delay)

        if skip:
            break

        y_offset += 20
        pygame.time.delay(500)

    if skip:
        screen.blit(background, (0, 0))
        screen.fill((0, 0, 0), pygame.Rect(0, image_height, screen.get_width(), screen.get_height() - image_height))
        y_offset = 425
        for line in text_lines:
            text_surface = font.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (20, y_offset))
            y_offset += 20
        pygame.display.flip()
        pygame.time.delay(1000)


# === JEU PRINCIPAL ===
def run_game(screen, level_chosen):
    clock = pygame.time.Clock()
    pygame.display.set_caption(f"Crabinator – Niveau {level_chosen}")

    # --- Chargement des ressources spécifiques au jeu ---
    menu_button_img = load_image(MENU_BUTTON_IMG_PATH, alpha=True)
    menu_button_img = pygame.transform.scale(menu_button_img, (100, 70))
    menu_button_rect = menu_button_img.get_rect(topright=(SCREEN_WIDTH - 20, 10))

    crab_img_collectible_orig = load_image(CRAB_COLLECTIBLE_IMG_PATH, alpha=True)
    crab_img_collectible = pygame.transform.scale(crab_img_collectible_orig, (PLAYER_WIDTH // 2, PLAYER_HEIGHT // 2))

    portal_img = load_image("assetsaffichage/fin.png", alpha=True)
    portal_img = pygame.transform.scale(portal_img, (128, 128))  # Taille personnalisable
    portal_rect_world = portal_img.get_rect(topleft=(4900, SCREEN_HEIGHT - 20 - 64-50))  # Fin du niveau

    # Sprites du joueur
    try:
        walk_anim = [pygame.transform.scale(load_image(f'{HERO_RUN_IMG_PATH_PREFIX}{i}).png', True),
                                            (PLAYER_WIDTH, PLAYER_HEIGHT)) for i in range(1, 15)]
        idle_anim = [pygame.transform.scale(load_image(f'{HERO_IDLE_IMG_PATH_PREFIX}{i}).png', True),
                                            (PLAYER_WIDTH, PLAYER_HEIGHT)) for i in range(1, 15)]
        jump_anim = [pygame.transform.scale(load_image(f'{HERO_JUMP_IMG_PATH_PREFIX}{i}).png', True),
                                            (PLAYER_WIDTH, PLAYER_HEIGHT)) for i in range(1, 17)]  # 16 frames
    except Exception as e:  # Plus générique si une image manque dans la séquence
        print(f"Erreur chargement animation joueur: {e}")
        return "menu"  # Retour au menu si animation non chargée

    # --- Variables du joueur ---
    crab_joueur_x_screen = 100  # Position à l'écran
    crab_joueur_y_screen = SCREEN_HEIGHT - 20 - PLAYER_HEIGHT
    crab_joueur_velocity = 5
    crab_joueur_jump_velocity = -16  # Un peu plus puissant
    gravity = 0.8
    crab_joueur_y_vel_world = 0  # Vitesse verticale (affecte la position dans le monde)
    crab_joueur_is_jumping = False
    crab_joueur_is_walking = False
    crab_joueur_facing_right = True
    current_frame, idle_frame, jump_frame = 0, 0, 0
    idle_counter = 0

    # --- Variables de tir ---
    ball_radius = 10
    ball_pos_world = None  # [x_monde, y_monde]
    ball_vel_world = None  # [vx_monde, vy_monde]
    selecting_trajectory = False

    # --- Variables de niveau ---
    scroll_x = 0
    ground_rect_world = pygame.Rect(0, SCREEN_HEIGHT - 20, 5000, 20)  # Coordonnées monde
    max_scroll_x = ground_rect_world.width - SCREEN_WIDTH

    platforms_world = []
    collectibles_world = []
    enemies_world = []
    collectibles_collected_count = 0
    collectible_type_name = ""
    bot_speed_base = 0  # Sera défini par niveau

    if level_chosen == 1:
        background_img_game = load_image(BACKGROUND_IMG_PATH_GAME)
        # Correction: flip horizontal pour boucle, pas vertical
        flipped_bg_img = pygame.transform.flip(background_img_game, True, False)
        bg_width = background_img_game.get_width()
        collectible_type_name = "Crabe(s)"
        bot_speed_base = 1.5  # Plus lent pour le niveau 1
        platforms_world = [
            pygame.Rect(500, 420, 100, 20), pygame.Rect(700, 360, 100, 20),
            pygame.Rect(1700, 420, 100, 20), pygame.Rect(1900, 360, 100, 20),
            pygame.Rect(2100, 300, 100, 20), pygame.Rect(2800, 420, 100, 20),
            pygame.Rect(3000, 360, 100, 20), pygame.Rect(3200, 420, 100, 20),
            pygame.Rect(3600, 360, 100, 20), pygame.Rect(4000, 420, 100, 20),
            pygame.Rect(4200, 360, 100, 20), pygame.Rect(4400, 300, 100, 20),
            pygame.Rect(4800, 420, 100, 20),
        ]
        collectibles_world = [
            {"rect": pygame.Rect(280, 505 - crab_img_collectible.get_height(), crab_img_collectible.get_width(),
                                 crab_img_collectible.get_height()), "collected": False, "name": "Carapatte1"},
            {"rect": pygame.Rect(750, 370 - crab_img_collectible.get_height(), crab_img_collectible.get_width(),
                                 crab_img_collectible.get_height()), "collected": False, "name": "Carapatte2"},
            {"rect": pygame.Rect(1360, 535 - crab_img_collectible.get_height(), crab_img_collectible.get_width(),
                                 crab_img_collectible.get_height()), "collected": False, "name": "Carapatte3"},
            {"rect": pygame.Rect(1600, 270 - crab_img_collectible.get_height(), crab_img_collectible.get_width(),
                                 crab_img_collectible.get_height()), "collected": False, "name": "Carapatte4"},
            # Original y: 270, crabe y: 270-h
            {"rect": pygame.Rect(2100, 310 - crab_img_collectible.get_height(), crab_img_collectible.get_width(),
                                 crab_img_collectible.get_height()), "collected": False, "name": "Carapatte5"},
            {"rect": pygame.Rect(2300, 525 - crab_img_collectible.get_height(), crab_img_collectible.get_width(),
                                 crab_img_collectible.get_height()), "collected": False, "name": "Carapatte5"},
            {"rect": pygame.Rect(2600, 525 - crab_img_collectible.get_height(), crab_img_collectible.get_width(),
                                 crab_img_collectible.get_height()), "collected": False, "name": "Carapatte6"},
            {"rect": pygame.Rect(3025, 325 - crab_img_collectible.get_height(), crab_img_collectible.get_width(),
                                 crab_img_collectible.get_height()), "collected": False, "name": "Carapatte6"},
            {"rect": pygame.Rect(3600, 525 - crab_img_collectible.get_height(), crab_img_collectible.get_width(),
                                 crab_img_collectible.get_height()), "collected": False, "name": "Carapatte6"},
            {"rect": pygame.Rect(3250, 400 - crab_img_collectible.get_height(), crab_img_collectible.get_width(),
                                 crab_img_collectible.get_height()), "collected": False, "name": "Carapatte7"},
            {"rect": pygame.Rect(4000, 270 - crab_img_collectible.get_height(), crab_img_collectible.get_width(),
                                 crab_img_collectible.get_height()), "collected": False, "name": "Carapatte8"},
            {"rect": pygame.Rect(4300, 325 - crab_img_collectible.get_height(), crab_img_collectible.get_width(),
                                 crab_img_collectible.get_height()), "collected": False, "name": "Carapatte9"},
            {"rect": pygame.Rect(4479, 525 - crab_img_collectible.get_height(), crab_img_collectible.get_width(),
                                 crab_img_collectible.get_height()), "collected": False, "name": "Carapatte9"},
            {"rect": pygame.Rect(4700, 525 - crab_img_collectible.get_height(), crab_img_collectible.get_width(),
                                 crab_img_collectible.get_height()), "collected": False, "name": "Carapatte9"},
        ]
        enemies_world = [  # Ajout de 'original_x', 'patrol_range', 'direction' pour le mouvement
            {"rect": pygame.Rect(1700, 420 - 30, 40, 30), "name": "Bot3", "original_x": 1700, "patrol_range": 0,
             "direction": 1, "speed_factor": 1},
            {"rect": pygame.Rect(1900, 360 - 30, 40, 30), "name": "Bot4", "original_x": 1900, "patrol_range": 0,
             "direction": 1, "speed_factor": 1},
            {"rect": pygame.Rect(2800, 420 - 30, 40, 30), "name": "Bot6", "original_x": 2800, "patrol_range": 0,
             "direction": 1, "speed_factor": 1},
            {"rect": pygame.Rect(3000, 360 - 30, 40, 30), "name": "Bot7", "original_x": 3000, "patrol_range": 0,
             "direction": 1, "speed_factor": 1},
            {"rect": pygame.Rect(3600, 360 - 30, 40, 30), "name": "Bot7", "original_x": 3000, "patrol_range": 0,
             "direction": 1, "speed_factor": 1},
            {"rect": pygame.Rect(4000, 420 - 30, 40, 30), "name": "Bot10", "original_x": 4000, "patrol_range": 0,
             "direction": 1, "speed_factor": 1},
            {"rect": pygame.Rect(4200, 360 - 30, 40, 30), "name": "Bot11", "original_x": 4200, "patrol_range": 0,
             "direction": 1, "speed_factor": 1},
            {"rect": pygame.Rect(4800, 420 - 30, 40, 30), "name": "Bot13", "original_x": 4800, "patrol_range": 0,
             "direction": 1, "speed_factor": 1},


            {"rect": pygame.Rect(600, SCREEN_HEIGHT - 20 - 30, 40, 30), "name": "BotSol1", "original_x": 600,
             "patrol_range": 100, "direction": 1, "speed_factor": 0.8},
            {"rect": pygame.Rect(1500, SCREEN_HEIGHT - 20 - 30, 40, 30), "name": "BotSol2", "original_x": 1500,
             "patrol_range": 100, "direction": 1, "speed_factor": 0.8},
            {"rect": pygame.Rect(2500, SCREEN_HEIGHT - 20 - 30, 40, 30), "name": "BotSol3", "original_x": 2500,
             "patrol_range": 100, "direction": 1, "speed_factor": 0.8},
            {"rect": pygame.Rect(3500, SCREEN_HEIGHT - 20 - 30, 40, 30), "name": "BotSol4", "original_x": 3500,
             "patrol_range": 100, "direction": 1, "speed_factor": 0.8},
            {"rect": pygame.Rect(4600, SCREEN_HEIGHT - 20 - 30, 40, 30), "name": "BotSol5", "original_x": 4600,
             "patrol_range": 100, "direction": 1, "speed_factor": 0.8},
            {"rect": pygame.Rect(4400, SCREEN_HEIGHT - 20 - 30, 40, 30), "name": "BotSol5", "original_x": 4400,
             "patrol_range": 100, "direction": 1, "speed_factor": 0.8},
            {"rect": pygame.Rect(2200, SCREEN_HEIGHT - 20 - 30, 40, 30), "name": "BotSol5", "original_x": 2200,
             "patrol_range": 100, "direction": 1, "speed_factor": 0.8},
        ]

    elif level_chosen == 2:
        background_img_game = load_image(BACKGROUND_IMG_PATH_GAME)
        # Correction: flip horizontal pour boucle, pas vertical
        flipped_bg_img = pygame.transform.flip(background_img_game, True, False)
        bg_width = background_img_game.get_width()
        collectible_type_name = "Crabes(s)"
        bot_speed_base = 1.7  # Plus rapide pour le niveau 2
        platforms_world = [
            pygame.Rect(200, 420, 100, 20), pygame.Rect(400, 360, 100, 20),
            pygame.Rect(1000, 420, 100, 20),
            pygame.Rect(1200, 450, 100, 20),
            pygame.Rect(1500, 360, 100, 20),

            pygame.Rect(2000, 300, 100, 20), pygame.Rect(2500, 420, 100, 20),
            pygame.Rect(2900, 360, 100, 20), pygame.Rect(3600, 420, 100, 20),
            pygame.Rect(3900, 360, 100, 20), pygame.Rect(4400, 420, 100, 20),
            pygame.Rect(4700, 360, 100, 20),
        ]
        collectibles_world = [
            {"rect": pygame.Rect(380, 538 - crab_img_collectible.get_height(), crab_img_collectible.get_width(),
                                 crab_img_collectible.get_height()), "collected": False, "name": "Pinceur1"},
            {"rect": pygame.Rect(450, 375 - crab_img_collectible.get_height(), crab_img_collectible.get_width(),
                                 crab_img_collectible.get_height()), "collected": False, "name": "Pinceur1"},
            {"rect": pygame.Rect(1000, 430 - crab_img_collectible.get_height(), crab_img_collectible.get_width(),
                                 crab_img_collectible.get_height()), "collected": False, "name": "Pinceur1"},
            {"rect": pygame.Rect(750, 538 - crab_img_collectible.get_height(), crab_img_collectible.get_width(),
                                 crab_img_collectible.get_height()), "collected": False, "name": "Pinceur2"},
            {"rect": pygame.Rect(2300, 538 - crab_img_collectible.get_height(), crab_img_collectible.get_width(),
                                 crab_img_collectible.get_height()), "collected": False, "name": "Pinceur2"},
            {"rect": pygame.Rect(1500, 460 - crab_img_collectible.get_height(), crab_img_collectible.get_width(),
                                 crab_img_collectible.get_height()), "collected": False, "name": "Pinceur3"},
            {"rect": pygame.Rect(1800, 300 - crab_img_collectible.get_height(), crab_img_collectible.get_width(),
                                 crab_img_collectible.get_height()), "collected": False, "name": "Pinceur4"},
            {"rect": pygame.Rect(2700, 300 - crab_img_collectible.get_height(), crab_img_collectible.get_width(),
                                 crab_img_collectible.get_height()), "collected": False, "name": "Pinceur6"},
            {"rect": pygame.Rect(3100, 300 - crab_img_collectible.get_height(), crab_img_collectible.get_width(),
                                 crab_img_collectible.get_height()), "collected": False, "name": "Pinceur7"},
            {"rect": pygame.Rect(3800, 300 - crab_img_collectible.get_height(), crab_img_collectible.get_width(),
                                 crab_img_collectible.get_height()), "collected": False, "name": "Pinceur7"},
            {"rect": pygame.Rect(4000, 270 - crab_img_collectible.get_height(), crab_img_collectible.get_width(),
                                 crab_img_collectible.get_height()), "collected": False, "name": "Pinceur8"},
            {"rect": pygame.Rect(4450, 380- crab_img_collectible.get_height(), crab_img_collectible.get_width(),
                                 crab_img_collectible.get_height()), "collected": False, "name": "Pinceur8"},
        ]
        enemies_world = [
            {"rect": pygame.Rect(200, 420 - 30, 40, 30), "name": "Gardien1", "original_x": 200, "patrol_range": 0,
             "direction": 1, "speed_factor": 1.2},
            {"rect": pygame.Rect(1500, 360 - 30, 40, 30), "name": "Gardien4", "original_x": 1500, "patrol_range": 0,
             "direction": 1, "speed_factor": 1.2},
            {"rect": pygame.Rect(2000, 300 - 30, 40, 30), "name": "Gardien5", "original_x": 2000, "patrol_range": 0,
             "direction": 1, "speed_factor": 1.2},
            {"rect": pygame.Rect(2500, 420 - 30, 40, 30), "name": "Gardien6", "original_x": 2500, "patrol_range": 0,
             "direction": 1, "speed_factor": 1.2},
            {"rect": pygame.Rect(2900, 360 - 30, 40, 30), "name": "Gardien7", "original_x": 2900, "patrol_range": 0,
             "direction": 1, "speed_factor": 1.2},
            {"rect": pygame.Rect(3600, 420 - 30, 40, 30), "name": "Gardien8", "original_x": 3600, "patrol_range": 0,
             "direction": 1, "speed_factor": 1.2},
            {"rect": pygame.Rect(3900, 360 - 30, 40, 30), "name": "Gardien9", "original_x": 3900, "patrol_range": 0,
             "direction": 1, "speed_factor": 1.2},
            {"rect": pygame.Rect(4400, 420 - 30, 40, 30), "name": "Gardien10", "original_x": 4400, "patrol_range": 0,
             "direction": 1, "speed_factor": 1.2},


            {"rect": pygame.Rect(600, SCREEN_HEIGHT - 20 - 30, 40, 30), "name": "Patrouilleur1", "original_x": 600,
             "patrol_range": 150, "direction": 1, "speed_factor": 1},
            {"rect": pygame.Rect(1500, SCREEN_HEIGHT - 20 - 30, 40, 30), "name": "Patrouilleur2", "original_x": 1500,
             "patrol_range": 150, "direction": 1, "speed_factor": 1},
            {"rect": pygame.Rect(2500, SCREEN_HEIGHT - 20 - 30, 40, 30), "name": "Patrouilleur3", "original_x": 2500,
             "patrol_range": 150, "direction": 1, "speed_factor": 1},
            {"rect": pygame.Rect(3500, SCREEN_HEIGHT - 20 - 30, 40, 30), "name": "Patrouilleur4", "original_x": 3500,
             "patrol_range": 150, "direction": 1, "speed_factor": 1},
            {"rect": pygame.Rect(4600, SCREEN_HEIGHT - 20 - 30, 40, 30), "name": "Patrouilleur5", "original_x": 4600,
             "patrol_range": 150, "direction": 1, "speed_factor": 1},
        ]
    # Ajuster la position Y des collectibles pour qu'ils soient POSÉS SUR le sol/plateforme
    # Cela suppose que leur rect.y original est le bas du crabe. Si c'est le haut, ajustez.
    for item in collectibles_world:
        item["rect"].y = item["rect"].y  # Si item["rect"].y est déjà le coin supérieur gauche.
        # Si c'était le bas, il faudrait faire item["rect"].bottom = original_y

    # --- Vies & invincibilité ---
    lives = 3
    invincible = False
    inv_time_start = 0
    INV_DURATION = 2000  # ms

    # --- Texte tutoriel ---
    show_tutorial_text = (level_chosen == 1)
    tutorial_font = load_font(FONT_PATH, 11)
    tutorial_lines = [
        "Utilise les fleches pour te deplacer,",
        "Espace pour sauter. Clique sur ton perso",
        "puis vise avec la souris pour tirer!"
    ]
    # Position Y de départ pour le texte du tutoriel
    tutorial_start_y = 120

    # --- Fonction pour dessiner la flèche de visée ---
    def draw_aiming_arrow(surface, start_pos_screen, mouse_pos_screen):
        pygame.draw.line(surface, BLACK, start_pos_screen, mouse_pos_screen, 3)
        angle = math.atan2(mouse_pos_screen[1] - start_pos_screen[1], mouse_pos_screen[0] - start_pos_screen[0])
        arrow_size = 10
        # Pointe gauche de la flèche
        left_x = mouse_pos_screen[0] - arrow_size * math.cos(angle + math.pi / 6)
        left_y = mouse_pos_screen[1] - arrow_size * math.sin(angle + math.pi / 6)
        # Pointe droite de la flèche
        right_x = mouse_pos_screen[0] - arrow_size * math.cos(angle - math.pi / 6)
        right_y = mouse_pos_screen[1] - arrow_size * math.sin(angle - math.pi / 6)
        pygame.draw.polygon(surface, BLACK, [mouse_pos_screen, (left_x, left_y), (right_x, right_y)])

    # --- Boucle de jeu principale ---
    game_running = True
    while game_running:
        dt = clock.tick(
            FPS) / 1000.0  # Delta time en secondes (pour physique indépendante du framerate, non utilisé ici mais bonne pratique)

        # --- Gestion des événements ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    if menu_button_rect.collidepoint(event.pos):
                        return "menu"

                    player_rect_screen = pygame.Rect(crab_joueur_x_screen, crab_joueur_y_screen, PLAYER_WIDTH,
                                                     PLAYER_HEIGHT)
                    if player_rect_screen.collidepoint(event.pos):
                        if collectibles_collected_count > 0:
                            selecting_trajectory = True
                        else:
                            # Peut-être un son "pas de munitions"
                            print("Pas de munitions pour tirer !")
                            selecting_trajectory = False  # S'assurer que c'est faux
                    # else: # Clic en dehors du joueur pendant la visée annule aussi
                    #    selecting_trajectory = False

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and selecting_trajectory:
                    if collectibles_collected_count > 0:  # Double vérification
                        mouse_pos_screen = event.pos
                        player_center_x_screen = crab_joueur_x_screen + PLAYER_WIDTH // 2
                        player_center_y_screen = crab_joueur_y_screen + PLAYER_HEIGHT // 2

                        dx_screen = mouse_pos_screen[0] - player_center_x_screen
                        dy_screen = mouse_pos_screen[1] - player_center_y_screen

                        # La balle part du centre du joueur (coordonnées monde)
                        ball_pos_world = [player_center_x_screen + scroll_x, player_center_y_screen]

                        # Calcul de la vélocité de la balle
                        # La puissance pourrait dépendre de la distance de la souris
                        distance = math.hypot(dx_screen, dy_screen)
                        if distance == 0: distance = 1  # Eviter division par zéro

                        power_multiplier = 0.15  # Ajuster pour la sensibilité/puissance du tir
                        max_speed = 20  # Vitesse maximale du projectile

                        vel_x = (dx_screen / distance) * min(distance * power_multiplier, max_speed)
                        vel_y = (dy_screen / distance) * min(distance * power_multiplier, max_speed)
                        ball_vel_world = [vel_x, vel_y]

                        collectibles_collected_count -= 1
                    selecting_trajectory = False

        # --- Logique de jeu (mouvements, collisions, etc.) ---

        # Mouvement du joueur (basé sur les touches)
        keys = pygame.key.get_pressed()
        previous_crab_is_walking = crab_joueur_is_walking
        crab_joueur_is_walking = False  # Réinitialiser à chaque frame

        if keys[pygame.K_RIGHT]:
            crab_joueur_is_walking = True
            crab_joueur_facing_right = True

            if crab_joueur_x_screen < SCREEN_WIDTH * 0.6 or scroll_x >= max_scroll_x:
                # Bouger le personnage à l’écran si on n’a plus de scroll
                crab_joueur_x_screen += crab_joueur_velocity
            elif scroll_x < max_scroll_x:
                # Sinon, scroller le monde
                scroll_x += crab_joueur_velocity

            # Limiter la position à droite de l'écran
            crab_joueur_x_screen = min(crab_joueur_x_screen, SCREEN_WIDTH - PLAYER_WIDTH)

        elif keys[pygame.K_LEFT]:
            crab_joueur_is_walking = True
            crab_joueur_facing_right = False

            if crab_joueur_x_screen > SCREEN_WIDTH * 0.4 or scroll_x <= 0:
                # Bouger le personnage si on ne peut plus scroller
                crab_joueur_x_screen -= crab_joueur_velocity
            elif scroll_x > 0:
                # Sinon, scroller le monde vers la gauche
                scroll_x -= crab_joueur_velocity

            # Limiter à gauche
            crab_joueur_x_screen = max(crab_joueur_x_screen, 0)

        # Réinitialiser l'animation de marche si l'état change
        if crab_joueur_is_walking and not previous_crab_is_walking:
            current_frame = 0

        # Saut du joueur
        if not crab_joueur_is_jumping and keys[pygame.K_SPACE]:
            crab_joueur_is_jumping = True
            crab_joueur_y_vel_world = crab_joueur_jump_velocity
            jump_frame = 0  # Réinitialiser l'animation de saut

        # Gravité et mouvement vertical du joueur
        crab_joueur_y_vel_world += gravity
        crab_joueur_y_screen += crab_joueur_y_vel_world

        # Hitbox du joueur en coordonnées monde pour les collisions
        player_rect_world = pygame.Rect(crab_joueur_x_screen + scroll_x, crab_joueur_y_screen, PLAYER_WIDTH,
                                        PLAYER_HEIGHT)
        on_ground_this_frame = False

        # Collision avec le sol (monde)
        if player_rect_world.colliderect(ground_rect_world):
            if crab_joueur_y_vel_world > 0:  # Si le joueur tombe
                player_rect_world.bottom = ground_rect_world.top
                crab_joueur_y_screen = player_rect_world.top  # Mettre à jour la coordonnée Y à l'écran
                crab_joueur_y_vel_world = 0
                crab_joueur_is_jumping = False
                on_ground_this_frame = True

        # Collision avec les plateformes (monde)
        for plat_world in platforms_world:
            if player_rect_world.colliderect(plat_world):
                # Collision par le dessus (atterrissage)
                # Le joueur doit tomber (vitesse Y > 0)
                # Et le bas du joueur dans la frame précédente devait être au-dessus ou au niveau du haut de la plateforme
                if crab_joueur_y_vel_world > 0 and (
                        player_rect_world.bottom - crab_joueur_y_vel_world) <= plat_world.top + 1:  # +1 pour marge
                    player_rect_world.bottom = plat_world.top
                    crab_joueur_y_screen = player_rect_world.top
                    crab_joueur_y_vel_world = 0
                    crab_joueur_is_jumping = False
                    on_ground_this_frame = True
                # Collision par le dessous (se cogne la tête)
                # Le joueur doit monter (vitesse Y < 0)
                # Et le haut du joueur dans la frame précédente devait être en dessous ou au niveau du bas de la plateforme
                elif crab_joueur_y_vel_world < 0 and (
                        player_rect_world.top - crab_joueur_y_vel_world) >= plat_world.bottom - 1:
                    player_rect_world.top = plat_world.bottom
                    crab_joueur_y_screen = player_rect_world.top
                    crab_joueur_y_vel_world = 0  # Arrêter la montée

        # Si le joueur tombe en dehors du monde (très bas)
        if player_rect_world.top > SCREEN_HEIGHT + 200:  # Une marge sous l'écran
            lives -= 1
            if lives <= 0:
                action_game_over = show_game_over_screen(screen)
                return action_game_over  # "restart", "menu", ou "quit"
            else:  # Réinitialiser la position du joueur
                crab_joueur_x_screen = 100
                crab_joueur_y_screen = SCREEN_HEIGHT - 20 - PLAYER_HEIGHT - 100  # Un peu au-dessus du sol
                scroll_x = 0
                crab_joueur_y_vel_world = 0
                crab_joueur_is_jumping = False
                invincible = True  # Courte invincibilité après une chute
                inv_time_start = pygame.time.get_ticks()

        # Collecte des items
        for item_data in collectibles_world:
            if not item_data["collected"] and player_rect_world.colliderect(item_data["rect"]):
                item_data["collected"] = True
                collectibles_collected_count += 1
                print(
                    f"{collectible_type_name[:-1]} collecté ! Total : {collectibles_collected_count}, Nom: {item_data['name']}")
                # Ajouter un son de collecte ici si désiré

        # Mouvement et physique de la balle
        if ball_pos_world:
            ball_vel_world[1] += gravity * 0.7  # Gravité sur la balle (peut être différente)
            ball_pos_world[0] += ball_vel_world[0]
            ball_pos_world[1] += ball_vel_world[1]

            ball_rect_world = pygame.Rect(ball_pos_world[0] - ball_radius, ball_pos_world[1] - ball_radius,
                                          ball_radius * 2, ball_radius * 2)

            # Collision balle avec sol
            if ball_rect_world.colliderect(ground_rect_world):
                if ball_vel_world[1] > 0:  # Si la balle tombe
                    ball_pos_world[1] = ground_rect_world.top - ball_radius
                    ball_vel_world[1] *= -0.6  # Rebond avec perte d'énergie
                    ball_vel_world[0] *= 0.8  # Friction au sol
                    if abs(ball_vel_world[1]) < 1: ball_vel_world[1] = 0  # Arrêter petits rebonds

            # Collision balle avec plateformes
            for plat_world in platforms_world:
                if ball_rect_world.colliderect(plat_world):
                    # Collision verticale simple
                    if ball_vel_world[1] > 0 and ball_rect_world.bottom >= plat_world.top and (
                            ball_rect_world.bottom - ball_vel_world[1]) <= plat_world.top + 1:
                        ball_pos_world[1] = plat_world.top - ball_radius
                        ball_vel_world[1] *= -0.6
                        ball_vel_world[0] *= 0.8
                    elif ball_vel_world[1] < 0 and ball_rect_world.top <= plat_world.bottom and (
                            ball_rect_world.top - ball_vel_world[1]) >= plat_world.bottom - 1:
                        ball_pos_world[1] = plat_world.bottom + ball_radius
                        ball_vel_world[1] *= -0.6  # Rebond sur le dessous
                    # Pourrait aussi gérer les collisions latérales si nécessaire
                    if abs(ball_vel_world[1]) < 0.5 and ball_vel_world[
                        1] != 0: ball_pos_world = None  # Arrêter si la balle roule bizarrement

            # Collision balle avec ennemis (itérer sur une copie pour suppression)
            for enemy_data in enemies_world[:]:
                if ball_rect_world.colliderect(enemy_data["rect"]):
                    print(f"Balle a touché {enemy_data['name']}")
                    enemies_world.remove(enemy_data)
                    ball_pos_world = None  # La balle disparaît
                    # Ajouter son/effet d'explosion
                    break  # Une balle ne touche qu'un ennemi

            # Si la balle sort très loin des limites
            if ball_pos_world and (
                    ball_pos_world[0] < -SCREEN_WIDTH or ball_pos_world[0] > ground_rect_world.width + SCREEN_WIDTH or
                    ball_pos_world[1] > SCREEN_HEIGHT + 200):
                ball_pos_world = None

        # Mouvement des ennemis
        player_center_world_x = player_rect_world.centerx
        for enemy_data in enemies_world:
            enemy_rect_world = enemy_data["rect"]
            current_bot_speed = bot_speed_base * enemy_data.get("speed_factor", 1)

            on_platform = False
            for plat in platforms_world:
                # On vérifie s'il y a une plateforme juste en dessous de l'ennemi (petite marge de 2 pixels)
                if enemy_rect_world.bottom == plat.top and \
                        plat.left <= enemy_rect_world.centerx <= plat.right:
                    on_platform = True
                    break

            if enemy_data["patrol_range"] > 0:
                # Ennemis au sol avec patrouille
                enemy_rect_world.x += current_bot_speed * enemy_data["direction"]
                if enemy_data["direction"] == 1 and enemy_rect_world.right > enemy_data["original_x"] + enemy_data[
                    "patrol_range"]:
                    enemy_data["direction"] = -1
                    enemy_rect_world.right = enemy_data["original_x"] + enemy_data["patrol_range"]
                elif enemy_data["direction"] == -1 and enemy_rect_world.left < enemy_data["original_x"] - enemy_data[
                    "patrol_range"]:
                    enemy_data["direction"] = 1
                    enemy_rect_world.left = enemy_data["original_x"] - enemy_data["patrol_range"]
            else:
                # Ennemis sur plateforme (sans patrouille) : aller-retour automatique
                if on_platform:
                    enemy_rect_world.x += current_bot_speed * enemy_data["direction"]

                    # Vérifie s'il va tomber (plus de plateforme dessous au prochain déplacement)
                    will_fall = True
                    next_center_x = enemy_rect_world.centerx + current_bot_speed * enemy_data["direction"]
                    for plat in platforms_world:
                        if enemy_rect_world.bottom == plat.top and \
                                plat.left <= next_center_x <= plat.right:
                            will_fall = False
                            break
                    if will_fall:
                        enemy_data["direction"] *= -1  # Change de direction
                else:
                    # S'il n'est pas sur une plateforme, on l'empêche d'avancer
                    enemy_data["direction"] *= -1

            # Simple gravité pour les ennemis (s'ils ne sont pas sur une plateforme fixe) - Optionnel
            # enemy_rect_world.y += gravity # Ils tomberaient des plateformes

        # Gestion de l'invincibilité
        current_time = pygame.time.get_ticks()
        if invincible and current_time - inv_time_start > INV_DURATION:
            invincible = False

        # Collision joueur - ennemis
        if not invincible:
            for enemy_data in enemies_world:
                if player_rect_world.colliderect(enemy_data["rect"]):
                    lives -= 1
                    invincible = True
                    inv_time_start = current_time
                    print(f"Touché par {enemy_data['name']}! Vies restantes : {lives}")
                    # Petit effet de recul (optionnel)
                    crab_joueur_y_vel_world = -5  # Petit saut
                    if player_rect_world.centerx < enemy_data["rect"].centerx:
                        crab_joueur_x_screen = max(0, crab_joueur_x_screen - 30)  # Recul gauche
                    else:
                        crab_joueur_x_screen = min(SCREEN_WIDTH - PLAYER_WIDTH,
                                                   crab_joueur_x_screen + 30)  # Recul droit

                    if lives <= 0:
                        action_game_over = show_game_over_screen(screen)
                        return action_game_over  # "restart", "menu", ou "quit"
                    break  # Une seule collision par frame suffit

        # Animation du joueur
        player_img_to_draw = None
        if crab_joueur_is_jumping:
            # S'assurer que jump_frame ne dépasse pas la longueur de l'animation
            player_img_to_draw = jump_anim[min(jump_frame, len(jump_anim) - 1)]
            if on_ground_this_frame and crab_joueur_y_vel_world == 0:  # Atterrissage
                crab_joueur_is_jumping = False  # Prêt pour idle/walk
                jump_frame = 0
            elif jump_frame < len(jump_anim) - 1:  # Continuer l'animation si en l'air
                jump_frame += 1
                # Ralentir l'animation de saut si nécessaire:
                # if pygame.time.get_ticks() % 100 < 50: # exemple de ralentissement
                #    jump_frame = min(jump_frame + 1, len(jump_anim) - 1)


        elif crab_joueur_is_walking:
            player_img_to_draw = walk_anim[current_frame]
            current_frame = (current_frame + 1) % len(walk_anim)
        else:  # Idle
            player_img_to_draw = idle_anim[idle_frame]
            idle_counter += 1
            if idle_counter >= 5:  # Vitesse de l'animation idle
                idle_counter = 0
                idle_frame = (idle_frame + 1) % len(idle_anim)

        if not crab_joueur_facing_right and player_img_to_draw:
            player_img_to_draw = pygame.transform.flip(player_img_to_draw, True, False)

        # --- Dessin de tous les éléments ---
        screen.fill(WHITE)  # Couleur de fond par défaut si l'image de fond ne couvre pas tout
        # --- Collision avec le portail de fin ---
        if player_rect_world.colliderect(portal_rect_world):
            return "win"

        # Dessin du fond en boucle (scroll parallax simple)
        for i in range(-1, int(SCREEN_WIDTH / bg_width) + 2):
            bg_x_on_screen = i * bg_width - (scroll_x % bg_width)
            screen.blit(background_img_game, (bg_x_on_screen, -380))  # Ajuster Y si l'image est haute
            # screen.blit(flipped_bg_img, (bg_x_on_screen, background_img_game.get_height() - 380)) # Pour une partie basse du fond si existe

        # Dessin du sol (coordonnées écran)
        ground_rect_screen = ground_rect_world.move(-scroll_x, 0)
        if ground_rect_screen.colliderect(screen.get_rect()):  # Optimisation: dessiner si visible
            pygame.draw.rect(screen, SAND_COLOR, ground_rect_screen, border_radius=4)
            pygame.draw.rect(screen, GREEN_BORDER, ground_rect_screen, 2, border_radius=4)

        # Dessin des plateformes (coordonnées écran)
        for plat_world in platforms_world:
            plat_screen_rect = plat_world.move(-scroll_x, 0)
            if plat_screen_rect.colliderect(screen.get_rect()):  # Optimisation
                pygame.draw.rect(screen, SAND_COLOR, plat_screen_rect, border_radius=4)
                pygame.draw.rect(screen, GREEN_BORDER, plat_screen_rect, 2, border_radius=4)

        # Dessin des collectibles (coordonnées écran)
        for item_data in collectibles_world:
            if not item_data["collected"]:
                item_screen_rect = item_data["rect"].move(-scroll_x, 0)
                if item_screen_rect.colliderect(screen.get_rect()):  # Optimisation
                    screen.blit(crab_img_collectible, item_screen_rect.topleft)

        # Dessin du portail
        portal_rect_screen = portal_rect_world.move(-scroll_x, 0)
        if portal_rect_screen.colliderect(screen.get_rect()):
            screen.blit(portal_img, portal_rect_screen.topleft)

        # Dessin des ennemis (coordonnées écran)
        for enemy_data in enemies_world:
            enemy_screen_rect = enemy_data["rect"].move(-scroll_x, 0)
            if enemy_screen_rect.colliderect(screen.get_rect()):  # Optimisation
                pygame.draw.rect(screen, BLUE_ENEMY, enemy_screen_rect)

        # Dessin du joueur
        if player_img_to_draw:
            if invincible:  # Effet de clignotement si invincible
                if pygame.time.get_ticks() % 200 < 100:  # Clignote toutes les 200ms (visible 100ms, invisible 100ms)
                    screen.blit(player_img_to_draw, (crab_joueur_x_screen, crab_joueur_y_screen))
            else:
                screen.blit(player_img_to_draw, (crab_joueur_x_screen, crab_joueur_y_screen))
        # Debug Hitbox joueur:
        # pygame.draw.rect(screen, PLAYER_DEBUG_COLOR if not invincible else INVINCIBLE_COLOR_DEBUG,
        #                 (crab_joueur_x_screen, crab_joueur_y_screen, PLAYER_WIDTH, PLAYER_HEIGHT), 2)

        # Dessin de la balle (coordonnées écran)
        if ball_pos_world:
            ball_screen_x = int(ball_pos_world[0] - scroll_x)
            ball_screen_y = int(ball_pos_world[1])  # Y de la balle est déjà "monde" mais s'affiche directement
            if 0 < ball_screen_x < SCREEN_WIDTH and 0 < ball_screen_y < SCREEN_HEIGHT:  # Si visible
                pygame.draw.circle(screen, RED, (ball_screen_x, ball_screen_y), ball_radius)

        # Dessin de la flèche de visée
        if selecting_trajectory:
            player_center_on_screen = (
            crab_joueur_x_screen + PLAYER_WIDTH // 2, crab_joueur_y_screen + PLAYER_HEIGHT // 2)
            draw_aiming_arrow(screen, player_center_on_screen, pygame.mouse.get_pos())

        # --- Dessin de l'Interface Utilisateur (UI) ---
        screen.blit(menu_button_img, menu_button_rect)

        ui_font = load_font(FONT_PATH, 18)
        lives_text_surf = ui_font.render(f"Vies: {lives}", True, BLACK)
        screen.blit(lives_text_surf, (20, 20))  # En haut à gauche

        collectible_text_surf = ui_font.render(f"{collectible_type_name}: {collectibles_collected_count}", True, BLACK)
        screen.blit(collectible_text_surf, (20, 50))

        # Affichage du texte tutoriel
        if show_tutorial_text:
            for i, line in enumerate(tutorial_lines):
                tut_surf = tutorial_font.render(line, True, BLACK)
                tut_rect = tut_surf.get_rect(
                    center=(SCREEN_WIDTH // 2, tutorial_start_y + i * 20))  # Ajuster Y et espacement

                # Fond semi-transparent pour le texte du tutoriel pour meilleure lisibilité
                bg_tut_surf = pygame.Surface((tut_rect.width + 10, tut_rect.height + 6), pygame.SRCALPHA)
                bg_tut_surf.fill((230, 230, 230, 180))  # Blanc cassé semi-transparent
                screen.blit(bg_tut_surf, (tut_rect.left - 5, tut_rect.top - 3))
                screen.blit(tut_surf, tut_rect)

        pygame.display.flip()  # Mettre à jour tout l'écran

    return "menu"  # Par défaut, si la boucle se termine autrement, retourner au menu


# === Boucle principale de l'application ===
def main():
        screen = initialize_pygame()
        current_game_state = "menu"
        selected_level = 1  # Niveau par défaut si on redémarre directement

        while True:
            if current_game_state == "menu":
                action = show_menu(screen)
                if action == "play":
                    current_game_state = "choose_level"
                elif action == "quit":
                    break
            elif current_game_state == "choose_level":
                level_choice = choose_level(screen)  # Peut retourner 1, 2, ou "quit"
                if isinstance(level_choice, int):  # Si un niveau est choisi
                    selected_level = level_choice
                    current_game_state = "run_game"
                elif level_choice == "quit":
                    break
                else:  # Si l'utilisateur ferme la fenêtre de choix de niveau sans choisir
                    current_game_state = "menu"
            elif current_game_state == "run_game":
                if selected_level == 1:  # Si le niveau 1 est choisi, on affiche la contextualisation
                    show_context(screen)
                game_outcome = run_game(screen, selected_level)  # Utilise selected_level
                if game_outcome == "menu":
                    current_game_state = "menu"
                elif game_outcome == "restart":
                    current_game_state = "run_game"  # Reste dans cet état pour relancer avec selected_level
                elif game_outcome == "win":
                    next_action = show_win_screen(screen)
                    if next_action == "menu":
                        current_game_state = "menu"
                    elif next_action == "quit":
                        break

                elif game_outcome == "quit":
                    break
            else:
                print(f"État de jeu inconnu: {current_game_state}")
                break  # Sécurité

        pygame.quit()

if __name__ == '__main__':
    main()