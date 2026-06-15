import pygame
import math


def run():
    pygame.init()


    HEIGHT = 600
    WIDTH = 800

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("Belajar Bola Berputar")

    radius = 25

    x = -25
    y = HEIGHT - radius

    running = True

    velocity_x = 200
    angle = 0

    while running:
        dt = clock.tick(120) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        # update posisi roda
        x += velocity_x * dt

        # update rotasi roda
        angle += (velocity_x / radius) * dt

        # kalau keluar kanan, balik ke kiri
        if x - radius > WIDTH:
            print("pre:", x)
            x = -radius
            print("after:", x)

        # titik ujung garis penanda roda
        line_end_x = x + math.cos(angle) * radius
        line_end_y = y + math.sin(angle) * radius

        # gambar
        screen.fill((30, 30, 30))

        # lantai
        pygame.draw.line(screen, (180, 180, 180), (0, y + radius), (WIDTH, y + radius), 2)

        # roda
        pygame.draw.circle(screen, (0, 150, 255), (int(x), int(y)), radius, 4)

        # garis penanda rotasi
        pygame.draw.line(
            screen,
            (255, 80, 80),
            (int(x), int(y)),
            (int(line_end_x), int(line_end_y)),
            5
        )

        pygame.display.flip()

    pygame.quit()


        

        



