import os
from flask import Flask
from flask_socketio import SocketIO
from models.database import db
from controllers import routes, chat

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, template_folder="views", static_folder="static")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "troque-esta-chave-em-producao")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "models", "rede_social.sqlite3")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = os.path.join(BASE_DIR, "static", "uploads")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

db.init_app(app)
routes.init_app(app)
chat.init_app(socketio)

with app.app_context():
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, "models"), exist_ok=True)
    db.create_all()

if __name__ == "__main__":
    socketio.run(app, host="127.0.0.1", port=5000, debug=True)
