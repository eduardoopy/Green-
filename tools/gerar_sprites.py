"""
Gera os sprites do Green (pixel art, fundo transparente).

Uso (na raiz do projeto):
    pip install pillow
    python tools/gerar_sprites.py

Cada sprite é desenhado numa grade de 32x32 pixels e ampliado 8x (256x256)
sem suavização, para preservar a estética pixel art.
Saída: frontend/assets/sprites/<nome>.png
"""
from pathlib import Path
from PIL import Image

GRID = 32
ESCALA = 8
SAIDA = Path(__file__).resolve().parent.parent / "frontend" / "assets" / "sprites"

# Paleta do Green
CONTORNO = (74, 85, 94, 255)
CORPO = (244, 246, 247, 255)
SOMBRA = (208, 214, 218, 255)
VISOR = (17, 20, 23, 255)
VERDE = (46, 230, 107, 255)
VERDE_ESC = (23, 160, 74, 255)
VERDE_FRACO = (30, 110, 60, 255)
LAGRIMA = (96, 190, 240, 255)
BRILHO = (200, 255, 220, 255)
VAZIO = (0, 0, 0, 0)


class Tela:
    def __init__(self):
        self.img = Image.new("RGBA", (GRID, GRID), VAZIO)

    def px(self, x, y, cor):
        if 0 <= x < GRID and 0 <= y < GRID:
            self.img.putpixel((x, y), cor)

    def rect(self, x0, y0, x1, y1, cor):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.px(x, y, cor)

    def salvar(self, nome):
        SAIDA.mkdir(parents=True, exist_ok=True)
        grande = self.img.resize((GRID * ESCALA, GRID * ESCALA), Image.NEAREST)
        grande.save(SAIDA / f"{nome}.png")


def caixa_arredondada(t, x0, y0, x1, y1, preenchimento, contorno=None):
    """Retângulo com cantos cortados. Contorno opcional."""
    if contorno:
        t.rect(x0, y0, x1, y1, contorno)
        for (cx, cy) in [(x0, y0), (x1, y0), (x0, y1), (x1, y1)]:
            t.px(cx, cy, VAZIO)
        t.rect(x0 + 1, y0 + 1, x1 - 1, y1 - 1, preenchimento)
    else:
        t.rect(x0, y0, x1, y1, preenchimento)
        for (cx, cy) in [(x0, y0), (x1, y0), (x0, y1), (x1, y1)]:
            t.px(cx, cy, VAZIO)


def desenhar_olhos(t, tipo):
    """Olhos verdes dentro do visor. Olho esquerdo x=10..12, direito x=19..21."""
    L, R, y = 10, 19, 9
    if tipo == "aberto":
        for x0 in (L, R):
            t.rect(x0, y, x0 + 2, y + 3, VERDE)
            t.px(x0, y, BRILHO)
    elif tipo == "piscando":
        for x0 in (L, R):
            t.rect(x0, y + 2, x0 + 2, y + 2, VERDE)
    elif tipo == "feliz":  # olhos em arco ^ ^
        for x0 in (L, R):
            t.px(x0 + 1, y + 1, VERDE)
            t.px(x0, y + 2, VERDE)
            t.px(x0 + 2, y + 2, VERDE)
            t.px(x0, y + 3, VERDE)
            t.px(x0 + 2, y + 3, VERDE)
    elif tipo == "surpreso":  # olhos maiores, pupila vazada
        for x0 in (L - 1, R):
            t.rect(x0, y - 1, x0 + 3, y + 4, VERDE)
            t.rect(x0 + 1, y, x0 + 2, y + 1, VISOR)
    elif tipo == "dormindo":
        for x0 in (L, R):
            t.rect(x0, y + 2, x0 + 2, y + 2, VERDE_FRACO)
    elif tipo == "triste":  # olhos caídos
        for x0 in (L, R):
            t.rect(x0, y + 1, x0 + 2, y + 3, VERDE)
        t.px(L, y + 1, VISOR)
        t.px(R + 2, y + 1, VISOR)
    elif tipo == "curioso":  # um olho maior que o outro
        t.rect(L, y + 1, L + 2, y + 3, VERDE)
        t.rect(R - 1, y - 1, R + 2, y + 3, VERDE)
        t.px(R - 1, y - 1, BRILHO)
    elif tipo == "atento":  # olhos altos e brilhantes
        for x0 in (L, R):
            t.rect(x0, y - 1, x0 + 2, y + 4, VERDE)
            t.px(x0, y - 1, BRILHO)


