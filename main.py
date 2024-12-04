import pygame, sys
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Project #3')

class vec_2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, vec):
        return vec_2d(self.x + vec.x, self.y + vec.y)
    
    def sub(self, vec):
        return vec_2d(self.x - vec.x, self.y - vec.y)
    
    def mult(self, num):
        return vec_2d(self.x * num, self.y * num)
    
    def abs(self):
        return ((self.x ** 2 + self.y ** 2) ** (1 / 2))
    
    def dot(self, vec):
        return self.x * vec.x + self.y * vec.y

class Circle:
    def __init__(self, px, py, vx, vy, static):
        self.position_x = px
        self.position_y = py
        self.velocity_x = vx
        self.velocity_y = vy
        self.static = static

class Line:
    def __init__(self, start_x, start_y, end_x, end_y):
        self.start_position_x = start_x
        self.start_position_y = start_y
        self.end_position_x = end_x
        self.end_position_y = end_y

mCircle1 = Circle(300, 200, 0, 0, True)
mCircle2 = Circle(350, 200, 0, 0, True)
mCircle3 = Circle(400, 200, 0, 0, True)
mCircle4 = Circle(330, 230, 0, 0, True)
# mCircle5 = Circle(370, 230, 0, 0, True)
# mCircle6 = Circle(350, 260, 0, 0, True)
# mCircle7 = Circle(350, 400, 0, -30, True)
circles = []

circles.append(mCircle1)
circles.append(mCircle2)
circles.append(mCircle3)
# circles.append(mCircle4)
# circles.append(mCircle5)
# circles.append(mCircle6)
# circles.append(mCircle7)

mLine1 = Line(200, 100, 200, 500)
mLine2 = Line(200, 500, 600, 500)
mLine3 = Line(600, 500, 600, 100)
mLine4 = Line(600, 100, 200, 100)
lines = []

mLine5 = Line(350, 100, 350, 120)
mLine6 = Line(450, 100, 450, 120)
mLine7 = Line(350, 120, 450, 120)

mLine8 = Line(350, 500, 350, 480)
mLine9 = Line(450, 500, 450, 480)
mLine10 = Line(350, 480, 450, 480)

lines.append(mLine1)
lines.append(mLine2)
lines.append(mLine3)
lines.append(mLine4)

collisions = []

click = False

screen.fill((255, 255, 255))

