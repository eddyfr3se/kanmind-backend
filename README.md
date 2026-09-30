# KanMind Backend

Backend for the KanMind project at Developer Akademie, built with Python,
Django and Django REST Framework. The planned API covers accounts, boards,
tasks and comments. The frontend is provided separately by the academy.

## Current state

Registration is implemented at `POST /api/registration/`. It returns a token,
fullname, email and user_id. The user model and initial migration are included.
Login, email lookup, boards, tasks and comments are still pending.

## Local setup

Tested with Python 3.14.7. Package versions are pinned in `requirements.txt`.
Run the following commands in the project directory on macOS or Linux:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
python -c 'from secrets import token_urlsafe; print(token_urlsafe(50))'
```

Copy the generated value into `DJANGO_SECRET_KEY` in your local `.env`.
Keep this file private. Load the variables into your terminal session:

```sh
set -a
source .env
set +a
python manage.py migrate
python manage.py check
python manage.py runserver
```

The backend runs at `http://127.0.0.1:8000/`. There is no homepage or API
index, so a 404 response at `/` and `/api/` is expected.
`/admin/login/` displays the Django admin login page.
If port 8000 is occupied, use `python manage.py runserver 8001` for the
setup check. Frontend integration later requires matching its API base URL.

The settings read environment variables directly; `.env` is not loaded
automatically. Load it again when opening a new terminal. `DJANGO_DEBUG=True`
is for local development only. These settings are not a production deployment.

To create your own local admin account after applying the migrations:

```sh
python manage.py createsuperuser
```

Sign in at `/admin/` with that username and password. No admin credentials
are stored in the repository. Set fullname in the admin if needed.

## Registration

Send JSON with `fullname`, `email`, `password` and `repeated_password`.
All four fields are required. Matching passwords and a valid, unused email
produce HTTP 201; invalid input produces HTTP 400.

Emails are stored in lowercase and duplicates are checked without regard to
case. Passwords are hashed by Django and never returned. The confirmation
password is only used for validation. The API does not add a password-strength
policy beyond non-empty, matching passwords because the supplied contract
does not specify one. Django's configured validators still apply to its admin
and management commands.

## Structure

- `core/`: settings and root URLs
- `auth_app/api/`: account endpoints, serializers and permissions
- `kanban_app/api/`: board, task and comment endpoints
- `docs/api-plan.md`: endpoint checklist
- `docs/data-model.md`: planned relationships and access rules

## Frontend and authentication

Use the [academy frontend](https://github.com/Developer-Akademie-Backendkurs/project.KanMind)
in a separate directory. Follow its README and license. It is not included here.
The expected API base URL is `http://127.0.0.1:8000/api/`.
Local frontend origins on port 5500 are configured for CORS; change them if
your Live Server uses another port.

Protected API endpoints use the `Authorization: Token <token>` header.
Registration is public and returns a token. The login endpoint is not
implemented yet. Frontend integration has not been tested.

## Checks

```sh
python manage.py check
python -m pip check
python manage.py test auth_app
```

Import `postman/registration.postman_collection.json` into Postman and run
the collection in order. Set `base_url` to your local server URL (default:
`http://127.0.0.1:8001`). Each run creates four fictional accounts with unique
email addresses, so use a local test database. No real credentials are included.

With Node.js installed, the same collection can be run with Newman:

```sh
npm exec --yes --package=newman@6.2.1 -- newman run postman/registration.postman_collection.json
```

See `docs/registration-checks.md` for the checked cases and results. These are
project tests; the academy's official PM collection has not been run.

## References

- [API specification](https://cdn.developerakademie.com/courses/Backend/EndpointDoku/index.html?name=kanmind)
- [Project checklist](https://docs.google.com/document/d/1-gUz-skb24UTLAiY5Y-wYDB6GEYI4H9vnxATo-2QsOM/edit)
- [Django 5.2 compatibility](https://docs.djangoproject.com/en/5.2/releases/5.2/)
