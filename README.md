# KanMind Backend

Backend for the Developer Akademie KanMind school project.

## Current status

Days 1 and 2 were rebuilt: the project setup and registration implementation
were rewritten using Django's built-in User and a separate UserProfile for
the full name. This replaces the previous custom user implementation.
The earlier commits remain in the repository history.

Django project structure, API configuration, and database migrations are in place.
Registration is implemented at `POST /api/registration/` and returns HTTP 201
with `token`, `fullname`, `email`, and `user_id`.

The following registration cases were manually checked in Postman and their
requests saved in the `KanMind` collection:

- Successful registration.
- Duplicate email address.
- Mismatched passwords.
- Invalid email address.
- Missing required fields.

Login is implemented at `POST /api/login/`. It accepts `email` and `password`
and returns HTTP 200 with `token`, `fullname`, `email`, and `user_id`.
The following login cases were manually checked in Postman and their requests
saved in the `KanMind` collection:

- Correct credentials: HTTP 200 with the expected response fields.
- Wrong password: HTTP 400 with an invalid credentials error.
- Missing email and password: HTTP 400 with required field errors.

Email lookup and the remaining API endpoints are not implemented yet.
The provided frontend has not been connected yet.

Day 3 is in progress. The next steps are authenticated email lookup and the first
frontend connection. Further changes will be committed in small, tested steps.

## Installation

The local setup uses Python 3.14, Django, Django REST Framework,
django-cors-headers, and SQLite. Dependency versions are in `requirements.txt`.
From a fresh checkout on macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Replace the placeholder in `.env` with a random local secret key. Generate one
with the following command and keep it private:

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Load the configuration and initialize the database:

```bash
set -a
source .env
set +a
python manage.py migrate
python manage.py createsuperuser
```

### Database compatibility

The rebuild changes the initial authentication migration and user model.
A fresh installation uses the current migrations normally. A database created
with the earlier custom user model cannot be upgraded by simply pulling the
code and running `migrate`. Preserve any existing data and use a separate fresh
database, or plan an explicit data migration if the old data must be retained.
The current rebuilt local database does not need to be reset.

## Local development

Run these commands from the project directory.
A local `.env` file with `DJANGO_SECRET_KEY` is required.

```bash
source .venv/bin/activate
set -a
source .env
set +a
python manage.py runserver 8001
```

Admin login page: http://127.0.0.1:8001/admin/login/

Stop the server with Control+C.

## Testing and limitations

Start the backend and run the saved registration and login requests in Postman.
Successful registration returns 201; the four invalid cases listed above
return 400. Use a new email address for each successful registration test.
For login, use an existing registered test user. Correct credentials return 200;
the wrong password and missing required field cases return 400.
The current Postman requests are saved in the local workspace collection;
an updated collection export is not yet included in this repository.
The earlier automated tests were removed during the rebuild. The official
Academy Postman suite has not been run against this version.

This is a local development setup with `DEBUG = True`. Email lookup, board, task,
and comment endpoints are still pending. Global API authentication uses
`Authorization: Token <token>`; registration and login allow unauthenticated
requests.
