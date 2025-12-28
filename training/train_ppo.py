from stable_baselines3 import PPO
from trading_env import ForexTradingEnv
from prepare_data import prepare_data

df = prepare_data("../data/EURUSD_H1.csv")
env = ForexTradingEnv(df)

model = PPO("MlpPolicy", env, verbose=1)
model.learn(300_000)
model.save("ppo_forex_model")
