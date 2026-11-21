from flask import Flask, render_template_string, request, redirect, session
import sqlite3, hashlib
app = Flask(__name__)
app.secret_key = "angotrader-segredo"
def db():
    c = sqlite3.connect("users.db")
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, nome TEXT, email TEXT UNIQUE, senha TEXT)")
    return c
HTML = """<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width, initial-scale=1'><style>body{background:#0a0f1e;color:white;font-family:Arial;text-align:center;padding:20px}.card{background:#141b33;padding:20px;border-radius:15px;max-width:400px;margin:auto}input{width:90%;padding:12px;margin:8px;border-radius:10px;border:none}button{width:95%;padding:13px;background:#00c853;color:white;border:none;border-radius:10px;font-weight:bold} .pair{background:#1e2745;padding:12px;margin:8px;border-radius:10px;display:flex;justify-content:space-between}</style></head><body><h1>AngoTrader</h1><div class='card'>{{conteudo}}</div></body></html>"""
@app.route("/")
def home():
    if "user" in session:
        return render_template_string(HTML, conteudo=f"<h2>Bem-vindo, {session['user']}</h2><p>Trava de Noticias: ATIVA</p><div class='pair'><span>EUR/USD</span><span>✅</span></div><div class='pair'><span>GBP/USD</span><span>✅</span></div><div class='pair'><span>BTC/USD</span><span>✅</span></div><button onclick=\"document.getElementById('sinal').innerHTML='SINAL: COMPRAR EUR/USD'\">ANALISAR AGORA</button><h2 id='sinal'></h2><a href='/sair' style='color:white'>Sair</a>")
    return render_template_string(HTML, conteudo="<h2>Entrar</h2><form method='post' action='/login'><input name='email' placeholder='Email' required><input name='senha' type='password' placeholder='Senha' required><button>ENTRAR</button></form><p>Nao tens conta?</p><a href='/cadastro'><button style='background:#ffc107;color:black'>CRIAR CONTA</button></a>")
@app.route("/cadastro")
def cadastro():
    return render_template_string(HTML, conteudo="<h2>Criar Conta</h2><form method='post' action='/criar'><input name='nome' placeholder='Nome' required><input name='email' placeholder='Email' required><input name='senha' type='password' placeholder='Senha' required><button>CRIAR CONTA</button></form>")
@app.route("/criar", methods=["POST"])
def criar():
    c=db(); h=hashlib.sha256(request.form['senha'].encode()).hexdigest()
    try:
        c.execute("INSERT INTO users (nome,email,senha) VALUES (?,?,?)",(request.form['nome'],request.form['email'],h)); c.commit()
    except: return "Email ja existe! <a href='/'>Voltar</a>"
    return redirect("/")
@app.route("/login", methods=["POST"])
def login():
    c=db(); h=hashlib.sha256(request.form['senha'].encode()).hexdigest()
    u=c.execute("SELECT nome FROM users WHERE email=? AND senha=?",(request.form['email'],h)).fetchone()
    if u: session['user']=u[0]; return redirect("/")
    return "Email ou senha errada! <a href='/'>Voltar</a>"
@app.route("/sair")
def sair():
    session.clear(); return redirect("/")
if __name__=="__main__":
    app.run(host="0.0.0.0", port=10000)
