from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.sql import func

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keycloak_id = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titolo = db.Column(db.String(200), nullable=False)
    contenuto = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    autore_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    autore = db.relationship("User", foreign_keys=[autore_id], backref="articoli")

    approved = db.Column(db.Boolean, default=False, nullable=False)
    approved_by_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    approved_by = db.relationship("User", foreign_keys=[approved_by_id], backref="articoli_approvati")

    def snippet(self, length=160):
        if not self.contenuto:
            return ""
        return (self.contenuto[:length] + "…") if len(self.contenuto) > length else self.contenuto