def desenhar_boca(t, tipo):
    y, cx = 14, 14
    if tipo == "neutra":
        t.rect(cx, y, cx + 3, y, VERDE_FRACO)
    elif tipo == "sorriso":
        t.rect(cx, y, cx + 3, y, VERDE)
        t.px(cx - 1, y - 1, VERDE)
        t.px(cx + 4, y - 1, VERDE)
    elif tipo == "aberta":
        t.rect(cx + 1, y - 1, cx + 2, y, VERDE)
    elif tipo == "fechada":
        t.rect(cx, y, cx + 3, y, VERDE)
    elif tipo == "o":
        t.rect(cx + 1, y - 1, cx + 2, y, VERDE)
    elif tipo == "triste":
        t.rect(cx, y - 1, cx + 3, y - 1, VERDE_FRACO)
        t.px(cx - 1, y, VERDE_FRACO)
        t.px(cx + 4, y, VERDE_FRACO)
    elif tipo == "dormindo":
        t.rect(cx + 1, y, cx + 2, y, VERDE_FRACO)


def desenhar_green(nome, olhos="aberto", boca="neutra", dy=0, h=0,
                   bracos="baixo", pernas="normal", luz_antena=VERDE, extras=None):
    """Desenha o Green completo.
    dy = deslocamento vertical do corpo (respirar / pular)
    h  = deslocamento horizontal da cabeça (inclinação)"""
    t = Tela()

    # Antena
    t.rect(15 + h, 3 + dy, 16 + h, 5 + dy, CONTORNO)
    t.rect(15 + h, 0 + dy, 16 + h, 2 + dy, luz_antena)
    if luz_antena == VERDE:
        t.px(15 + h, 0 + dy, BRILHO)

    # Cabeça
    caixa_arredondada(t, 6 + h, 5 + dy, 25 + h, 17 + dy, CORPO, CONTORNO)
    t.rect(8 + h, 16 + dy, 23 + h, 16 + dy, SOMBRA)
    # Laterais verdes (orelhas)
    t.rect(4 + h, 9 + dy, 5 + h, 13 + dy, VERDE_ESC)
    t.rect(26 + h, 9 + dy, 27 + h, 13 + dy, VERDE_ESC)
    t.rect(4 + h, 9 + dy, 4 + h, 13 + dy, CONTORNO)
    t.rect(27 + h, 9 + dy, 27 + h, 13 + dy, CONTORNO)

    # Visor
    caixa_arredondada(t, 8 + h, 7 + dy, 23 + h, 15 + dy, VISOR)

    # Olhos e boca
    sub = Tela()
    desenhar_olhos(sub, olhos)
    desenhar_boca(sub, boca)
    for y in range(GRID):
        for x in range(GRID):
            p = sub.img.getpixel((x, y))
            if p[3]:
                t.px(x + h, y + dy, p)

    # Corpo
    caixa_arredondada(t, 10, 18 + dy, 21, 26 + dy, CORPO, CONTORNO)
    t.rect(11, 25 + dy, 20, 25 + dy, SOMBRA)
    G = ["01110",
         "10000",
         "10110",
         "10010",
         "01110"]
    for gy, linha in enumerate(G):
        for gx, c in enumerate(linha):
            if c == "1":
                t.px(13 + gx, 19 + gy + dy, VERDE_ESC)

    # Braços
    if bracos == "baixo":
        for x0 in (8, 22):
            t.rect(x0, 19 + dy, x0 + 1, 24 + dy, CONTORNO)
        t.rect(8, 20 + dy, 8, 23 + dy, CORPO)
        t.rect(23, 20 + dy, 23, 23 + dy, CORPO)
        t.px(8, 24 + dy, VERDE_ESC)
        t.px(23, 24 + dy, VERDE_ESC)
    elif bracos == "alto":  # braços afastados e levantados (abaixo da cabeça)
        for x0 in (6, 24):
            t.rect(x0, 18 + dy, x0 + 1, 22 + dy, CONTORNO)
            t.rect(x0 if x0 == 6 else x0 + 1, 19 + dy, x0 if x0 == 6 else x0 + 1, 21 + dy, CORPO)
            t.rect(x0, 18 + dy, x0 + 1, 18 + dy, VERDE_ESC)
    elif bracos == "meio":  # um braço levantado
        t.rect(8, 19 + dy, 9, 24 + dy, CONTORNO)
        t.rect(8, 20 + dy, 8, 23 + dy, CORPO)
        t.rect(23, 18 + dy, 24, 22 + dy, CONTORNO)
        t.rect(24, 19 + dy, 24, 21 + dy, CORPO)
        t.rect(23, 18 + dy, 24, 18 + dy, VERDE_ESC)
    elif bracos == "caido":
        for x0 in (8, 22):
            t.rect(x0, 20 + dy, x0 + 1, 25 + dy, CONTORNO)
        t.rect(8, 21 + dy, 8, 24 + dy, CORPO)
        t.rect(23, 21 + dy, 23, 24 + dy, CORPO)

    # Pernas
    if pernas == "normal":
        t.rect(11, 27 + dy, 13, 30 + dy, CONTORNO)
        t.rect(18, 27 + dy, 20, 30 + dy, CONTORNO)
        t.rect(12, 27 + dy, 12, 29 + dy, CORPO)
        t.rect(19, 27 + dy, 19, 29 + dy, CORPO)
        t.rect(11, 30 + dy, 13, 30 + dy, VERDE_ESC)
        t.rect(18, 30 + dy, 20, 30 + dy, VERDE_ESC)
    elif pernas == "dobrada":  # agachado (dormindo)
        t.rect(10, 27 + dy, 13, 29 + dy, CONTORNO)
        t.rect(18, 27 + dy, 21, 29 + dy, CONTORNO)
        t.rect(11, 28 + dy, 12, 28 + dy, CORPO)
        t.rect(19, 28 + dy, 20, 28 + dy, CORPO)

    if extras:
        extras(t, dy)

    t.salvar(nome)


