import os
from dotenv import load_dotenv
load_dotenv()
CFG = {
    "TOKEN": os.getenv("DERIV_TOKEN"),
    "APP_ID": "1089",
    "SYMBOLS": ['R_10', 'R_25', 'R_50', 'R_75', 'R_100', 'R_10_1s', 'R_25_1s', 'R_50_1s', 'R_75_1s', 'R_100_1s', '1HZ10V', '1HZ25V', '1HZ50V', '1HZ75V', '1HZ100V', 'BOOM300', 'BOOM500', 'BOOM600', 'BOOM900', 'BOOM1000', 'CRASH300', 'CRASH500', 'CRASH600', 'CRASH900', 'CRASH1000'],
    "TF": 60,
    "TF_H1": 3600,
    "RISK": float(os.getenv("RISK_PCT","0.3")),
    "MAX_DD": 5.0,
    "MAX_POS": int(os.getenv("MAX_POSITIONS","5")),
    "DAILY_PROFIT_LOCK": 6.0,
    "ADX_MIN": 18,
    "TG_TOKEN": os.getenv("TELEGRAM_TOKEN"),
    "TG_CHAT": os.getenv("TELEGRAM_CHAT_ID"),
}
