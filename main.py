import random
import pygame

from pygame.locals import K_w, K_a, K_s, K_d

pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
running = True
font = pygame.font.Font(None, 24)
wfont = pygame.font.Font(None, 48)
tempo_limite = 6000
intervalo_frutas = 4000
intervalo_serpentes = 4000
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
         self.velocidade = 4
         self.sentido = -1 #-1 e 1 são esquerda e direita
         self.vertical_speed = 0 

    def move_left(self):
        if self.sentido == -1:
            self.image = pygame.transform.flip(self.image, True, False)       
        self.rect.x -= self.velocidade
        self.sentido = 1
        if self.rect.x < 0:
            self.rect.x += self.velocidade

    def move_right(self):
        if self.sentido == 1:
            self.image = pygame.transform.flip(self.image, True, False)
            print(self.rect.x)
        if self.rect.right < 600:
            self.rect.x += self.velocidade
        self.sentido = -1
            

    def jump(self, pode_pular): 
        if pode_pular:
            self.vertical_speed = -8

    def tick(self):
        self.rect.y += self.vertical_speed
        self.vertical_speed += 0.3
        self.detectar_colisoes(blocos, frutas, serpentes)

    def detectar_colisoes(self, blocos, frutas, serpentes):
        global pode_pular, qt_serpentes_eliminadas, qt_frutas_coletadas
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

        if self.rect.bottom >= 660:
            return "game_over"
       
        colididas = pygame.sprite.spritecollide(self, serpentes, False)
        for cobra in colididas:
            print(cobra.tempo_aviso)
            if cobra.tempo_aviso <= 0:
                if self.rect.bottom < (cobra.rect.bottom - serpente_altura//2):
                    self.jump(True)
                    pontos_spawn_serpentes_disponiveis.append(cobra.index)
                    serpentes.remove(cobra)
                    qt_serpentes_eliminadas += 1
                    print(qt_serpentes_eliminadas, 'a bct ')
                else:
                    return "game_over"
        
        frutas_colididas = pygame.sprite.spritecollide(player, frutas, True)
        for banana in frutas_colididas:
            qt_frutas_coletadas += 1
            pontos_spawn_frutas_disponiveis.append(banana.index)
            print(qt_frutas_coletadas)
            frutas.remove(banana)


        

class blocosSprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        tronco_img = pygame.image.load('tronco1.png').convert_alpha()
        tronco_img = pygame.transform.scale(tronco_img, (32*5, 7*5))
        self.image = tronco_img
        self.rect = tronco_img.get_rect()
        self.rect.topleft = (x, y)

class serpentesSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, bloco, index):
        super().__init__()
        serpente_img = pygame.image.load('serpente.png').convert_alpha()
        serpente_img = pygame.transform.scale(serpente_img, (40,40))
        self.serpente_img = pygame.transform.flip(serpente_img, True, False)
        aviso_img = pygame.image.load('aviso.png').convert_alpha()
        aviso_img = pygame.transform.scale(aviso_img, (30, 30))
        self.image = aviso_img
        self.tempo_aviso = 100
        self.rect = serpente_img.get_rect()
        self.rect.topleft = (x, y)
        self.bloco = bloco
        self.sentido = 1
        self.index = index

    def tick(self):
        if self.tempo_aviso <= 0:    
            self.rect.x += self.sentido 
            if self.rect.topleft[0] <= self.bloco.rect.topleft[0]:
                self.image = pygame.transform.flip(self.image, True, False)
                self.sentido = 1
            elif self.rect.topright[0] >= self.bloco.rect.topright[0]:
                self.image = pygame.transform.flip(self.image, True, False)
                self.sentido = -1
        else:
            self.tempo_aviso -=1
            if self.tempo_aviso == 0:
                self.image = self.serpente_img


class frutaSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, index):
        super().__init__()
        fruta_img = pygame.image.load('maca.png').convert_alpha()
        fruta_img = pygame.transform.scale(fruta_img, (30,30))
        self.image = fruta_img
        self.rect = fruta_img.get_rect()
        self.rect.topleft = (x, y)
        self.index = index

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
    fruta = frutaSprite(x, y, i)
    return fruta

def criar_serpentes():
    i = random.choice(pontos_spawn_serpentes_disponiveis)
    pontos_spawn_serpentes_disponiveis.remove(i)
    x, y = pontos_spawn_serpentes[i]
    serpente = serpentesSprite(x, y, blocos.sprites()[i], i)
    return serpente

