# Example file showing a circle moving on screen
import pygame, math
from ball import Ball
import pygame
from collisions import check_collision_ball_rect, get_closest_point_and_distance_to_the_platform, get_closest_platform_data,get_distance_to_platforms

GRAVITY = 1

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

y_acc = 0 # y axis acceleration

ball = Ball(circle_radius, "red", player_pos)
rect_floor = pygame.Rect(0, screen.get_height() * 0.73, screen.get_width(), 20)
rect_platform1 = pygame.Rect(screen.get_width() * 0.55, PLATFORM_1_Y, 150, 50)
rect_platform2 = pygame.Rect(screen.get_width() * 0.70, PLATFORM_2_Y, 100, 50)
rect_platform3 = pygame.Rect(screen.get_width() * 0.88, PLATFORM_3_Y, 50, 5)
platforms = [rect_floor, rect_platform1,rect_platform2,rect_platform3]

while running:

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        
        # Handle movement
        if keys[pygame.K_a]:  # Move left
            ball.player_pos.x -= 5

        elif keys[pygame.K_d]:  # Move right
            ball.player_pos.x += 5
            
     
        
        collision_top = False
        for i, platform in enumerate(platforms):
            collision = check_collision_ball_rect(ball, platform)
            if collision:
                if collision["top"]:
                    print("Collision top")
                    collision_top = True
                    y_acc = 0
                    GRAVITY = 0
                    if keys[pygame.K_w]:
                        y_acc = 20
                    ball.player_pos.y = platform.top - ball.radius - y_acc
                if collision["bottom"]:
                    y_acc = 0
                    ball.player_pos.y = platform.bottom + ball.radius
                if collision["left"] and keys[pygame.K_a] == 1:
                    ball.player_pos.x = platform.left - ball.radius
                    x_velocity = 0
                if collision["right"] and keys[pygame.K_d] == 0:
                    ball.player_pos.x = platform.right + ball.radius
                    x_velocity = 0

        if y_acc < 0 or not collision_top:
            GRAVITY = 1
            y_acc += 1
            
        
        ball.player_pos.y += GRAVITY + y_acc    
        


        # Apply gravity
        

        screen.fill("purple")
        pygame.draw.circle(screen, "red", ball.player_pos, 40)
        pygame.draw.rect(screen, "green", rect_floor)
        pygame.draw.rect(screen, "blue", rect_platform1)
        pygame.draw.rect(screen, "blue", rect_platform2)
        pygame.draw.rect(screen, "blue", rect_platform3)
        # flip() the display to put your work on screen
        pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
        dt = clock.tick(60) / 1000

pygame.quit()