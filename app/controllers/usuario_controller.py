import os

from flask import (Blueprint, abort, current_app, flash, g, make_response,
                   redirect, render_template, request, url_for)
from werkzeug.utils import secure_filename

from app.controllers.auth_controller import EMAIL_RE, data_valida
from app.utils.auth_middleware import login_required
from app.models.user_model import Usuario

usuarios_bp = Blueprint("usuarios", __name__)

EXT_FOTO = {"png", "jpg", "jpeg", "gif", "webp", "avif", "jfif"}


@usuarios_bp.route("/usuarios")
@login_required
def listar_usuarios():
    """Rota de listagem exigida pelo projeto"""
    usuarios = Usuario.get_all()
    return render_template("usuarios/listar.html", usuarios=usuarios)


@usuarios_bp.route("/perfil", methods=["GET", "POST"])
@login_required
def perfil():
    # g.usuario já foi carregado pelo middleware global
    user = g.usuario

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        data_nascimento = request.form.get("data_nascimento", "").strip()
        foto_file = request.files.get("foto")

        erro = None
        outro = Usuario.get_by_email(email) if email else None
        if not email or not EMAIL_RE.match(email):
            erro = "Informe um e-mail válido."
        elif outro and outro.id != user.id:
            erro = "Este e-mail já está em uso por outro usuário."
        elif data_nascimento and not data_valida(data_nascimento):
            erro = "Data de nascimento inválida."
        elif foto_file and foto_file.filename and \
                foto_file.filename.rsplit(".", 1)[-1].lower() not in EXT_FOTO:
            erro = "Formato de imagem não permitido."

        if erro:
            flash(erro, "danger")
            return redirect(url_for("usuarios.perfil"))

        user.email = email
        user.data_nascimento = data_nascimento or None

        # Upload de foto de perfil
        if foto_file and foto_file.filename != "":
            upload_folder = os.path.join(current_app.static_folder, "uploads")
            os.makedirs(upload_folder, exist_ok=True)

            # secure_filename evita nomes maliciosos (ex.: "../../app.py")
            filename = f"user_{user.id}_{secure_filename(foto_file.filename)}"
            foto_file.save(os.path.join(upload_folder, filename))

            user.foto = filename

        user.atualizar_perfil()
        current_app.logger.info(f"Perfil atualizado para o usuário: {user.username}")
        flash("Perfil atualizado com sucesso!", "success")
        return redirect(url_for("usuarios.perfil"))

    # COOKIES: lê a preferência de tema salva no navegador
    modo_visualizacao = request.cookies.get("tema_preferido", "tema-escuro")

    return render_template("usuarios/perfil.html", user=user, modo_visualizacao=modo_visualizacao)


@usuarios_bp.route("/perfil/<int:user_id>")
@login_required
def ver_perfil_usuario(user_id):
    usuario_alvo = Usuario.get_by_id(user_id)
    if not usuario_alvo:
        abort(404)  # Aciona a página 404.html personalizada
    return render_template("usuarios/perfil_publico.html", usuario=usuario_alvo)


@usuarios_bp.route("/mudar-preferencia-cookie", methods=["POST"])
@login_required
def mudar_preferencia_cookie():
    resposta = make_response(redirect(url_for("usuarios.perfil")))

    # Recebe 'tema-escuro' ou 'tema-claro'
    novo_tema = request.form.get("tema", "tema-escuro")
    resposta.set_cookie("tema_preferido", novo_tema, max_age=60 * 60 * 24 * 30)

    flash("Preferência de tema salva com sucesso!", "success")
    return resposta
