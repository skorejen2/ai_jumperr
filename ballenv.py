import gymnasium as gym
from gymnasium import spaces
import pygame
import numpy as np
from ball import Ball

class BallEnv(gym.Env):
    def __init__(self):
        super(BallEnv, self).__init__()

        SCREEN_WIDTH = 1280
        SCREEN_HEIGHT = 720

        #Init pygame
        pygame.init()
        self.screen = pygame.display.set_mode((1280,720))
        self.clock = pygame.time.Clock()

        # Ball properties
        self.ball = Ball(40,"red",pygame.Vector2(self.screen.get_width()/2,self.screen.get_height()/2))
        self.gravity = 10
        self.y_acc = 0
        self.on_ground = False

        rect_floor = pygame.Rect(0, self.screen.get_height() * 0.73, self.screen.get_width(), 20)
        rect_platform1 = pygame.Rect(self.screen.get_width() * 0.55, self.screen.get_height() * 0.65, 150, 50)
        rect_platform2 = pygame.Rect(self.screen.get_width() * 0.70, self.screen.get_height() * 0.45, 100, 50)
        rect_platform3 = pygame.Rect(self.screen.get_width() * 0.88, self.screen.get_height() * 0.38, 50, 5)
        platforms = [rect_floor, rect_platform1,rect_platform2,rect_platform3]

        self._max_dy = 1200 # max vertical speed
        self._max_dx = 300 # max horizontal speed

        
        # Define action and observation space
        # Example: Discrete action space (0 or 1) and continuous observation space (array of floats)
        self.action_space = spaces.Discrete(3)  # Three possible actions: left, right, up

        # observation for ball_x, ball_y, dx, dy, dx_platform, dy_platform, is_on_ground
        self.observation_space = spaces.Box(
            low = np.array([0,0,-500,-1200,0,0,0]), 
            high = np.array([SCREEN_WIDTH, SCREEN_HEIGHT, self._max_dx, self._max_dy, SCREEN_WIDTH, SCREEN_HEIGHT, 1]),
            dtype=np.float32
            )
        
    def reset(self, seed=None, options=None):
        # Reset environment and return the initial state
        self.ball.player_pos = pygame.Vector2(self.screen.get_width()/2,self.screen.get_height()/2)  # Random initial state between 0 and 1
        self.y_acc = 0
        self.on_ground = False
        return self._get_obs(), {}

    def step(self, action):
        # Apply action and return the new state, reward, done flag, and additional info

        # Handle movement
        if action == 0:  # Move left
            self.ball.player_pos.x -= -5
        elif action == 1:  # Move right
            self.ball.player_pos.x += 5
        elif action == 2 and self.on_ground:  # Jump
            self.y_acc = -15
            self.on_ground = False

        # Apply gravity
        self.y_acc += 1
        self.ball.play_pos.y += self.y_acc
        

        # Apply gravity
        self.y_acc += 1
        self.ball.player_pos.y += self.y_acc

        self.state = np.random.random()  # Random new state after taking an action
        reward = 1 if self.state > 0.5 else 0  # Example: positive reward for state > 0.5
        done = self.state > 0.9  # Done if state exceeds 0.9
        info = {}  # Additional info (optional)
        return np.array([self.state]), reward, done, info

    def render(self):
        # Render the current state of the environment (optional)
        print(f"Current state: {self.state}")
