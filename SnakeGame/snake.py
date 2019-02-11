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

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.headpos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.headpos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.headpos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.headpos[:]] = [self.dirnx, self.dirny]

        for index, cube in enumerate(self.body):
            pos = cube.pos[:]
            if pos in self.turns:
                turn = self.turns[p]
                cube.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(pos)
            else:
                if cube.dirnx == -1 and cube.pos[0] <= 0:
                    cube.pos = (cube.rows - 1, cube.pos[1])
                elif cube.dirnx == 1 and cube.pos[0] >= cube.rows - 1:
                    cube.pos = (0, cube.pos[1])
                elif cube.dirny == 1 and cube.pos[1] >= cube.rows - 1:
                    cube.pos = (cube.pos[0], 0)
                elif cube.dirny == -1 and cube.pos[1] <= 0:
                    cube.pos = (cube.pos[0], cube.rows - 1)
                else:
                    c.move(c.dirnx, c.dirny)


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
        # 每次循环绘制一条纵向线和一条横向线
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