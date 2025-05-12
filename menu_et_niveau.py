from load_image import *
# ---------------------------------------------------------------
# Affiche le menu principal du jeu Crabinator.
# - Charge et affiche le fond et le bouton "Play"
# - Affiche le titre du jeu centré au-dessus du bouton
# - Attend que l'utilisateur clique sur le bouton pour démarrer
# - Retourne "play" si l'utilisateur clique sur "Play"
# - Retourne "quit" si l'utilisateur ferme la fenêtre
# ---------------------------------------------------------------
def show_menu(screen, BACKGROUND_IMG_PATH_MENU, PLAY_BUTTON_IMG_PATH, SCREEN_WIDTH, SCREEN_HEIGHT, FONT_PATH, BLACK):
    # Charge le fond du menu
    background = load_image(BACKGROUND_IMG_PATH_MENU)

    # Charge et redimensionne l'image du bouton "Play"
    play_button_img = load_image(PLAY_BUTTON_IMG_PATH, alpha=True)
    play_button_img = pygame.transform.scale(play_button_img, (300, 200))

    # Positionne le bouton au centre horizontalement, et vers le bas de l'écran
    play_button_rect = play_button_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5))

    # Charge et prépare le texte du titre
    font_title = load_font(FONT_PATH, 48)
    title_text = font_title.render("CRABINATOR", True, BLACK)

    # Positionne le titre juste au-dessus du bouton "Play"
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, play_button_rect.top + 30))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"  # Fermer le jeu
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    return "play"  # Lancement du jeu si clic sur le bouton

        # Affichage des éléments sur l'écran
        screen.blit(background, (0, 0))
        screen.blit(title_text, title_rect)
        screen.blit(play_button_img, play_button_rect)
        pygame.display.flip()

# ---------------------------------------------------------------
# Fonction interne pour dessiner un bouton de niveau
def draw_level_button(rect, text,screen,font_button,BLACK):
            # Fond semi-transparent du bouton
            btn_bg_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            btn_bg_surface.fill((220, 220, 220, 200))  # Gris clair
            screen.blit(btn_bg_surface, rect.topleft)

            # Bordure du bouton
            pygame.draw.rect(screen, BLACK, rect, 2, border_radius=10)

            # Texte centré sur le bouton
            label = font_button.render(text, True, BLACK)
            label_rect = label.get_rect(center=rect.center)
            screen.blit(label, label_rect)
# ---------------------------------------------------------------
# Affiche un écran de sélection de niveau avec deux boutons :
# - Permet de choisir entre le niveau 1 (Facile) ou niveau 2 (Moyen)
# - Affiche un fond, un titre, et deux boutons cliquables
# - Retourne "1" ou "2" selon le niveau choisi, ou "quit" si l'utilisateur ferme la fenêtre
# ---------------------------------------------------------------
def choose_level(screen,BACKGROUND_IMG_PATH_MENU,FONT_PATH,BLACK,SCREEN_WIDTH):
    # Charge l’image de fond du menu
    background = load_image(BACKGROUND_IMG_PATH_MENU)

    # Dimensions des boutons de sélection
    button_width, button_height = 350, 80

    # Chargement des polices pour le titre et les boutons
    font_title = load_font(FONT_PATH, 30)
    font_button = load_font(FONT_PATH, 20)

    # Création du texte du titre
    title_text = font_title.render("CHOISIS TON NIVEAU", True, BLACK)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))

    # Définition et positionnement du bouton pour le niveau 1
    level1_rect = pygame.Rect(0, 0, button_width, button_height)
    level1_rect.center = (SCREEN_WIDTH // 2, 250)

    # Définition et positionnement du bouton pour le niveau 2
    level2_rect = pygame.Rect(0, 0, button_width, button_height)
    level2_rect.center = (SCREEN_WIDTH // 2, 370)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"  # Quitter le jeu si la fenêtre est fermée
            if event.type == pygame.MOUSEBUTTONDOWN:
                if level1_rect.collidepoint(event.pos):
                    return 1  # Niveau 1 sélectionné
                elif level2_rect.collidepoint(event.pos):
                    return 2  # Niveau 2 sélectionné

        # Affiche l’image de fond
        screen.blit(background, (0, 0))

        # Dessine un fond semi-transparent derrière le titre pour la lisibilité
        title_bg_surface = pygame.Surface((title_rect.width + 20, title_rect.height + 20), pygame.SRCALPHA)
        title_bg_surface.fill((255, 255, 255, 180))  # Blanc transparent
        screen.blit(title_bg_surface, (title_rect.x - 10, title_rect.y - 10))
        screen.blit(title_text, title_rect)  # Affiche le titre

        draw_level_button(level1_rect, "NIVEAU 1 (Facile)",screen,font_button,BLACK)
        draw_level_button(level2_rect, "NIVEAU 2 (Moyen)",screen,font_button,BLACK)

        # Met à jour l’affichage
        pygame.display.flip()



