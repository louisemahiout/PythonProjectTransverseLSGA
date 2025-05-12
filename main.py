from fichierprincipal import *

# Initialisation de la fenêtre Pygame et de la musique de fond
screen = initialize_pygame(SCREEN_WIDTH, SCREEN_HEIGHT, MUSIC_PATH)

# L’état initial du jeu est le menu principal
current_game_state = "menu"

# Le niveau par défaut est 1, utilisé si le joueur redémarre immédiatement le jeu
selected_level = 1

# === Boucle principale du jeu ===
while True:
    # --- ÉTAT : MENU PRINCIPAL ---
    if current_game_state == "menu":
        # Affiche le menu principal et attend une action du joueur
        action = show_menu(
            screen,
            BACKGROUND_IMG_PATH_MENU,
            PLAY_BUTTON_IMG_PATH,
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            FONT_PATH,
            BLACK
        )
        # Si le joueur clique sur "Jouer", passer à l'écran de sélection de niveau
        if action == "play":
            current_game_state = "choose_level"
        # Si le joueur clique sur "Quitter", sortir de la boucle
        elif action == "quit":
            break

    # --- ÉTAT : CHOIX DE NIVEAU ---
    elif current_game_state == "choose_level":
        # Affiche l’écran de choix de niveau et récupère le choix (1, 2, ou "quit")
        level_choice = choose_level(screen, BACKGROUND_IMG_PATH_MENU, FONT_PATH, BLACK, SCREEN_WIDTH)

        if isinstance(level_choice, int):  # Si le joueur a choisi un niveau valide
            selected_level = level_choice
            current_game_state = "run_game"  # Passer à l’état de jeu
        elif level_choice == "quit":  # Si le joueur choisit de quitter
            break
        else:
            current_game_state = "menu"  # Retour au menu si choix invalide ou fenêtre fermée

    # --- ÉTAT : LANCEMENT DU JEU (NIVEAU) ---
    elif current_game_state == "run_game":
        # Si le niveau 1 est choisi, afficher l’introduction narrative (contextualisation)
        if selected_level == 1:
            show_context(screen, FONT_PATH, BLACK, SCREEN_WIDTH, SCREEN_HEIGHT)

        # Lancer la boucle de jeu principale (selon le niveau choisi)
        game_outcome, score = run_game(
            screen,
            selected_level,
            MENU_BUTTON_IMG_PATH,
            SCREEN_WIDTH,
            CRAB_COLLECTIBLE_IMG_PATH,
            PLAYER_WIDTH,
            PLAYER_HEIGHT,
            ENEMY_IMG_PATH,
            SCREEN_HEIGHT,
            HERO_RUN_IMG_PATH_PREFIX,
            HERO_IDLE_IMG_PATH_PREFIX,
            HERO_JUMP_IMG_PATH_PREFIX,
            BACKGROUND_IMG_PATH_GAME,
            BACKGROUND_IMG_PATH_GAME2,
            BACKGROUND_IMG_PATH_MENU,
            FONT_PATH,
            RED,
            BLACK,
            WHITE,
            SAND_COLOR,
            GREEN_BORDER,
            FPS
        )

        # Gérer le retour en fonction de l’issue du jeu
        if game_outcome == "menu":
            current_game_state = "menu"
            selected_level = None  # Réinitialiser pour revenir à la sélection
        elif game_outcome == "restart":
            current_game_state = "run_game"  # Rejouer le même niveau
        elif game_outcome == "win":
            # Affiche l’écran de victoire
            action_win, score = show_win_screen(screen, score, BACKGROUND_IMG_PATH_MENU, FONT_PATH, SCREEN_WIDTH, BLACK,
                                                WHITE)
            if action_win == "menu":
                selected_level = None  # Réinitialise le niveau
                current_game_state = "menu"
            elif action_win == "quit":
                break

    # --- ÉTAT : SORTIE (en cas de fermeture via le jeu) ---
    elif game_outcome == "quit":
        break

    # --- ÉTAT INCONNU : sécurité ---
    else:
        print(f"État de jeu inconnu: {current_game_state}")
        break  # Quitte la boucle si l’état est invalide

# Fermeture propre de Pygame
pygame.quit()

