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
Board retrieval, partial updates, and deletion are implemented at
`/api/boards/{board_id}/`. Task creation is implemented at `POST /api/tasks/`.
Task updates, deletion, personal lists, and comment endpoints remain pending.
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
`fullname`. Since Day 6, `tasks` contains the board's actual tasks.

Six board detail requests were manually executed through the Postman desktop
app and saved in the `KanMind` collection:

- Owner retrieves a board: HTTP 200 with the expected board and member fields.
- Member retrieves a shared board: HTTP 200 with the same response structure.
- An authenticated outsider retrieves an existing foreign board: HTTP 403.
- Request without a token: HTTP 401.
- Request with an invalid token: HTTP 401.
- Request for a nonexistent board with a valid token: HTTP 404.

`PATCH /api/boards/{board_id}/` allows owners and members to change the title
and replace the members list. Omitted fields stay unchanged. It returns HTTP
200 with `id`, `title`, `owner_data`, and `members_data`; each user object
contains `id`, `email`, and `fullname`. Ownership and tasks are not writable
through this endpoint. PUT is not enabled.

Twelve update cases were manually executed through the Postman desktop app
and their requests saved in the `KanMind` collection:

- Owner changes only the title: HTTP 200; membership stays unchanged.
- Owner replaces members: HTTP 200; the previous selection is replaced.
- Member changes the title: HTTP 200.
- Member replaces members: HTTP 200.
- Owner sends an empty members list: HTTP 200; all members are removed.
- Empty title: HTTP 400 with a title validation error.
- Unknown member ID: HTTP 400 with a members validation error.
- Authenticated outsider updates an existing foreign board: HTTP 403.
- Missing token: HTTP 401.
- Invalid token: HTTP 401.
- Nonexistent board with a valid token: HTTP 404.
- PUT with a valid owner token: HTTP 405; the board stays unchanged.

Follow-up GET requests confirmed membership replacement, the empty members
list, and unchanged board data after rejected requests.

`DELETE /api/boards/{board_id}/` allows only the owner to delete. Six deletion
cases were manually executed through the Postman desktop app and their
requests saved in the `KanMind` collection:

- Owner deletes a separately created disposable test board: HTTP 204 with
  an empty response body. A subsequent owner GET returned HTTP 404.
- Member attempts deletion: HTTP 403; a subsequent owner GET returned 200.
- Authenticated outsider attempts deletion: HTTP 403; a subsequent owner GET
  returned 200.
- Missing token: HTTP 401 with a missing credentials error.
- Invalid token: HTTP 401 with an invalid token error.
- Nonexistent board with a valid token: HTTP 404.

For the member deletion test, membership was restored first and confirmed
in the response. The successful owner deletion used a board with no members,
confirming that ownership alone grants the deletion right.

Board details, PATCH, and DELETE are implemented and manually checked for
Day 5. Task integration and cascade deletion of tasks and comments remain
follow-up work once those models exist. These manual checks do not establish
an official Academy test coverage result.

### Day 6 progress

The Task model, migration, and admin registration are in place. Tasks belong
to a board and retain their creator. Status and priority use explicit choices;
assignee and reviewer are optional user relationships. The authenticated user
is saved as the creator by the view.

`POST /api/tasks/` requires board membership. Ownership without membership
does not grant permission to create tasks. Assignees and reviewers must be
members of the same board. Successful creation returns HTTP 201 with `id`,
`board`, `title`, `description`, `status`, `priority`, `assignee`, `reviewer`,
`due_date`, and `comments_count`. Assigned users contain `id`, `email`, and
`fullname`; unassigned roles return null.

Twenty-four task requests were manually executed in the Postman desktop app
and saved in the local `KanMind` collection:

- Four successful cases: no assignments, both assignments, explicit null
  assignments, and reviewer only with omitted description (HTTP 201).
- Board-foreign assignee or reviewer, unknown assignee or reviewer, invalid
  status or priority, empty title, invalid date, missing board, missing required
  fields, and a noninteger board value (HTTP 400).
- Missing or invalid token (HTTP 401).
- An outsider and an owner without membership (HTTP 403).
- An unknown board (HTTP 404).
- GET, PUT, PATCH, and DELETE on `/api/tasks/` (HTTP 405).

