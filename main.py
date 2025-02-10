# Example file showing a circle moving on screen
import pygame, math # type: ignore
from ball import Ball

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0.016

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
circle_radius = 40



gravity_speed = 10
y_acc = 0 # y axis acceleration
jumping = False



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

    print(f'Dist x: {distance_x} Dist y: {distance_y}')
    if distance < ball.radius:
        collision_sides = {
            "top": ball.player_pos.y < rect.top and abs(ball.player_pos.y + ball.radius - rect.top) < 300,
            "bottom": ball.player_pos.y > rect.bottom and abs(ball.player_pos.y - ball.radius - rect.bottom) < 300,
            "left": ball.player_pos.x < rect.left and abs(ball.player_pos.x + ball.radius - rect.left) < 300,
            "right": ball.player_pos.x > rect.right and abs(ball.player_pos.x - ball.radius - rect.right) < 300,
        }
        return collision_sides
    return None

        
    

ball = Ball(circle_radius, "red", player_pos)
rect_floor = pygame.Rect(0, screen.get_height() * 0.73, screen.get_width(), 20)
rect_platform1 = pygame.Rect(screen.get_width()* 0.55, screen.get_height() * 0.60, 100, 40)
rect_platform2 = pygame.Rect(screen.get_width()* 0.62, screen.get_height() * 0.50, 120, 40)
rect_platform3 = pygame.Rect(screen.get_width()* 0.70, screen.get_height() * 0.40, 150, 40)

while running:
     
    
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    

    platforms = [rect_platform1, rect_platform2, rect_platform3]
    
    
    # print(f"circle x:{ball.player_pos[0]}, circle y: {ball.player_pos[1]}, y_acc: {y_acc}")

    # Draw elements
    # print(f'Ball x position predraw collision check: {ball.player_pos.x}')
    pygame.draw.circle(screen, "red", ball.player_pos, ball.radius)
    pygame.draw.rect(screen, "green", rect_floor)
    pygame.draw.rect(screen, "blue", rect_platform1)
    pygame.draw.rect(screen, "blue", rect_platform2)
    pygame.draw.rect(screen, "blue", rect_platform3)

    keys = pygame.key.get_pressed()
    # the player cannot use downward key, the gravity is working
    # if (player_pos[1]+circle_radius <= rect_floor.top-rect_floor.height ):
    #     if keys[pygame.K_s]:
    #         player_pos.y += 300 * dt
    
    # IF KEY PRESSED AND COLLISION HAPPENING, DISABLE MOVEMENT INTO THAT DIRECTION

    for platform in platforms:

        collision = check_collision_rect_ball(ball, rect_platform1)
        if collision:
            if collision["top"]:
                print("COLLISION top")
                gravity_speed = 0
                y_acc = 0
                ball.player_pos.y = platform.top - ball.radius

            if collision["bottom"]:
                print("COLLISION bottom")
                y_acc = 0
                ball.player_pos.y = platform.bottom + ball.radius

            if collision["left"]:
                print("COLLISION left")
                ball.player_pos.x = platform.left - ball.radius
                print(f'Ball x position post collision check: {ball.player_pos.x}')

            if collision["right"]:
                print("COLLISION right")
                ball.player_pos.x = platform.right + ball.radius
        else:
            gravity_speed = 10

            

    

    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt
    
    if (player_pos[1]+circle_radius <= rect_floor.top-rect_floor.height ):
         player_pos.y += gravity_speed * 20 * dt

    

    if(y_acc == 0 and player_pos[1]+circle_radius >= rect_floor.top-rect_floor.height):
        if keys[pygame.K_w]:
            print("w pressed")
            y_acc = 1200
            gravity_speed = 0
    elif(y_acc > 0):
        player_pos.y -= y_acc * dt
        y_acc -= 50
        gravity_speed += 2
           # player_pos.y -= 500 * dt

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()