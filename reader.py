from flask import Blueprint, render_template, abort, session
from flask_login import login_required

from models import Article
from kc_client import get_keycloak_openid

reader_bp = Blueprint("reader", __name__)


@reader_bp.route("/articolo/<int:id>")
@login_required
def leggi_articolo(id):
    articolo = Article.query.get_or_404(id)

    token = session.get("kc_token")
    if not token or "access_token" not in token:
        abort(401)

    access_token = token["access_token"]
    keycloak_openid = get_keycloak_openid()

    full_status = keycloak_openid.has_uma_access(access_token, "article#full")
    if full_status.is_authorized:
        view_mode = "full"
    else:
        preview_status = keycloak_openid.has_uma_access(access_token, "article#preview")
        if not preview_status.is_authorized:
            abort(403)
        view_mode = "preview"

    if not articolo.approved and view_mode == "preview":
        abort(403)

    return render_template("articolo.html", articolo=articolo, view_mode=view_mode)
