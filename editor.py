from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user

from models import db, Article, User
from security import require_permission


editor_bp = Blueprint("editor", __name__)


def _get_or_create_current_author():
    autore = User.query.filter_by(keycloak_id=current_user.id).first()
    if not autore:
        autore = User(keycloak_id=current_user.id, username=current_user.username)
        db.session.add(autore)
        db.session.commit()
    return autore


@editor_bp.route("/editor")
@login_required
@require_permission("editor-dashboard#view")
def editor_dashboard():
    autore = _get_or_create_current_author()
    articoli = Article.query.filter_by(autore=autore).order_by(Article.id.desc()).all()
    return render_template("editor_dashboard.html", articoli=articoli)


@editor_bp.route("/editor/nuovo", methods=["GET", "POST"])
@login_required
@require_permission("article#create")
def nuovo_articolo():
    if request.method == "POST":
        titolo = request.form["titolo"]
        contenuto = request.form["contenuto"]
        autore = _get_or_create_current_author()
        new_article = Article(titolo=titolo, contenuto=contenuto, autore=autore)
        db.session.add(new_article)
        db.session.commit()
        return redirect(url_for("editor.editor_dashboard"))
    return render_template("editor_nuovo.html")


@editor_bp.route("/editor/articolo/<int:id>/modifica", methods=["GET", "POST"])
@login_required
@require_permission("article#edit")
def modifica_articolo(id):
    articolo = Article.query.get_or_404(id)
    autore = _get_or_create_current_author()
    if articolo.autore_id != autore.id:
        abort(403)

    if request.method == "POST":
        articolo.titolo = request.form["titolo"]
        articolo.contenuto = request.form["contenuto"]
        db.session.commit()
        return redirect(url_for("editor.editor_dashboard"))

    return render_template("editor_modifica.html", articolo=articolo)


@editor_bp.route("/editor/articolo/<int:id>/elimina", methods=["POST"])
@login_required
@require_permission("article#delete")
def elimina_articolo(id):
    articolo = Article.query.get_or_404(id)
    db.session.delete(articolo)
    db.session.commit()
    return redirect(url_for("editor.editor_dashboard"))
