import gymnasium as gym
from gymnasium import spaces
import pygame
import numpy as np
from ball import Ball
from collisions import check_collision_ball_rect, get_closest_point_of_the_platform, get_closest_platform_data

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
GROUND_Y = 520  # Assuming the floor starts at y = 520
PLATFORM_1_Y = 470  # Example y-coordinates
PLATFORM_2_Y = 320
PLATFORM_3_Y = 250  # Highest platform (goal)
BALL_RADIUS = 40

class BallEnv(gym.Env):
    def __init__(self):
        super(BallEnv, self).__init__()

        

        #Init pygame
        pygame.init()
        self.screen = pygame.display.set_mode((1280,720))
        self.clock = pygame.time.Clock()

        # Ball properties
        self.ball = Ball(BALL_RADIUS,"red",pygame.Vector2(self.screen.get_width()/2,self.screen.get_height()/2))
        self.gravity = 10
        self.y_acc = 0
        self.x_velocity = 0

        rect_floor = pygame.Rect(0, GROUND_Y, self.screen.get_width(), 40)
        rect_platform1 = pygame.Rect(self.screen.get_width() * 0.55, PLATFORM_1_Y, 150, 50)
        rect_platform2 = pygame.Rect(self.screen.get_width() * 0.70, PLATFORM_2_Y, 100, 50)
        rect_platform3 = pygame.Rect(self.screen.get_width() * 0.88, PLATFORM_3_Y, 50, 5)
        self.platforms = [rect_floor, rect_platform1,rect_platform2,rect_platform3]

        self._max_dy = 500 # max vertical speed
        self._max_dx = 500 # max horizontal speed

        
        # Define action and observation space
        # Example: Discrete action space (0 or 1) and continuous observation space (array of floats)
        self.action_space = spaces.Discrete(3)  # Three possible actions: left, right, up

        # observation for ball_x, ball_y, dx, dy, dx_platform, dy_platform, distance nearet platform 
        # current localtion of the ball
        # current velocity of the ball
        # current nearest platform location
        # set min and max value for each

        self.observation_space = spaces.Box(
            low = np.array([-200,-100,-500,-1200,0,0,0]), 
            high = np.array([SCREEN_WIDTH, SCREEN_HEIGHT+100, self._max_dx, self._max_dy, SCREEN_WIDTH, SCREEN_HEIGHT, 1500]),
            dtype=np.float32
            )
        
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)  # Ensure proper Gym environment reset behavior
        self.ball.player_pos = pygame.Vector2(self.screen.get_width()/2, self.screen.get_height()/2)
        self.y_acc = 0
        self.x_velocity = 0  # Reset velocity as well
        return self._get_obs(), {}


    # 1 step is represented as 1 fps 
    # hence, when we are running at 60fps ~= 0.016s
    # and running at 300px horizontally per second
    # we get 5px movement per fps
    def step(self, action):
        # Apply action and return the new state, reward, done flag, and additional info
        reward = -0.05
        # Handle movement
        if action == 0:  # Move left
            self.ball.player_pos.x -= 10
            #reward = 0.001
        elif action == 1:  # Move right
            self.ball.player_pos.x += 10
            #reward = 0.001


        

        for i, platform in enumerate(self.platforms):
            collision = check_collision_ball_rect(self.ball, platform)
            if collision:
                if collision["top"]:
                    print("Collision top")
                    self.y_acc = 0
                    if not action == 2:
                        self.ball.player_pos.y = platform.top - self.ball.radius
                    else:
                        self.y_acc = -15
                if collision["bottom"]:
                    self.y_acc = 0
                    self.ball.player_pos.y = platform.bottom + self.ball.radius
                if collision["left"] and action == 1:
                    self.ball.player_pos.x = platform.left - self.ball.radius
                    self.x_velocity = 0

                if collision["right"] and action == 0:
                    self.ball.player_pos.x = platform.right + self.ball.radius
                    self.x_velocity = 0

        # Apply gravity
        self.y_acc += 1
        self.ball.player_pos.y += self.y_acc
        
        done = False
        # print(f'Ball x: {self.ball.player_pos.x}, y: {self.ball.player_pos.y}, action = {action}, plat1_y = {PLATFORM_1_Y}, plat2_y = {PLATFORM_2_Y}')
        if action == 2:
            pass # Reward jumping onto platforms

        # Get distance to the nearest platform
        _, _, dist = get_closest_point_of_the_platform(self.ball, self.platforms[2])

        # Reward for reducing distance to platforms
        reward += (1/dist)  # Encourage movement toward platforms
        print(f'Reward: {reward}, dist {dist}')
        collision_plat1 = check_collision_ball_rect(self.ball, self.platforms[1])
        collision_plat2 = check_collision_ball_rect(self.ball, self.platforms[2])
        collision_plat3 = check_collision_ball_rect(self.ball, self.platforms[3])
        if(collision_plat1 is not None and collision_plat1["top"]):
            print("Platform 1 reached")
            reward = 1000
        elif(collision_plat2 is not None and collision_plat2["top"]):
            print("Platform 2 reached")
            reward = 2000
        elif(collision_plat3 is not None and collision_plat3["top"]):
            print("Platform 3 reached")
            reward = 30000
        # if (PLATFORM_1_Y > self.ball.player_pos.y) and (self.ball.player_pos.y <= PLATFORM_2_Y):
        #     print("Ball reached plat 1")
        #     reward = 3
        # elif(PLATFORM_2_Y > self.ball.player_pos.y) and (self.ball.player_pos.y <= PLATFORM_3_Y):
        #     print("Ball reached plat 2")
        #     reward = 5
        # elif(self.ball.player_pos.y <= PLATFORM_3_Y):
        #     print("Ball reached plat 3")
        #     reward = 10
        # Heavy penalty for falling off
        if self.ball.player_pos.y > GROUND_Y:
            print(self.ball.player_pos.y)
            print("Ball fell down")
            reward = -100  # Strong penalty for falling
            done = True   # End episode if ball falls off
        print(f'Reward: {reward}, dist {dist}')
        # ✅ Return 5 values: observation, reward, terminated, truncated, info
        observation = self._get_obs()
        terminated = done  # True if the episode should end
        truncated = False  # You can change this if there's a max step limit
        return observation, reward, terminated, truncated, {}

    def _get_obs(self):
        nearest_x, nearest_y, distance_nearest = get_closest_platform_data(self.ball, self.platforms)
        
        return np.array([self.ball.player_pos.x,
                         self.ball.player_pos.y,
                         self.x_velocity,
                         self.y_acc,
                         nearest_x,
                         nearest_y,
                         distance_nearest
                         ], dtype=np.float32)
    def render(self):
        self.screen.fill((0, 0, 0))
        pygame.draw.circle(self.screen, "red", (int(self.ball.player_pos.x), int(self.ball.player_pos.y)), self.ball.radius)
        for platform in self.platforms:
            pygame.draw.rect(self.screen, "green", platform)
        pygame.display.flip()
        self.clock.tick(60)