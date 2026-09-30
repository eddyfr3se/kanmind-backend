# KanMind Backend

Backend for the KanMind project at Developer Akademie, built with Python,
Django and Django REST Framework. The planned API covers accounts, boards,
tasks and comments. The frontend is provided separately by the academy.

## Current state

The project and app structure are set up. API endpoints and database models
are not implemented yet. The admin URL is configured; database setup and
an admin account will follow after the user model decision.

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
python manage.py check
python manage.py runserver
```

The backend runs at `http://127.0.0.1:8000/`. There is no homepage or API
endpoint yet, so a 404 response at `/` and `/api/` is expected.
`/admin/login/` displays the Django admin login page.
If port 8000 is occupied, use `python manage.py runserver 8001` for the
setup check. Frontend integration later requires matching its API base URL.

The settings read environment variables directly; `.env` is not loaded
automatically. Load it again when opening a new terminal. `DJANGO_DEBUG=True`
is for local development only. These settings are not a production deployment.

After the user model is settled, database setup will use:

```sh
python manage.py migrate
python manage.py createsuperuser
```

Do not run these steps yet if you are following the initial project stage.

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

The API will use the `Authorization: Token <token>` header. Registration and
login will allow unauthenticated requests. They are not available yet.

## Checks

```sh
python manage.py check
python -m pip check
```

Postman requests and tests will be added with the endpoints. No API acceptance
tests or academy test collection have been run at this stage.

## References

- [API specification](https://cdn.developerakademie.com/courses/Backend/EndpointDoku/index.html?name=kanmind)
- [Project checklist](https://docs.google.com/document/d/1-gUz-skb24UTLAiY5Y-wYDB6GEYI4H9vnxATo-2QsOM/edit)
- [Django 5.2 compatibility](https://docs.djangoproject.com/en/5.2/releases/5.2/)
