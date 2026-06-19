from flask import Flask, send_file, request, jsonify
from flask_socketio import SocketIO
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

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

    socketio.emit("novo_valor", {
        "valor": ultimo_valor,
        "online": True
    })

    return jsonify({"ok": True})

def verificar_offline():
    global ultimo_recebimento

    while True:
        online = (time.time() - ultimo_recebimento) < 3

        socketio.emit("status", {
            "online": online,
            "valor": ultimo_valor
        })

        socketio.sleep(1)

if __name__ == "__main__":
    socketio.start_background_task(verificar_offline)
    socketio.run(app, host="0.0.0.0", port=5000)