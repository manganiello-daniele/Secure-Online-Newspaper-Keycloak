# Secure Online Newspaper with Keycloak

Academic web-security project implementing an online newspaper with **Flask** and centralized authentication/authorization through **Keycloak**.

The application separates reader, editor and administrator functionality and uses Keycloak OpenID Connect for authentication together with UMA-style authorization checks for protected actions and article access.

## Features

- Keycloak-based login and logout using OpenID Connect
- Role/permission-aware reader, editor and administrator areas
- Article creation, editing, approval and publication workflow
- Fine-grained authorization checks through Keycloak UMA permissions
- SQLAlchemy persistence layer
- Example XACML policy for authorization rules
- LDAP seed data for example users and attributes
- Optional HashiCorp Vault integration for runtime secrets

## Architecture

```text
Browser
  |
  v
Flask application
  |-- Authentication ---> Keycloak / OIDC
  |-- Authorization ----> Keycloak UMA
  |-- Persistence ------> SQLite / SQLAlchemy
  |-- Optional secrets -> HashiCorp Vault
  |
  +-- Reader / Editor / Admin blueprints
```

## Project structure

```text
.
├── app.py
├── auth.py
├── admin.py
├── editor.py
├── reader.py
├── security.py
├── kc_client.py
├── oauth_client.py
├── models.py
├── authforce/
│   └── article-policy.xml
├── templates/
├── static/
├── init_users_ldap.ldif
├── run_secure.sh
├── requirements.txt
└── .env.example
```

## Requirements

- Python 3
- Keycloak
- Flask
- Authlib
- python-keycloak
- SQLAlchemy
- Optional: HashiCorp Vault

Install the Python dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Copy `.env.example` values into your environment or configure equivalent variables through your preferred secret-management solution.

Required Keycloak settings include:

- `KEYCLOAK_BASE_URL`
- `KEYCLOAK_REALM`
- `KEYCLOAK_CLIENT_ID`
- `KEYCLOAK_CLIENT_SECRET`

Application secrets are intentionally **not stored in this repository**.

## Run

With the required environment variables configured:

```bash
python app.py
```

The Flask application listens on port `5000` by default.

For the Vault-based startup flow:

```bash
export VAULT_TOKEN="..."
./run_secure.sh
```

## Authorization model

The project demonstrates fine-grained permissions for actions such as:

- viewing administrative/editor dashboards
- creating and editing articles
- approving articles
- reading preview or full article content

The sample XACML policy under `authforce/` documents an authorization model based on roles and subscription attributes.

## Security notes

This public version intentionally excludes local databases, virtual environments, uploaded content, binaries and real application secrets. Example LDAP passwords are placeholders and must be changed before use.

## Disclaimer

This repository contains an academic project developed for educational purposes. The configuration should be reviewed and hardened before any production deployment.
