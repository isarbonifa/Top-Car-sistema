import re
from datetime import date, datetime

from flask import Blueprint, flash, redirect, render_template, request, session, url_for, current_app
from werkzeug.security import check_password_hash

from app.utils.auth_middleware import guest_required, login_required
from app.models.user_model import Usuario

auth_bp = Blueprint("auth", __name__)

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def data_valida(texto):
    try:
        d = datetime.strptime(texto, "%Y-%m-%d").date()
    except ValueError:
        return False
    return date(1900, 1, 1) <= d <= date.today()


@auth_bp.route("/login", methods=["GET", "POST"])
@guest_required
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Informe usuário e senha.", "danger")
            return render_template("auth/login.html")

        user = Usuario.get_by_username(username)

        if user and check_password_hash(user.password, password):
            # Limpa sessões anteriores e configura nova sessão com ID e nome
            session.clear()
            session.permanent = True
            session["user_id"] = user.id
            session["username"] = user.username

            # Mantém compatibilidade caso use 'user' em algum lugar antigo
            session["user"] = user.username

            current_app.logger.info(f"Login realizado com sucesso para o usuário: {username}")
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("main.welcome"))
        else:
            current_app.logger.warning(f"Falha de login para o usuário: {username}")
            flash("Usuário ou senha incorretos.", "danger")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    current_app.logger.info(f"Usuário desconectado: {session.get('username')}")
    session.clear()  # Encerra e limpa a sessão completamente
    flash("Você saiu da conta.", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/register", methods=["GET", "POST"])
@guest_required
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        email = request.form.get("email", "").strip().lower()
        data_nascimento = request.form.get("data_nascimento", "").strip()

        # Validação no servidor
        erro = None
        if not username or not password or not email:
            erro = "Preencha usuário, senha e e-mail."
        elif not (3 <= len(username) <= 30):
            erro = "O usuário deve ter entre 3 e 30 caracteres."
        elif " " in username:
            erro = "O usuário não pode conter espaços."
        elif len(password) < 6:
            erro = "A senha deve ter pelo menos 6 caracteres."
        elif not EMAIL_RE.match(email):
            erro = "Informe um e-mail válido."
        elif data_nascimento and not data_valida(data_nascimento):
            erro = "Data de nascimento inválida."

        if erro:
            flash(erro, "danger")
            return redirect(url_for("auth.register"))

        if Usuario.get_by_username(username):
            flash("Este usuário já existe.", "warning")
            return redirect(url_for("auth.register"))

        if Usuario.get_by_email(email):
            flash("Este e-mail já está cadastrado.", "warning")
            return redirect(url_for("auth.register"))

        novo_usuario = Usuario(
            username=username,
            password=password,
            email=email,
            data_nascimento=data_nascimento or None,
            foto=None,
        )
        novo_usuario.save()
        current_app.logger.info(f"Novo usuário cadastrado: {username}")

        flash("Cadastro realizado com sucesso! Faça login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")
