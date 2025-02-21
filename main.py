import random
import pygame

from pygame.locals import K_w, K_a, K_s, K_d

pygame.init()
screen = pygame.display.set_mode((600,600))
clock = pygame.time.Clock()
running = True
font = pygame.font.Font(None, 24)
tempo_limite = 30000
intervalo_frutas = 7000
intervalo_serpentes = 5000
inicio_tempo = pygame.time.get_ticks()
contador_ticks_serpentes = 0
contador_ticks_frutas = 0
pontos_spawn_frutas = [(240, 106), (440, 106), (365, 256), (80, 376), (520,376)]
pontos_spawn_serpentes = [    (80, 96), (360, 96), (235, 236), (80, 356), (360, 356)]
modo_de_jogo = 'abertura'

class playerSprite(pygame.sprite.Sprite):
    def __init__(self):
         super().__init__()
         macaco_img = pygame.image.load('macaco.png').convert_alpha()
         macaco_img = pygame.transform.scale(macaco_img, (8*5, 12*5))
         self.image = macaco_img
         self.rect = macaco_img.get_rect()
         self.rect.topleft = (235, 286)
         self.velocidade = 1.2
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
        if self.rect.x + 27*3 > 600:
            self.rect.x -= self.velocidade
        for bloco in blocos:
            if bloco.rect.x > self.rect.x:
                self.rect.x += self.velocidade
        
        self.sentido = -1

    def jump(self):
        if self.vertical_speed == 0:
            self.vertical_speed = -10
        

    def tick(self, tempo_restante):
        self.rect.y += self.vertical_speed
        self.vertical_speed += 0.3
        self.detectar_colisoes(blocos, frutas, serpentes, tempo_restante)

    def detectar_colisoes(self, blocos, frutas, serpentes, tempo_restante):
        global qtpontos
        colididos = pygame.sprite.spritecollide(self, blocos, False)
        for bloco in colididos:
            if self.vertical_speed > 0 and self.rect.bottom >= bloco.rect.top:
                self.rect.bottom = bloco.rect.top
                self.vertical_speed = 0 
            elif self.vertical_speed < 0 and self.rect.top <= bloco.rect.bottom:
                self.rect.top = bloco.rect.bottom
                self.vertical_speed = 0

        
        
        if self.rect.bottom >= 660:
            return "game_over"
       
        if pygame.sprite.spritecollide(self, serpentes, False):
            print(45)
            return "game_over"
       
        contagem_pontos = pygame.sprite.spritecollide(player, frutas, True)
        for _ in contagem_pontos:
            qtpontos += 1   
            tempo_restante += 5    

        

class blocosSprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        tronco_img = pygame.image.load('tronco1.png').convert_alpha()
        tronco_img = pygame.transform.scale(tronco_img, (32*5, 7*5))
        self.image = tronco_img
        self.rect = tronco_img.get_rect()
        self.rect.topleft = (x, y)

class serpentesSprite(pygame.sprite.Sprite):
    def __init__(self, x ,y):
        super().__init__()
        serpente_img = pygame.image.load('serpente.png').convert_alpha()
        serpente_img = pygame.transform.scale(serpente_img, (40,40))
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

def gameplay():
    global contador_ticks_serpentes, contador_ticks_frutas, tempo_limite, running
    tempo_passado = pygame.time.get_ticks() - inicio_tempo
    tempo_restante = ((tempo_limite - tempo_passado) // 1000)

    tempo_atual_serpentes = pygame.time.get_ticks()
    tempo_atual_frutas = pygame.time.get_ticks()

    screen.fill((119, 162, 230))
    player.tick(tempo_restante)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move_left(blocos)
    if keys[pygame.K_RIGHT]:
        player.move_right(blocos)
    if keys[pygame.K_UP]:
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
    frutas.draw(screen)
    pygame.display.flip()

def menu():
    global modo_de_jogo
    abertura = pygame.image.load('abertura.png')
    texto = font.render("Pressione ENTER para começar", True, (255, 255, 255))
    texto_rect = texto.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(abertura, (0, 0))
    screen.blit(texto, texto_rect)
    pygame.display.flip()
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()  # Fechar o jogo
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    modo_de_jogo = "gameplay"



# definir os sprites e os grupos
player = playerSprite()
blocos = pygame.sprite.Group()
blocos.add(blocosSprite(80, 146))
blocos.add(blocosSprite(360, 146))
blocos.add(blocosSprite(235, 286))
blocos.add(blocosSprite(80, 406))
blocos.add(blocosSprite(360, 406))
frutas = pygame.sprite.Group()
serpentes = pygame.sprite.Group()

todos_sprites = pygame.sprite.Group([player, blocos, serpentes, frutas])

qtpontos = 0

# loop principal
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if modo_de_jogo == "gameplay":
        gameplay()
    elif modo_de_jogo == 'abertura':
        menu()

    clock.tick(60)

pygame.quit()
