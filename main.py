# Example file showing a circle moving on screen
import pygame # type: ignore

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0.016

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
circle_radius = 20

gravity_speed = 10
y_acc = 0 # y axis acceleration
jumping = False

while running:
     
    
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    rect_floor = pygame.Rect(0, screen.get_height() * 0.73, screen.get_width(), 20)
    print(f"circle x:{player_pos[0]}, circle y: {player_pos[1]}, y_acc: {y_acc}")
    pygame.draw.circle(screen, "red", player_pos, 40)
    pygame.draw.rect(screen, "green", rect_floor)

    keys = pygame.key.get_pressed()
    # the player cannot use downward key, the gravity is working
    # if (player_pos[1]+circle_radius <= rect_floor.top-rect_floor.height ):
    #     if keys[pygame.K_s]:
    #         player_pos.y += 300 * dt
    
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