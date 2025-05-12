
from load_image import *
import sys

def show_context(screen, FONT_PATH, BLACK, SCREEN_WIDTH, SCREEN_HEIGHT):
    # Charger une image de fond représentant l'univers du jeu
    background = pygame.image.load("assetsaffichage/image_ennemie.jpg").convert()
    font = pygame.font.Font(FONT_PATH, 11)  # Police pour les lignes de contexte

    # Texte d’introduction affiché progressivement
    text_lines = [
        "Bienvenue dans l’univers de Crabinator !",
        "La plage est envahie par des créatures terrifiantes qui menacent",
        "tout sur leur passage. Mais elles ont une faiblesse : elles",
        "détestent les crabes! Alors attrape-en, vise bien… et bombarde",
        "-les pour te défendre et t'enfuire!"
    ]

    # Affiche l'image de fond
    screen.blit(background, (0, 0))

    # Dessine un rectangle noir en dessous si l'image est plus petite que l'écran
    image_height = background.get_height()
    screen.fill((0, 0, 0), pygame.Rect(0, image_height, screen.get_width(), screen.get_height() - image_height))
    pygame.display.flip()

    # Position verticale de départ pour le texte
    y_offset = 425
    line_delay = 50  # Délai entre chaque caractère
    skip = False     # Flag pour sauter l’intro

    # === BOUTON "PASSER" ===
    skip_button_font = load_font(FONT_PATH, 18)
    skip_button_text = skip_button_font.render("Passer", True, BLACK)
    skip_button_rect = pygame.Rect(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 60, 120, 40)

    # Dessine le bouton "Passer" (blanc avec bord noir)
    pygame.draw.rect(screen, (255, 255, 255), skip_button_rect, border_radius=10)
    pygame.draw.rect(screen, BLACK, skip_button_rect, 2, border_radius=10)
    screen.blit(skip_button_text, skip_button_text.get_rect(center=skip_button_rect.center))
    pygame.display.flip()

    # Affichage progressif de chaque ligne
    for line in text_lines:
        rendered_line = ""  # Ligne actuellement affichée, caractère par caractère

        for char in line:
            # Gérer les événements pendant que le texte se déroule
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if skip_button_rect.collidepoint(event.pos):
                        skip = True  # L’utilisateur a cliqué sur "Passer"
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    skip = True  # L’utilisateur appuie sur espace pour passer

            if skip:
                break  # Arrêter l'affichage progressif si l’utilisateur veut passer

            rendered_line += char  # Ajouter un caractère à la ligne affichée

            # Redessiner le fond et la zone noire
            screen.blit(background, (0, 0))
            screen.fill((0, 0, 0), pygame.Rect(0, image_height, screen.get_width(), screen.get_height() - image_height))

            # Redessiner le bouton "Passer"
            pygame.draw.rect(screen, (255, 255, 255), skip_button_rect, border_radius=10)
            pygame.draw.rect(screen, BLACK, skip_button_rect, 2, border_radius=10)
            screen.blit(skip_button_text, skip_button_text.get_rect(center=skip_button_rect.center))

            # Afficher les lignes déjà complètement rendues
            for i in range(len(text_lines)):
                if i < text_lines.index(line):
                    text_surface = font.render(text_lines[i], True, (255, 255, 255))
                    screen.blit(text_surface, (20, 425 + i * 20))

            # Afficher la ligne en cours (en train de se dessiner)
            text_surface = font.render(rendered_line, True, (255, 255, 255))
            screen.blit(text_surface, (20, y_offset))

            pygame.display.flip()
            pygame.time.delay(line_delay)  # Délai entre chaque lettre

        if skip:
            break  # Si on a quitté, on sort de la boucle principale

        y_offset += 20  # Décaler verticalement pour la ligne suivante
        pygame.time.delay(500)  # Petite pause entre les lignes

    # Si l’utilisateur a cliqué sur "Passer", afficher tout le texte d’un coup
    if skip:
        screen.blit(background, (0, 0))
        screen.fill((0, 0, 0), pygame.Rect(0, image_height, screen.get_width(), screen.get_height() - image_height))
        y_offset = 425
        for line in text_lines:
            text_surface = font.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (20, y_offset))
            y_offset += 20
        pygame.display.flip()
        pygame.time.delay(1000)  # Pause finale pour laisser lire
