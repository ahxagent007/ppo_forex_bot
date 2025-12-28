import MetaTrader5 as mt5

SYMBOL = "EURUSD"
TIMEFRAME = mt5.TIMEFRAME_H1

def connect():
    if not mt5.initialize():
        raise RuntimeError("MT5 failed")

def rates(n=300):
    return mt5.copy_rates_from_pos(SYMBOL, TIMEFRAME, 0, n)

def position():
    pos = mt5.positions_get(symbol=SYMBOL)
    return pos[0] if pos else None

def send(order_type, lot):
    mt5.order_send({
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": SYMBOL,
        "volume": lot,
        "type": order_type,
        "deviation": 20,
        "magic": 999
    })
