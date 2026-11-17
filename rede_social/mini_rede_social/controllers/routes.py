import os
import uuid
from functools import wraps
from flask import render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models.database import db, Usuario, Post

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash("Faça login para acessar essa página.", "warning")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped

def init_app(app):
    @app.before_request
    def protect_routes():
        protected = ("/feed", "/upload", "/chat")
        if request.path.startswith(protected) and "user_id" not in session:
            flash("Entre na sua conta para continuar.", "warning")
            return redirect(url_for("login"))

    @app.route("/")
    def index():
        return redirect(url_for("feed" if "user_id" in session else "login"))

    @app.route("/cadastro", methods=["GET", "POST"])
    def cadastro():
        if request.method == "POST":
            nome = request.form.get("nome", "").strip()
            email = request.form.get("email", "").strip().lower()
            senha = request.form.get("senha", "")
            if not nome or not email or not senha:
                flash("Preencha todos os campos.", "danger")
                return render_template("cadastro.html")
            if len(senha) < 6:
                flash("A senha precisa ter pelo menos 6 caracteres.", "danger")
                return render_template("cadastro.html")
            if Usuario.query.filter_by(email=email).first():
                flash("Este e-mail já está cadastrado.", "danger")
                return render_template("cadastro.html")
            usuario = Usuario(nome=nome, email=email,
                              senha=generate_password_hash(senha, method="scrypt"))
            db.session.add(usuario)
            db.session.commit()
            flash("Cadastro realizado! Agora faça seu login.", "success")
            return redirect(url_for("login"))
        return render_template("cadastro.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form.get("email", "").strip().lower()
            senha = request.form.get("senha", "")
            usuario = Usuario.query.filter_by(email=email).first()
            if usuario and check_password_hash(usuario.senha, senha):
                session.clear()
                session["user_id"] = usuario.id
                session["usuario_nome"] = usuario.nome
                session["usuario_email"] = usuario.email
                flash(f"Bem-vindo(a), {usuario.nome}!", "success")
                return redirect(url_for("feed"))
            flash("E-mail ou senha incorretos.", "danger")
        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        flash("Você saiu da sua conta.", "info")
        return redirect(url_for("login"))

    @app.route("/feed")
    @login_required
    def feed():
        posts = Post.query.order_by(Post.data_criacao.desc()).all()
        return render_template("feed.html", posts=posts)

    @app.route("/upload", methods=["POST"])
    @login_required
    def upload():
        arquivo = request.files.get("file")
        legenda = request.form.get("legenda", "").strip()
        if not arquivo or arquivo.filename == "":
            flash("Selecione uma imagem.", "danger")
            return redirect(url_for("feed"))
        if not allowed_file(arquivo.filename):
            flash("Formato inválido. Use PNG, JPG, JPEG ou GIF.", "danger")
            return redirect(url_for("feed"))
        original = secure_filename(arquivo.filename)
        extensao = original.rsplit(".", 1)[1].lower()
        nome_arquivo = f"{uuid.uuid4().hex}.{extensao}"
        caminho = os.path.join(current_app.config["UPLOAD_FOLDER"], nome_arquivo)
        arquivo.save(caminho)
        post = Post(imagem=nome_arquivo, legenda=legenda[:255], usuario_id=session["user_id"])
        db.session.add(post)
        db.session.commit()
        flash("Sua publicação foi enviada!", "success")
        return redirect(url_for("feed"))

    @app.route("/chat")
    @login_required
    def chat_page():
        return render_template("chat.html")
