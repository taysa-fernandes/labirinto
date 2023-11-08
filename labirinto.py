import pygame
import sys
from collections import deque

pygame.init()

LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Labirinto")

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

imagem_mouse = pygame.image.load("rato1.jpg")
imagem_queijo = pygame.image.load("queijo.jpg")

def carregar_labirinto(arquivo):
    with open(arquivo, "r") as arquivo_labirinto:
        linhas = arquivo_labirinto.readlines()
    labirinto = []

    for linha in linhas:
        linha_celulas = []
        for celula in linha.strip():
            if celula == '1':
                linha_celulas.append(1)
            elif celula == '0':
                linha_celulas.append(0)
            elif celula == 'm':
                linha_celulas.append(2)
            elif celula == 'e':
                linha_celulas.append(3)
        labirinto.append(linha_celulas)
    return labirinto

labirinto = carregar_labirinto("labirinto.txt")

TAMANHO_CELULA = 20

posicao_jogador_x, posicao_jogador_y = None, None
posicao_objetivo_x, posicao_objetivo_y = None, None

imagens_celulas = {
    1: pygame.Surface((TAMANHO_CELULA, TAMANHO_CELULA)),
    2: imagem_mouse,
    3: imagem_queijo,
}

for y, linha in enumerate(labirinto):
    for x, celula in enumerate(linha):
        if celula == 2:  
            posicao_jogador_x = x
            posicao_jogador_y = y
        elif celula == 3:  
            posicao_objetivo_x = x
            posicao_objetivo_y = y

executando = True
encontrou_queijo = False


pilha = deque()
pilha.append((posicao_jogador_x, posicao_jogador_y))

while executando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False
        if not encontrou_queijo:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    if posicao_jogador_x > 0 and labirinto[posicao_jogador_y][posicao_jogador_x - 1] != 1:
                        pilha.append((posicao_jogador_x, posicao_jogador_y))
                        labirinto[posicao_jogador_y][posicao_jogador_x] = 0
                        posicao_jogador_x -= 1
                elif evento.key == pygame.K_RIGHT:
                    if posicao_jogador_x < len(labirinto[0]) - 1 and labirinto[posicao_jogador_y][posicao_jogador_x + 1] != 1:
                        pilha.append((posicao_jogador_x, posicao_jogador_y))
                        labirinto[posicao_jogador_y][posicao_jogador_x] = 0
                        posicao_jogador_x += 1
                elif evento.key == pygame.K_UP:
                    if posicao_jogador_y > 0 and labirinto[posicao_jogador_y - 1][posicao_jogador_x] != 1:
                        pilha.append((posicao_jogador_x, posicao_jogador_y))
                        labirinto[posicao_jogador_y][posicao_jogador_x] = 0
                        posicao_jogador_y -= 1
                elif evento.key == pygame.K_DOWN:
                    if posicao_jogador_y < len(labirinto) - 1 and labirinto[posicao_jogador_y + 1][posicao_jogador_x] != 1:
                        pilha.append((posicao_jogador_x, posicao_jogador_y))
                        labirinto[posicao_jogador_y][posicao_jogador_x] = 0
                        posicao_jogador_y += 1

            if posicao_jogador_x == posicao_objetivo_x and posicao_jogador_y == posicao_objetivo_y:
                encontrou_queijo = True

    TELA.fill(BRANCO)

    for y, linha in enumerate(labirinto):
        for x, celula in enumerate(linha):
            imagem = imagens_celulas.get(celula, None)
            if imagem is not None:
                TELA.blit(imagem, (x * TAMANHO_CELULA, y * TAMANHO_CELULA))

    TELA.blit(imagem_mouse, (posicao_jogador_x * TAMANHO_CELULA, posicao_jogador_y * TAMANHO_CELULA))

    pygame.display.update()

    if encontrou_queijo:
        pygame.quit()
        sys.exit()
