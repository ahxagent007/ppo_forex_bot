import time, csv
import MetaTrader5 as mt5

from mt5_connector import connect, rates, position, send
from indicators import indicators
from state_builder import state
from news_filter import news_block
from risk_manager import RiskManager
from rl_agent import Agent

connect()
agent = Agent("ppo_forex_model.zip")
risk = RiskManager(mt5.account_info().balance)

LOT = 0.01

while True:
    if news_block():
        time.sleep(3600)
        continue

    row = indicators(rates())
    pos = position()
    obs = state(row, pos)

    action = agent.act(obs)

    if action == 1 and not pos:
        send(mt5.ORDER_TYPE_BUY, LOT)

    elif action == 2 and not pos:
        send(mt5.ORDER_TYPE_SELL, LOT)

    elif action == 3 and pos:
        send(
            mt5.ORDER_TYPE_SELL if pos.type == mt5.POSITION_TYPE_BUY else mt5.ORDER_TYPE_BUY,
            pos.volume
        )

    balance = mt5.account_info().balance
    risk.check(balance)

    with open("trade_log.csv", "a", newline="") as f:
        csv.writer(f).writerow([time.time(), action, balance])

    time.sleep(3600)
