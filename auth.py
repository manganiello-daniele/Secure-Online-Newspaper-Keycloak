from flask import Blueprint, redirect, url_for, session, current_app, render_template
from flask_login import login_user, logout_user, login_required
from oauth_client import oauth
from security import KcUser


auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    redirect_uri = url_for("auth.callback", _external=True)
    return oauth.keycloak.authorize_redirect(redirect_uri)


@auth.route("/auth/callback")
def callback():
    token = oauth.keycloak.authorize_access_token()

    try:
        userinfo = oauth.keycloak.parse_id_token(token)
    except Exception:
        userinfo = oauth.keycloak.userinfo()

    sub = userinfo.get("sub")
    username = userinfo.get("preferred_username") or userinfo.get("email") or sub

    session["kc_token"] = token
    session["kc_user"] = {"sub": sub, "username": username}

    user = KcUser(sub=sub, username=username)
    login_user(user)
    return redirect(url_for("home"))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()

    base_url = current_app.config["KEYCLOAK_BASE_URL"]
    realm = current_app.config["KEYCLOAK_REALM"]
    client_id = current_app.config["KEYCLOAK_CLIENT_ID"]
    redirect_uri = url_for("home", _external=True)

    logout_url = (
        f"{base_url}/realms/{realm}/protocol/openid-connect/logout"
        f"?client_id={client_id}"
        f"&post_logout_redirect_uri={redirect_uri}"
        f"&logout_redirect_uri={redirect_uri}"
    )
    return redirect(logout_url)


@auth.route("/login-page")
def login_page():
    return render_template("login.html")
