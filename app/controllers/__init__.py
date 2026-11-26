from app.controllers.main_controller import main_bp
from app.controllers.auth_controller import auth_bp
from app.controllers.usuario_controller import usuarios_bp
from app.controllers.comentario_controller import comentarios_bp
from app.controllers.sugestao_controller import sugestoes_bp


def register_blueprints(app):
    """Registra todos os blueprints (sem url_prefix: as URLs continuam as mesmas)."""
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(comentarios_bp)
    app.register_blueprint(sugestoes_bp)
