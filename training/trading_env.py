import gymnasium as gym
from gymnasium import spaces
import numpy as np

TRANSACTION_COST = 0.00005

class ForexTradingEnv(gym.Env):

    def __init__(self, df, balance=10_000):
        super().__init__()

        self.df = df.reset_index(drop=True)
        self.balance = balance
        self.start_balance = balance

        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(5,), dtype=np.float32
        )

    def reset(self, seed=None, options=None):
        self.step_idx = 0
        self.position = 0
        self.entry_price = 0
        self.max_balance = self.balance
        return self._obs(), {}

    def _obs(self):
        row = self.df.iloc[self.step_idx]
        return np.array([
            row["return"],
            row["RSI"] / 100,
            row["EMA_diff"],
            row["ATR_ratio"],
            self.position
        ], dtype=np.float32)

    def step(self, action):
        row = self.df.iloc[self.step_idx]
        price = row["close"]
        reward = 0

        # ----- ACTIONS -----
        if action == 1 and self.position == 0:
            self.position = 1
            self.entry_price = price
            reward -= TRANSACTION_COST

        elif action == 2 and self.position == 0:
            self.position = -1
            self.entry_price = price
            reward -= TRANSACTION_COST

        elif action == 3 and self.position != 0:
            pnl = (price - self.entry_price) * self.position
            self.balance += pnl
            reward += pnl
            self.position = 0
            reward -= TRANSACTION_COST

        # ----- UNREALIZED -----
        if self.position != 0:
            reward += (price - self.entry_price) * self.position * 0.1

        # ----- RISK PENALTIES -----
        self.max_balance = max(self.max_balance, self.balance)
        drawdown = self.max_balance - self.balance
        reward -= drawdown * 0.1

        if action != 0:
            reward -= 0.01

        if row["ATR_ratio"] > 1.5:
            reward -= 0.05

        self.step_idx += 1
        done = self.step_idx >= len(self.df) - 1

        return self._obs(), reward, done, False, {}
