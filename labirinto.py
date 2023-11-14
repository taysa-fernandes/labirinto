import pygame
import sys
from collections import deque

pygame.init()

LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Labirinto")

BRANCO = (255, 255, 255)

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
posicao_anterior_x, posicao_anterior_y = None, None

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
            posicao_anterior_x = x
            posicao_anterior_y = y
        elif celula == 3:
            posicao_objetivo_x = x
            posicao_objetivo_y = y

executando = True
encontrou_queijo = False

pilha = deque()
pilha_solucao = deque()
caminhos_visitados = set()

posicao_anterior_x, posicao_anterior_y = posicao_jogador_x, posicao_jogador_y

while executando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False

    TELA.fill(BRANCO)

    for y, linha in enumerate(labirinto):
        for x, celula in enumerate(linha):
            imagem = imagens_celulas.get(celula, None)
            if imagem is not None:
                TELA.blit(imagem, (x * TAMANHO_CELULA, y * TAMANHO_CELULA))

    if not encontrou_queijo:
        movimentos = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        movimento_valido = False

        for movimento in movimentos:
            nova_pos_x = posicao_jogador_x + movimento[0]
            nova_pos_y = posicao_jogador_y + movimento[1]
            if (
                0 <= nova_pos_x < len(labirinto[0])
                and 0 <= nova_pos_y < len(labirinto)
                and labirinto[nova_pos_y][nova_pos_x] != 1
                and (nova_pos_x, nova_pos_y) not in caminhos_visitados
            ):
                posicao_anterior_x, posicao_anterior_y = posicao_jogador_x, posicao_jogador_y
                movimento_valido = True
                pilha.append((posicao_jogador_x, posicao_jogador_y))
                caminhos_visitados.add((posicao_jogador_x, posicao_jogador_y))
                labirinto[posicao_jogador_y][posicao_jogador_x] = 0
                posicao_jogador_x, posicao_jogador_y = nova_pos_x, nova_pos_y
                pygame.time.delay(100)

                if posicao_jogador_x == posicao_objetivo_x and posicao_jogador_y == posicao_objetivo_y:
                    encontrou_queijo = True
                break

        if not movimento_valido:
            if pilha:
                pilha_solucao.append((posicao_jogador_x, posicao_jogador_y))
                caminhos_visitados.add((posicao_jogador_x, posicao_jogador_y))
                posicao_anterior_x, posicao_anterior_y = posicao_jogador_x, posicao_jogador_y
                posicao_jogador_x, posicao_jogador_y = pilha.pop()

    else:
        pilha_solucao.append((posicao_jogador_x, posicao_jogador_y))
        if pilha_solucao:
            posicao_anterior_x, posicao_anterior_y = posicao_jogador_x, posicao_jogador_y
            posicao_jogador_x, posicao_jogador_y = pilha_solucao.pop()
            caminhos_visitados.add((posicao_jogador_x, posicao_jogador_y))
            labirinto[posicao_jogador_y][posicao_jogador_x] = 0

    TELA.blit(imagem_mouse, (posicao_jogador_x * TAMANHO_CELULA, posicao_jogador_y * TAMANHO_CELULA))

    pygame.display.update()


    if encontrou_queijo:
        print("achou queijo")
        pygame.quit()
        sys.exit()
