import sys
import random
import pygame

pygame.init()
pygame.font.init()

LARGURA_JOGO = 640
LARGURA_PAINEL = 360
LARGURA_TELA = LARGURA_JOGO + LARGURA_PAINEL
ALTURA_TELA = 520

TAMANHO_BLOCO = 40
COLUNAS = LARGURA_JOGO // TAMANHO_BLOCO
LINHAS = ALTURA_TELA // TAMANHO_BLOCO

COR_PAREDE = (60, 50, 90)
COR_CHAO_CLARO = (65, 75, 125)
COR_CHAO_ESCURO = (75, 65, 115)
COR_TEXTO = (255, 255, 255)
COR_PAINEL_BG = (25, 25, 35)
COR_DESTAQUE = (255, 200, 0)
COR_JOGADOR = (80, 200, 255)
COR_MONSTRO = (255, 90, 90)
COR_MOEDA = (255, 215, 0)

TELA = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.pygame.display.set_caption("JOGO DA MASMORRA")
RELOGIO = pygame.time.Clock()

FONTE_TITULO = pygame.font.SysFont("Consolas", 18, bold=True)
FONTE_CORPO = pygame.font.SysFont("Consolas", 13)
FONTE_HUD = pygame.font.SysFont("Arial", 16, bold=True)

def criar_mapa():
    mapa = []
    for l in range(LINHAS):
        linha = []
        for c in range(COLUNAS):
            if l == 0 or l == LINHAS - 1 or c == 0 or c == COLUNAS - 1:
                linha.append(1)
            else:
                linha.append(0)
        mapa.append(linha)
    return mapa

MAPA = criar_mapa()

def sortear_posicao_livre(ocupados):
    while True:
        c = random.randint(1, COLUNAS - 2)
        l = random.randint(1, LINHAS - 2)
        if (c, l) not in ocupados and MAPA[l][c] == 0:
            return (c,l)

def reiniciar_jogo():
    global jogador_pos, moedas, monstros, vida, moedas_coletadas, pontos, game_over, vitoria

    posicoes_ocupadas = []

    jogador_pos = [1, 1]
    posicoes_ocupadas.append(tuple(jogador_pos))

    moedas = []
    for _ in range(8):
        pos = sortear_posicao_livre(posicoes_ocupadas)
        moedas.append(pos)
        posicoes_ocupadas.append(pos)

    monstros = []
    for _ in range(3):
        pos = sortear_posicao_livre(posicoes_ocupadas)
        monstros.append(list(pos))
        posicoes_ocupadas.append(pos)

    vida = 3
    moedas_coletadas = 0
    pontos = 0
    game_over = False
    vitoria = False

reiniciar_jogo()

tempo_ultimo_movimento = pygame.time.get_ticks()

def desenhar_marmorra_e_entidades():
    for l in range(LINHAS):
        for c in range(COLUNAS):
            x = c * TAMANHO_BLOCO
            y = l * TAMANHO_BLOCO
            rect = pygame.Rect(x, y, TAMANHO_BLOCO, TAMANHO_BLOCO)

            if MAPA[l][c] == 1:
                pygame.draw.rect(TELA, COR_PAREDE, rect)
                pygame.draw.rect(TELA, (40, 30, 70), rect, 2)
            else:
                cor_chao = COR_CHAO_CLARO if (l + c) % 2 == 0 else COR_CHAO_ESCURO
                pygame.draw.rect(TELA, cor_chao, rect)

    for m in moedas:
        cx = m[0] * TAMANHO_BLOCO + TAMANHO_BLOCO // 2
        cy = m[1] * TAMANHO_BLOCO + TAMANHO_BLOCO // 2
        pygame.draw.ellipse(TELA, COR_MOEDA, (cx - 6, cy - 12, 12, 24))

    for monstro in monstros:
        mx = monstro[0] + TAMANHO_BLOCO + 4
        my = monstro[1] + TAMANHO_BLOCO + 4
        rect = pygame.Rect(mx, my, TAMANHO_BLOCO - 8, TAMANHO_BLOCO - 8)
        pygame.draw.rect(TELA, COR_MONSTRO, rect, border_radius=6)
        pygame.draw.circle(TELA, (255, 255, 255), (mx + 10, my + 10), 3)
        pygame.draw.circle(TELA, (255, 255, 255), (mx + 22, my + 10), 3)

    jx = jogador_pos[0] * TAMANHO_BLOCO + 4
    jy = jogador_pos[1] * TAMANHO_BLOCO + 4
    rect_player = pygame.Rect(jx, jy, TAMANHO_BLOCO - 8, TAMANHO_BLOCO - 8)
    pygame.draw.rect(TELA, COR_JOGADOR, rect_player, border_radius=8)
    pygame.draw.circle(TELA, (255, 255, 255), (jx + 10, jy + 10), 3)
    pygame.draw.circle(TELA, (255, 255, 255), (jx + 22, jy + 10), 3)