def vitoria(qtpontos):

    global tempo_limite, qt_frutas_coletadas, qt_serpentes_eliminadas, contador_ticks_frutas, contador_ticks_serpentes, modo_de_jogo, inicio_tempo
    vitoria = pygame.image.load('vitoria.png')
    win_text = wfont.render('Você ganhou!', True, 'black')
    score_text = font.render(f'Score: {qtpontos}', True, 'black')
    jogar_novamente = font.render('aperte ENTER para jogar novamente', True, 'black')
    screen.blit(vitoria,(0, 0))
    screen.blit(win_text, (250, 0))
    screen.blit(jogar_novamente, (250, 200))
    screen.blit(score_text, (20, 20))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()  # Fechar o jogo
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                tempo_limite = 6000
                qt_frutas_coletadas = 0
                qt_serpentes_eliminadas = 0
                qtpontos = 0
                contador_ticks_serpentes = 0
                contador_ticks_frutas = 0
                inicio_tempo = pygame.time.get_ticks()
                modo_de_jogo = "gameplay"

def gameplay():
    global qtpontos, modo_de_jogo
    fundo = pygame.image.load('background.png')
    qtpontos = qt_frutas_coletadas * 5 + qt_serpentes_eliminadas * 10
    global contador_ticks_serpentes, contador_ticks_frutas, tempo_limite, running, serpente
    tempo_passado = pygame.time.get_ticks() - inicio_tempo
    tempo_restante = ((tempo_limite - tempo_passado) // 1000)

    tempo_atual_serpentes = pygame.time.get_ticks()
    tempo_atual_frutas = pygame.time.get_ticks()

    screen.fill((119, 162, 230))
    player.tick()
    for serpente in serpentes:
        serpente.tick()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move_left()
    if keys[pygame.K_RIGHT]:
        player.move_right()
    if keys[pygame.K_UP]:
        player.jump(pode_pular)

    if pontos_spawn_serpentes_disponiveis:
        if tempo_atual_serpentes - contador_ticks_serpentes >= intervalo_serpentes:
            serpentes.add(criar_serpentes())
            contador_ticks_serpentes = tempo_atual_serpentes

    if pontos_spawn_frutas_disponiveis:
        if tempo_atual_frutas - contador_ticks_frutas >= intervalo_frutas:
            frutas.add(criar_frutas())
            contador_ticks_frutas = tempo_atual_frutas

# vitoria e derrota
    resultado = player.detectar_colisoes(blocos, frutas, serpentes)
    if resultado == "game_over":
        print('vc perdeu a')
        
    if tempo_restante <= 0:
        modo_de_jogo = "vitoria"

    # textos e sprites
    screen.blit(fundo, (0, 0))
    texto_tempo = font.render(f"Tempo: {tempo_restante // 60}:{tempo_restante % 60}", True, 'black')
    pontos = font.render(f"{qtpontos}", True, 'black')
    screen.blit(pontos, (10,10))
    screen.blit(texto_tempo, (300, 10))
    serpentes.draw(screen)
    frutas.draw(screen)
    todos_sprites.draw(screen)
    pygame.display.flip()

def menu():
    global modo_de_jogo, inicio_tempo
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
                inicio_tempo = pygame.time.get_ticks()
                modo_de_jogo = "gameplay"



# definir os sprites e os grupos
player = playerSprite()
blocos = pygame.sprite.Group()
blocos.add(blocosSprite(60, 186))
blocos.add(blocosSprite(420, 186))
blocos.add(blocosSprite(240, 286))
blocos.add(blocosSprite(60, 376))
blocos.add(blocosSprite(420, 376))

pontos_spawn_serpentes = [(bloco.rect.topleft[0], bloco.rect.topleft[1] - serpente_altura) for bloco in blocos]
pontos_spawn_frutas = [(bloco.rect.topleft[0] + (bloco_largura//2 - fruta_largura//2), bloco.rect.topleft[1] - fruta_largura - 10) for bloco in blocos]
pontos_spawn_serpentes_disponiveis = [i for i in range(len(pontos_spawn_serpentes))]
pontos_spawn_frutas_disponiveis = [i for i in range(len(pontos_spawn_frutas))]
frutas = pygame.sprite.Group()
serpentes = pygame.sprite.Group()
todos_sprites = pygame.sprite.Group([player, blocos])

qt_serpentes_eliminadas = 0
qt_frutas_coletadas = 0

# loop principal
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if modo_de_jogo == "gameplay":
        gameplay()
    elif modo_de_jogo == 'abertura':
        menu()
    elif modo_de_jogo == 'vitoria':
        vitoria(qtpontos)

    clock.tick(60)

pygame.quit()