import pygame

class Snake(object):
   body = []
   turns = {}

   def __init__(self, color, pos):
       self.color = color
       self.head = cube(pos)
       self.body.append(self.head)
       self.dirnx = 0
       self.dirny = 1

   def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

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
        # 每个循环绘制一条纵向线和一条横向线
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