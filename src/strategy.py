import pandas as pd, ta
def signal(df, dfh, cfg, sym):
    h=dfh.copy(); h['kijun']=(h['high'].rolling(26).max()+h['low'].rolling(26).min())/2
    h['sa']=((h['high'].rolling(9).max()+h['low'].rolling(9).min())/2 + h['kijun'])/2
    h['sb']=(h['high'].rolling(52).max()+h['low'].rolling(52).min())/2
    h1b=h['close'].iloc[-2] > max(h['sa'].iloc[-2], h['sb'].iloc[-2]); h1s=h['close'].iloc[-2] < min(h['sa'].iloc[-2], h['sb'].iloc[-2])
    d=df.copy(); h5,l5,c5=d['high'],d['low'],d['close']
    kijun=(h5.rolling(26).max()+l5.rolling(26).min())/2; tenkan=(h5.rolling(9).max()+l5.rolling(9).min())/2
    sa=((tenkan+kijun)/2).shift(26); sb=((h5.rolling(52).max()+l5.rolling(52).min())/2).shift(26)
    ct=pd.concat([sa,sb],1).max(1); cb=pd.concat([sa,sb],1).min(1)
    d['kijun']=kijun; d['atr']=ta.volatility.average_true_range(h5,l5,c5,14); d['adx']=ta.trend.adx(h5,l5,c5,14); d['atr_pct']=d['atr']/c5*100; d['atr_rank']=d['atr_pct'].rolling(100).rank(pct=True)
    last=d.iloc[-2]
    if last['adx']<cfg["ADX_MIN"]: return None
    long=c5.iloc[-2]>ct.iloc[-2] and h1b and d.iloc[-3]['low']<=kijun.iloc[-3] and last['close']>last['open']
    short=c5.iloc[-2]<cb.iloc[-2] and h1s and d.iloc[-3]['high']>=kijun.iloc[-3] and last['close']<last['open']
    if not (long or short): return None
    spiky=sym.startswith(("BOOM","CRASH","1HZ")); r=last['atr_rank']
    tp=(2.5 if r<0.3 else 3.8) if spiky else (1.8 if r<0.3 else 2.5)
    sl=(2.2 if r<0.3 else 3.0) if spiky else (1.2 if r<0.3 else 1.8)
    return {"side":"BUY" if long else "SELL","atr":float(last['atr']),"kijun":float(last['kijun']),"tp":tp,"sl":sl,"score":float(last['adx']*(1+r)),"adx":float(last['adx'])}
