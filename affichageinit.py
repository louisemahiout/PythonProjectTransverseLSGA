import pygame
pygame.init()
class Game:
    def __init__(self):
        self.is_playing=False
        self.all_players=pygame.sprite.Group()
        self.player=Player(self)
        self.all_players.add(self.player)

#classe représentant notre joueur
class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.health=100
        self.max_health=100
        self.attack=10
        self.velocity=5
        self.image=pygame.image.load('assetsaffichage/boutonplay.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (300, 200))
        self.rect=self.image.get_rect()
        self.rect.x=200
        self.rect.y=300

pygame.display.set_caption('Crabinator')
screen=pygame.display.set_mode((725,550))
background= pygame.image.load("assetsaffichage/fond1.jpg").convert()
player = Player()

running=True

while running:

    screen.blit(background,(0,0))
    screen.blit(player.image, player.rect)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
            print("Fermeture du jeu")







