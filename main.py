import pygame
from pygame.locals import K_w, K_a, K_s, K_d

class playerSprite(pygame.sprite.Sprite):
    def __init__(self):
         super().__init__()
         macaco_img = pygame.image.load('macaco.png').convert_alpha()
         macaco_img = pygame.transform.scale(macaco_img, (27*3, 30*3))
         self.image = macaco_img
         self.rect = macaco_img.get_rect()
         self.rect.topleft = (320,120)
         self.velocidade = 5
         self.sentido = -1 #-1 e 1 são esquerda e direita
         self.vertical_speed = 0

    def move_left(self):
        if self.sentido == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        
        self.rect.x -= self.velocidade
        for colisao in colidido:
            if colisao.rect.x < self.rect.x:
                self.rect.x += self.velocidade
        
        self.sentido = 1

    def move_right(self):
        if self.sentido == 1:
            self.image = pygame.transform.flip(self.image, True, False)

        self.rect.x += self.velocidade
        for colisao in colidido:
            if colisao.rect.x > self.rect.x:
                self.rect.x -= self.velocidade
        
        self.sentido = -1


    # def jump(self):
        # limitar a movimentação no ar (double jumps e voar)
        # testar colisão????

    def tick(self):
        if pygame.key.get_pressed()[K_w]:
            self.rect.y -= 3
        if pygame.key.get_pressed()[K_a]:
            self.rect.x -= 3
        if pygame.key.get_pressed()[K_s]:
            self.rect.y += 3
        if pygame.key.get_pressed()[K_d]:
            self.rect.x += 3
        
        self.rect.y += self.vertical_speed
        self.vertical_speed += 0.1
        for colisao in colidido:
            if colisao.rect.y > self.rect.y:
                self.rect.y -= 1
        

class blocosSprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        tronco_img = pygame.image.load('tronco.png').convert_alpha()
        tronco_img = pygame.transform.scale(tronco_img, (32*7, 10*7))
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

class frutaSprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        fruta_img = pygame.image.load('maca.png').convert_alpha()
        fruta_img = pygame.transform.scale(fruta_img, (30,30))
        self.image = fruta_img
        self.rect = fruta_img.get_rect()
        self.rect.topleft = (x, y)



pygame.init()
screen = pygame.display.set_mode((600,600))
clock = pygame.time.Clock()
running = True

player = playerSprite()
blocos = pygame.sprite.Group()
for i in range(4):
    blocos.add(blocosSprite(20, 20 + 170 * i))
frutas = pygame.sprite.Group()
for i in range(5):  
    frutas.add(frutaSprite(250, 50 + 120 * i))
serpentes = serpentesSprite(50,50)
todos_sprites = pygame.sprite.Group([player, blocos, serpentes, frutas])

pontos = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((119, 162, 230))
    player.tick()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move_left()
    if keys[pygame.K_RIGHT]:
        player.move_right()

    colidido = pygame.sprite.spritecollide(player, blocos, False)
    if colidido:
        for tronco in colidido:
            print(f'O porrinha que colidiu ta aqui o {tronco.rect.topleft}')

    
    contagem_pontos = pygame.sprite.spritecollide(player, frutas, False)
    for fruta in contagem_pontos:
        frutas.remove(fruta)   
        todos_sprites.remove(fruta) 
        pontos += 1
    print(pontos)
            
            
   
    todos_sprites.draw(screen)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
