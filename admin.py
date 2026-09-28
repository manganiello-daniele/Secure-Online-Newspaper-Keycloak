from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

from models import db, Article, User
from security import require_permission

admin_bp = Blueprint("admin", __name__)


def _get_or_create_current_user():
    u = User.query.filter_by(keycloak_id=current_user.id).first()
    if not u:
        u = User(keycloak_id=current_user.id, username=current_user.username)
        db.session.add(u)
        db.session.commit()
    return u


@admin_bp.route("/admin")
@login_required
@require_permission("admin-dashboard#view")
def admin_dashboard():
    non_approvati = Article.query.filter_by(approved=False).count()
    return render_template("admin_dashboard.html", non_approvati=non_approvati)


@admin_bp.route("/admin/articoli-da-approvare")
@login_required
@require_permission("article#approve")
def articoli_da_approvare():
    articoli = Article.query.filter_by(approved=False).order_by(Article.created_at.desc()).all()
    return render_template("admin_articoli.html", articoli=articoli)


@admin_bp.route("/admin/articolo/<int:id>/approva", methods=["POST"])
@login_required
@require_permission("article#approve")
def approva_articolo(id):
    articolo = Article.query.get_or_404(id)
    admin_user = _get_or_create_current_user()
    articolo.approved = True
    articolo.approved_by = admin_user
    db.session.commit()
    return redirect(url_for("admin.articoli_da_approvare"))
