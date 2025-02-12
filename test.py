import gym
from ballenv import BallEnv
from stable_baselines3 import A2C

# Assume CustomEnv is your custom environment that follows the Gym API
env = BallEnv()

# Initialize the A2C model with the custom environment
model = A2C("MlpPolicy", env, verbose=1)

# Train the model
model.learn(total_timesteps=10_000)

# Use the trained model to interact with the environment
obs = env.reset()
for i in range(1000):
    action, _state = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)
    env.render()

    if done:
        obs = env.reset()  # Reset environment when done
