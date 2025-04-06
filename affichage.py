import pygame

#Partie MENU

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
        title_text = font.render("CRABINATOR", True, (0, 0, 0))  # Jaune vif
        title_rect = title_text.get_rect(center=(725 // 2, 300))  # Centré

        # Dans ta boucle principale du menu :
        screen.blit(background, (0, 0))

        # Affiche le titre
        screen.blit(title_text, title_rect)

        # Affiche le bouton
        screen.blit(play_button, play_button_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return False  # L'utilisateur a fermé la fenêtre
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    return True  # Le joueur a cliqué sur PLAY

# Partie JEU PRINCIPAL

def run_game():
    # Paramètres de la fenêtre
    screen_width = 725
    screen_height = 550
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Jeu avec Terrain")
    background = pygame.image.load("assetsaffichage/fond2.jpg").convert()
    # Crée une version miroir (flip vertical)
    flipped_bg = pygame.transform.flip(background, False, True)

    background_width = background.get_width()

    # Couleurs
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    BROWN = (139, 69, 19)

    # Variables du personnage
    x, y = 100, 500  # Position initiale
    width, height = 64, 64  # Taille du personnage
    velocity = 5  # Vitesse du personnage
    jump_velocity = -15  # Vitesse du saut
    gravity = 0.8  # Gravité du personnage

    # Initialisation du mouvement du saut
    is_jumping = False
    jump_frame = 0  # Compteur pour l'animation du saut
    y_velocity = 0  # Vitesse verticale du personnage

    # Taille des images redimensionnées (augmentée)
    new_width = 64  # Nouvelle largeur de l'image
    new_height = 64  # Nouvelle hauteur de l'image

    # Chargement et redimensionnement des sprites à partir du dossier 'png'
    walk_right = [
        pygame.transform.scale(pygame.image.load(f'Hero/Run ({i}).png').convert_alpha(), (new_width, new_height)) for i
        in range(1, 15)]
    walk_left = [
        pygame.transform.scale(pygame.image.load(f'Hero/Run ({i}).png').convert_alpha(), (new_width, new_height)) for i
        in range(1, 15)]
    idle = [pygame.transform.scale(pygame.image.load(f'Hero/Idle ({i}).png').convert_alpha(), (new_width, new_height))
            for i in range(1, 15)]
    jump = [pygame.transform.scale(pygame.image.load(f'Hero/Jump ({i}).png').convert_alpha(), (new_width, new_height))
            for i in range(1, 17)]

    # Animation
    clock = pygame.time.Clock()
    current_frame = 0
    idle_frame = 0
    idle_counter = 0
    is_walking = False
    facing_right = True

    # Définir le terrain avec hitboxes
    terrain = [
        pygame.Rect(0, screen_height - 20, 3000, 20),
        pygame.Rect(500, 420, 100, 20),
        pygame.Rect(700, 360, 100, 20),
        pygame.Rect(900, 300, 100, 20),
        pygame.Rect(1100, 240, 100, 20),
        pygame.Rect(1300, 300, 100, 20),
        pygame.Rect(1500, 360, 100, 20),
        pygame.Rect(1700, 420, 100, 20),
        pygame.Rect(1900, 360, 100, 20),
        pygame.Rect(2100, 300, 100, 20),
        pygame.Rect(2300, 240, 100, 20),
        pygame.Rect(2500, 300, 100, 20),
        pygame.Rect(2700, 360, 100, 20)
    ]

    #position du joueur
    x, y = 100, 436  # correspond à hauteur = 64 (500 - 64)

    # Variables pour le défilement de l'écran
    scroll_x = 0

    # Boucle principale du jeu
    run = True
    while run:
        clock.tick(60)  # Framerate (images par seconde)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Détection des touches pressées
        keys = pygame.key.get_pressed()

        # Déplacement du personnage
        if keys[pygame.K_LEFT]:
            x -= velocity
            is_walking = True
            facing_right = False
            if x < screen_width / 2 and scroll_x > 0:
                scroll_x -= velocity
                x += velocity
        elif keys[pygame.K_RIGHT]:
            x += velocity
            is_walking = True
            facing_right = True
            if x > screen_width / 2 and scroll_x < terrain[-1].right - screen_width:
                scroll_x += velocity
                x -= velocity
        else:
            is_walking = False

        # Définir la hitbox du personnage
        hitbox = pygame.Rect(x, y, new_width, new_height)

        # Appliquer la gravité en continu
        y_velocity += gravity
        y += y_velocity

        # Vérifier les collisions avec le terrain
        for rect in terrain:
            rect_scrolled = rect.move(-scroll_x, 0)
            if hitbox.colliderect(rect_scrolled):
                if y_velocity > 0:  # Si le personnage tombe
                    y = rect_scrolled.top - new_height
                    y_velocity = 0
                    is_jumping = False
                elif y_velocity < 0:  # Si le personnage saute
                    y_velocity = 0

        # Empêcher le personnage de passer sous les plateformes
        if y + new_height > screen_height:
            y = screen_height - new_height
            y_velocity = 0
            is_jumping = False

        # Logique du saut
        if not is_jumping and keys[pygame.K_SPACE]:  # Si la touche espace est pressée, effectuer un saut
            is_jumping = True
            y_velocity = jump_velocity  # Appliquer la vitesse de saut
            jump_frame = 0  # Revenir au premier frame de l'animation du saut

        jump_frame += 1
        if jump_frame >= len(jump):  # Arrêter l'animation après 16 images
            jump_frame = len(jump) - 1  # Dernière image de l'animation de saut

        # Animation du personnage
        if is_walking and not is_jumping:
            current_frame += 1
            if current_frame >= len(walk_right):
                current_frame = 0
        elif not is_jumping:
            idle_counter += 1
            if idle_counter >= 5:  # Ajustez cette valeur pour ralentir l'animation d'attente
                idle_counter = 0
                idle_frame += 1
                if idle_frame >= len(idle):
                    idle_frame = 0

        # Affichage du fond en boucle
        for i in range((screen_width + scroll_x) // background_width + 2):
            x_bg = i * background_width - (scroll_x % background_width)
            screen.blit(background, (x_bg, 0))
            screen.blit(flipped_bg, (x_bg, background.get_height()))

        # Dessiner le terrain avec hitboxes
        for rect in terrain:
            rect_scrolled = rect.move(-scroll_x, 0)
            pygame.draw.rect(screen, BROWN, rect_scrolled, border_radius=4)
            pygame.draw.rect(screen, (0, 100, 0), rect_scrolled, 2, border_radius=4)

        if is_jumping:
            # Afficher l'animation du saut, inversée si le personnage regarde à gauche
            if facing_right:
                screen.blit(jump[jump_frame], (x, y))
            else:
                flipped_jump = pygame.transform.flip(jump[jump_frame], True, False)
                screen.blit(flipped_jump, (x, y))
        elif is_walking:
            # Afficher l'animation de marche, inversée si le personnage regarde à gauche
            if facing_right:
                screen.blit(walk_right[current_frame], (x, y))
            else:
                flipped_image = pygame.transform.flip(walk_right[current_frame], True, False)
                screen.blit(flipped_image, (x, y))
        else:
            # Afficher l'animation d'attente (idle)
            if facing_right:
                screen.blit(idle[idle_frame], (x, y))  # Normal pour la droite
            else:
                flipped_idle = pygame.transform.flip(idle[idle_frame], True, False)
                screen.blit(flipped_idle, (x, y))  # Inversé pour la gauche

        # Dessiner la hitbox du personnage (pour visualiser la hitbox, vous pouvez la dessiner)
        pygame.draw.rect(screen, (255, 0, 0), hitbox, 2)  # Dessiner la hitbox en rouge

        pygame.display.update()  # Actualiser l'écran

    # Quitter Pygame
    pygame.quit()


# === Lancement ===

if show_menu():
    run_game()
