from flask import Flask, send_file, request, jsonify
import time
import os

app = Flask(__name__)

ultimo_valor = 0
ultimo_recebimento = 0

@app.route("/")
def index():
    return send_file("index.html")

@app.route("/dados", methods=["POST"])
def receber_dados():
    global ultimo_valor, ultimo_recebimento

    dados = request.get_json()
    ultimo_valor = int(dados.get("valor", 0))
    ultimo_recebimento = time.time()

    return jsonify({"ok": True})

@app.route("/status")
def status():
    online = (time.time() - ultimo_recebimento) < 4

    return jsonify({
        "online": online,
        "valor": ultimo_valor
    })

if __name__ == "__main__":
    porta = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=porta)
# forcar novo deploy
