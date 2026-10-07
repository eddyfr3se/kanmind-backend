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

Board creation and listing are implemented at `/api/boards/`.
Board retrieval is implemented at `GET /api/boards/{board_id}/`.
Board update and delete endpoints, plus task and comment endpoints,
are not implemented yet.
The provided frontend is connected to the local backend. Login was checked
through the frontend. After a registration test in Safari, the dashboard
displayed the entered full name and an authenticated session.

Day 3 is complete: login, token authentication, email lookup, and the first
frontend connection for registration and login are in place.

### Day 4 progress

The Board model, initial migration, and admin registration are in place.
A board was created successfully through the admin interface. The input
serializer accepts `title` and `members`; the list serializer provides `id`,
`title`, `member_count`, `ticket_count`, `tasks_to_do_count`,
`tasks_high_prio_count`, and `owner_id`.

Django's system check passed, and the list serializer was checked against the
saved test board. Member counts use the board's actual membership. Task counts
temporarily default to zero until the Task model and counting logic are added.

`POST /api/boards/` creates a board and returns its short representation with
HTTP 201. The authenticated user becomes the owner, independently of any
owner fields supplied in the request. Ownership does not automatically add
the user to the members list.

`GET /api/boards/` returns HTTP 200 with only boards owned by or shared with
the authenticated user. A board appears once even when both conditions apply.
Both operations require token authentication.

Eleven board requests were manually executed through the Postman desktop app
and saved in the `KanMind` collection:

- Create a board with members: HTTP 201 and all seven response fields.
- Create a board with an empty members list: HTTP 201, member count zero,
  and the authenticated user as owner despite supplied foreign owner IDs.
- List boards as owner: HTTP 200, including ownership without membership,
  excluding a foreign board, and no duplicate for an owner who is also a member.
- List boards as member: HTTP 200 with the shared board, excluding other boards.
- Create with an empty title: HTTP 400.
- Create with a missing title: HTTP 400.
- Create with an unknown member ID: HTTP 400.
- List without a token: HTTP 401.
- List with an invalid token: HTTP 401.
- Create without a token: HTTP 401.
- Create with an invalid token: HTTP 401.

Day 4 board setup, creation, and listing are implemented and manually checked.
Actual task counting and tests with nonzero task counts remain pending.
Day 5 covers board details, updates, and deletion with their permissions.

### Day 5 progress

`GET /api/boards/{board_id}/` requires token authentication and allows the
board owner or a member to retrieve the board. It returns `id`, `title`,
`owner_id`, `members`, and `tasks`. Each member contains `id`, `email`, and
`fullname`. The task list is temporarily empty until the Task model is added.

Six board detail requests were manually executed through the Postman desktop
app and saved in the `KanMind` collection:

- Owner retrieves a board: HTTP 200 with the expected board and member fields.
- Member retrieves a shared board: HTTP 200 with the same response structure.
- An authenticated outsider retrieves an existing foreign board: HTTP 403.
- Request without a token: HTTP 401.
- Request with an invalid token: HTTP 401.
- Request for a nonexistent board with a valid token: HTTP 404.

Board PATCH and DELETE operations and their tests remain pending.

## Development diary

The entries below summarize the completed learning stages. Day numbers refer
to the project plan, not necessarily to separate calendar dates. Days 1 and 2
describe the rebuilt implementation; the earlier repository history is retained.

### Day 1 - Project setup

- Prepared the Django project `core`, the `auth_app` and `kanban_app` apps,
  and separate API directories with central URL configuration.
- Configured the virtual environment, dependencies, local secret key handling,
  token authentication settings, and CORS for the separate frontend.
- Excluded local secrets, the database, environment, and caches from Git.
- Added setup instructions and a placeholder environment example.
- Checked that Django's system check passed and the development server started.

### Day 2 - Registration

- Rebuilt registration using Django's built-in User and a separate UserProfile
  for the full name, replacing the earlier custom user implementation.
