from flask import Flask, request, redirect, session, render_template_string
import sqlite3, hashlib, os

app = Flask(__name__)
app.secret_key = "angotrader2026"

def db():
    c = sqlite3.connect("users.db")
    c.execute("CREATE TABLE IF NOT EXISTS users (name TEXT, email TEXT PRIMARY KEY, pass TEXT)")
    return c

HTML = """
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<title>AngoTrader Bot</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Arial}
body{background:#0b0e11;color:white}
.top{background:#181a20;padding:12px 15px;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0}
.logo{font-size:22px;font-weight:900}.logo span{color:#fcd535}
.top a{color:white;text-decoration:none;font-size:13px;margin-left:12px}
.btn{background:#fcd535;color:black;padding:8px 14px;border-radius:6px;font-weight:900;text-decoration:none;font-size:13px}
.hero{padding:30px 15px;text-align:center}
.hero h1{font-size:32px;line-height:1.2}.hero h1 span{color:#fcd535}
.hero p{color:#848e9c;margin:12px 0 20px}
.card{background:#1e2329;border-radius:12px;padding:15px;margin:12px}
.row{display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid #2b3139}
.green{color:#0ecb81}.red{color:#f6465d}
input{width:100%;padding:13px;margin:8px 0;border-radius:8px;border:1px solid #2b3139;background:#1e2329;color:white}
button{width:100%;padding:14px;background:#fcd535;border:none;border-radius:8px;font-weight:900;font-size:16px}
canvas{width:100%;height:180px}
.small{color:#848e9c;font-size:13px;text-align:center;margin-top:10px}
.tabs{display:flex;gap:8px;justify-content:center;margin:15px}
.tab{background:#1e2329;padding:8px 16px;border-radius:20px;font-size:13px}
.tab.on{background:#fcd535;color:black;font-weight:900}
</style></head><body>
<div class="top"><div class="logo">⚡ ANGO<span>TRADER</span></div><div><a href="/">Início</a><a href="/?page=login">Entrar</a></div></div>

{% if page=='login' %}
<div class="card" style="max-width:400px;margin:30px auto">
<h2 style="text-align:center">Entrar na tua conta</h2><p class="small">Bem-vindo de volta ao AngoTrader</p>
<form method="POST" action="/login"><input name="email" placeholder="Email" required><input name="pass" type="password" placeholder="Senha" required><button>ENTRAR</button></form>
<p class="small">Não tens conta? <a href="/?page=register" style="color:#fcd535">Criar conta</a></p>
</div>

{% elif page=='register' %}
<div class="card" style="max-width:400px;margin:30px auto">
<h2 style="text-align:center">Criar conta grátis</h2>
<form method="POST" action="/register"><input name="name" placeholder="Nome completo" required><input name="email" placeholder="Email" required><input name="pass" type="password" placeholder="Criar senha" required><button>CRIAR CONTA</button></form>
<p class="small">Já tens conta? <a href="/?page=login" style="color:#fcd535">Entrar</a></p>
</div>

{% elif user %}
<div class="hero"><h2>Bem-vindo, {{user}} 👋</h2><p>Estás dentro do AngoTrader Bot</p><a class="btn" href="/logout">Sair</a></div>
<div class="card"><h3>🤖 Bot EGGY - Status: ATIVO</h3><p class="small" style="text-align:left">Estratégia EGGY a analisar o mercado para ti...</p></div>

{% else %}
<div class="hero"><h1>Negocia como os grandes.<br><span>Opera como angolano.</span></h1><p>Sinais IA • Live Trading • Análise EGGY • Feito em Angola</p><a class="btn" href="/?page=register">Começar Grátis →</a><br><br><a href="/?page=login" style="color:white">Já tenho conta</a></div>
<div class="tabs"><div class="tab on">BTC</div><div class="tab">ETH</div><div class="tab">SOL</div><div class="tab">XAU/USD</div></div>
<div class="card"><canvas id="c"></canvas><div class="row"><b>BTC / USDT</b><b class="green">$97,450 +2.4%</b></div><div class="row"><span>ETH / USDT</span><span class="green">$3,842 +1.8%</span></div><div class="row"><span>SOL / USDT</span><span class="red">$214 -0.9%</span></div><div class="row"><span>OURO / USD</span><span class="green">$2,912 +0.6%</span></div></div>
<div class="card"><h3>🔥 Sinal de Hoje - EGGY</h3><p style="margin:10px 0"><b class="green">COMPRAR BTC</b> - Entrada $97,200 • Alvo $99,500 • Stop $96,000</p><p class="small" style="text-align:left">Confiança IA: 87% • Força: Alta</p></div>
<div class="card" style="text-align:center"><h3>Porquê AngoTrader?</h3><p class="small">✅ Sinais todos os dias<br>✅ Sem complicação<br>✅ 100% Angolano</p><br><a class="btn" href="/?page=register">Criar Conta Grátis</a></div>
{% endif %}
<script>
var cv=document.getElementById('c'); if(cv){var x=cv.getContext('2d'); x.strokeStyle='#fcd535'; x.lineWidth=3; x.beginPath(); x.moveTo(0,140); var p=[140,120,130,100,110,90,105,70,80,60,75,40,50,30,20]; p.forEach((y,i)=>x.lineTo(i*25,y)); x.stroke();}
</script></body></html>
"""

@app.route("/")
def home():
    page = request.args.get("page","home")
    return render_template_string(HTML, page=page, user=session.get("user"))

@app.route("/register", methods=["POST"])
def register():
    c=db(); 
    try: c.execute("INSERT INTO users VALUES (?,?,?)",(request.form["name"], request.form["email"], hashlib.sha256(request.form["pass"].encode()).hexdigest())); c.commit()
    except: pass
    c.close(); session["user"]=request.form["name"]; return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    c=db(); r=c.execute("SELECT name FROM users WHERE email=? AND pass=?",(request.form["email"], hashlib.sha256(request.form["pass"].encode()).hexdigest())).fetchone(); c.close()
    if r: session["user"]=r[0]; return redirect("/")
    return redirect("/?page=login")

@app.route("/logout")
def logout(): session.clear(); return redirect("/")

if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
