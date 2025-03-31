import pygame
import time


fps = 120  # fps
G = 6.67 / 10 ** 11  # gravity constant
k = 1000000  # метров в одном пикселе
mouse_x, mouse_y = 0, 0  # start mouse point
time_speed = 10000  # coeeficient of acceleration the program
# coeeficient of acceleration greater then  10 ^ 5, the very big errors could be occured

pygame.init()
screen = pygame.display.set_mode((1500, 800))
pygame.display.set_caption("Planetary acceleration")
style = pygame.font.SysFont("arial", 36)
render_fps = style.render('fps ' + str(fps), True, 'blue')
render_time_speed = style.render('acceleration: ' + str(time_speed), True, 'blue')


class Planet:
    def __init__(self, x, y, r, m, color):
        self.x = x  # x cord
        self.y = y  # y cord
        self.r = r  # planet radius
        self.m = m  # planet weight
        self.color = color  # planet color
        self.speed = [0, 0]  # planet speed
        self.f = [0, 0]  # the power which is working with the planet
        self.status = True  # planet present or not
        self.trace_count = 0  # not very often show planet traectory fps
        self.trace = []  # point of the planet traectory

    def update_coordinates(self):  # update speed, cords and traectory
        self.speed[0] += (self.f[0] / self.m) * time_speed ** 2 / fps ** 2
        self.speed[1] += (self.f[1] / self.m) * time_speed ** 2 / fps ** 2

        self.x += self.speed[0]
        self.y += self.speed[1]

        self.trace_count += (self.speed[0] ** 2 + self.speed[1] ** 2) ** 0.5
        if self.trace_count / k >= 7:  # if the number less then traectory will be bigger
            self.trace_count = 0
            self.trace.append((self.x, self.y))
        if len(self.trace) > 1000:  # not slow down fps, when many
            self.trace.pop(0)

    def draw(self):  # show all planets and traektories
        pygame.draw.circle(screen, self.color, ((self.x - mouse_x) / k, (self.y - mouse_y) / k), self.r / k)
        for i in self.trace:
            pygame.draw.circle(screen, self.color, ((i[0] - mouse_x) / k, (i[1] - mouse_y) / k), 1)


def update_forces(planets, collides):
    for i in range(len(planets)):
        for j in range(i + 1, len(planets)):
            dif_x = planets[j].x - planets[i].x  # diff between two planets by x
            dif_y = planets[j].y - planets[i].y  # diff by two planets by y
            d = (dif_x ** 2 + dif_y ** 2) ** 0.5  # pifagor distance between planets
            f = G * planets[i].m * planets[j].m / d ** 2  # the power between two planets

            planets[i].f[0] += dif_x * f / d  # update powers
            planets[i].f[1] += dif_y * f / d

            planets[j].f[0] -= dif_x * f / d
            planets[j].f[1] -= dif_y * f / d

            if planets[i].r + planets[j].r > d:  # find what planets are crashed each other
                collides.append((i, j))


def remove_collides(planets, collides):
    for i in collides:
        p1 = planets[i[0]]
        p2 = planets[i[1]]
        if p1.status and p2.status:  # if both planets present
            if p1.m > p2.m:  # which planet is bigger then it win
                new_planet = Planet(p1.x, p1.y, p1.r + p2.r, p1.m + p2.m, p1.color)
            else:
                new_planet = Planet(p2.x, p2.y, p1.r + p2.r, p1.m + p2.m, p2.color)

            new_planet.speed = [(p1.m * p1.speed[0] + p2.m * p2.speed[0]) / (p1.m + p2.m),
                                (p1.m * p1.speed[1] + p2.m * p2.speed[1]) / (p1.m + p2.m)]

            planets.append(new_planet)
            p1.status = p2.status = 0


planets = []

# # Sun
# p = Planet(0, 0, 696_000_000, 1.9891 * 10 ** 30, 'orange')
# planets.append(p)
#
# for i in range(14, 20):
#     p = Planet((-1) ** i * (i * 10 ** 9 + 10 ** 9), 0, 1, 1, 'green')
#     planets.append(p)
#     planets[i - 13].speed[1] += (-1) ** i * 29273.6 * time_speed / fps
# Earth
p = Planet(-152 * 10 ** 9, 0, 6371000, 5.9722 * 10 ** 24, 'green')
planets.append(p)
planets[0].speed[1] += 29273.6 * time_speed / fps # скорость вокруг солнца

