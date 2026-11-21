from flask import Flask, request, redirect, session
import sqlite3, hashlib
app = Flask(__name__)
app.secret_key = "angotrader-segredo"

def db():
    c = sqlite3.connect("users.db")
    c.execute("CREATE TABLE IF NOT EXISTS users (nome TEXT, email TEXT PRIMARY KEY, senha TEXT)")
    return c

HTML = """<!DOCTYPE html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'><style>
body{background:#0a0a0a;color:white;font-family:Arial;text-align:center;padding:20px}
.box{background:#1a1a1a;padding:20px;border-radius:15px;max-width:350px;margin:auto}
input{width:90%;padding:12px;margin:8px;border-radius:8px;border:none}
button{width:95%;padding:13px;background:#FFD700;border:none;border-radius:8px;font-weight:bold;font-size:16px}
a{color:#FFD700}
</style></head><body>
<h1 style='color:#FFD700'>ANGOTRADER</h1>
<div class='box'><h2>Entrar</h2>
<form action='/login' method='post'>
<input name='email' placeholder='Email' required><br>
<input name='senha' type='password' placeholder='Senha' required><br>
<button>ENTRAR</button></form>
<p><a href='/cadastro'>Criar conta</a></p></div></body></html>"""

HTML2 = """<!DOCTYPE html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'><style>
body{background:#0a0a0a;color:white;font-family:Arial;text-align:center;padding:20px}
.box{background:#1a1a1a;padding:20px;border-radius:15px;max-width:350px;margin:auto}
input{width:90%;padding:12px;margin:8px;border-radius:8px;border:none}
button{width:95%;padding:13px;background:#FFD700;border:none;border-radius:8px;font-weight:bold;font-size:16px}
a{color:#FFD700}
</style></head><body>
<h1 style='color:#FFD700'>ANGOTRADER</h1>
<div class='box'><h2>Criar Conta</h2>
<form action='/criar' method='post'>
<input name='nome' placeholder='Nome' required><br>
<input name='email' placeholder='Email' required><br>
<input name='senha' type='password' placeholder='Senha' required><br>
<button>CRIAR CONTA</button></form>
<p><a href='/'>Voltar</a></p></div></body></html>"""

@app.route("/")
def home():
    if "user" in session:
        return f"<h1 style='text-align:center;font-family:Arial'>Bem-vindo, {session['user']}!</h1><p style='text-align:center'><a href='/sair'>Sair</a></p>"
    return HTML

@app.route("/cadastro")
def cadastro():
    return HTML2

@app.route("/criar", methods=["POST"])
def criar():
    c = db()
    try:
        c.execute("INSERT INTO users VALUES (?,?,?)", (request.form["nome"], request.form["email"], hashlib.sha256(request.form["senha"].encode()).hexdigest()))
        c.commit()
    except:
        return "Email ja existe! <a href='/cadastro'>Voltar</a>"
    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    c = db()
    s = hashlib.sha256(request.form["senha"].encode()).hexdigest()
    u = c.execute("SELECT nome FROM users WHERE email=? AND senha=?", (request.form["email"], s)).fetchone()
    if u:
        session["user"] = u[0]
        return redirect("/")
    return "Email ou senha errada! <a href='/'>Voltar</a>"

@app.route("/sair")
def sair():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
