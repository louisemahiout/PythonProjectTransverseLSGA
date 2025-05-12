import pygame
from load_image import *
# La partie où elle perd le jeu
def show_game_over_screen(screen, score, BACKGROUND_IMG_PATH_MENU, FONT_PATH, SCREEN_WIDTH, SCREEN_HEIGHT, RED, BLACK, WHITE):
    # Charge une image de fond (peut être un visuel spécifique à l'écran Game Over)
    background = load_image(BACKGROUND_IMG_PATH_MENU)
    title_font = load_font(FONT_PATH, 36)     # Police pour le titre "PERDU"
    button_font = load_font(FONT_PATH, 18)    # Police pour les boutons

    # Crée un overlay noir semi-transparent pour assombrir l'arrière-plan
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))

    # Dimensions et position des boutons "Relancer" et "Menu"
    button_width = 400
    button_height = 60
    restart_button_rect = pygame.Rect((SCREEN_WIDTH - button_width) // 2, 300, button_width, button_height)
    menu_button_rect = pygame.Rect((SCREEN_WIDTH - button_width) // 2, 380, button_width, button_height)

    running = True
    while running:
        # Gère les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "quit", score  # Quitter le jeu
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button_rect.collidepoint(event.pos):
                    return "restart", score  # Relancer le niveau
                elif menu_button_rect.collidepoint(event.pos):
                    return "menu", score  # Revenir au menu

        # Affiche le fond et l'overlay assombri
        screen.blit(background, (0, 0))
        screen.blit(overlay, (0, 0))

        # Titre "PERDU"
        title_text = title_font.render("PERDU", True, RED)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 225))
        screen.blit(title_text, title_rect)

        # Affiche le score final
        small_font = load_font(FONT_PATH, 20)
        score_text = small_font.render(f"Score final : {score}", True, BLACK)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 330))
        screen.blit(score_text, score_rect)

        # Dessine les boutons
        pygame.draw.rect(screen, WHITE, restart_button_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, menu_button_rect, border_radius=10)

        # Texte des boutons
        restart_text = button_font.render("Relancer le niveau", True, BLACK)
        screen.blit(restart_text, restart_text.get_rect(center=restart_button_rect.center))

        menu_text = button_font.render("Retour au menu", True, BLACK)
        screen.blit(menu_text, menu_text.get_rect(center=menu_button_rect.center))

        # Rafraîchit l'affichage
        pygame.display.flip()

# La partie où elle gagne le jeu
def show_win_screen(screen, score, BACKGROUND_IMG_PATH_MENU, FONT_PATH, SCREEN_WIDTH, BLACK, WHITE):
    # Charge l'image de fond du menu pour l'écran de victoire
    background = load_image(BACKGROUND_IMG_PATH_MENU)
    font = load_font(FONT_PATH, 36)         # Police pour le titre "TU T'ES ENFUI!"
    button_font = load_font(FONT_PATH, 20)  # Police pour le bouton

    # Définition du bouton de retour au menu
    button_rect = pygame.Rect((SCREEN_WIDTH - 300) // 2, 350, 300, 60)

    while True:
        # Gère les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "quit", score  # Quitter le jeu
            if event.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(event.pos):
                return "menu", score  # Retourner au menu principal

        # Affiche le fond
        screen.blit(background, (0, 0))

        # Texte de victoire
        win_text = font.render("TU T'ES ENFUI!", True, BLACK)
        screen.blit(win_text, win_text.get_rect(center=(SCREEN_WIDTH // 1.85, 290)))

        # Affiche le score final
        small_font = load_font(FONT_PATH, 20)
        score_text = small_font.render(f"Score final : {score}", True, BLACK)
        screen.blit(score_text, score_text.get_rect(center=(SCREEN_WIDTH // 2, 330)))

        # Dessine le bouton de retour au menu
        pygame.draw.rect(screen, WHITE, button_rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, button_rect, 2, border_radius=10)  # Bordure noire

        # Texte du bouton
        label = button_font.render("Retour au menu", True, BLACK)
        screen.blit(label, label.get_rect(center=button_rect.center))

        # Met à jour l'affichage
        pygame.display.flip()
