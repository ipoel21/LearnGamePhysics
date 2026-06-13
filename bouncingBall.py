import pygame

#version myself
def runV1():
    pygame.init()

    WIDTH = 800
    HEIGHT = 600

    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption("Belajar Grafitasi")

    clock = pygame.time.Clock()

    x = 400
    y = 100

    velocity_y = 0

    grafity = 980

    radius = 25

    jump_power = -900

    floor_y = HEIGHT - 25

    running = True

    loop_jump = True

    while running:
        dt = clock.tick(165) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and floor_y == y:
                    jump_power = -900
                    velocity_y = jump_power
                    loop_jump = True

        pre_y = y
        pre_v_y = velocity_y
        velocity_y += grafity * dt
        y += velocity_y * dt

        if y >= floor_y:
            velocity_y = 0
            y = floor_y 

            if jump_power >= -1:
                loop_jump = False

            if loop_jump:
                jump_power *= 0.8
                velocity_y = jump_power
                


        screen.fill((30,30,30)) 
        pygame.draw.circle(screen,(0,150,255), (int(x), int(y)), radius)
        pygame.display.flip()

    pygame.quit()

#Version improve
def runV2():
    pygame.init()

    WIDTH = 800
    HEIGHT = 600

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Belajar Gravitasi dan Bounce")

    clock = pygame.time.Clock()

    x = 400
    y = 100

    radius = 25

    velocity_y = 0
    gravity = 980

    jump_power = -900
    bounce = 0.8

    floor_y = HEIGHT - radius

    running = True

    while running:
        dt = clock.tick(165) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and y >= floor_y:
                    velocity_y = jump_power

        # update fisika
        velocity_y += gravity * dt
        y += velocity_y * dt

        # collision dengan lantai
        if y >= floor_y:
            y = floor_y

            # kalau jatuhnya masih cukup cepat, pantulkan
            if abs(velocity_y) > 50:
                print("Previus:",velocity_y, abs(velocity_y))
                velocity_y = -velocity_y * bounce
                print("After: ",velocity_y, abs(velocity_y))
            else:
                velocity_y = 0

        # gambar
        screen.fill((30, 30, 30))

        pygame.draw.line(
            screen,
            (200, 200, 200),
            (0, floor_y + radius),
            (WIDTH, floor_y + radius),
            2
        )

        pygame.draw.circle(
            screen,
            (0, 150, 255),
            (int(x), int(y)),
            radius
        )

        pygame.display.flip()

    pygame.quit()