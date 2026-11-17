from flask import session, request
from flask_socketio import emit

def init_app(socketio):
    @socketio.on("connect")
    def on_connect():
        if "user_id" not in session:
            return False

    @socketio.on("join")
    def on_join():
        if "user_id" not in session:
            return
        nome = session.get("usuario_nome", "Usuário")
        emit("showmsg", {"usuario": "Sistema", "mensagem": f"{nome} entrou no chat."}, broadcast=True)

    @socketio.on("msg")
    def on_message(data):
        if "user_id" not in session:
            return
        mensagem = (data.get("mensagem") or "").strip()[:500]
        if not mensagem:
            return
        emit("showmsg", {
            "usuario": session.get("usuario_nome", "Usuário"),
            "mensagem": mensagem
        }, broadcast=True)
