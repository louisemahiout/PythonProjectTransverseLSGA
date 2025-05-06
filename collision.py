import pygame
import sys
import math
import time

# === Foncti ons MENU & NIVEAUX (inchangées) ===

def show_menu():
    pygame.init()
    font = pygame.font.SysFont("Arial", 24)
    pygame.mixer.init()
    pygame.mixer.music.load("assetsaffichage/musique.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)
    pygame.display.set_caption('Crabinator')
    screen = pygame.display.set_mode((725, 550))
    background = pygame.image.load("assetsaffichage/fond1.jpg").convert()
    play_button = pygame.image.load('assetsaffichage/boutonplay.png').convert_alpha()
    new_w, new_h = 64, 64
    crab_img = pygame.image.load("assetsaffichage/crabe.png").convert_alpha()
    crab_img = pygame.transform.scale(crab_img,(new_w // 2, new_h// 2))  # moitié de la taille du joueur
    play_button = pygame.transform.scale(play_button, (300, 200))
    play_button_rect = play_button.get_rect(topleft=(200, 300))

    running = True
    while running:
        screen.blit(background, (0, 0))
        screen.blit(play_button, play_button_rect)
        font = pygame.font.Font("assetsaffichage/PressStart2P.ttf", 48)
        title_text = font.render("CRABINATOR", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(725 // 2, 300))
        screen.blit(title_text, title_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    return True

def choose_level():
    screen = pygame.display.set_mode((725, 550))
    background = pygame.image.load("assetsaffichage/fond1.jpg").convert()
    button_width, button_height = 300, 100
    level1_rect = pygame.Rect((725 // 2 - button_width // 2, 250 - button_height // 2), (button_width, button_height))
    level2_rect = pygame.Rect((725 // 2 - button_width // 2, 400 - button_height // 2), (button_width, button_height))
    font = pygame.font.Font("assetsaffichage/PressStart2P.ttf", 24)
    title_text = font.render("CHOISIS TON NIVEAU", True, (0, 0, 0))
    title_rect = title_text.get_rect(center=(725 // 2, 100))

    running = True
    while running:
        screen.blit(background, (0, 0))
        # fond semi-transparent pour le titre
        bg_rect = pygame.Surface((title_rect.width + 20, title_rect.height + 20), pygame.SRCALPHA)
        bg_rect.fill((255, 255, 255, 180))
        screen.blit(bg_rect, (title_rect.x - 10, title_rect.y - 10))
        screen.blit(title_text, title_rect)

        # NIVEAU 1
        label1 = font.render("TUTORIEL(easy)", True, (0, 0, 0))
        bg1 = pygame.Surface((label1.get_width()+20, label1.get_height()+20), pygame.SRCALPHA)
        bg1.fill((255,255,255,180))
        screen.blit(bg1, (level1_rect.centerx - label1.get_width()//2 - 10,
                          level1_rect.centery - label1.get_height()//2 - 10))
        screen.blit(label1, (level1_rect.centerx - label1.get_width()//2,
                             level1_rect.centery - label1.get_height()//2))

        # NIVEAU 2
        label2 = font.render("JOUER(medium)", True, (0, 0, 0))
        bg2 = pygame.Surface((label2.get_width()+20, label2.get_height()+20), pygame.SRCALPHA)
        bg2.fill((255,255,255,180))
        screen.blit(bg2, (level2_rect.centerx - label2.get_width()//2 - 10,
                          level2_rect.centery - label2.get_height()//2 - 10))
        screen.blit(label2, (level2_rect.centerx - label2.get_width()//2,
                             level2_rect.centery - label2.get_height()//2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if level1_rect.collidepoint(event.pos):
                    return 1
                elif level2_rect.collidepoint(event.pos):
                    return 2

# === JEU PRINCIPAL AVEC ENNEMIS & VIES ===

def run_game():
    # Initialisation
    pygame.init()
    screen_width, screen_height = 725, 550
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Crabinator – Niveau")
    clock = pygame.time.Clock()


    # Bouton MENU
    menu_button = pygame.image.load("assetsaffichage/boutonmenu.png").convert_alpha()
    menu_button = pygame.transform.scale(menu_button, (100, 70))
    menu_button_rect = menu_button.get_rect(topright=(screen_width - 20, 10))

    # Fond & terrain
    background = pygame.image.load("assetsaffichage/fond2.jpg").convert()
    flipped_bg = pygame.transform.flip(background, False, True)
    bg_w = background.get_width()
    SAND = (237,201,175)
    # Le sol
    ground = pygame.Rect(0, screen_height - 20, 5000, 20)

    # Les plateformes
    platforms = [
        pygame.Rect(500, 420, 100, 20),
        pygame.Rect(700, 360, 100, 20),
        pygame.Rect(1700, 420, 100, 20),
        pygame.Rect(1900, 360, 100, 20),
        pygame.Rect(2100, 300, 100, 20),
        pygame.Rect(2800, 420, 100, 20),
        pygame.Rect(3000, 360, 100, 20),
    ]

    # Personnage
    new_w, new_h = 64, 64
    # Chargement du sprite de crabe pour les collectibles
    crab_img = pygame.image.load("assetsaffichage/crabe.png").convert_alpha()
    crab_img = pygame.transform.scale(crab_img, (new_w // 2, new_h // 2))
    x, y = 100, screen_height - 20 - new_h
    velocity = 5
    jump_velocity = -15
    gravity = 0.8
    y_vel = 0
    is_jumping = False
    is_walking = False
    facing_right = True

    # Sprites
    walk = [pygame.transform.scale(
        pygame.image.load(f'Hero/Run ({i}).png').convert_alpha(), (new_w, new_h)
    ) for i in range(1, 15)]
    idle = [pygame.transform.scale(
        pygame.image.load(f'Hero/Idle ({i}).png').convert_alpha(), (new_w, new_h)
    ) for i in range(1, 15)]
    jump_anim = [pygame.transform.scale(
        pygame.image.load(f'Hero/Jump ({i}).png').convert_alpha(), (new_w, new_h)
    ) for i in range(1, 17)]
    cur_frame = 0
    idle_frame = 0
    idle_counter = 0
    jump_frame = 0

    # Balle de crabe-tir
    ball_radius = 10
    ball_pos = None
    ball_vel = None
    selecting_trajectory = False
    arrow_end = None

    # Ennemi (bots)
    bots = [
        pygame.Rect(400, screen_height - 50, 40, 30),
        pygame.Rect(800, screen_height - 50, 40, 30),
        pygame.Rect(1200, screen_height - 50, 40, 30),
    ]
    bot_speed = 3

    # Vies & invincibilité
    lives = 3
    invincible = False
    inv_time = 0
    INV_DURATION = 2000  # ms

    # Fonctions auxiliaires
    def draw_arrow(start, end):
        pygame.draw.line(screen, (0,0,0), start, end, 3)
        ang = math.atan2(end[1]-start[1], end[0]-start[0])
        size = 10
        left = (end[0] - size*math.cos(ang - math.pi/6),
                end[1] - size*math.sin(ang - math.pi/6))
        right = (end[0] - size*math.cos(ang + math.pi/6),
                 end[1] - size*math.sin(ang + math.pi/6))
        pygame.draw.polygon(screen, (0,0,0), [end, left, right])

    def draw_scene(scroll_x):
        # Fond en boucle
        for i in range((screen_width + scroll_x)//bg_w + 2):
            x_bg = i*bg_w - (scroll_x % bg_w)
            screen.blit(background, (x_bg, -380))
            screen.blit(flipped_bg, (x_bg, background.get_height()))

        # Affichage du sol
        r = ground.move(-scroll_x, 0)
        pygame.draw.rect(screen, SAND, r, border_radius=4)
        pygame.draw.rect(screen, (0, 100, 0), r, 2, border_radius=4)

        # Affichage des plateformes
        for platform in platforms:
            r = platform.move(-scroll_x, 0)
            pygame.draw.rect(screen, SAND, r, border_radius=4)
            pygame.draw.rect(screen, (0, 100, 0), r, 2, border_radius=4)

    crabs = [
        {"rect": pygame.Rect(300, 460, crab_img.get_width(), crab_img.get_height()), "collected": False},
        {"rect": pygame.Rect(700, 350, crab_img.get_width(), crab_img.get_height()), "collected": False},
        {"rect": pygame.Rect(1200, 460, crab_img.get_width(), crab_img.get_height()), "collected": False},
        {"rect": pygame.Rect(1500, 270, crab_img.get_width(), crab_img.get_height()), "collected": False},
        {"rect": pygame.Rect(1800, 460, crab_img.get_width(), crab_img.get_height()), "collected": False},
        {"rect": pygame.Rect(2200, 270, crab_img.get_width(), crab_img.get_height()), "collected": False},
        {"rect": pygame.Rect(2500, 460, crab_img.get_width(), crab_img.get_height()), "collected": False},
        {"rect": pygame.Rect(2800, 200, crab_img.get_width(), crab_img.get_height()), "collected": False},
        {"rect": pygame.Rect(3200, 460, crab_img.get_width(), crab_img.get_height()), "collected": False},
        {"rect": pygame.Rect(3500, 270, crab_img.get_width(), crab_img.get_height()), "collected": False},
    ]
    crabs_collected = 0

    # Boucle principale
    scroll_x = 0
    running = True
    while running:
        dt = clock.tick(60)
        # Événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button_rect.collidepoint(event.pos):
                    lvl = choose_level()
                    if lvl in (1,2):
                        run_game()
                    return
                hitbox = pygame.Rect(x, y, new_w, new_h)
                if hitbox.collidepoint(event.pos):
                    selecting_trajectory = True
            elif event.type == pygame.MOUSEBUTTONUP and selecting_trajectory:
                arrow_end = event.pos
                dx = arrow_end[0] - (x + new_w//2)
                dy = arrow_end[1] - (y + new_h//2)
                power = 0.2
                ball_pos = [x + new_w//2, y + new_h//2]
                ball_vel = [dx*power, dy*power]
                selecting_trajectory = False

        # Touche
        keys = pygame.key.get_pressed()
        is_walking = False
        if keys[pygame.K_RIGHT]:
            is_walking = True
            facing_right = True
            if x < screen_width/2 or scroll_x >= (platforms[-1].right) - screen_width:
                x += velocity
            else:
                scroll_x += velocity
        elif keys[pygame.K_LEFT]:
            is_walking = True
            facing_right = False
            if x > screen_width/2 or scroll_x <= 0:
                x -= velocity
            else:
                scroll_x -= velocity

        # Saut
        if not is_jumping and keys[pygame.K_SPACE]:
            is_jumping = True
            y_vel = jump_velocity

        # Gravité personnage
        y_vel += gravity
        y += y_vel

        # Collision terrain personnage
        hitbox = pygame.Rect(x, y, new_w, new_h)
        on_ground = False  # <- à déclarer avant la boucle

        for rect in [ground] + platforms:
            r = rect.move(-scroll_x, 0)

            if hitbox.colliderect(r):
                # Collision par le haut (tomber sur une plateforme)
                if y_vel > 0 and hitbox.bottom <= r.bottom:
                    y = r.top - new_h
                    y_vel = 0
                    is_jumping = False
                    on_ground = True
                # Si tu veux bloquer la tête contre le dessous de la plateforme :
                elif y_vel < 0 and hitbox.top >= r.bottom - 10:
                    y_vel = 0

        if not on_ground and y + new_h >= screen_height:
            y = screen_height - new_h
            y_vel = 0
            is_jumping = False

        # Animation perso
        if is_jumping:
            img = jump_anim[jump_frame]
        elif is_walking:
            img = walk[cur_frame]
        else:
            img = idle[idle_frame]
        if not facing_right:
            img = pygame.transform.flip(img, True, False)

        # Avance frames
        if is_jumping:
            jump_frame = min(jump_frame+1, len(jump_anim)-1)
        elif is_walking:
            cur_frame = (cur_frame+1) % len(walk)
        else:
            idle_counter += 1
            if idle_counter >= 5:
                idle_counter = 0
                idle_frame = (idle_frame+1) % len(idle)

        # Mise à jour balle
        if ball_pos:
            ball_vel[1] += gravity
            ball_pos[0] += ball_vel[0]
            ball_pos[1] += ball_vel[1]
            # Rebond murs
            if ball_pos[0]-ball_radius <= 0 or ball_pos[0]+ball_radius >= screen_width:
                ball_vel[0] *= -0.8
            # Rebond sol
            if ball_pos[1]+ball_radius >= screen_height:
                ball_vel[1] *= -0.7
                ball_pos[1] = screen_height - ball_radius

            # Rebond plateformes
            ball_rect = pygame.Rect(ball_pos[0]-ball_radius, ball_pos[1]-ball_radius,
                                     ball_radius*2, ball_radius*2)
            for rect in [ground] + platforms:
                r = rect.move(-scroll_x,0)
                if ball_rect.colliderect(r):
                    if ball_vel[1] > 0 and ball_pos[1] < r.top:
                        ball_pos[1] = r.top - ball_radius
                        ball_vel[1] *= -0.7
        # Arrêter complètement la balle si elle est trop lente
            speed = math.hypot(ball_vel[0], ball_vel[1])
            if speed < 1:  # seuil à ajuster si besoin
                ball_vel = None
                ball_pos = None



        # Déplacement bots
        for b in bots:
            # b.x est en coords monde
            player_world_x = x + scroll_x
            if abs(b.x - player_world_x) <= 200:
                if b.x < player_world_x:
                    b.x += bot_speed
                else:
                    b.x -= bot_speed

        # Gestion invincibilité
        now = pygame.time.get_ticks()
        if invincible and now - inv_time > INV_DURATION:
            invincible = False

        # Collision perso <-> bots
        player_rect = pygame.Rect(x, y, new_w, new_h)
        for b in bots:
            b_scr = b.move(-scroll_x, 0)
            if player_rect.colliderect(b_scr) and not invincible:
                lives -= 1
                invincible = True
                inv_time = now
                print(f"Touché ! Vies restantes : {lives}")
                if lives <= 0:
                    print("Game Over!")
                    running = False

        # Dessin
        screen.fill((255,255,255))
        draw_scene(scroll_x)

        # Dessiner bots
        for b in bots:
            b_scr = b.move(-scroll_x, 0)
            pygame.draw.rect(screen, (0,0,255), b_scr)

        # Dessiner perso
        color = (255,165,0) if invincible else (255,0,0)
        screen.blit(img, (x, y))
        # pygame.draw.rect(screen, color, player_rect, 2)

        # Dessiner balle et flèche
        if ball_pos:
            pygame.draw.circle(screen, (255,0,0), (int(ball_pos[0]), int(ball_pos[1])), ball_radius)
        if selecting_trajectory:
            end = pygame.mouse.get_pos()
            draw_arrow((x+new_w//2, y+new_h//2), end)

        # Bouton menu
        screen.blit(menu_button, menu_button_rect)

        # Afficher lives
        font = pygame.font.SysFont(None, 36)
        txt = font.render(f"Vies : {lives}", True, (0,0,0))
        screen.blit(txt, (10,10))

        pygame.display.update()

    pygame.quit()


# === LANCEMENT ===
if show_menu():
    lvl = choose_level()
    if lvl in (1,2):
        run_game()
