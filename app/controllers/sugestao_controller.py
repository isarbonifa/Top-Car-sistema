from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for

from app.utils.auth_middleware import login_required
from app.models.sugestao_model import Sugestao

sugestoes_bp = Blueprint("sugestoes", __name__)


@sugestoes_bp.route("/sugestoes", methods=["GET", "POST"])
@login_required
def sugestoes():
    user_id = session.get("user_id")
    current_username = session.get("username")
    is_admin = (current_username == "admin")

    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        texto = request.form.get("texto", "").strip()

        if not titulo or not texto:
            flash("Preencha o título e o texto da sugestão.", "danger")
            return redirect(url_for("sugestoes.sugestoes"))

        nova_sugestao = Sugestao(
            usuario_id=user_id,
            username=current_username,
            titulo=titulo,
            texto=texto,
        )
        nova_sugestao.save()
        current_app.logger.info(f"Sugestão criada pelo usuário: {current_username}")
        flash("Sugestão enviada com sucesso!", "success")
        return redirect(url_for("sugestoes.sugestoes"))

    # Admin vê todas; usuário comum vê só as suas
    if is_admin:
        lista_sugestoes = Sugestao.get_all()
    else:
        lista_sugestoes = Sugestao.get_by_usuario(user_id)

    return render_template("sugestoes/sugestoes.html", sugestoes=lista_sugestoes, is_admin=is_admin)


@sugestoes_bp.route("/sugestoes/excluir/<int:id>", methods=["POST"])
@login_required
def excluir_sugestao(id):
    user_id = session.get("user_id")
    is_admin = (session.get("username") == "admin")

    Sugestao.delete(id, user_id, is_admin=is_admin)
    flash("Sugestão removida com sucesso.", "info")
    return redirect(url_for("sugestoes.sugestoes"))
