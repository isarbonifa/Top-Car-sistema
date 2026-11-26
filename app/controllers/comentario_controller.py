from flask import Blueprint, current_app, flash, g, redirect, render_template, request, session, url_for

from app.utils.auth_middleware import login_required
from app.models.comment_model import Comentario

comentarios_bp = Blueprint("comentarios", __name__)

TEXTO_MIN = 2
TEXTO_MAX = 500


def validar_texto(texto):
    """Retorna mensagem de erro ou None se o texto for válido."""
    if not texto:
        return "O comentário não pode ficar vazio."
    if len(texto) < TEXTO_MIN:
        return f"O comentário deve ter pelo menos {TEXTO_MIN} caracteres."
    if len(texto) > TEXTO_MAX:
        return f"O comentário deve ter no máximo {TEXTO_MAX} caracteres."
    return None


@comentarios_bp.route("/comentarios", methods=["GET", "POST"])
@login_required
def comentarios():
    user_id = session.get("user_id")
    username = g.usuario.username
    is_admin = (username == "admin")
    comentario_em_edicao = None
    edit_id = request.args.get("edit_id", type=int)

    if edit_id:
        c = Comentario.get_by_id(edit_id)
        if c and c.usuario_id == user_id:
            comentario_em_edicao = c

    if request.method == "POST":
        texto = request.form.get("texto", "").strip()
        comment_id = request.form.get("comment_id", type=int)

        erro = validar_texto(texto)
        if erro:
            flash(erro, "danger")
            return redirect(url_for("comentarios.comentarios", edit_id=comment_id))

        if comment_id:
            # Edição: o filtro por usuario_id fica no Model
            if Comentario.update(comment_id, user_id, texto):
                current_app.logger.info(f"Comentário {comment_id} editado por {username}")
                flash("Comentário editado com sucesso!", "success")
            else:
                current_app.logger.warning(f"Edição negada do comentário {comment_id} para {username}")
                flash("Você não pode editar este comentário.", "danger")
        else:
            Comentario(usuario_id=user_id, username=username, texto=texto).save()
            current_app.logger.info(f"Comentário criado por {username}")
            flash("Comentário publicado!", "success")

        return redirect(url_for("comentarios.comentarios"))

    return render_template(
        "comentarios/comentarios.html",
        user_id=user_id,
        is_admin=is_admin,
        comentarios=Comentario.get_all(),
        comentario_em_edicao=comentario_em_edicao,
    )


@comentarios_bp.route("/comentarios/excluir/<int:id>", methods=["POST"])
@login_required
def excluir_comentario(id):
    user_id = session.get("user_id")
    is_admin = (session.get("username") == "admin")

    if Comentario.delete(id, user_id, is_admin=is_admin):
        current_app.logger.info(f"Comentário {id} excluído por {session.get('username')}")
        flash("Comentário excluído com sucesso.", "info")
    else:
        current_app.logger.warning(f"Exclusão negada do comentário {id} para {session.get('username')}")
        flash("Você não tem permissão para excluir este comentário.", "danger")
    return redirect(url_for("comentarios.comentarios"))
