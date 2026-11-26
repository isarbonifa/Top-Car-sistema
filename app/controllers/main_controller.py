from flask import Blueprint, render_template, session
from app.utils.auth_middleware import guest_required, login_required

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@guest_required
def home():
    return render_template("main/home.html")


@main_bp.route("/welcome")
@login_required
def welcome():
    current_user = session.get("user")
    return render_template("main/welcome.html", username=current_user)


@main_bp.route("/jogo")
@login_required
def jogo():
    return render_template("main/jogo.html")
