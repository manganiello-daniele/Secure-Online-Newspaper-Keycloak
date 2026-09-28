import os

from flask import Flask, render_template, session
from flask_login import LoginManager

from models import db, Article
from reader import reader_bp
from auth import auth
from admin import admin_bp
from editor import editor_bp
from oauth_client import oauth
from security import KcUser


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "dev-only-change-me")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "SQLALCHEMY_DATABASE_URI", "sqlite:///giornale.db"
)

# ---- Keycloak configuration ----
app.config["KEYCLOAK_BASE_URL"] = os.environ.get("KEYCLOAK_BASE_URL", "http://localhost:8180")
app.config["KEYCLOAK_REALM"] = os.environ.get("KEYCLOAK_REALM", "giornale")
app.config["KEYCLOAK_CLIENT_ID"] = os.environ.get("KEYCLOAK_CLIENT_ID", "giornale-flask")
app.config["KEYCLOAK_CLIENT_SECRET"] = os.environ.get("KEYCLOAK_CLIENT_SECRET")

# ---- Extensions ----
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "auth.login_page"

oauth.init_app(app)
oauth.register(
    name="keycloak",
    client_id=app.config["KEYCLOAK_CLIENT_ID"],
    client_secret=app.config["KEYCLOAK_CLIENT_SECRET"],
    server_metadata_url=(
        f"{app.config['KEYCLOAK_BASE_URL']}"
        f"/realms/{app.config['KEYCLOAK_REALM']}/.well-known/openid-configuration"
    ),
    client_kwargs={"scope": "openid profile email"},
)

app.register_blueprint(reader_bp)
app.register_blueprint(auth)
app.register_blueprint(admin_bp)
app.register_blueprint(editor_bp)


@login_manager.user_loader
def load_user(user_id: str):
    data = session.get("kc_user")
    if not data or data.get("sub") != user_id:
        return None
    return KcUser(sub=data["sub"], username=data["username"])


@app.route("/")
def home():
    articoli = Article.query.filter_by(approved=True).order_by(Article.created_at.desc()).all()
    return render_template("home.html", articoli=articoli)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=5000, debug=True)
