import os

CFG = {
    "RISK_PCT": float(os.getenv("RISK_PCT", 1.0)),
    "SL_PIPS": int(os.getenv("SL_PIPS", 100)),
    "RR": float(os.getenv("RR", 3.0)),
    "MULTIPLIER": int(os.getenv("MULTIPLIER", 500)),
    "ADX_MIN": float(os.getenv("ADX_MIN", 18)),
    "RSI_MIN": int(os.getenv("RSI_MIN", 30)),
    "RSI_MAX": int(os.getenv("RSI_MAX", 70)),
    "ATR_MULT": 1.5,
    "SWING_LOOKBACK": 10,
    "AVOID_SWING": os.getenv("AVOID_SWING", "True") == "True",
    "VOL_FILTER": os.getenv("VOL_FILTER", "True") == "True",
    "MAX_SPREAD": int(os.getenv("MAX_SPREAD", 20)),
    "SCAN_INTERVAL": 30,
    "MAX_POSITIONS": 5,
    "CHART_BARS": 50,
    "EXCLUDED_SYMBOLS": ["BOOM", "CRASH"]
}

SYMBOLS = [
    "R_10","R_25","R_50","R_75","R_100",
    "1HZ10V","1HZ25V","1HZ50V","1HZ75V","1HZ100V",
    "JD10","JD25","JD50","JD75","JD100",
    "WL10","WL25","WL50","WL75","WL100"
]

SYMBOL_NAMES = {
    "R_10":"Vol 10","R_25":"Vol 25","R_50":"Vol 50","R_75":"Vol 75","R_100":"Vol 100",
    "1HZ10V":"Vol 10 1s","1HZ25V":"Vol 25 1s","1HZ50V":"Vol 50 1s","1HZ75V":"Vol 75 1s","1HZ100V":"Vol 100 1s",
    "JD10":"Jump 10","JD25":"Jump 25","JD50":"Jump 50","JD75":"Jump 75","JD100":"Jump 100",
    "WL10":"Step 10","WL25":"Step 25","WL50":"Step 50","WL75":"Step 75","WL100":"Step 100"
}