finish = False
while not finish:
    for event in pygame.event.get():
        if event.type == QUIT:
            finish = True

    for circle in circles:
        circle.velocity_x *= 1.0
        circle.position_x += circle.velocity_x

        circle.velocity_y *= 1.0
        circle.position_y += circle.velocity_y

    if pygame.mouse.get_pressed()[0]:
        for circle in circles:
            x = pygame.mouse.get_pos()[0] - circle.position_x
            y = pygame.mouse.get_pos()[1] - circle.position_y

            if x > -15 and x < 15 and y > -15 and y < 15:
                circle.static = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:  # A 키를 누르면 왼쪽으로 이동
        mCircle2.velocity_x -= 0.2
    if keys[pygame.K_d]:  # D 키를 누르면 오른쪽으로 이동
        mCircle2.velocity_x += 0.2
    if keys[pygame.K_w]:  # W 키를 누르면 위로 이동
        mCircle2.velocity_y -= 0.1
    if keys[pygame.K_s]:  # S 키를 누르면 아래로 이동
        mCircle2.velocity_y += 0.1


    for circle in circles:
        if not circle.static:
            if pygame.mouse.get_pressed()[0]:
                circle.velocity_x = pygame.mouse.get_pos()[0] - circle.position_x
                circle.velocity_y = pygame.mouse.get_pos()[1] - circle.position_y
                circle.static = True


    for circle1 in circles:
        for circle2 in circles:
            pos_vec = vec_2d(circle1.position_x - circle2.position_x, circle1.position_y - circle2.position_y)
            overlap = pos_vec.abs() - 30

            if circle1 == circle2:
                continue

            else:
                if overlap <= 0:

                    collisions.append([circle1, circle2])

                    if pos_vec.abs() == 0:
                        circle1.position_x += 1
                        circle1.position_y += 1

                    else:
                        circle1.position_x -= pos_vec.mult(overlap / pos_vec.abs() * 0.5).x
                        circle1.position_y -= pos_vec.mult(overlap / pos_vec.abs() * 0.5).y
                        circle2.position_x += pos_vec.mult(overlap / pos_vec.abs() * 0.5).x
                        circle2.position_y += pos_vec.mult(overlap / pos_vec.abs() * 0.5).y

    
    for circle in circles:
        if circle == mCircle1:
            for line in lines:
                line_ = vec_2d(line.end_position_x - line.start_position_x, line.end_position_y - line.start_position_y)
                pos_vec = vec_2d(circle.position_x - line.start_position_x, circle.position_y - line.start_position_y)
                pos_norm = line_.mult(1 / line_.abs())
                dot = line_.dot(pos_vec) / line_.abs()
                project = pos_norm.mult(dot)
                norm = pos_vec.sub(project)
                overlap = norm.abs() - 16
                abs = line_.abs()

                if dot > 0 and dot < abs:
                    if overlap <= 0:
                        mCircle = Circle(line.start_position_x + project.x, line.start_position_y + project.y, -circle.velocity_x, -circle.velocity_y, False)
                        collisions.append([circle, mCircle])

                        if norm.abs() == 0:
                            circle.position_x += 1
                            circle.position_y += 1

                        else:
                            circle.position_x -= norm.mult(overlap / norm.abs()).x
                            circle.position_y -= norm.mult(overlap / norm.abs()).y
        else:
            for line in lines:
                line_ = vec_2d(line.end_position_x - line.start_position_x, line.end_position_y - line.start_position_y)
                pos_vec = vec_2d(circle.position_x - line.start_position_x, circle.position_y - line.start_position_y)
                pos_norm = line_.mult(1 / line_.abs())
                dot = line_.dot(pos_vec) / line_.abs()
                project = pos_norm.mult(dot)
                norm = pos_vec.sub(project)
                overlap = norm.abs() - 16
                abs = line_.abs()

                if dot > 0 and dot < abs:
                    if overlap <= 0:
                        if norm.abs() == 0:
                            circle.position_x += 1
                            circle.position_y += 1

                        else:
                            circle.position_x -= norm.mult(overlap / norm.abs()).x
                            circle.position_y -= norm.mult(overlap / norm.abs()).y


    for collision in collisions:
        pos_vec = vec_2d(collision[0].position_x - collision[1].position_x, collision[0].position_y - collision[1].position_y)

        if pos_vec.abs() == 0:
            Normal = pos_vec.mult(1 / 1E-5)

        else:
            Normal = pos_vec.mult(1 / pos_vec.abs())

        dif_x = collision[0].velocity_x - collision[1].velocity_x
        dif_y = collision[0].velocity_y - collision[1].velocity_y
        p = Normal.x * dif_x + Normal.y * dif_y

        collision[0].velocity_x = collision[0].velocity_x - p * Normal.x
        collision[0].velocity_y = collision[0].velocity_y - p * Normal.y

        collision[1].velocity_x = collision[1].velocity_x + p * Normal.x
        collision[1].velocity_y = collision[1].velocity_y + p * Normal.y

    collisions.clear()

    screen.fill((255, 255, 255))

    for circle in circles:
        if not circle.static:
            pygame.draw.circle(screen, (255, 255, 0), (circle.position_x, circle.position_y), 15)

        else:
            if (circle == mCircle2):
                pygame.draw.circle(screen, (255, 0, 0), (mCircle2.position_x, mCircle2.position_y), 15)
            elif (circle == mCircle3):
                pygame.draw.circle(screen, (0, 255, 0), (mCircle3.position_x, mCircle3.position_y), 15)
            else:
                pygame.draw.circle(screen, (0, 0, 0), (circle.position_x, circle.position_y), 15)
            # pygame.draw.circle(screen, (0, 0, 0), (circle.position_x, circle.position_y), 15)
        
    for line in lines:
        pygame.draw.line(screen, (0, 0, 0), (line.start_position_x, line.start_position_y), (line.end_position_x, line.end_position_y), 1)

    pygame.draw.line(screen, (0, 0, 0), (mLine5.start_position_x, mLine5.start_position_y), (mLine5.end_position_x, mLine5.end_position_y), 1)
    pygame.draw.line(screen, (0, 0, 0), (mLine6.start_position_x, mLine6.start_position_y), (mLine6.end_position_x, mLine6.end_position_y), 1)
    pygame.draw.line(screen, (0, 0, 0), (mLine7.start_position_x, mLine7.start_position_y), (mLine7.end_position_x, mLine7.end_position_y), 1)

    pygame.draw.line(screen, (0, 0, 0), (mLine8.start_position_x, mLine8.start_position_y), (mLine8.end_position_x, mLine8.end_position_y), 1)
    pygame.draw.line(screen, (0, 0, 0), (mLine9.start_position_x, mLine9.start_position_y), (mLine9.end_position_x, mLine9.end_position_y), 1)
    pygame.draw.line(screen, (0, 0, 0), (mLine10.start_position_x, mLine10.start_position_y), (mLine10.end_position_x, mLine10.end_position_y), 1)

    pygame.display.update()
    pygame.time.Clock().tick(120)
pygame.quit()
sys.exit()
