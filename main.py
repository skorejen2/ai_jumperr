# Example file showing a circle moving on screen
import pygame, math
from ball import Ball

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0.016

PLATFORM_1_Y = 470  # Example y-coordinates
PLATFORM_2_Y = 320
PLATFORM_3_Y = 250  # Highest platform (goal)

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
circle_radius = 40

gravity_speed = 10
y_acc = 0 # y axis acceleration

def check_collision_rect_ball(ball : Ball, rect : pygame.Rect):
    x = ball._player_pos[0]
    y = ball._player_pos[1]
    closest_x = 0
    closest_y = 0
    direction = 0

    if (x < rect.left and x < rect.right):
        closest_x = rect.left
    elif(x > rect.left and x > rect.right):
        closest_x = rect.right
    else:
        closest_x = x

    if (y < rect.top and y < rect.bottom):
        closest_y = rect.top
    elif(y > rect.top and y > rect.bottom):
        closest_y = rect.bottom
    else:
        closest_y = y
    
    # count distance from closest point
    # from pitagoraes
    distance_x = abs(x - closest_x)
    distance_y = abs(y - closest_y)

    distance = math.sqrt(distance_x**2 + distance_y**2)

    # print(f'Dist x: {distance_x} Dist y: {distance_y}')
    if distance < ball.radius:
        collision_sides = {
            "top": ball.player_pos.y < rect.top and abs(ball.player_pos.y + ball.radius - rect.top) < 300,
            "bottom": ball.player_pos.y > rect.bottom and abs(ball.player_pos.y - ball.radius - rect.bottom) < 300,
            "left": ball.player_pos.x < rect.left and abs(ball.player_pos.x + ball.radius - rect.left) < 5,
            "right": ball.player_pos.x > rect.right and abs(ball.player_pos.x - ball.radius - rect.right) < 5,
        }
        return collision_sides
    return None

ball = Ball(circle_radius, "red", player_pos)
rect_floor = pygame.Rect(0, screen.get_height() * 0.73, screen.get_width(), 20)
rect_platform1 = pygame.Rect(screen.get_width() * 0.55, PLATFORM_1_Y, 150, 50)
rect_platform2 = pygame.Rect(screen.get_width() * 0.70, PLATFORM_2_Y, 100, 50)
rect_platform3 = pygame.Rect(screen.get_width() * 0.88, PLATFORM_3_Y, 50, 5)
platforms = [rect_floor, rect_platform1,rect_platform2,rect_platform3]

while running:
     
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



    keys = pygame.key.get_pressed()

    # object collision logic

    collision = False
    for platform in platforms:

        collision = check_collision_rect_ball(ball, platform)
        if collision:
            if collision["top"]:
                gravity_speed = 0
                y_acc = 0
                if not keys[pygame.K_w]:
                    ball.player_pos.y = platform.top - ball.radius
                else:
                    y_acc = 1000
            if collision["bottom"]:
                y_acc = 0
                ball.player_pos.y = platform.bottom + ball.radius

            if collision["left"]:
                ball.player_pos.x = platform.left - ball.radius

            if collision["right"]:
                ball.player_pos.x = platform.right + ball.radius
        else:
            gravity_speed = 10
    

    if keys[pygame.K_a]:
        ball.player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        ball.player_pos.x += 300 * dt
    
    if (ball.player_pos.y + ball.radius <= rect_floor.top):
        ball.player_pos.y += gravity_speed * 20 * dt


    if(y_acc > 0 or not collision):
        print(y_acc)
        ball.player_pos.y -= y_acc * dt
        y_acc -= 40
        gravity_speed += 2
        

           # player_pos.y -= 500 * dt

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")
    pygame.draw.circle(screen, "red", player_pos, 40)
    pygame.draw.rect(screen, "green", rect_floor)
    pygame.draw.rect(screen, "blue", rect_platform1)
    pygame.draw.rect(screen, "blue", rect_platform2)
    pygame.draw.rect(screen, "blue", rect_platform3)
    
    # Prevent ball from going off-screen
    if ball.player_pos.x - ball.radius < 0:
        ball.player_pos.x = ball.radius
    if ball.player_pos.x + ball.radius > screen.get_width():
        ball.player_pos.x = screen.get_width() - ball.radius
    if ball.player_pos.y + ball.radius > screen.get_height():
        ball.player_pos.y = screen.get_height() - ball.radius
        gravity_speed = 0
    if ball.player_pos.y - ball.radius < 0:
        ball.player_pos.y = ball.radius

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()