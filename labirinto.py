import pygame
import sys
from collections import deque

pygame.init()

LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Labirinto")

BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)

IMAGEM_RATO = pygame.image.load("rato1.jpg")
IMAGEM_QUEIJO = pygame.image.load("queijo.jpg")

TAMANHO_CELULA = 20

def carregar_labirinto(arquivo):
    with open(arquivo, "r") as arquivo_labirinto:
        linhas = arquivo_labirinto.readlines()
        
    labirinto = []
    encontrou_rato = False

    for y, linha in enumerate(linhas):
        linha_celulas = []
        for x, celula in enumerate(linha.strip()):
            if celula == '1':
                linha_celulas.append(1)
            elif celula == '0':
                linha_celulas.append(0)
            elif celula == 'm':
                linha_celulas.append(2)
                encontrou_rato = True
            elif celula == 'e':
                linha_celulas.append(3)
        labirinto.append(linha_celulas)
    
    if not encontrou_rato:
        print("Labirinto não possui entrada para o rato (m).")
        sys.exit()

    return labirinto

def desenhar_labirinto():
    TELA.fill(BRANCO)
    for y, linha in enumerate(labirinto):
        for x, celula in enumerate(linha):
            if (x, y) in caminhos_visitados:
                pygame.draw.rect(TELA, VERMELHO, (x * TAMANHO_CELULA, y * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))
            else:
                imagem = imagens_celulas.get(celula, None)
                if imagem is not None:
                    TELA.blit(imagem, (x * TAMANHO_CELULA, y * TAMANHO_CELULA))

def movimento_possivel(pos_x, pos_y):
    movimentos = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for movimento in movimentos:
        nova_pos_x = pos_x + movimento[0]
        nova_pos_y = pos_y + movimento[1]
        if (
            0 <= nova_pos_x < len(labirinto[0])
            and 0 <= nova_pos_y < len(labirinto)
            and labirinto[nova_pos_y][nova_pos_x] != 1
            and (nova_pos_x, nova_pos_y) not in caminhos_visitados
        ):
            return True
    return False

def movimentar_jogador():
    global posicao_jogador_x, posicao_jogador_y

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
            movimento_valido = True
            pilha.append((posicao_jogador_x, posicao_jogador_y))
            caminhos_visitados.add((posicao_jogador_x, posicao_jogador_y))
            labirinto[posicao_jogador_y][posicao_jogador_x] = 0
            posicao_jogador_x, posicao_jogador_y = nova_pos_x, nova_pos_y

            if posicao_jogador_x == posicao_objetivo_x and posicao_jogador_y == posicao_objetivo_y:
                global encontrou_queijo
                encontrou_queijo = True
            break

    return movimento_valido

def retroceder_jogador():
    global posicao_jogador_x, posicao_jogador_y

    if pilha:
        pilha_solucao.append((posicao_jogador_x, posicao_jogador_y))
        caminhos_visitados.add((posicao_jogador_x, posicao_jogador_y))
        posicao_anterior_x, posicao_anterior_y = posicao_jogador_x, posicao_jogador_y
        posicao_jogador_x, posicao_jogador_y = pilha.pop()
        pygame.draw.rect(TELA, VERMELHO, (posicao_jogador_x * TAMANHO_CELULA, posicao_jogador_y * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))

def main():
    global posicao_jogador_x, posicao_jogador_y, posicao_anterior_x, posicao_anterior_y
    global encontrou_queijo

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        desenhar_labirinto()

        if not encontrou_queijo:
            movimento_valido = movimentar_jogador()

            if not movimento_valido:
                if not movimento_possivel(posicao_jogador_x, posicao_jogador_y) and not pilha:
                    print("Labirinto sem saída")
                    pygame.quit()
                    sys.exit()

                retroceder_jogador()

        else:
            if pilha_solucao:
                posicao_anterior_x, posicao_anterior_y = posicao_jogador_x, posicao_jogador_y
                posicao_jogador_x, posicao_jogador_y = pilha_solucao.pop()
                caminhos_visitados.add((posicao_jogador_x, posicao_jogador_y))
                labirinto[posicao_jogador_y][posicao_jogador_x] = 0
                pilha_solucao.append((posicao_jogador_x, posicao_jogador_y))
                pygame.draw.rect(TELA, VERMELHO, (posicao_jogador_x * TAMANHO_CELULA, posicao_jogador_y * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))

        TELA.blit(IMAGEM_RATO, (posicao_jogador_x * TAMANHO_CELULA, posicao_jogador_y * TAMANHO_CELULA))
        pygame.display.update()

        pygame.time.delay(100)  

        if encontrou_queijo:
            print("Achou o queijo!")
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    labirinto = carregar_labirinto("labirinto.txt")
    posicao_jogador_x, posicao_jogador_y = None, None
    posicao_objetivo_x, posicao_objetivo_y = None, None
    posicao_anterior_x, posicao_anterior_y = None, None

    imagens_celulas = {
        1: pygame.Surface((TAMANHO_CELULA, TAMANHO_CELULA)),
        2: IMAGEM_RATO,
        3: IMAGEM_QUEIJO,
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

    pilha = deque()
    pilha_solucao = deque()
    caminhos_visitados = set()

    posicao_anterior_x, posicao_anterior_y = posicao_jogador_x, posicao_jogador_y
    encontrou_queijo = False

    main()
