from stable_baselines3 import PPO

class Agent:
    def __init__(self, model):
        self.model = PPO.load(model)

    def act(self, obs):
        a, _ = self.model.predict(obs, deterministic=True)
        return int(a)
