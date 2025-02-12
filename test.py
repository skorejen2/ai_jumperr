from ballenv import BallEnv
from stable_baselines3 import PPO,A2C

env = BallEnv()
model = PPO.load("ball_jumper_model")

obs, _ = env.reset()
for _ in range(1000):
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, done, truncated, _ = env.step(action)

    env.render()
    if done:
        obs, _ = env.reset()
