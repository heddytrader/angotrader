
from flask import Flask, render_template_string
import os
from datetime import datetime
from zoneinfo import ZoneInfo
app = Flask(__name__)
TZ = ZoneInfo("Africa/Luanda")
HTML = """
<!DOCTYPE html><html lang="pt"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AngoTrader</title>
<script src="https://unpkg.com/lightweight-charts@4.1.3/dist/lightweight-charts.standalone.production.js"></script>
<style>
*{margin:0;box-sizing:border-box} body{background:#0b0e14;color:#fff;font-family:Arial}
.top{display:flex;align-items:center;gap:10px;padding:12px;background:#11141d}
.logo{width:44px;height:44px;background:#facc15;color:#000;font-weight:900;font-size:20px;display:flex;align-items:center;justify-content:center;border-radius:10px}
.badge{font-size:10px;background:#facc15;color:#000;padding:3px 8px;border-radius:20px;font-weight:bold}
.sub{font-size:11px;color:#94a3b8}.head{padding:12px}.head h2{font-size:15px}.head p{font-size:11px;color:#94a3b8}
.card{background:#12161f;margin:10px;border-radius:14px;padding:12px}
.row{display:flex;justify-content:space-between;align-items:center}
.price{font-size:26px;font-weight:900}.down{color:#ef4444;background:#3a1212;padding:4px 8px;border-radius:6px;font-size:12px}
.tabs{display:flex;gap:8px;margin:10px 0}.tabs button{padding:8px 14px;border-radius:8px;border:0;background:#1e2433;color:#fff;font-weight:bold}.tabs .on{background:#f59e0b;color:#000}
#chart{height:360px}
.footer{position:fixed;bottom:0;left:0;right:0;background:#11141d;display:flex;justify-content:space-around;padding:10px 0;font-size:11px;text-align:center}
.footer .on{color:#facc15}
.btns{display:flex;gap:10px;margin-top:10px}.buy{flex:1;background:#22c55e;border:0;padding:14px;border-radius:10px;font-weight:900;color:#fff;font-size:16px}.sell{flex:1;background:#ef4444;border:0;padding:14px;border-radius:10px;font-weight:900;color:#fff;font-size:16px}
.btns button:disabled{opacity:0.4}
#mercado{margin:10px;padding:12px;border-radius:10px;text-align:center;font-weight:900;font-size:16px}
.aberto{background:#14532d;color:#fff}.fechado{background:#7f1d1d;color:#fff}
#login{position:fixed;inset:0;background:#0b0e14;z-index:99;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:20px}
#login .logo{width:70px;height:70px;font-size:30px;border-radius:18px}
#login input{width:100%;max-width:320px;padding:14px;margin:6px 0;border-radius:10px;border:1px solid #333;background:#12161f;color:#fff;font-size:15px}
#login button{width:100%;max-width:320px;padding:14px;margin-top:10px;border:0;border-radius:10px;background:#facc15;font-weight:900;font-size:16px}
</style></head><body>
<div id="login">
<div class="logo">AT</div><h2 style="margin:12px 0 4px">AngoTrader</h2><p style="color:#94a3b8;font-size:13px;margin-bottom:16px">Feito em Angola 🇦🇴</p>
<input id="email" type="email" placeholder="Email"><input id="senha" type="password" placeholder="Senha">
<button onclick="entrar()">ENTRAR</button><p id="erro" style="color:#ef4444;margin-top:10px;font-size:13px"></p>
</div>
<div class="top"><div class="logo">AT</div><div><b>AngoTrader Bot</b> <span class="badge">ACESSO TOTAL</span><br><span class="sub">DONO • PRO • Simples</span></div></div>
<div id="mercado" class="{{classe}}">{{status}} • {{data}} | {{hora}} Luanda</div>
<div class="head"><h2>GRÁFICO DE VELAS AO VIVO (EUR/USD):</h2><p>Tempo Real • Sessão Londres / Nova Iorque</p></div>
<div class="card">
<div class="row"><div><b>EURUSD</b> <span style="background:#facc15;color:#000;font-size:10px;padding:2px 6px;border-radius:4px">FOREX</span></div><div><span class="price" id="p">$1.0431</span> <span class="down">-1.05%</span></div></div>
<div class="tabs"><button class="on" onclick="setTF(this,1)">1M</button><button onclick="setTF(this,5)">5M</button><button onclick="setTF(this,15)">15M</button><span style="margin-left:auto;font-size:12px;color:#94a3b8">Tempo Real 1s</span></div>
<div id="chart"></div>
<div class="btns"><button class="buy" id="bBuy" onclick="trade('COMPRA')">▲ COMPRA</button><button class="sell" id="bSell" onclick="trade('VENDA')">▼ VENDA</button></div>
<p id="msg" style="text-align:center;margin-top:8px;color:#facc15"></p>
</div>
<div style="height:70px"></div>
<div class="footer"><div>⊞<br>Painel</div><div>📶<br>Sinais IA</div><div class="on">📊<br>Análise IA</div><div>🔴<br>Ao Vivo</div><div>•••<br>Mais</div></div>
<script>
let MERCADO_ABERTO = {{aberto_js}};
function entrar(){let e=document.getElementById('email').value;let s=document.getElementById('senha').value;if(!e||!s){document.getElementById('erro').innerText='Escreve o email e a senha';return;}document.getElementById('login').style.display='none';localStorage.setItem('ango_email',e);}
if(localStorage.getItem('ango_email')){document.getElementById('login').style.display='none';}
if(!MERCADO_ABERTO){document.getElementById('bBuy').disabled=true;document.getElementById('bSell').disabled=true;document.getElementById('msg').innerText='Mercado fechado - Negociação bloqueada até abertura';}
let price=1.0431, data=[], last=1.0431;
for(let i=0;i<50;i++){let o=last;let c=o+(Math.random()-0.5)*0.0008;let h=Math.max(o,c)+Math.random()*0.0003;let l=Math.min(o,c)-Math.random()*0.0003;let t=Math.floor(Date.now()/1000)-(50-i)*60;data.push({time:t,open:o,high:h,low:l,close:c});last=c}
const chart=LightweightCharts.createChart(document.getElementById('chart'),{layout:{background:{color:'#12161f'},textColor:'#ddd'},grid:{vertLines:{color:'#1e2433'},horzLines:{color:'#1e2433'}},width:document.getElementById('chart').clientWidth,height:360});
const s=chart.addCandlestickSeries({upColor:'#22c55e',downColor:'#ef4444',wickUpColor:'#22c55e',wickDownColor:'#ef4444'});s.setData(data);
function setTF(el,m){document.querySelectorAll('.tabs button').forEach(b=>b.classList.remove('on'));el.classList.add('on');document.getElementById('msg').innerText='Timeframe: '+m+'M';}
function trade(t){if(!MERCADO_ABERTO){alert('Mercado Fechado!');return;}document.getElementById('msg').innerText=t+' executada em $'+price.toFixed(4);}
setInterval(()=>{if(!MERCADO_ABERTO)return;price+=(Math.random()-0.5)*0.0004;let lc=data[data.length-1];let upd={time:Math.floor(Date.now()/1000),open:lc.open,high:Math.max(lc.high,price),low:Math.min(lc.low,price),close:price};s.update(upd);data[data.length-1]=upd;document.getElementById('p').innerText='$'+price.toFixed(4);},1000);
</script></body></html>
"""
def mercado_status(now):
    wd = now.weekday() # 0=Seg ... 5=Sab, 6=Dom
    h = now.hour
    if wd == 5: return False
    if wd == 6 and h < 23: return False
    if wd == 4 and h >= 23: return False
    return True
@app.route("/")
def home():
    agora=datetime.now(TZ)
    aberto=mercado_status(agora)
    status="🟢 MERCADO ABERTO" if aberto else "🔴 MERCADO FECHADO"
    classe="aberto" if aberto else "fechado"
    return render_template_string(HTML, status=status, classe=classe, data=agora.strftime("%d/%m/%Y"), hora=agora.strftime("%H:%M:%S"), aberto_js="true" if aberto else "false")
@app.route("/health")
def h(): return {"status":"ok"}
if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",5000)))
