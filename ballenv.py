import gymnasium as gym
from gymnasium import spaces
import numpy as np

class BallEnv(gym.Env):
    def __init__(self):
        super(BallEnv, self).__init__()
        
        # Define action and observation space
        # Example: Discrete action space (0 or 1) and continuous observation space (array of floats)
        self.action_space = spaces.Discrete(2)  # Two possible actions (e.g., left, right)
        self.observation_space = spaces.Box(low=np.array([0]), high=np.array([1]), dtype=np.float32)
        
    def reset(self):
        # Reset environment and return the initial state
        self.state = np.random.random()  # Random initial state between 0 and 1
        return np.array([self.state])

    def step(self, action):
        # Apply action and return the new state, reward, done flag, and additional info
        self.state = np.random.random()  # Random new state after taking an action
        reward = 1 if self.state > 0.5 else 0  # Example: positive reward for state > 0.5
        done = self.state > 0.9  # Done if state exceeds 0.9
        info = {}  # Additional info (optional)
        return np.array([self.state]), reward, done, info

    def render(self):
        # Render the current state of the environment (optional)
        print(f"Current state: {self.state}")
