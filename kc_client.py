from flask import current_app
from keycloak import KeycloakOpenID


def get_keycloak_openid():
    """Restituisce un client KeycloakOpenID configurato per questo progetto.

    Usa i parametri presenti in app.config.
    """
    base_url = current_app.config["KEYCLOAK_BASE_URL"]
    realm = current_app.config["KEYCLOAK_REALM"]
    client_id = current_app.config["KEYCLOAK_CLIENT_ID"]
    client_secret = current_app.config["KEYCLOAK_CLIENT_SECRET"]

    return KeycloakOpenID(
        server_url=base_url + "/",
        realm_name=realm,
        client_id=client_id,
        client_secret_key=client_secret,
    )
