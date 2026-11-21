from flask import Flask, request, redirect, url_for, session, render_template_string
import os

app = Flask(__name__)
app.secret_key = "angotrader-secreto-123"

# Base de dados simples na memória
users = {}

HTML = """
<!DOCTYPE html>
<html lang="pt">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AngoTrader - Negocia como os grandes</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box;font-family:Arial,sans-serif}
  body{background:#0a0a0a;color:white;min-height:100vh}
  .top{padding:15px 20px;display:flex;justify-content:space-between;align-items:center}
  .logo{font-weight:900;font-size:22px}
  .logo span{color:#FFD700}
  .btn-yellow{background:#FFD700;color:black;padding:10px 18px;border-radius:25px;font-weight:800;border:none;cursor:pointer;text-decoration:none;font-size:14px}
  .btn-outline{border:1px solid #333;padding:10px 18px;border-radius:25px;color:white;text-decoration:none;font-size:14px}
  .hero{padding:30px 20px;text-align:center}
  .hero h1{font-size:32px;line-height:1.2}
  .hero h1 span{color:#FFD700}
  .hero p{color:#aaa;margin:15px 0 25px}
  .card{background:#141414;border:1px solid #222;border-radius:20px;padding:20px;margin:20px;text-align:left}
  .price{font-size:28px;font-weight:900}
  .up{color:#00ff88}
  .signal{margin-top:15px;background:#1a1a00;border:1px solid #FFD700;padding:15px;border-radius:15px}
  .form-box{max-width:400px;margin:20px auto;background:#141414;padding:25px;border-radius:20px}
  input{width:100%;padding:13px;border-radius:12px;border:1px solid #333;background:#0a0a0a;color:white;margin-top:8px;margin-bottom:12px;outline:none;font-size:15px}
  .pass-wrap{position:relative}
  .pass-wrap input{padding-right:45px}
  .eye{position:absolute;right:12px;top:19px;cursor:pointer;font-size:18px;background:none;border:none}
  label{font-size:13px;color:#aaa}
  .full{width:100%;padding:14px;border-radius:25px;background:#FFD700;border:none;font-weight:900;cursor:pointer;font-size:15px}
  a{color:#FFD700}
</style>
</head>
<body>
<div class="top">
  <div class="logo">⚡ ANGO<span>TRADER</span></div>
  <div>
    {% if session.get('user') %}
      <span style="font-size:13px">Olá, {{ session.get('user') }}</span>
      <a href="/logout" class="btn-outline" style="margin-left:10px">Sair</a>
    {% else %}
      <a href="/login" class="btn-outline">Entrar</a>
      <a href="/register" class="btn-yellow" style="margin-left:8px">Criar Conta</a>
    {% endif %}
  </div>
</div>

{% if page == 'home' %}
<div class="hero">
  <h1>Negocia como os grandes.<br><span>Opera como angolano.</span></h1>
  <p>Sinais, gráficos e trading simplificado para Angola.</p>
  <a href="/register" class="btn-yellow" style="display:inline-block;padding:14px 28px">Criar Conta Grátis →</a>
</div>
<div class="card">
  <div style="display:flex;justify-content:space-between"><b>₿ BTC / USDT</b><span class="up">+2.4% ↗</span></div>
  <div class="price" style="margin-top:10px">$97,450</div>
  <div style="color:#888;font-size:13px;margin-top:5px">Bitcoin • Gráfico ao vivo</div>
  <div style="background:#222;height:60px;border-radius:10px;margin-top:15px;display:flex;align-items:flex-end;gap:4px;padding:8px">
    <div style="background:#FFD700;width:100%;height:30%"></div>
    <div style="background:#FFD700;width:100%;height:45%"></div>
    <div style="background:#FFD700;width:100%;height:35%"></div>
    <div style="background:#FFD700;width:100%;height:60%"></div>
    <div style="background:#FFD700;width:100%;height:80%"></div>
    <div style="background:#FFD700;width:100%;height:95%"></div>
  </div>
  <div class="signal">
    <b>🔥 Sinal de Hoje - EGGY</b><br>
    <span style="font-size:13px;color:#ccc">COMPRAR BTC • Confiança 87%</span>
  </div>
</div>
{% endif %}

{% if page == 'register' %}
<div class="form-box">
  <h2>Criar Conta Grátis</h2>
  <p style="color:#aaa;font-size:13px;margin:8px 0 20px">Junta-te à comunidade AngoTrader</p>
  {% if erro %}<p style="color:#ff5555;margin-bottom:10px">{{ erro }}</p>{% endif %}
  <form method="POST">
    <label>Nome</label><input name="nome" placeholder="Teu nome" required>
    <label>Email</label><input name="email" type="email" placeholder="teu@email.com" required>
    <label>Senha</label>
    <div class="pass-wrap">
      <input id="senha1" name="senha" type="password" placeholder="Cria uma senha" required>
      <button type="button" class="eye" onclick="verSenha('senha1', this)">👁️</button>
    </div>
    <button class="full">Criar Conta →</button>
  </form>
  <p style="text-align:center;margin-top:15px;font-size:13px">Já tens conta? <a href="/login">Entrar</a></p>
</div>
{% endif %}

{% if page == 'login' %}
<div class="form-box">
  <h2>Bem-vindo de volta 👋</h2>
  <p style="color:#aaa;font-size:13px;margin:8px 0 20px">Entra para ver os sinais de hoje</p>
  {% if erro %}<p style="color:#ff5555;margin-bottom:10px">{{ erro }}</p>{% endif %}
  <form method="POST">
    <label>Email</label><input name="email" type="email" placeholder="teu@email.com" required>
    <label>Senha</label>
    <div class="pass-wrap">
      <input id="senha2" name="senha" type="password" placeholder="Tua senha" required>
      <button type="button" class="eye" onclick="verSenha('senha2', this)">👁️</button>
    </div>
    <button class="full">Entrar →</button>
  </form>
  <p style="text-align:center;margin-top:15px;font-size:13px">Não tens conta? <a href="/register">Criar Conta</a></p>
</div>
{% endif %}

<script>
function verSenha(id, btn){
  var campo = document.getElementById(id);
  if(campo.type === "password"){
    campo.type = "text";
    btn.textContent = "🙈";
  } else {
    campo.type = "password";
    btn.textContent = "👁️";
  }
}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML, page="home")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email","").lower().strip()
        senha = request.form.get("senha")
        if email in users:
            return render_template_string(HTML, page="register", erro="Este email já tem conta. Faz login.")
        users[email] = {"nome": nome, "senha": senha}
        session["user"] = nome
        return redirect(url_for("home"))
    return render_template_string(HTML, page="register", erro=None)

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email","").lower().strip()
        senha = request.form.get("senha")
        u = users.get(email)
        if u and u["senha"] == senha:
            session["user"] = u["nome"]
            return redirect(url_for("home"))
        return render_template_string(HTML, page="login", erro="Email ou senha errada. Tenta de novo.")
    return render_template_string(HTML, page="login", erro=None)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
