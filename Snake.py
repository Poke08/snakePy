import pygame
import sys
import random

class Snake(object):

    def __init__(self):
        self.length = STARTLENGTH
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = (0, 255, 50)

    def get_head_positions(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point
    
    def move(self):
        cur = self.get_head_positions()
        x, y = self.direction
        new = (((cur[0] + (x*GRIDSIZE)) % SCREEN_WIDTH), (cur[1] + (y*GRIDSIZE)) % SCREEN_HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):

        global score, speed

        speed = STARTSPEED
        score = STARTSCORE
        self.length = STARTLENGTH
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])


    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRIDSIZE, GRIDSIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, self.color, r, 1)


    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.turn(UP)
                elif event.key == pygame.K_s:
                    self.turn(DOWN)
                elif event.key == pygame.K_a:
                    self.turn(LEFT)
                elif event.key == pygame.K_d:
                    self.turn(RIGHT)

class Food(object):
    def __init__(self):
        self.position = (0, 0)
        self.color = (random.randint(0, 255), 0, random.randint(0, 255))
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH-1) * GRIDSIZE, random.randint(0, GRID_HEIGHT-1) * GRIDSIZE)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, self.color, r, 1)

def drawGrid(surface):
    for y in range(0, int(GRID_HEIGHT)):
        for x in range(0, int(GRID_WIDTH)):
            r = pygame.Rect((x*GRIDSIZE, y*GRIDSIZE), (GRIDSIZE, GRIDSIZE))
            if (x + y) % 2 == 0:
                pygame.draw.rect(surface, (0, 60, 0), r)
            else:
                pygame.draw.rect(surface, (0, 100, 0), r)



SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

GRIDSIZE = 20
GRID_WIDTH = SCREEN_WIDTH / GRIDSIZE
GRID_HEIGHT = SCREEN_HEIGHT / GRIDSIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
SPEEDCAP = 30
STARTSPEED = 7
STARTLENGTH = 1
NUMFOODS = 5
STARTSCORE = 0
score = STARTSCORE
speed = STARTSPEED

def main():
    pygame.init()

    global score, speed

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)

    snake = Snake()
    foods = [Food() for i in range(NUMFOODS)]

    myfont = pygame.font.SysFont("monospace", 16)
    
    while (True):
        clock.tick(speed)
        snake.handle_keys()
        drawGrid(surface)
        snake.move()

        for food in foods:
            if snake.get_head_positions() == food.position:
                snake.length += 1
                speed += 0.5
                score += 1
                food.randomize_position()
                
        if speed > SPEEDCAP:
            speed = SPEEDCAP
        snake.draw(surface)
        for food in foods:
            food.draw(surface)
        screen.blit(surface, (0, 0))
        text = myfont.render("Score: {0}".format(score), 1, (255, 255, 255))
        text2 = myfont.render("Speed: {0}".format(speed), 1, (255, 255, 255))
        screen.blit(text, (5, 10))
        screen.blit(text2, (200, 10))
        pygame.display.update()
        

main()
