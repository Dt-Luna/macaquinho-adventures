import random
import pygame

from pygame.locals import K_w, K_a, K_s, K_d

class playerSprite(pygame.sprite.Sprite):
    def __init__(self):
         super().__init__()
         macaco_img = pygame.image.load('macaco.png').convert_alpha()
         macaco_img = pygame.transform.scale(macaco_img, (27*3, 30*3))
         self.image = macaco_img
         self.rect = macaco_img.get_rect()
         self.rect.topleft = (0,0)
         self.velocidade = 3
         self.sentido = -1 #-1 e 1 são esquerda e direita
         self.vertical_speed = 0

    def move_left(self, blocos):
        if self.sentido == -1:
            self.image = pygame.transform.flip(self.image, True, False)       
        self.rect.x -= self.velocidade
        if self.rect.x < 0:
            self.rect.x += self.velocidade
        for bloco in blocos:
            if bloco.rect.x < self.rect.x: 
                self.rect.x -= self.velocidade
        
        self.sentido = 1

    def move_right(self, blocos):
        if self.sentido == 1:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect.x += self.velocidade
        if self.rect.x > 600:
            self.rect.x -= self.velocidade
        for bloco in blocos:
            if bloco.rect.x > self.rect.x:
                self.rect.x += self.velocidade
        
        self.sentido = -1

    def jump(self):
        if self.vertical_speed == 0:
            self.vertical_speed = -10
        

    def tick(self):
        if pygame.key.get_pressed()[K_w]:
            self.rect.y -= 10
        if pygame.key.get_pressed()[K_a]:
            self.rect.x -= 3
        if pygame.key.get_pressed()[K_s]:
            self.rect.y += 10
        if pygame.key.get_pressed()[K_d]:
            self.rect.x += 3
        
        self.rect.y += self.vertical_speed
        self.vertical_speed += 0.3

    def detectar_colisoes(self, blocos, frutas, serpentes, tempo_restante):
        global qtpontos
        colididos = pygame.sprite.spritecollide(self, blocos, False)
        for bloco in colididos:
            if self.rect.bottom >= bloco.rect.top:
                self.rect.bottom = bloco.rect.top
                self.vertical_speed = 0 
                print('HAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHA')
        if pygame.sprite.spritecollide(self, serpentes, False):
            return "game_over"
        contagem_pontos = pygame.sprite.spritecollide(player, frutas, False)
        for fruta in contagem_pontos:
            frutas.remove(fruta)   
            todos_sprites.remove(fruta) if fruta in todos_sprites else None
            qtpontos += 1   
            tempo_restante += 5    
        

class blocosSprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        tronco_img = pygame.image.load('tronco.png').convert_alpha()
        tronco_img = pygame.transform.scale(tronco_img, (32*5, 10*5))
        self.image = tronco_img
        self.rect = tronco_img.get_rect()
        self.rect.topleft = (x, y)

class serpentesSprite(pygame.sprite.Sprite):
    def __init__(self, x ,y):
        super().__init__()
        serpente_img = pygame.image.load('serpente.png').convert_alpha()
        serpente_img = pygame.transform.scale(serpente_img, (50,50))
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

def criar_frutas():
    x, y = random.choice(pontos_spawn_frutas)
    fruta = frutaSprite(x, y)
    return fruta

def criar_serpentes():
    x, y = random.choice(pontos_spawn_serpentes)
    serpente = serpentesSprite(x, y)
    return serpente




   

pygame.init()
screen = pygame.display.set_mode((600,600))
clock = pygame.time.Clock()
running = True
font = pygame.font.Font(None, 24)
tempo_limite = 120000
intervalo_frutas = 7000
intervalo_serpentes = 5000
inicio_tempo = pygame.time.get_ticks()
contador_ticks_serpentes = 0
contador_ticks_frutas = 0
pontos_spawn_frutas = [(60,125), (280, 125), (340, 305), (60, 505), (380, 500)]
pontos_spawn_serpentes = [(30,125), (270, 125), (330, 305), (50, 505), (370, 500)]

# definir os sprites e os grupos
player = playerSprite()
blocos = pygame.sprite.Group()
blocos.add(blocosSprite(40, 120))
blocos.add(blocosSprite(360, 120))
blocos.add(blocosSprite(220, 300))
blocos.add(blocosSprite(40, 500))
blocos.add(blocosSprite(360, 500))
frutas = pygame.sprite.Group()
serpentes = pygame.sprite.Group()

todos_sprites = pygame.sprite.Group([player, blocos, serpentes, frutas])

qtpontos = 0

# loop principal
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    tempo_passado = pygame.time.get_ticks() - inicio_tempo
    tempo_restante = ((tempo_limite - tempo_passado) // 1000)

    tempo_atual_serpentes = pygame.time.get_ticks()
    tempo_atual_frutas = pygame.time.get_ticks()

    screen.fill((119, 162, 230))
    player.tick()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move_left(blocos)
    if keys[pygame.K_RIGHT]:
        player.move_right(blocos)
    if keys[pygame.K_SPACE]:
        player.jump()
        print(1)

    if tempo_atual_serpentes - contador_ticks_serpentes >= intervalo_serpentes:
        serpentes.add(criar_serpentes())
        contador_ticks_serpentes = tempo_atual_serpentes
        print(1)
   
    if tempo_atual_frutas - contador_ticks_frutas >= intervalo_frutas:
        frutas.add(criar_frutas())
        contador_ticks_frutas = tempo_atual_frutas
        print(2)

    print(player.vertical_speed)

# possiveis game overs
    resultado = player.detectar_colisoes(blocos, frutas, serpentes, tempo_restante)
    if resultado == "game_over":
        running = False
    if tempo_restante <= 0:
        running = False

    # textos e sprites
    texto_tempo = font.render(f"Tempo: {tempo_restante // 60}:{tempo_restante % 60}", True, 'black')
    pontos = font.render(f"{qtpontos}", True, 'black')
    screen.blit(pontos, (10,10))
    screen.blit(texto_tempo, (300, 10))
    todos_sprites.draw(screen)
    serpentes.draw(screen)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
