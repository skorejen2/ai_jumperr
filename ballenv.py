import gymnasium as gym
from gymnasium import spaces
import pygame
import numpy as np
from ball import Ball
from collisions import check_collision_ball_rect, get_closest_point_and_distance_to_the_platform, get_closest_platform_data,get_distance_to_platforms

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
GROUND_Y = 520  # Assuming the floor starts at y = 520
PLATFORM_1_Y = 470  # Example y-coordinates
PLATFORM_2_Y = 400
PLATFORM_3_Y = 250  # Highest platform (goal)
BALL_RADIUS = 40
GRAVITY = 1

class BallEnv(gym.Env):
    def __init__(self):
        super(BallEnv, self).__init__()

        

        #Init pygame
        pygame.init()
        self.screen = pygame.display.set_mode((1280,720))
        self.clock = pygame.time.Clock()

        # Ball properties
        self.ball = Ball(BALL_RADIUS,"red",pygame.Vector2(self.screen.get_width()/2,self.screen.get_height()/2))

        self.y_acc = 0
        self.x_velocity = 0
        
        

        rect_floor = pygame.Rect(0, GROUND_Y, self.screen.get_width(), 40)
        rect_platform1 = pygame.Rect(self.screen.get_width() * 0.55, PLATFORM_1_Y, 150, 50)
        rect_platform2 = pygame.Rect(self.screen.get_width() * 0.70, PLATFORM_2_Y, 100, 50)
        rect_platform3 = pygame.Rect(self.screen.get_width() * 0.88, PLATFORM_3_Y, 50, 5) # goal
        self.platforms = [rect_floor, rect_platform1,rect_platform2,rect_platform3]

        self._max_dy = 500 # max vertical speed
        self._max_dx = 500 # max horizontal speed

        

        # Define action and observation space
        # Example: Discrete action space (0 or 1) and continuous observation space (array of floats)
        self.action_space = spaces.Discrete(3)  # Three possible actions: left, right, up

        # observation for ball_x, ball_y, dx, dy, dx_platform, dy_platform, distance nearest platform 
        # current localtion of the ball
        # current velocity of the ball
        # current nearest platform location
        # set min and max value for each

        self.observation_space = spaces.Box(
            low = np.array([-200,-100,50,-1200,0,0,0,0]), 
            high = np.array([SCREEN_WIDTH, SCREEN_HEIGHT+100, self._max_dx, self._max_dy, SCREEN_WIDTH, SCREEN_HEIGHT, 1500,1500]),
            dtype=np.float32
            )
        
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)  # Ensure proper Gym environment reset behavior
        self.ball.player_pos = pygame.Vector2(self.screen.get_width()/2, self.screen.get_height()/2)
        self.y_acc = 0
        self.x_velocity = 0  # Reset velocity as well
        _, _ ,self.goal_distance = get_closest_point_and_distance_to_the_platform(self.ball, self.platforms[3])
        return self._get_obs(), {}


    # 1 step is represented as 1 fps 
    # hence, when we are running at 60fps ~= 0.016s
    # and running at 300px horizontally per second
    # we get 5px movement per fps
    def step(self, action):
        # Apply action and return the new state, reward, done flag, and additional info
        self.action = action
       
        
        if action is not None:
            # Handle movement
            if action == 0:  # Move left
                self.ball.player_pos.x -= 5
                self.x_velocity = -5
                #reward = 0.001
            elif action == 1:  # Move right
                self.ball.player_pos.x += 5
                self.x_velocity = 5
                #reward = 0.001
        
        collision_top = False
        for i, platform in enumerate(self.platforms):
            collision = check_collision_ball_rect(self.ball, platform)
            if collision:
                if collision["top"]:
                    collision_top = True
                    self.y_acc = 0
                    if action == 2:
                        self.y_acc = 20
                    else:
                        self.ball.player_pos.y = platform.top - self.ball.radius
                if collision["bottom"]:
                    self.ball.player_pos.y = platform.bottom + self.ball.radius
                if collision["left"] and action == 1:
                    self.ball.player_pos.x = platform.left - self.ball.radius
                    self.x_velocity = 0
                if collision["right"] and action == 0:
                    self.ball.player_pos.x = platform.right + self.ball.radius
                    self.x_velocity = 0

        

        if self.y_acc > 0 or not collision_top:
            self.y_acc -= 1

        # Call render() at the end of the step to update the display
        # self.render()

        # Apply gravity
        self.ball.player_pos.y += GRAVITY - self.y_acc

        done = False

        # Get distance to platform 3 (goal)
        _, _, current_dist = get_closest_point_and_distance_to_the_platform(self.ball, self.platforms[3])
        self.goal_distance = current_dist


        reward = -1 # Encourage movement toward platforms

        dist_reward = int((1/self.goal_distance) * 10000)
        reward += dist_reward

        # print(f'Dist reward: {dist_reward}, current_dist: {current_dist}')

        collision_plat0 = check_collision_ball_rect(self.ball, self.platforms[0])
        collision_plat1 = check_collision_ball_rect(self.ball, self.platforms[1])
        collision_plat2 = check_collision_ball_rect(self.ball, self.platforms[2])
        collision_plat3 = check_collision_ball_rect(self.ball, self.platforms[3])

        if self.y_acc != 0 and self.ball.player_pos.y < GROUND_Y:
             reward += 10
        if self.x_velocity != 0 :
            reward += 1
        if (collision_plat0 is not None and collision_plat0["top"]):
            reward -= 50
            #print(" - 50 reward for hitting floor")
        if(collision_plat1 is not None and collision_plat1["top"]):
            #print(" + 100 reward for reaching p1")
            reward += 2
        elif(collision_plat2 is not None and collision_plat2["top"]):
            #print(" + 500 reward for reaching p2")
            reward += 3
        elif(collision_plat3 is not None and collision_plat3["top"]):
            print("p3 reached")
            #print(" + 5000 reward for reaching p2")
            reward += 30000000

        if self.ball.player_pos.y >= GROUND_Y:
            #print("Ball fell down")
            reward += -1000 # Strong penalty for falling
            done = True   # End episode if ball falls off  
            print("Ball fell under the ground==================================================")
        # ✅ Return 5 values: observation, reward, terminated, truncated, info
        observation = self._get_obs()
        terminated = done  # True if the episode should end
        truncated = False  # You can change this if there's a max step limit
        return observation, reward, terminated, truncated, {}

    def _get_obs(self):
        nearest_x, nearest_y, distance_nearest = get_closest_platform_data(self.ball, self.platforms)
        #print(f'Goal Dist: {int(self.goal_distance)}')
        #print(f'y_acc: {self.y_acc}')
        return np.array([self.ball.player_pos.x,
                         self.ball.player_pos.y,
                         self.x_velocity,
                         self.y_acc,
                         nearest_x,
                         nearest_y,
                         distance_nearest,
                         self.goal_distance
                         ], dtype=np.float32)
    def render(self):
            # Fill the background
        self.screen.fill("pink")
        
        # Draw the ball
        pygame.draw.circle(
            self.screen,
            "red",
            (int(self.ball.player_pos.x), int(self.ball.player_pos.y)),
            self.ball.radius
        )
        
        # Draw the platforms
        for platform in self.platforms:
            pygame.draw.rect(self.screen, "blue", platform)
        
        # Initialize a font (you can change the font type and size as desired)
        font = pygame.font.SysFont("Arial", 18)
        
        # Prepare text surfaces for each parameter
        text_ball_pos = font.render(f"Ball Position: ({self.ball.player_pos.x:.1f}, {self.ball.player_pos.y:.1f})", True, (0,0,0))
        text_velocity = font.render(f"X Velocity: {self.x_velocity:.1f}", True, (0,0,0))
        text_y_acc = font.render(f"Y Acceleration: {self.y_acc:.1f}", True, (0,0,0))
        text_goal_dist = font.render(f"Goal Distance: {self.goal_distance:.1f}", True, (0,0,0))
        text_action = font.render(f"Action taken: {self.action}", True, (0,0,0))
        
        # Blit the text surfaces onto the screen at desired positions
        self.screen.blit(text_ball_pos, (10, 10))
        self.screen.blit(text_velocity, (10, 30))
        self.screen.blit(text_y_acc, (10, 50))
        self.screen.blit(text_goal_dist, (10, 70))
        self.screen.blit(text_action, (10, 90))
        
        # Update the display
        pygame.display.flip()
        self.clock.tick(60)