Board details now use the nested TaskSerializer. Seven detail cases were
checked in Postman: owner and member access to a board with tasks (200),
an empty task list on another board (200), outsider access (403), missing
and invalid tokens (401), and an unknown board (404). Returned tasks included
nested assignments, null roles, dates, statuses, priorities, and the current
zero comment counts. An initial HTTP 500 caused by the old ListField
placeholder was corrected; the affected requests were repeated successfully.

Day 6 task creation and board detail integration are implemented and manually
checked. Board counters still use temporary zero values. Comment counting,
task updates, deletion, personal lists, cascade checks, and the complete
frontend workflow remain later stages. These checks are not an official
Academy test coverage result.

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

### Day 5 - Board details, updates, and deletion

- Added nested member data and the documented board detail response.
- Connected the board ID route to a RetrieveUpdateDestroyAPIView, enabling
  GET, PATCH, and DELETE while excluding PUT.
- Reused the input ModelSerializer for partial title and membership updates;
  added a separate serializer for `owner_data` and `members_data` responses.
- Allowed owners and members to read and update, but only owners to delete,
  using an object permission. Kept missing objects distinct from denied access.
- Manually executed and saved six detail, twelve update, and six deletion
  cases in the Postman desktop app. Expected status codes and checked behavior
  are recorded in the Day 5 progress section above.
- Confirmed persisted membership changes with GET requests and verified that
  forbidden member and outsider deletion attempts left the boards intact.
- Created a disposable board, deleted it as its owner, checked the empty
  HTTP 204 response, and confirmed its absence with a subsequent HTTP 404 GET.
- Updated the README and this diary with the implemented behavior and actual
  manual test results.
- Remaining follow-up: integrate tasks on Day 6, check cascading task/comment
  deletion after both models exist, and test the full board frontend workflow.

### Day 6 - Task creation and board detail integration

- Added the Task model with board, creator, optional assignee and reviewer,
  title, description, status, priority, and due date.
- Created and applied migration `0002_task` and registered Task in admin.
- Added separate input and response serializers with membership validation
  for assignments and nested user data in responses.
- Implemented authenticated task creation, requiring board membership and
  saving the creator from the current user.
- Replaced the board detail task placeholder with a nested TaskSerializer.
- Manually checked and saved 24 task requests through the Postman desktop
  app and checked seven board detail cases after integration.
- Corrected the old task ListField placeholder after a 500 response and
  repeated the affected Postman requests successfully.
- Remaining follow-up: task PATCH and DELETE on Day 7, personal lists and
  actual board counters on Day 8, and comments on Day 9.

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

Start the backend and run the saved registration, login, email lookup, board,
and task requests in Postman.
Successful registration returns 201; the four invalid cases listed above
return 400. Use a new email address for each successful registration test.
For login, use an existing registered test user. Correct credentials return 200;
the wrong password and missing required field cases return 400.
For email lookup, send `Authorization: Token <token>` from a successful login
and use the `email` query parameter. The six cases and expected status codes
are listed above.
For boards, use separate owner and member test users and send their login
tokens. Successful POST requests create new local test boards on each run.
The eleven creation/listing, six detail, twelve update, and six deletion
requests and their expected results are listed above. Before a member test,
ensure the test user is currently a member: replacing members with an empty
list removes that role. Create a fresh disposable board for each successful
owner deletion test, use its returned ID, and confirm its absence with GET.
For an outsider check, use a valid token belonging to a user who neither owns nor belongs to the requested board.
For task creation, use a board member token and member IDs for assignments.
Successful POST requests create additional local tasks; update board and user
IDs to match your local database. The Day 6 section lists the tested cases.
The current Postman requests are saved in the local workspace collection;
an updated collection export is not yet included in this repository.
The earlier automated tests were removed during the rebuild. The official
Academy Postman suite has not been run against this version.

The first frontend checks covered login and registration leading to the
dashboard. Board creation, listing, retrieval, updates, and deletion were
checked in Postman; their frontend workflow has not been tested yet. The complete frontend
workflow still needs to be tested after the remaining endpoints are implemented.

This is a local development setup with `DEBUG = True`. Task creation and
board detail task lists are implemented. Task PATCH, DELETE, personal lists,
and comment operations remain pending. Cascade deletion involving tasks and
comments has not been tested; the Comment model is not implemented yet.
Board task counts and task comment counts currently default to zero.
Global API authentication uses
`Authorization: Token <token>`; registration and login allow unauthenticated
requests.
