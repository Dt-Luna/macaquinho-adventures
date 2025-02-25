import random
import pygame

from pygame.locals import K_w, K_a, K_s, K_d

pygame.init()
screen = pygame.display.set_mode((600,600))
clock = pygame.time.Clock()
running = True
font = pygame.font.Font(None, 24)
tempo_limite = 600000
intervalo_frutas = 4000
intervalo_serpentes = 5000
inicio_tempo = pygame.time.get_ticks()
contador_ticks_serpentes = 0
contador_ticks_frutas = 0
serpente_altura = 40
fruta_largura = 30
bloco_largura = 160
pode_pular = True

modo_de_jogo = 'abertura'

class playerSprite(pygame.sprite.Sprite):
    def __init__(self):
         super().__init__()
         macaco_img = pygame.image.load('macaco.png').convert_alpha()
         macaco_img = pygame.transform.scale(macaco_img, (8*3, 12*3))
         self.image = macaco_img
         self.rect = macaco_img.get_rect()
         self.rect.topleft = (235, 286)
         self.velocidade = 1.5
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

    def jump(self, pode_pular): 
        if pode_pular:
            self.vertical_speed = -8

        

    def tick(self, tempo_restante):
        self.rect.y += self.vertical_speed
        self.vertical_speed += 0.3
        self.detectar_colisoes(blocos, frutas, serpentes, tempo_restante)

    def detectar_colisoes(self, blocos, frutas, serpentes, tempo_restante):
        global qtpontos, pode_pular
        pode_pular = False
        colididos = pygame.sprite.spritecollide(self, blocos, False)
        for bloco in colididos:
            direcao_p = [0, 0]
            menor_p = float('inf')
            penetra_baixo = max(bloco.rect.bottom - self.rect.top, 0)
            if menor_p > penetra_baixo:
                menor_p = penetra_baixo
                direcao_p = [0, 1]
            penetra_cima = max(self.rect.bottom - bloco.rect.top, 0)
            if menor_p > penetra_cima:
                menor_p = penetra_cima
                direcao_p = [0, -1]
            penetra_esquerda = max(bloco.rect.right - self.rect.left, 0)
            if menor_p > penetra_esquerda:
                menor_p = penetra_esquerda
                direcao_p = [-1, 0]
            penetra_direita = max(self.rect.right - bloco.rect.left, 0)
            if menor_p > penetra_direita:
                menor_p = penetra_direita
                direcao_p = [1, 0]

            if direcao_p[1] == 1 or direcao_p[1] == -1:
                self.vertical_speed = 0
            
            if direcao_p[1] == -1:
                pode_pular = True

            self.rect.x -= menor_p * direcao_p[0]
            self.rect.y += menor_p * direcao_p[1]

            print(menor_p, direcao_p)
                
            # if self.rect.x < bloco.rect.x or self.rect.x > bloco.rect.x:
            #     self.rect.bottom = bloco.rect.top
            #     self.vertical_speed = 0 
            
            # if self.vertical_speed > 0 and self.rect.bottom >= bloco.rect.top:
            # elif self.vertical_speed < 0 and self.rect.top <= bloco.rect.bottom:
            #     self.rect.top = bloco.rect.bottom
            #     self.vertical_speed = 0 
            #     # pode_pular = False

        if self.rect.bottom >= 660:
            return "game_over"
       
        colididas = pygame.sprite.spritecollide(self, serpentes, False)
        for cobra in colididas:
            if self.rect.bottom < (cobra.rect.bottom - serpente_altura//2):
                serpentes.remove(cobra)
                self.jump(True)
            else:
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
    def __init__(self, x, y, bloco):
        super().__init__()
        serpente_img = pygame.image.load('serpente.png').convert_alpha()
        serpente_img = pygame.transform.scale(serpente_img, (40,40))
        self.image = serpente_img
        self.rect = serpente_img.get_rect()
        self.rect.topleft = (x, y)
        self.bloco = bloco
        self.sentido = 1

    def tick(self):
        self.rect.x += self.sentido 
        if self.rect.topleft[0] <= self.bloco.rect.topleft[0]:
            self.image = pygame.transform.flip(self.image, True, False)
            self.sentido = 1
        elif self.rect.topright[0] >= self.bloco.rect.topright[0]:
            self.image = pygame.transform.flip(self.image, True, False)
            self.sentido = -1

class frutaSprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        fruta_img = pygame.image.load('maca.png').convert_alpha()
        fruta_img = pygame.transform.scale(fruta_img, (30,30))
        self.image = fruta_img
        self.rect = fruta_img.get_rect()
        self.rect.topleft = (x, y)

class avisoSprite(pygame.sprite.Sprite):
    def __initi__(self, x, y):
        super().__init__()
        aviso_img = pygame.image.load('aviso.png').convert_alpha()
        aviso_img = pygame.transform.scale(aviso_img, (40, 40))
        self.image = aviso_img
        self.rect = aviso_img
        self.rect.topleft = (x,y)


def criar_frutas():
    i = random.choice(pontos_spawn_frutas_disponiveis)
    pontos_spawn_frutas_disponiveis.remove(i)
    x, y = pontos_spawn_frutas[i]
    fruta = frutaSprite(x, y)
    return fruta

def criar_serpentes():
    i = random.choice(pontos_spawn_serpentes_disponiveis)
    pontos_spawn_serpentes_disponiveis.remove(i)
    x, y = pontos_spawn_serpentes[i]
    serpente = serpentesSprite(x, y, blocos.sprites()[i])
    return serpente

def gameplay():
    global contador_ticks_serpentes, contador_ticks_frutas, tempo_limite, running, serpente
    tempo_passado = pygame.time.get_ticks() - inicio_tempo
    tempo_restante = ((tempo_limite - tempo_passado) // 1000)

    tempo_atual_serpentes = pygame.time.get_ticks()
    tempo_atual_frutas = pygame.time.get_ticks()

    screen.fill((119, 162, 230))
    player.tick(tempo_restante)
    for serpente in serpentes:
        serpente.tick()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move_left(blocos)
    if keys[pygame.K_RIGHT]:
        player.move_right(blocos)
    if keys[pygame.K_UP]:
        player.jump(pode_pular)

    if pontos_spawn_serpentes_disponiveis:
        if tempo_atual_serpentes - contador_ticks_serpentes >= intervalo_serpentes:
            serpentes.add(criar_serpentes())
            contador_ticks_serpentes = tempo_atual_serpentes

    # if tempo_atual_serpentes - contador_ticks_serpentes >= intervalo_serpentes - 2:
    #     todos_sprites.add(criar_serpentes())
    #     contador_ticks_serpentes = tempo_atual_serpentes

    if pontos_spawn_frutas_disponiveis:
        if tempo_atual_frutas - contador_ticks_frutas >= intervalo_frutas:
            frutas.add(criar_frutas())
            contador_ticks_frutas = tempo_atual_frutas

# possiveis game overs
    resultado = player.detectar_colisoes(blocos, frutas, serpentes, tempo_restante)
    if resultado == "game_over":
        print('vc perdeu a')
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

pontos_spawn_serpentes = [(bloco.rect.topleft[0], bloco.rect.topleft[1] - serpente_altura) for bloco in blocos]
pontos_spawn_frutas = [(bloco.rect.topleft[0] + (bloco_largura//2 - fruta_largura//2), bloco.rect.topleft[1] - fruta_largura - 10) for bloco in blocos]
pontos_spawn_serpentes_disponiveis = [i for i in range(len(pontos_spawn_serpentes))]
pontos_spawn_frutas_disponiveis = [i for i in range(len(pontos_spawn_frutas))]
print(pontos_spawn_serpentes_disponiveis)
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
