import pygame


# Initialisation de Pygame
pygame.init()


# Paramètres de la fenêtre
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jeu avec Terrain")


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
walk_right = [pygame.transform.scale(pygame.image.load(f'Hero/Run ({i}).png'), (new_width, new_height)) for i in range(1, 15)]  # Images de marche droite
walk_left = [pygame.transform.scale(pygame.image.load(f'Hero/Run ({i}).png'), (new_width, new_height)) for i in range(1, 15)]  # Images de marche gauche
idle = [pygame.transform.scale(pygame.image.load(f'Hero/Idle ({i}).png'), (new_width, new_height)) for i in range(1, 15)]  # Images d'attente
jump = [pygame.transform.scale(pygame.image.load(f'Hero/Jump ({i}).png'), (new_width, new_height)) for i in range(1, 17)]  # Images du saut


# Animation
clock = pygame.time.Clock()
current_frame = 0
idle_frame = 0
idle_counter = 0
is_walking = False
facing_right = True


# Définir le terrain avec hitboxes
terrain = [
   pygame.Rect(0, 550, 1600, 50),  # Sol plus long
   pygame.Rect(200, 450, 100, 20),  # Plateforme
   pygame.Rect(400, 350, 150, 20),  # Plateforme
   pygame.Rect(600, 250, 100, 20),  # Plateforme
   pygame.Rect(800, 450, 100, 20),  # Plateforme supplémentaire
   pygame.Rect(1000, 350, 150, 20),  # Plateforme supplémentaire
   pygame.Rect(1200, 250, 100, 20)   # Plateforme supplémentaire
]


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


   # Affichage des animations
   screen.fill(WHITE)  # Fond blanc


   # Dessiner le terrain avec hitboxes
   for rect in terrain:
       rect_scrolled = rect.move(-scroll_x, 0)
       pygame.draw.rect(screen, BROWN, rect_scrolled)
       pygame.draw.rect(screen, (0, 255, 0), rect_scrolled, 2)  # Dessiner la hitbox en vert


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
