from flask import Flask, render_template_string
import os
from datetime import datetime
import pytz

app = Flask(__name__)

# Timezone Luanda
TZ = pytz.timezone("Africa/Luanda")

HTML = """
<!DOCTYPE html>
<html lang="pt">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AngoTrader</title>
<style>
body{margin:0;font-family:Arial,sans-serif;background:#0f172a;color:white;text-align:center;padding:20px}
.card{background:#1e293b;border-radius:15px;padding:20px;max-width:450px;margin:20px auto}
h1{color:#facc15}
.price{font-size:42px;font-weight:bold;color:#22c55e}
.closed{background:#ef4444;padding:10px;border-radius:10px;font-weight:bold}
.btn{background:#facc15;color:black;padding:12px 20px;border:none;border-radius:10px;font-weight:bold;font-size:16px;margin-top:15px}
small{color:#94a3b8}
</style>
</head>
<body>
<h1>👑 AngoTrader</h1>
<p>Data: {{ data }} | Hora Luanda: {{ hora }}</p>

<div class="card">
<h2>EUR/USD</h2>
<div class="price">{{ preco }}</div>
<p>{{ status }}</p>
{% if fechado %}
<div class="closed">MERCADO FECHADO</div>
<p>O mercado abre Segunda-feira às 00:00</p>
{% else %}
<p>Mercado Aberto</p>
{% endif %}
<button class="btn" onclick="alert('AngoTrader - Em breve!')">Negociar Agora</button>
</div>
<p><small>AngoTrader - Feito em Angola 🇦🇴</small></p>
</body>
</html>
"""

@app.route("/")
def home():
    agora = datetime.now(TZ)
    data = agora.strftime("%d/%m/%Y")
    hora = agora.strftime("%H:%M:%S")
    # Mercado fechado sabado e domingo
    fechado = agora.weekday() >= 5
    preco = "1.0845"
    status = "MERCADO FECHADO - Fim de semana" if fechado else "Ao vivo"
    return render_template_string(HTML, data=data, hora=hora, preco=preco, status=status, fechado=fechado)

@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
