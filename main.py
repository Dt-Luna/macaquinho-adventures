import pygame

class playerSprite(pygame.sprite.Sprite):
    def __init__(self):
         super().__init__()
         macaco_img = pygame.image.load('macaco.png').convert_alpha()
         macaco_img = pygame.transform.scale(macaco_img, (150,150))
         self.image = macaco_img
         self.rect = macaco_img.get_rect()
         self.rect.topleft = (320,120)
         self.velocidade = 10
         self.sentido = -1 #-1 e 1 são esquerda e direita
         self.vertical_speed = 0

    def move_left(self):
        if self.sentido == 1:
            self.sentido == -1
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.rect.x -= self.velocidade

    def move_right(self):
        if self.sentido == -1:
            self.sentido == 1
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.rect.x += self.velocidade

    # def jump(self):
        # limitar a movimentação no ar (double jumps e voar)
        # testar colisão????



    # def tick(self):
        # self.rect.y += self.vertical_speed
        # self.vertical_speed += 0.1

class blocosSprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        tronco_img = pygame.image.load('tronco.png').convert_alpha()
        tronco_img = pygame.transform.scale(tronco_img, (150,150))
        self.image = tronco_img
        self.rect = tronco_img.get_rect()
        self.rect.topleft = (x, y)

class serpentesSprite(pygame.sprite.Sprite):
    def __init__(self, x ,y):
        super().__init__()
        serpente_img = pygame.image.load('serpente.png').convert_alpha()
        serpente_img = pygame.transform.scale(serpente_img, (100,100))
        self.image = serpente_img
        self.rect = serpente_img.get_rect()
        self.rect.topleft = (x, y)

        

pygame.init()
screen = pygame.display.set_mode((600,600))
clock = pygame.time.Clock()
running = True

player = playerSprite()
blocos = [blocosSprite(50+i*200, 40+i*100)for i in range(2)]
serpentes = serpentesSprite(50,50)
todos_sprites = pygame.sprite.Group([player, blocos, serpentes])

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # player.tick()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move_left()
    if keys[pygame.K_RIGHT]:
        player.move_right()
            
    screen.fill((119, 162, 230))
    todos_sprites.draw(screen)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
