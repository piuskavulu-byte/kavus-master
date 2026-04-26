import pandas as pd
import numpy as np
import ta
from config import CFG

def add_indicators(df):
    df = df.copy()
    # Ichimoku
    df['tenkan'] = (df['high'].rolling(9).max() + df['low'].rolling(9).min()) / 2
    df['kijun'] = (df['high'].rolling(26).max() + df['low'].rolling(26).min()) / 2
    df['span_a'] = ((df['tenkan'] + df['kijun']) / 2).shift(26)
    df['span_b'] = ((df['high'].rolling(52).max() + df['low'].rolling(52).min()) / 2).shift(26)
    # ADX
    df['adx'] = ta.trend.adx(df['high'], df['low'], df['close'], window=14)
    # RSI
    df['rsi'] = ta.momentum.rsi(df['close'], window=14)
    # ATR
    df['atr'] = ta.volatility.average_true_range(df['high'], df['low'], df['close'], window=14)
    # Volume MA
    df['vol_ma'] = df['tick_volume'].rolling(20).mean()
    return df

def get_swings(df, lookback=10):
    highs = df['high'].rolling(lookback, center=True).max()
    lows = df['low'].rolling(lookback, center=True).min()
    swing_high = df['high'][(df['high'] == highs)].iloc[-1] if not highs.empty else None
    swing_low = df['low'][(df['low'] == lows)].iloc[-1] if not lows.empty else None
    return swing_high, swing_low

def check_signal(df, df_h1):
    if len(df) < 100 or len(df_h1) < 60:
        return None, "Not enough data"

    df = add_indicators(df)
    last = df.iloc[-1]
    prev = df.iloc[-2]
    h1_last = df_h1.iloc[-1]

    # Filters
    if last['adx'] < CFG['ADX_MIN']:
        return None, f"ADX {last['adx']:.1f} < {CFG['ADX_MIN']}"

    if not CFG['RSI_MIN'] <= last['rsi'] <= CFG['RSI_MAX']:
        return None, f"RSI {last['rsi']:.1f} out of range"

    if CFG['VOL_FILTER'] and last['tick_volume'] < last['vol_ma']:
        return None, "Low volume"

    # Ichimoku logic
    cloud_top = max(last['span_a'], last['span_b'])
    cloud_bot = min(last['span_a'], last['span_b'])

    # BUY: bounce off kijun + break above cloud + H1 bullish
    buy_cond = (
        prev['low'] <= prev['kijun'] <= prev['high'] and
        last['close'] > cloud_top and
        h1_last['close'] > h1_last['kijun'] and
        last['close'] > last['tenkan']
    )

    # SELL: bounce off kijun + break below cloud + H1 bearish
    sell_cond = (
        prev['high'] >= prev['kijun'] >= prev['low'] and
        last['close'] < cloud_bot and
        h1_last['close'] < h1_last['kijun'] and
        last['close'] < last['tenkan']
    )

    if CFG['AVOID_SWING']:
        sh, sl = get_swings(df, CFG['SWING_LOOKBACK'])
        if buy_cond and sh and (sh - last['close']) < 50:
            return None, f"Swing high too close: {sh - last['close']:.1f} pips"
        if sell_cond and sl and (last['close'] - sl) < 50:
            return None, f"Swing low too close: {last['close'] - sl:.1f} pips"

    if buy_cond:
        return "BUY", f"ADX:{last['adx']:.1f} RSI:{last['rsi']:.1f} H1:UP"
    if sell_cond:
        return "SELL", f"ADX:{last['adx']:.1f} RSI:{last['rsi']:.1f} H1:DOWN"

    return None, "No setup"

def calc_sl_tp(entry, side, balance):
    pip = 0.001
    sl_pips = CFG['SL_PIPS']
    tp_pips = sl_pips * CFG['RR']

    if side == "BUY":
        sl = entry - sl_pips * pip
        tp = entry + tp_pips * pip
    else:
        sl = entry + sl_pips * pip
        tp = entry - tp_pips * pip

    risk_amt = balance * (CFG['RISK_PCT'] / 100)
    amount = risk_amt / sl_pips # $ per pip for 500x
    return round(sl, 3), round(tp, 3), round(amount, 2)
