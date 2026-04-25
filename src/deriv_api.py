import websockets,json
from src.config import CFG
class Deriv:
    async def connect(self): self.ws=await websockets.connect(f"wss://ws.derivws.com/websockets/v3?app_id={CFG['APP_ID']}"); await self.ws.send(json.dumps({"authorize":CFG["TOKEN"]})); await self.ws.recv()
    async def candles(self,s,tf): await self.ws.send(json.dumps({"ticks_history":s,"style":"candles","granularity":tf,"count":200,"end":"latest"})); return json.loads(await self.ws.recv())['candles']
    async def balance(self): await self.ws.send(json.dumps({"balance":1})); return json.loads(await self.ws.recv())['balance']['balance']
    async def positions(self): await self.ws.send(json.dumps({"portfolio":1})); d=json.loads(await self.ws.recv()); return d.get('portfolio',{}).get('contracts',[])
    async def trade(self,sym,side,amt):
        ct="CALL" if side=="BUY" else "PUT"
        await self.ws.send(json.dumps({"proposal":1,"amount":amt,"basis":"stake","contract_type":ct,"currency":"USD","duration":5,"duration_unit":"m","symbol":sym}))
        p=json.loads(await self.ws.recv())
        if 'error' in p: return p
        await self.ws.send(json.dumps({"buy":p['proposal']['id'],"price":amt})); return json.loads(await self.ws.recv())
