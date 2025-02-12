import pygame
from ball import Ball
import math

def check_collision_ball_rect(ball : Ball, rect : pygame.Rect):
        x = ball._player_pos[0]
        y = ball._player_pos[1]
        closest_x = 0
        closest_y = 0

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

def get_closest_point_of_the_platform(ball, rect):
    x = ball._player_pos.x
    y = ball._player_pos.y

    closest_x = 0
    closest_y = 0

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

    return closest_x, closest_y, distance

def get_closest_platform_data(ball, platforms):

    nearest_platform_x, nearest_platform_y, min_distance = get_closest_point_of_the_platform(ball, platforms[0])
    
    for platform in platforms[1:]:
        x, y, distance = get_closest_point_of_the_platform(ball, platform)
        if( distance < min_distance):
            nearest_platform_x = x
            nearest_platform_y = y
            min_distance = distance
    return nearest_platform_x, nearest_platform_y, distance

     
