from ballenv import BallEnv
from stable_baselines3 import PPO,A2C

# Assume CustomEnv is your custom environment that follows the Gym API
env = BallEnv()

# Initialize the A2C model with the custom environment
model = PPO("MlpPolicy", env, verbose=1, learning_rate=0.0003)

model.learn(total_timesteps=20000)

# Save model
model.save("ball_jumper_model")
