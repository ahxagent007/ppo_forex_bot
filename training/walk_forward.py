from stable_baselines3 import PPO
from trading_env import ForexTradingEnv

def walk_forward(df, splits=3):
    size = len(df) // splits
    for i in range(splits - 1):
        train = df[: size * (i + 1)]
        env = ForexTradingEnv(train)
        model = PPO("MlpPolicy", env)
        model.learn(100_000)
        model.save(f"ppo_model_{i}")