- Added validation for required fields, email format, duplicate email addresses,
  and matching passwords. Used Django's password hashing when creating users.
- Returned a token, full name, email, and user ID after successful registration.
- Applied the authentication and profile migrations to the rebuilt local database.
- Manually checked and saved five registration requests in Postman: success,
  duplicate email, mismatched passwords, invalid email, and missing fields.
- Documented the database compatibility limitation of the rebuild.

### Day 3 - Login and first frontend connection

- Implemented email and password login with DRF token authentication.
- Added authenticated email lookup with the documented user response fields.
- Manually checked and saved three login cases and six email lookup cases
  in Postman, including validation and authentication failures.
- Started the provided frontend separately and configured its backend URL
  and the matching local CORS origins.
- Checked frontend login and observed an authenticated dashboard displaying
  the entered full name after registration in Safari.
- Updated the README and committed and pushed the completed work.

### Day 4 - Board creation and listing

- Created the Board model with a title, owner, and members, applied its initial
  migration, and registered it in Django admin.
- Created a test board through the admin interface.
- Implemented authenticated board creation and listing with explicit serializers.
- Set ownership from the authenticated user and limited listing to owned or
  shared boards, without duplicate entries.
- Returned actual member counts; task counts remain temporary zero values.
- Manually checked and saved eleven board requests through the Postman desktop
  app, covering creation, visibility, invalid input, and authentication failures.
- Updated the README and pushed commits `900bddc` (model, admin, serializers)
  and `1901793` (creation and listing API).
- Remaining follow-up: real task counts and the board frontend workflow.

### Day 5 - In progress

Completed so far:

- Added a member serializer with `id`, `email`, and the profile's full name.
- Added a board detail serializer with nested members and an empty task list
  until the Task model is implemented.
- Django's system check passed. A local serializer check confirmed the five
  board detail fields and the temporary empty task list.
- Connected the detail serializer to a RetrieveAPIView and board ID route.
- Added an object permission allowing the board owner or a member to read.
- Manually executed and saved six detail requests in the Postman desktop app:
  owner and member access (200), outsider access (403), missing and invalid
  tokens (401), and a nonexistent board (404).
- Checked that all six requests were saved with their intended URLs.

Remaining work:

- Implement partial updates for the title and replacement of the members list.
- Allow owners and members to update; allow only owners to delete.
- Check responses, permissions, validation, missing objects, and empty HTTP 204
  responses through the Postman desktop app.
- Update this diary with actual results, update the README status, and commit
  and push completed, checked work.
- Integrate actual tasks into board details on Day 6. Cascade checks involving
  tasks and comments must wait until those models exist.

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

Start the backend and run the saved registration, login, email lookup, and board
requests in Postman.
Successful registration returns 201; the four invalid cases listed above
return 400. Use a new email address for each successful registration test.
For login, use an existing registered test user. Correct credentials return 200;
the wrong password and missing required field cases return 400.
For email lookup, send `Authorization: Token <token>` from a successful login
and use the `email` query parameter. The six cases and expected status codes
are listed above.
For boards, use separate owner and member test users and send their login
tokens. Successful POST requests create new local test boards on each run.
The eleven creation/listing requests and six detail requests, including their
expected results, are listed above. For an outsider check, use a valid token
belonging to a user who neither owns nor belongs to the requested board.
The current Postman requests are saved in the local workspace collection;
an updated collection export is not yet included in this repository.
The earlier automated tests were removed during the rebuild. The official
Academy Postman suite has not been run against this version.

The first frontend checks covered login and registration leading to the
dashboard. Board creation, listing, and retrieval have been checked in Postman;
their frontend workflow has not been tested yet. The complete frontend
workflow still needs to be tested after the remaining endpoints are implemented.

This is a local development setup with `DEBUG = True`. Board update and delete
operations, task operations, and comment operations are still pending.
Board detail task lists are temporarily empty until tasks are implemented.
Task counts currently default to zero. Global API authentication uses
`Authorization: Token <token>`; registration and login allow unauthenticated
requests.
