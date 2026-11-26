from flask import Flask, render_template, session, g
from datetime import timedelta
from app.models.user_model import Usuario
import logging
import mimetypes
mimetypes.add_type("application/wasm", ".wasm")


def create_app():
    app = Flask(
        __name__, template_folder="views/templates", static_folder="views/static"
    )

    app.secret_key = "sua_chave_secreta_super_segura"
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)

    from app.controllers.auth_controller import auth_bp
    from app.controllers.main_controller import main_bp
    from app.controllers.comentario_controller import comentarios_bp
    from app.controllers.sugestao_controller import sugestoes_bp
    from app.controllers.usuario_controller import usuarios_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(comentarios_bp)
    app.register_blueprint(sugestoes_bp)
    app.register_blueprint(usuarios_bp)

    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)

    @app.before_request
    def carregar_usuario_global():
        user_id = session.get("user_id")
        if user_id:
            # Valida no banco se o usuário realmente existe (exigência do professor)
            g.usuario = Usuario.get_by_id(user_id)
        else:
            g.usuario = None

    
    @app.errorhandler(404)
    def pagina_nao_encontrada(e):
        app.logger.warning(f"Tentativa de acesso a página inexistente: {e}")
        return render_template("404.html"), 404

    return app