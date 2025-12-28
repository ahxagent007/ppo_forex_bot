import numpy as np
import MetaTrader5 as mt5

def state(row, pos):
    p = 0
    if pos:
        p = 1 if pos.type == mt5.POSITION_TYPE_BUY else -1

    return np.array([
        row["return"],
        row["RSI"] / 100,
        row["EMA_diff"],
        row["ATR_ratio"],
        p
    ], dtype=np.float32)
