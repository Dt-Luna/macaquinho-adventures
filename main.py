import pygame

class playerSprite(pygame.sprite.Sprite):
    def __init__(self):
         super().__init__()
         macaco_img = pygame.image.load('macaco.png').convert_alpha()
         macaco_img = pygame.transform.scale(macaco_img, (50,50))
         self.image = macaco_img
         self.rect = macaco_img.get_rect()
         self.rect.topleft = (320,120)
         self.velocidade = 10
         self.sentido = -1 #-1 e 1 são esquerda e direita, -2 e 2 são baixo e cima
         self.vertical_speed = 0

    def tick(self):
        self.rect.y += self.vertical_speed
        # self.vertical_speed += 0.1

pygame.init()
screen = pygame.display.set_mode((640,450))
clock = pygame.time.Clock()
running = True

player = playerSprite()
todos_sprites = pygame.sprite.Group([player])

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.tick()
            
    screen.fill((255,255,255))
    todos_sprites.draw(screen)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
