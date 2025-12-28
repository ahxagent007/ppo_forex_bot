import datetime

BLOCK_HOURS = [(12,14)]

def news_block():
    h = datetime.datetime.utcnow().hour
    return any(start <= h <= end for start, end in BLOCK_HOURS)
