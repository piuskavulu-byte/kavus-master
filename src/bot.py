import asyncio,pandas as pd
from datetime import datetime
from src.config import CFG
from src.strategy import signal
from src.telegram import alert,start,STATE
from src.deriv_api import Deriv
import matplotlib.pyplot as plt
plt.style.use('dark_background')

async def get_df(d,s): c=await d.candles(s,CFG["TF"]); df=pd.DataFrame(c); df['time']=pd.to_datetime(df['epoch'],unit='s'); df.set_index('time',inplace=True); return df
async def get_h1(d,s): c=await d.candles(s,CFG["TF_H1"]); df=pd.DataFrame(c); df['time']=pd.to_datetime(df['epoch'],unit='s'); df.set_index('time',inplace=True); return df

def plot(df,sym,side):
    d=df.tail(50); fig,ax=plt.subplots(figsize=(8,4)); ax.plot(d.index,d['close']); ax.set_title(f"{sym} {side}"); p=f"/tmp/{sym}.png"; plt.savefig(p,dpi=120); plt.close(); return p

async def main():
    tg=start(); asyncio.create_task(tg.run_polling(close_loop=False))
    d=Deriv(); await d.connect(); eq=await d.balance(); STATE["equity"]=eq
    alert(f"✅ MASTER BOT LIVE — trading {len(CFG['SYMBOLS'])} indices simultaneously (max {CFG['MAX_POS']} positions)")
    while True:
        try:
            eq=await d.balance(); STATE["equity"]=eq; pos=await d.positions()
            active_syms={p['symbol'] for p in pos}; STATE["active"]={s:1 for s in active_syms}
            scores={}
            for sym in CFG["SYMBOLS"]:
                if len(active_syms) >= CFG["MAX_POS"] and sym not in active_syms: continue
                df=await get_df(d,sym); dfh=await get_h1(d,sym); sig=signal(df,dfh,CFG,sym); scores[sym]=sig or {"score":0,"side":"-"}
                if sig and not STATE["paused"] and sym not in active_syms and len(active_syms) < CFG["MAX_POS"]:
                    risk=CFG["RISK"]/100; size=max(0.35, round(eq*risk/(sig["atr"]*sig["sl"]),2))
                    img=plot(df,sym,sig["side"]); r=await d.trade(sym,sig["side"],size)
                    if 'buy' in r: alert(f"🎯 {sig['side']} {sym} ${size}",img); active_syms.add(sym)
            STATE["scores"]=scores
            await asyncio.sleep(20)
        except Exception as e: alert(f"⚠️ {e}"); await asyncio.sleep(30)

if __name__=="__main__": asyncio.run(main())
