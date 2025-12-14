import pygame
import random
import sys
import os

# inicialização do pygame
pygame.init()

# config da tela
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Asteroid Game")

# Cores
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
CINZA = (200, 200, 200)
PRETO = (0, 0, 0)

# fonte
fonte = pygame.font.SysFont('Times New Roman', 35)

# imagem de fundo
caminho_imagem_fundo = os.path.join("C:\\Users\\higor\\Documents\\Python\\Game\\assest", "espaco.png")
try:
    imagem_fundo = pygame.image.load(caminho_imagem_fundo)
    imagem_fundo = pygame.transform.scale(imagem_fundo, (largura, altura))
except pygame.error as e:
    print(f"Erro ao carregar a imagem de fundo: {e}")
    sys.exit()

# imagem da nave
caminho_imagem_nave = os.path.join("C:\\Users\\higor\\Documents\\Python\\Game\\assest", "nave.png")
try:
    imagem_nave = pygame.image.load(caminho_imagem_nave)
    imagem_nave = pygame.transform.scale(imagem_nave, (50, 40))
except pygame.error as e:
    print(f"Erro ao carregar a imagem da nave: {e}")
    sys.exit()

# imagem do asteroide
caminho_imagem_asteroide = os.path.join("C:\\Users\\higor\\Documents\\Python\\Game\\assest", "asteroide.png")
try:
    imagem_asteroide_base = pygame.image.load(caminho_imagem_asteroide)
except pygame.error as e:
    print(f"Erro ao carregar a imagem do asteroide: {e}")
    sys.exit()

# imagem do tiro
caminho_imagem_tiro = os.path.join("C:\\Users\\higor\\Documents\\Python\\Game\\assest", "tiro.png")
try:
    imagem_tiro = pygame.image.load(caminho_imagem_tiro)
    imagem_tiro = pygame.transform.scale(imagem_tiro, (5, 10))
except pygame.error as e:
    print(f"Erro ao carregar a imagem do tiro: {e}")
    sys.exit()

# tamanhos dos asteroides
tamanhos_asteroides = {
    "pequeno": {"dimensao": (30, 30), "raio_colisao": 15},
    "medio": {"dimensao": (50, 50), "raio_colisao": 25},
    "grande": {"dimensao": (70, 70), "raio_colisao": 35}
}
imagens_asteroides = {
    tamanho: pygame.transform.scale(imagem_asteroide_base, info["dimensao"])
    for tamanho, info in tamanhos_asteroides.items()
}

# nave
nave_largura, nave_altura = 50, 40
nave_x = largura // 2 - nave_largura // 2
nave_y = altura - 60
velocidade_nave = 6

# tiros
tiros = []
velocidade_tiro = 8
max_tiros = 5

# asteroides
asteroides = []
velocidade_asteroide = 4
for _ in range(5):
    x = random.randint(0, largura - 70)
    y = random.randint(-600, -50)
    tamanho = random.choice(["pequeno", "medio", "grande"])
    asteroides.append([x, y, tamanho])

# pontuação
pontos = 0

def desenhar_nave(x, y):
    tela.blit(imagem_nave, (x, y))

def desenhar_asteroide(x, y, tamanho):
    imagem = imagens_asteroides[tamanho]
    dimensao = tamanhos_asteroides[tamanho]["dimensao"]
    tela.blit(imagem, (x - dimensao[0] // 2, y - dimensao[1] // 2))

def desenhar_tiro(x, y):
    tela.blit(imagem_tiro, (x, y))

def mostrar_texto(texto, x, y):
    img = fonte.render(texto, True, BRANCO)
    tela.blit(img, (x, y))

def game_over():
    tela.fill(PRETO)
    mostrar_texto("GAME OVER", largura // 2 - 100, altura // 2 - 30)
    mostrar_texto(f"Pontos: {pontos}", largura // 2 - 70, altura // 2 + 10)
    pygame.display.update()
    pygame.time.wait(3000)
    main()

def main():
    global nave_x, tiros, asteroides, pontos

    # resetar o jogo
    nave_x = largura // 2 - nave_largura // 2
    tiros = []
    asteroides = [
        [random.randint(0, largura - 70), random.randint(-600, -50), random.choice(["pequeno", "medio", "grande"])]
        for _ in range(5)
    ]
    pontos = 0

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        tela.blit(imagem_fundo, (0, 0))  # Desenha o fundo antes dos outros elementos

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # controles
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and nave_x > 0:
            nave_x -= velocidade_nave
        if teclas[pygame.K_RIGHT] and nave_x < largura - nave_largura:
            nave_x += velocidade_nave
        if teclas[pygame.K_SPACE]:
            if len(tiros) <= max_tiros:
                if pontos < 25:
                    tiros.append([nave_x + nave_largura // 2 - 2, nave_y - nave_altura])
                elif pontos < 50:
                    tiros.append([nave_x + 5, nave_y - nave_altura])
                    tiros.append([nave_x + nave_largura - 10, nave_y - nave_altura])
                else:
                    tiros.append([nave_x + nave_largura // 2 - 2, nave_y - nave_altura])
                    tiros.append([nave_x + 5, nave_y - nave_altura])
                    tiros.append([nave_x + nave_largura - 10, nave_y - nave_altura])

        # upgrade tiros
        for tiro in tiros[:]:
            tiro[1] -= velocidade_tiro
            if tiro[1] < 0:
                tiros.remove(tiro)

        # upgrade asteroides
        for asteroide in asteroides:
            asteroide[1] += velocidade_asteroide
            dimensao = tamanhos_asteroides[asteroide[2]]["dimensao"]
            if asteroide[1] > altura:
                asteroide[1] = random.randint(-100, -50)
                asteroide[0] = random.randint(0, largura - dimensao[0])
                asteroide[2] = random.choice(["pequeno", "medio", "grande"])

        # colisões tiro e asteroide
        for tiro in tiros[:]:
            for asteroide in asteroides[:]:
                raio = tamanhos_asteroides[asteroide[2]]["raio_colisao"]
                distancia = ((tiro[0] - asteroide[0]) ** 2 + (tiro[1] - asteroide[1]) ** 2) ** 0.5
                if distancia < raio:
                    try:
                        tiros.remove(tiro)
                        asteroides.remove(asteroide)
                        pontos += 1
                        tamanho_novo = random.choice(["pequeno", "medio", "grande"])
                        asteroides.append([random.randint(0, largura - tamanhos_asteroides[tamanho_novo]["dimensao"][0]), random.randint(-600, -50), tamanho_novo])
                    except:
                        pass

        # colisões nave e asteroide
        for asteroide in asteroides:
            raio = tamanhos_asteroides[asteroide[2]]["raio_colisao"] + 10
            distancia = ((nave_x + nave_largura // 2 - asteroide[0]) ** 2 + (nave_y - asteroide[1]) ** 2) ** 0.5
            if distancia < raio:
                game_over()

        # desenhar objetos
        desenhar_nave(nave_x, nave_y)
        for asteroide in asteroides:
            desenhar_asteroide(asteroide[0], asteroide[1], asteroide[2])
        for tiro in tiros:
            desenhar_tiro(tiro[0], tiro[1])

        mostrar_texto(f'Pontos: {pontos}', 10, 10)

        pygame.display.update()

if __name__ == '__main__':
    main()