# Moon
p = Planet(-363104000 - 152 * 10 ** 9, 0, 1737100, 7.35 * 10 ** 22, 'grey')
planets.append(p)
planets[1].speed[1] = 1023 * time_speed / fps # скорость вокруг земли
planets[1].speed[1] += 29273.6 * time_speed / fps # скорость вокруг солнца

# Merkury
p = Planet(-69.8 * 10 ** 9, 0, 2439700, 3.33022 * 10 ** 23, "yellow")
planets.append(p)
planets[2].speed[1] += 38000 * time_speed / fps # Скорость вокруг солнца

# Venus
p = Planet(-109 * 10 ** 9, 0, 6051800, 4.8675 * 10 ** 24, "white")
planets.append(p)
planets[3].speed[1] += 34000 * time_speed / fps

# Mars
p = Planet(-249.2 * 10 ** 9, 0, 3390000, 6.4171 * 10 ** 23, "red")
planets.append(p)
planets[4].speed[1] += 23000 * time_speed / fps

# Jupiter
p = Planet(-816.521 * 10 ** 9, 0, 71492000, 1.8986 * 10 ** 27, "brown")
planets.append(p)
planets[5].speed[1] += 12500 * time_speed / fps

# Saturn
p = Planet(-1.51 * 10 ** 12, 0, 60268000, 5.6846 * 10 ** 26, "beige")
planets.append(p)
planets[6].speed[1] += 9100 * time_speed / fps

# Uran
p = Planet(-3 * 10 ** 12, 0, 	25362000, 8.6813 * 10 ** 25, "pink")
planets.append(p)
planets[7].speed[1] += 6300 * time_speed / fps

# Neptune
p = Planet(-4.5 * 10 ** 12, 0, 24622000, 	1.02409 * 10 ** 26, "blue")
planets.append(p)
planets[8].speed[1] += 4950 * time_speed / fps

# Sun
p = Planet(0, 0, 696_000_000, 1.9891 * 10 ** 30, 'orange')
planets.append(p)


tick = 0
tm = time.time()
running = True
while running:
    tick += 1
    if tick == 100:
        tick = 0
        render_fps = style.render("fps:" + str(int(100 / (time.time() - tm))), True, "blue")
        tm = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:  # any mouse button press
            x = event.pos[0]
            y = event.pos[1]
            new_x = mouse_x + x * k
            new_y = mouse_y + y * k

            if event.button == 4:  # mouse wheel up
                k *= 0.85
                mouse_x = new_x - x * k
                mouse_y = new_y - y * k

            if event.button == 5:  # mouse wheel down
                k /= 0.85
                mouse_x = new_x - x * k
                mouse_y = new_y - y * k

            if event.button == 3:  # right mouse button
                planets.append(Planet(new_x, new_y, 6371000, 5.9722 * 10 ** 24, 'blue'))

            if event.button == 2:  # mouse wheel press
                if time_speed >= 100000:
                    time_speed = 1
                    for i in planets:
                        i.speed[0] /= 100000  # less speed planets
                        i.speed[1] /= 100000
                else:
                    time_speed *= 10
                    for i in planets:
                        i.speed[0] *= 10
                        i.speed[1] *= 10

                render_time_speed = style.render('acceleration: ' + str(time_speed), True, 'blue')

        if event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0]:
                mouse_x -= event.rel[0] * k
                mouse_y -= event.rel[1] * k

    collides = []
    update_forces(planets, collides)  # find all colisions

    remove_collides(planets, collides)

    screen.fill("black")  # update black background

    new_planets = []
    for planet in planets:
        if planet.status:  # choose just present planets
            planet.update_coordinates()
            planet.f = [0, 0]
            new_planets.append(planet)
            planet.draw()
    planets = new_planets

    screen.blit(render_fps, (10, 10))  # fps
    screen.blit(render_time_speed, (10, 50))  # acceleration
    pygame.display.update()
pygame.quit()
