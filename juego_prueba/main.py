import pygame
import random
import sys


pygame.init()


ANCHO, ALTO = 1000, 800
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego para prueba con Pygame")


BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)

FPS = 60
RELOJ = pygame.time.Clock()


class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(VERDE)
        self.rect = self.image.get_rect()
        self.rect.center = (ANCHO // 2, ALTO - 50)
        self.velocidad = 5

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT] and self.rect.right < ANCHO:
            self.rect.x += self.velocidad

class Enemigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(ROJO)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ANCHO - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.velocidad = random.randint(3, 8)

    def update(self):
        self.rect.y += self.velocidad
        if self.rect.top > ALTO:
            self.rect.x = random.randint(0, ANCHO - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.velocidad = random.randint(3, 8)


def mostrar_menu():
    PANTALLA.fill(NEGRO)
    fuente = pygame.font.Font(None, 74)
    texto = fuente.render("Presiona ENTER para comenzar el juego", True, BLANCO)
    PANTALLA.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - texto.get_height() // 2))
    pygame.display.flip()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    esperando = False

def mostrar_pausa():
    PANTALLA.fill(NEGRO)
    fuente = pygame.font.Font(None, 60)
    texto = fuente.render("Juego Pausado. Presiona P para continuar", True, BLANCO)
    PANTALLA.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - texto.get_height() // 2))
    pygame.display.flip()

    pausado = True
    while pausado:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p:
                    pausado = False

def mostrar_fin_juego(puntaje):
    PANTALLA.fill(NEGRO)
    fuente = pygame.font.Font(None, 65)
    texto = fuente.render(f"Juego Terminado. Puntuación: {puntaje}", True, BLANCO)
    PANTALLA.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - texto.get_height() // 2))
    fuente_pequeña = pygame.font.Font(None, 50)
    texto_reiniciar = fuente_pequeña.render("R para reiniciar o Q para salir", True, BLANCO)
    PANTALLA.blit(texto_reiniciar, (ANCHO // 2 - texto_reiniciar.get_width() // 2, ALTO // 2 + 100))
    pygame.display.flip()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    esperando = False
                    juego()
                if evento.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def juego():
    jugador = Jugador()
    enemigos = pygame.sprite.Group()

    for _ in range(5):
        enemigo = Enemigo()
        enemigos.add(enemigo)

    todos_los_sprites = pygame.sprite.Group()
    todos_los_sprites.add(jugador)
    todos_los_sprites.add(enemigos)

    puntaje = 0
    start_ticks = pygame.time.get_ticks()

    jugando = True
    while jugando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jugando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p:
                    mostrar_pausa()

        todos_los_sprites.update()

        segundos = (pygame.time.get_ticks() - start_ticks) // 1000
        puntaje = segundos

        if pygame.sprite.spritecollide(jugador, enemigos, False):
            jugando = False
            mostrar_fin_juego(puntaje)

        PANTALLA.fill(BLANCO)
        todos_los_sprites.draw(PANTALLA)

        fuente_puntaje = pygame.font.Font(None, 36)
        texto_puntaje = fuente_puntaje.render(f"Puntaje: {puntaje}", True, NEGRO)
        PANTALLA.blit(texto_puntaje, (10, 10))

        pygame.display.flip()

        RELOJ.tick(FPS)

def main():
    mostrar_menu()
    juego()

if __name__ == "__main__":
    main()
    pygame.quit()
