import pandas as pd
import numpy as np

def prepare_data(csv):
    df = pd.read_csv(csv)

    df["return"] = df["close"].pct_change()

    df["EMA50"] = df["close"].ewm(span=50, adjust=False).mean()
    df["EMA200"] = df["close"].ewm(span=200, adjust=False).mean()
    df["EMA_diff"] = df["EMA50"] - df["EMA200"]

    delta = df["close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    rs = gain.rolling(14).mean() / loss.rolling(14).mean()
    df["RSI"] = 100 - (100 / (1 + rs))

    tr = np.maximum(
        df["high"] - df["low"],
        np.maximum(
            abs(df["high"] - df["close"].shift()),
            abs(df["low"] - df["close"].shift())
        )
    )

    df["ATR"] = tr.rolling(14).mean()
    df["ATR_ratio"] = df["ATR"] / df["ATR"].rolling(50).mean()

    df.dropna(inplace=True)
    return df.reset_index(drop=True)