# ---------- símbolos ao redor do personagem ----------
def extra_zzz(t, dy):
    for (x, y) in [(27, 4), (28, 4), (29, 4), (28, 5), (27, 6), (28, 6), (29, 6)]:
        t.px(x, y, CONTORNO)
    for (x, y) in [(24, 0), (25, 0), (25, 1), (24, 2), (25, 2)]:
        t.px(x, y, CONTORNO)


def extra_interrogacao(t, dy):
    for (x, y) in [(28, 1), (29, 1), (30, 2), (29, 3), (28, 4), (28, 6)]:
        t.px(x, y, VERDE_ESC)


def extra_exclamacao(t, dy):
    for y in range(1, 5):
        t.px(28, y, VERDE_ESC)
    t.px(28, 6, VERDE_ESC)


def extra_ondas(t, dy):
    for (x, y) in [(29, 10), (30, 11), (30, 12), (30, 13), (29, 14)]:
        t.px(x, y, VERDE)
    for (x, y) in [(2, 10), (1, 11), (1, 12), (1, 13), (2, 14)]:
        t.px(x, y, VERDE)


def extra_lagrima(t, dy):
    t.px(11, 14 + dy, LAGRIMA)
    t.px(11, 15 + dy, LAGRIMA)


def main():
    # Idle: parado, respirando e piscando
    desenhar_green("idle_1")
    desenhar_green("idle_2", dy=1)
    desenhar_green("idle_blink", olhos="piscando")

    # Feliz: pulando
    desenhar_green("happy_1", olhos="feliz", boca="sorriso", bracos="alto")
    desenhar_green("happy_2", olhos="feliz", boca="sorriso", bracos="alto", dy=-2)

    # Surpreso
    desenhar_green("surprised", olhos="surpreso", boca="o", bracos="alto",
                   dy=1, extras=extra_exclamacao)

    # Dormindo
    desenhar_green("sleeping_1", olhos="dormindo", boca="dormindo", bracos="caido",
                   pernas="dobrada", dy=1, luz_antena=VERDE_FRACO, extras=extra_zzz)
    desenhar_green("sleeping_2", olhos="dormindo", boca="dormindo", bracos="caido",
                   pernas="dobrada", dy=2, luz_antena=VERDE_FRACO, extras=extra_zzz)

    # Triste
    desenhar_green("sad", olhos="triste", boca="triste", bracos="caido",
                   dy=1, luz_antena=VERDE_FRACO, extras=extra_lagrima)

    # Curioso: cabeça inclinada para o lado
    desenhar_green("curious", olhos="curioso", bracos="meio", h=1,
                   extras=extra_interrogacao)

    # Falando: boca alterna aberta/fechada
    desenhar_green("talking_1", boca="aberta")
    desenhar_green("talking_2", boca="fechada", dy=1)

    # Ouvindo: olhos atentos e ondas sonoras
    desenhar_green("listening", olhos="atento", bracos="meio", extras=extra_ondas)

    print("Sprites gerados em:", SAIDA)


if __name__ == "__main__":
    main()
