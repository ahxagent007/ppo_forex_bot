import pandas as pd
import numpy as np

def indicators(rates):
    df = pd.DataFrame(rates)

    df["return"] = df["close"].pct_change()
    df["EMA50"] = df["close"].ewm(50).mean()
    df["EMA200"] = df["close"].ewm(200).mean()
    df["EMA_diff"] = df["EMA50"] - df["EMA200"]

    delta = df["close"].diff()
    rs = delta.clip(lower=0).rolling(14).mean() / (-delta.clip(upper=0)).rolling(14).mean()
    df["RSI"] = 100 - (100 / (1 + rs))

    tr = np.maximum(df["high"] - df["low"], abs(df["high"] - df["close"].shift()))
    df["ATR"] = tr.rolling(14).mean()
    df["ATR_ratio"] = df["ATR"] / df["ATR"].rolling(50).mean()

    df.dropna(inplace=True)
    return df.iloc[-1]
