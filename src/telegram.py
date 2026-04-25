import asyncio
from telegram import Bot,Update
from telegram.ext import ApplicationBuilder,CommandHandler
from src.config import CFG
bot=Bot(CFG["TG_TOKEN"])
STATE={"equity":0,"paused":False,"scores":{},"active":{}}
def alert(t,img=None):
    async def _s():
        if img:
            with open(img,'rb') as f: await bot.send_photo(CFG["TG_CHAT"],f,caption=t,parse_mode='Markdown')
        else: await bot.send_message(CFG["TG_CHAT"],t,parse_mode='Markdown')
    asyncio.run(_s())
async def status(u,c): act=", ".join(STATE["active"].keys()) or "none"; await u.message.reply_text(f"📊 MASTER [{ 'PAUSED' if STATE['paused'] else 'ON'}]\nActive: {act}\nEquity ${STATE['equity']:.0f}",parse_mode='Markdown')
async def rotate(u,c):
    s=STATE["scores"]; top=sorted(s.items(),key=lambda x:x[1].get('score',0),reverse=True)[:12]
    txt="🔄 Top signals\n"+ "\n".join([f"{k}: {v.get('side','-')} {v.get('score',0):.1f}" for k,v in top])
    await u.message.reply_text(txt)
async def pause(u,c): STATE["paused"]=True; await u.message.reply_text("⏸️ Paused all")
async def resume(u,c): STATE["paused"]=False; await u.message.reply_text("▶️ Resumed")
def start(): a=ApplicationBuilder().token(CFG["TG_TOKEN"]).build(); a.add_handler(CommandHandler("status",status)); a.add_handler(CommandHandler("rotate",rotate)); a.add_handler(CommandHandler("pause",pause)); a.add_handler(CommandHandler("resume",resume)); return a
