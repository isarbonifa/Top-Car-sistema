from functools import wraps
from flask import flash, g, redirect, session, url_for

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Se não tem user_id na sessão OU o g.usuario não foi carregado corretamente
        if "user_id" not in session or not g.get("usuario"):
            session.clear() # Limpa resíduos para evitar loop
            flash("Faça login para acessar esta página.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function


def guest_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Se já está logado, manda para o welcome (nunca para o login)
        if "user_id" in session and g.get("usuario"):
            return redirect(url_for("main.welcome"))
        return f(*args, **kwargs)
    return decorated_function