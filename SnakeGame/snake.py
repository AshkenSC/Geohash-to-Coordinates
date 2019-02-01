import pygame

def redrawWindow(surface):
    global rows, width
    surface.fill((0, 0, 0))
    drawGrid(width, rows, surface)
    pygame.display.update()

def drawGrid(width, rows, surface):
    '''绘制游戏背景方格'''
    sizeBetween = width // rows
    x = 0
    y = 0

    for l in range(rows):
        x += sizeBetween
        y += sizeBetween
        # 绘制一条纵向线和横向线
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, width))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (width, y))

def main():
    global width, rows
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    flag = True

    clock = pygame.time.Clock()

    # 游戏主循环
    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        redrawWindow(win)

main()