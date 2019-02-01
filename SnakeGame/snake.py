import pygame

def main():
    width = 500
    height = 500
    rows = 20
    win = pygame.display.set_mode((width, height))
    flag = True

    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        redrawWindow(win)

def redrawWindow(win):
    win.fill((0, 0, 0))
    drawGrid(surface)
    pygame.display.update()