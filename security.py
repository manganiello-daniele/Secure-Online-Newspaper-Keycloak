from functools import wraps
from flask import abort, session, current_app
from flask_login import UserMixin, current_user
from kc_client import get_keycloak_openid


class KcUser(UserMixin):
    def __init__(self, sub: str, username: str):
        self.id = sub
        self.username = username


def require_permission(permission: str):
    """Chiede a Keycloak se l'utente ha la permission UMA 'resource#scope'."""

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                return abort(401)

            token = session.get("kc_token")
            if not token or "access_token" not in token:
                return abort(401)

            access_token = token["access_token"]
            keycloak_openid = get_keycloak_openid()
            try:
                auth_status = keycloak_openid.has_uma_access(access_token, [permission])
            except Exception as e:
                current_app.logger.exception(
                    f"Errore Keycloak has_uma_access({permission}): {e}"
                )
                return abort(500)

            if not auth_status.is_authorized:
                try:
                    perms = keycloak_openid.get_permissions(access_token)
                    current_app.logger.warning(
                        "Accesso negato per %s, permessi token: %s",
                        permission,
                        perms,
                    )
                except Exception:
                    current_app.logger.warning(
                        "Accesso negato per %s e impossibile leggere i permessi",
                        permission,
                    )
                return abort(403)

            return view_func(*args, **kwargs)

        return wrapper

    return decorator
