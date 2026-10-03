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

Email lookup is implemented at `GET /api/email-check/?email=...` and requires
token authentication. A matching user returns HTTP 200 with `id`, `email`,
and `fullname`. The following cases were manually checked in Postman and their
requests saved in the `KanMind` collection:

- Existing email with a valid token: HTTP 200 with the expected response fields.
- Unknown email with a valid token: HTTP 404.
- Invalid email with a valid token: HTTP 400.
- Missing email with a valid token: HTTP 400.
- Missing authentication: HTTP 401.
- Invalid token: HTTP 401.

Board, task, and comment endpoints are not implemented yet.
The provided frontend is connected to the local backend. Login was checked
through the frontend. After a registration test in Safari, the dashboard
displayed the entered full name and an authenticated session.

Day 3 is complete: login, token authentication, email lookup, and the first
frontend connection for registration and login are in place. Day 4 starts with
the board model, migrations, admin configuration, creation, and listing.

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

## Connecting the separate frontend

Use the [provided Academy frontend](https://github.com/Developer-Akademie-Backendkurs/project.KanMind)
in a separate directory outside this backend repository. Keep its license and
origin notices. To clone it alongside the backend, run from the backend directory:

```bash
git clone https://github.com/Developer-Akademie-Backendkurs/project.KanMind.git ../KanMind_Frontend
```

If the frontend is already cloned, use that directory. In its
`shared/js/config.js`, set the API base URL to match the backend port:

```javascript
const API_BASE_URL = 'http://127.0.0.1:8001/api/';
```

Keep the Django server running in its terminal. Open the frontend's root
`index.html` with Live Server in the editor. The tested frontend address is
http://127.0.0.1:5500/pages/auth/login.html.
The backend's `CORS_ALLOWED_ORIGINS` must allow the frontend's actual origin,
including its hostname and port.

Register a local test user with a new email address, then use that user's
credentials for login. The frontend sends the returned token in
`Authorization: Token <token>` for protected requests. Its preset guest
credentials do not automatically create a local backend user.

## Testing and limitations

Start the backend and run the saved registration, login, and email lookup
requests in Postman.
Successful registration returns 201; the four invalid cases listed above
return 400. Use a new email address for each successful registration test.
For login, use an existing registered test user. Correct credentials return 200;
the wrong password and missing required field cases return 400.
For email lookup, send `Authorization: Token <token>` from a successful login
and use the `email` query parameter. The six cases and expected status codes
are listed above.
The current Postman requests are saved in the local workspace collection;
an updated collection export is not yet included in this repository.
The earlier automated tests were removed during the rebuild. The official
Academy Postman suite has not been run against this version.

The first frontend checks covered login and registration leading to the
dashboard. These checks do not verify the pending board, task, or comment
operations. Empty dashboard sections are expected at this stage; the complete
frontend workflow still needs to be tested after those endpoints are implemented.

This is a local development setup with `DEBUG = True`. Board, task,
and comment endpoints are still pending. Global API authentication uses
`Authorization: Token <token>`; registration and login allow unauthenticated
requests.
