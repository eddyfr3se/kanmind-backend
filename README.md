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
Task updates and deletion are implemented at `/api/tasks/{task_id}/`.
Personal task lists are implemented at `GET /api/tasks/assigned-to-me/` and
`GET /api/tasks/reviewing/`. Board task counters use actual task data.
Days 1–13 are documented below, including implementation, frontend checks
and a repeatable Postman regression run. Comments can be
listed and created at `/api/tasks/{task_id}/comments/` and deleted at
`/api/tasks/{task_id}/comments/{comment_id}/`. Task comment counts use actual
comment data. All 16 planned API operations are implemented. The central
frontend workflows were checked in Safari on Day 10; the remaining limitations
and official Academy acceptance tests are described below.
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
used temporary zero values at this stage; Day 8 replaces them with actual counts.

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
Actual task counting and tests with nonzero counts were completed on Day 8.
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
Day 5. Task integration followed on Day 6; cascade deletion involving tasks
and comments was checked on Day 9. These manual checks do not establish
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
checked. Task updates and deletion followed on Day 7, and personal lists and
board counters on Day 8. Comment counting and cascade checks followed on Day 9.
The central frontend workflows were checked on Day 10. These checks are not
an official Academy test coverage result.

### Day 7 progress

`PATCH /api/tasks/{task_id}/` requires board membership. It updates only the
supplied fields and rejects a different `board` ID. An explicitly supplied
unchanged board ID is accepted since the Day 10 integration correction.
New assignees and reviewers must belong to the task's board. HTTP 200 responses
contain `id`,
`title`, `description`, `status`, `priority`, `assignee`, `reviewer`, and
`due_date`, using nested user data or null for assignments.

`DELETE /api/tasks/{task_id}/` permits the task creator or board owner to delete
and returns HTTP 204 with no response body. Assignment or membership alone
never grants deletion rights. GET and PUT are not enabled on this route.

The following cases were manually executed through the Postman desktop app:

- Title-only and multi-field updates: 200, with omitted values preserved and
  the documented response fields.
- Clearing assignments with null, clearing description, and empty PATCH: 200.
- Board change or an explicitly supplied unchanged board: 400 at this stage.
  Day 10 corrected the unchanged-ID case to 200; board changes remain rejected.
- Invalid status or priority, empty/null title, invalid/null date: 400.
- Board-foreign or unknown assignee/reviewer IDs: 400.
- PATCH and DELETE without a token or with an invalid token: 401.
- PATCH by an owner without membership or an unrelated outsider: 403.
- PATCH and DELETE for unknown tasks: 404.
- Member who is assignee/reviewer but not creator: PATCH 200, DELETE 403.
- Creator removed from membership: PATCH 403, DELETE 204.
- DELETE by an outsider: 403.
- DELETE by a board owner without membership, and by an owner/creator: 204.
- Repeated DELETE after successful deletion: 404.
- GET and PUT on the task detail route: 405.

Board detail requests confirmed that rejected deletion preserved the task and
that permitted deletion removed tasks from the board's list. Empty HTTP 204
response bodies were observed in Postman. Disposable tasks and a separate
test board were created through the app and removed afterward; the existing
boards, tasks, and membership were preserved.

Saved request templates cover disposable task creation, partial-title updates,
board-change validation, and owner deletion. Cases were executed by changing
request values; not every case has a separate saved request. Successful update
and deletion templates use `task_id` and `disposable_task_id` placeholders that
must be filled with appropriate local IDs before running. The requests are
saved locally. No export was included at that stage; the separate Day 11
regression collection is now included. Official PM results remain outstanding.

Day 7 updates and deletion are implemented and manually checked. Personal task
lists and actual board counters followed on Day 8.

### Day 8 progress

`GET /api/tasks/assigned-to-me/` filters tasks by the authenticated assignee.
`GET /api/tasks/reviewing/` filters independently by the authenticated reviewer.
Both return HTTP 200 lists with the documented task fields, nested user data
or null assignments, and `comments_count` (a zero placeholder at this stage,
replaced with actual counts on Day 9).

The following cases were executed in the Postman desktop app:

- Correct role filtering, a task with both roles appearing once in each list,
  and separate assignee-only and reviewer-only tasks: HTTP 200.
- A user with no assignments: HTTP 200 and an empty list on both endpoints.
- Missing and invalid tokens on both endpoints: HTTP 401.
- POST, PUT, PATCH, and DELETE on both list routes: HTTP 405.
- Five after-response assertions for successful lists checked status, exact
  task IDs, duplicates, role IDs, and documented task/user fields; all passed.

Board list counters now count all tasks, tasks with status `to-do`, and tasks
with priority `high` for each board using SerializerMethodField and ORM queries.
Postman checks covered empty and populated boards, owner and member views,
an owner who is also a member, outsider visibility, and missing/invalid tokens.
Disposable tasks tested to-do/high, done/high, and to-do/low combinations.
Follow-up GET requests verified the counters after every creation, separate
status and priority updates, and deletion. Other boards kept their counters.
Five assertions checked successful list status, board IDs, absence of duplicates,
exact per-board counters, and the seven documented response fields; all passed.
Task and board cleanup returned 204, with an empty-body assertion on task
deletion. The original board counters and personal lists passed again afterward.

Requests and after-response scripts are saved in the local Postman collection.
Cases were sent individually, not with Collection Runner. Baseline assertions
use local fixture IDs and counts; adapt them when the database changes.
The disposable setup templates were subsequently saved with collection variables
for returned board/task IDs; these revised setup scripts have not been rerun.
All disposable Day 8 data was removed, preserving the existing boards and tasks.
These checks do not establish the official Academy PM test coverage result.

### Day 9 progress

The Comment model stores its task, author, content and automatic creation time.
Migration `0003_comment` is applied, and Comment is registered in Django admin.
The ModelSerializer returns `id`, `created_at`, `author` as the full name, and
`content`. Only content is writable; the view sets the task and authenticated
author. Generic Views and permissions follow the patterns from earlier stages.

`GET /api/tasks/{task_id}/comments/` lists only that task's comments, ordered
by creation time and then ID. `POST` on the same route requires board membership
and returns 201. Ownership alone does not grant read or create permission.
`DELETE /api/tasks/{task_id}/comments/{comment_id}/` allows only the comment
author and returns an empty 204 response. This author right remains valid after
membership removal. The comment must belong to the task in the URL.

The following checks were executed through the Postman desktop app:

- Member and owner/member creation: 201 with the four documented fields.
  Supplied author, ID, timestamp and task fields did not override server values.
- Member and owner/member listing: 200; chronological order, empty lists and
  separation between tasks were confirmed.
- Empty or whitespace-only content, missing content, null, list, object and
  boolean content: 400.
- Missing and invalid tokens for GET, POST and DELETE: 401.
- Outsider and owner without membership reading or creating: 403.
- Owner, other member and outsider deleting another author's comment: 403.
- Unknown task/comment IDs and a comment under the wrong task URL: 404.
- Successful author deletion: 204 with an empty body; repeated deletion: 404.
- Removed member reading or creating: 403; deleting their own comment: 204.
- PUT, PATCH and DELETE on the list route, and GET, POST, PUT and PATCH on
  the comment detail route: 405.

After-response assertions verified successful comment fields, authors, content,
server ID/time, list order and IDs, response status and empty 204 bodies.
`comments_count` was checked in board details, assigned-to-me and reviewing.
Counts fell after comment deletion, and rejected deletes preserved the comments.
Task deletion removed its comments while another task and comment remained.
Board deletion removed its task and comment. Follow-up API requests and
supplementary read-only ORM inspections confirmed the cascade and cleanup.
All disposable Day 9 data was removed; original boards, tasks and membership
were preserved. The original board's comment counts were zero afterward.

Five request templates are saved in the local Postman collection. Cases were
sent individually by changing request values, not through Collection Runner;
not every case has a separate request. Create/delete templates now use
`comment_task_id` and `comment_id` collection variables. This final variable
configuration was saved after cleanup and was not rerun at that stage.
Day 11 uses a separate exported regression collection; the official Academy
PM suite remains untested. Postman was restarted after
a duplicate-request UI action failed; no backend fix was needed during testing.

### Day 10 progress

The provided frontend was served separately on port 5500 and tested visibly
in Safari against the backend on port 8001. The following workflows were checked:

- Wrong-password rejection, existing-user login, logout, and new-user
  registration leading to an authenticated dashboard.
- Board creation with explicitly selected owner/member accounts, listing,
  retrieval, title changes by a member, and member removal and re-addition.
- Unknown invitation email rejection.
- Task creation with different assignee and reviewer accounts, a due date,
  status changes, and title, description and priority updates.
- Persistence of task changes, assignments and comments after page reload.
- Separate Assigned and To Review lists for the test accounts.
- Comments by two users in chronological order, the author's delete control,
  deletion of the author's comment, and updated comment counts in the dashboard.
- Denied task and board deletion by a member who was neither creator nor owner.
- Successful task deletion by its creator and board deletion by its owner.

Task editing initially failed because the frontend includes the unchanged
board ID in its PATCH body. The update serializer previously rejected any
supplied board field. It now compares the supplied ID with the existing board
and rejects only a different value. The field remains outside the writable
serializer fields. The failed frontend edit was repeated successfully and
its saved values were verified after reload.

Regression requests were executed in the Postman desktop app: the unchanged
board ID and an omitted board field returned 200; a different ID and null
returned 400. The request `Tasks - unchanged board ID accepted` was saved in
the local collection with status and response-field assertions. Both passed
again when the saved request was rerun. A supplementary read-only database
check confirmed that the existing task had not moved to another board.

Disposable board, task and comment data was removed with the user's approval;
the original boards and tasks remained. Django's system check and the Git
whitespace check passed. These results do not establish official PM coverage.
The frontend limitations and remaining acceptance checks are listed below.

### Day 11 progress

A separate regression collection was built and run in the Postman desktop
app's local Collection Runner on 14 October 2026. The complete repeat run
executed **172 requests and 387 assertions: 387 passed, 0 failed, 0 skipped,
and 0 execution errors**.

The checks cover authentication, validation, board visibility and counters,
task assignments and partial updates, separate personal lists, comments,
role-specific permissions, missing objects and cascade deletion. Newly created
disposable fixtures were used for membership changes and deletion and removed
at the end. Successful registration remains covered by the Day 10 frontend
check; the Runner checks registration errors using existing fictional accounts.

An initial assertion expected an object for a missing-board error, while the
backend returned a controlled HTTP 400 JSON list. The assertion was corrected,
saved and rerun before the successful full run. No backend change was needed.

The [regression collection](postman/kanmind-regression.postman_collection.json)
and [empty environment example](postman/kanmind-local.postman_environment.example.json)
are included without actual passwords, tokens or captured runtime IDs.
[Recorded results and reproduction instructions](postman/TEST_RESULTS.md)
explain the required local accounts and fixture cleanup. These are project
checks, not the official Academy PM suite, and do not establish its required
95% coverage result.

### Day 12 progress

Installation was checked in a separate temporary directory using an archive
of the committed backend and the updated README. A fresh Python 3.14.7 virtual
environment installed all pinned dependencies successfully. A new local secret
key and separate SQLite database were used; the existing project database was
not changed. All migrations applied, Django's system check passed, no pending
model changes were detected, and `pip check` found no broken requirements.

The test server started on port 8012 to avoid the existing backend on 8001.
A temporary superuser was created with `createsuperuser --noinput` and logged
in through the browser. Board, task and comment administration list pages
opened successfully. The interactive superuser prompts and a fresh GitHub
clone were not tested. The temporary server was stopped afterward.

The README now includes backend clone and directory-change commands. Unused
imports and scaffold comments were removed from five otherwise empty Django
files. Long lines in settings and four migrations were wrapped. Python syntax
tree comparisons confirmed that the settings and migration definitions stayed
unchanged; these formatting edits were made after the installation check.

The structure and reviewed API code follow the required separation of models,
serializers, views, permissions and URLs. A scan of versioned Python files found
no functions or methods exceeding 14 physical lines, no debug `print()` calls,
and no `fields = "__all__"`.

The current school checklist was read in Google Docs and compared with the
project structure, models, serializers, views, permissions, URLs and recorded
test results. Short class docstrings were added to the application models and
API classes. At that review stage, the 38 functions and methods had at most 13 physical
lines. The subsequent task-ID check adds one short method.
`pycodestyle` 2.15.0 reported no violations across the versioned Python files
in both apps, `core` and `manage.py`. It was installed temporarily outside the
project and is not a runtime dependency. A redundant import-group blank line
was removed. Syntax tree comparisons confirmed that these documentation and
formatting changes did not alter executable logic.

All 16 operations were compared with the current endpoint documentation in the
browser. Two discrepancies were corrected: board-detail tasks now use a separate
serializer without the extra `board` field, and malformed Task DELETE IDs return
HTTP 400 rather than a routing 404. Numeric missing IDs still return 404. The
assigned-to-me filter follows the endpoint description and permission text;
its status-code explanation inconsistently mentions reviewers as well.

Targeted Postman app checks passed three board-detail assertions and five
assertions for each personal list. Six task-ID requests passed all 12 status
and JSON-error assertions. After both corrections, the full Postman desktop
Collection Runner run passed all 387 assertions across 172 requests, with no
failures, skipped assertions or execution errors. Approved new fixture boards,
tasks and comments were removed, and the final list confirmed their absence.
Request 067 was updated in the app and the public collection to match the
nested task fields. The malformed-ID checks are separate from that collection.
Details are recorded in [TEST_RESULTS.md](postman/TEST_RESULTS.md).

Day 12's code review, documented installation check and API comparison are
complete. This does not establish full API acceptance: the official Academy
PM result and remaining frontend checks are still open. A fresh GitHub clone
and interactive superuser prompts were not exercised in the installation check.

### Day 13 progress

The remaining guest-login, task-status display and removed-member workflows
were checked in Safari using a new local test board and fictional accounts.
Guest login now uses a locally registered, nonstaff test user configured only
in the separate frontend. The Academy's preset account was not present in the
local database. No new backend endpoint was added.

A status change was saved correctly by the backend, but opening the edit dialog
immediately showed the previous status. In the separate frontend's
`pages/board/board.js`, `modifyTaskStatus` now updates `currentTask.status` from
the successful PATCH response before refreshing the board. The edit dialog then
showed the new Review status immediately; saving and reloading preserved it.
This local frontend correction is not part of this backend repository.

A member could open the new board before removal. After removal through board
settings, a fresh member login no longer listed that board. Its direct URL
showed no board title or task data. The provided frontend displays an empty
placeholder instead of a clear access-denied message in that case.

No downloadable official PM test collection was found on the accessible
Academy project and submission pages. This does not prove that no such suite
exists. The official 95% acceptance result remains unverified. These Safari
checks are separate from the recorded Postman collection results.

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
- Returned actual member counts; task counts used temporary zero values then.
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

### Day 7 - Task updates and deletion

- Added an object permission: board members can edit; creators or board owners
  can delete. Kept authentication separate from object permissions.
- Added an update serializer that rejects board changes and validates new
  assignments, plus a separate serializer for the PATCH response.
- Connected the task ID route to a Generic View restricted to PATCH, DELETE,
  and OPTIONS. Used partial updates to preserve omitted fields.
- Manually checked updates, validation, authentication, missing tasks, method
  restrictions, and distinct member/creator/owner deletion roles in Postman.
- Verified creator deletion after membership removal and owner deletion
  without membership, with empty 204 responses and subsequent 404 results.
- Removed disposable test data and preserved the existing local data.
- Saved reusable Postman request templates and documented actual manual checks.
- Remaining follow-up: personal task lists and board counters on Day 8,
  comments on Day 9, and the full frontend workflow and official tests later.

### Day 8 - Personal task lists and board counters

- Added two authenticated ListAPIView classes with separate assignee and
  reviewer filters in get_queryset, and connected their API routes.
- Replaced temporary board task counts with actual total, to-do, and high
  priority counts using SerializerMethodField, filter, and count.
- Checked role filtering, empty lists, authentication failures, and forbidden
  write methods through the Postman desktop app.
- Checked board counts after creation, status and priority updates, and deletion,
  including owner/member overlap and independent counts on separate boards.
- Added and executed after-response assertions; successful lists passed all
  five checks. Rechecked the original lists and counts after test-data cleanup.
- Saved local Postman request templates and updated the README and diary.
- Remaining follow-up: comments and actual comment counts on Day 9, followed
  by the full frontend workflow, systematic testing, and submission checks.

### Day 9 - Task comments

- Added Comment with task and author relationships, content, creation time and
  a short string representation; created and applied migration `0003_comment`.
- Registered comments in Django admin and added a ModelSerializer with explicit
  response fields and read-only author, ID and timestamp.
- Added list/create and delete Generic Views, API routes, board membership
  permission for reading/creation, and an author-only deletion permission.
- Restricted methods and checked task/comment URL matching before deletion.
- Replaced the task comment-count placeholder with an actual relation count.
- Executed successful, invalid-input, authentication, role, missing-object,
  method, ordering, count and cascade checks in the Postman desktop app.
- Confirmed the distinct rights of an author removed from board membership.
- Removed disposable test data and preserved original local data; saved request
  templates and documented the results and remaining test limitations.
- Remaining follow-up: the full frontend workflow on Day 10, systematic
  Collection Runner checks, a collection export, official PM tests and final
  installation/submission checks.

### Day 10 - Frontend workflow and task update correction

- Tested registration, login, boards, tasks and comments through Safari using
  the separate Academy frontend and local backend.
- Checked separate assignee/reviewer views, persisted values after reload,
  membership changes, and different editing/deletion rights.
- Corrected task validation to accept the unchanged board ID included by the
  frontend while continuing to reject a board change.
- Repeated the frontend edit and checked unchanged, different, omitted and
  null board values through the Postman desktop app.
- Saved and reran an unchanged-board request with two passing assertions.
- Removed approved disposable test data and verified the original data remained.
- Updated this README and diary with actual results and known limitations.
- Remaining follow-up: repeatable Collection Runner coverage, collection export,
  the frontend display issue below, official PM tests and clean installation.

### Day 11 - Repeatable Postman regression tests

- Built a separate collection with 172 requests and post-response assertions.
- Configured a private local environment for existing fictional role accounts.
- Checked validation, response fields, counters and distinct permission rules
  through the Postman desktop app's Collection Runner.
- Corrected one test assertion for a controlled missing-board error response;
  no backend source change was required.
- Completed a full repeat run with all 387 assertions passing and no execution
  errors, skipped assertions or failed assertions.
- Removed the new disposable fixtures through the approved cleanup requests.
- Exported the collection through the app and cleared credentials, runtime
  values and public export metadata from the repository copy.
- Added an empty environment example and recorded actual results and setup steps.
- Remaining work: clean-checkout installation, the full school checklist,
  official PM acceptance tests and the remaining frontend checks below.

### Day 12 - Installation and code review

- Added backend download and directory-change commands to the installation guide.
- Installed the committed backend in a separate temporary environment and applied
  all migrations to a fresh SQLite database, preserving the existing database.
- Checked dependencies, Django configuration and pending model changes.
- Started the temporary server, created a test superuser without interactive
  prompts, and opened the board, task and comment admin lists in the browser.
- Stopped the temporary server after the checks.
- Reviewed app structure, API responsibilities and method lengths.
- Removed unused imports and scaffold comments and wrapped long settings and
  migration lines, verifying unchanged Python definitions for formatting edits.
- Read the current school checklist and compared its requirements with the
  implementation and recorded test evidence.
- Added short class docstrings to models, serializers, views and permissions.
- Checked all 38 functions and methods against the 14-line limit; the longest
  has 13 lines. Ran pycodestyle successfully with no violations.
- Verified that documentation and import-spacing changes left executable
  logic unchanged; no new API test run was performed for these edits.
- Compared all 16 operations with the current official endpoint documentation.
- Added a separate nested task serializer for board details and updated request
  067's exact-field assertion in the Postman app and public collection.
- Corrected malformed Task DELETE IDs to return 400 while preserving 404 for
  numeric missing IDs; six targeted requests passed all 12 assertions.
- Repeated the complete Postman app collection after both corrections: 172
  requests and 387 assertions, all passed, with approved fixture cleanup.
- Remaining work: official Academy PM tests, remaining frontend checks and final
  submission review. Interactive superuser prompts and a fresh GitHub clone
  remain untested; installation was checked from a committed archive.

### Day 13 - Remaining frontend checks

- Configured a fictional local guest account in the separate frontend and
  checked Guest Log in successfully in Safari.
- Reproduced the stale status in the task edit dialog and corrected the local
  frontend's current-task copy after a successful status PATCH.
- Checked the new status immediately in the editor and after saving/reloading.
- Checked member access before removal, removed the member through settings,
  and checked the member's overview and direct board link after a fresh login.
- Recorded the remaining placeholder message for denied frontend board access.
- Looked for official PM materials on accessible Academy pages; no downloadable
  test collection was found and no official acceptance result is claimed.
- Remaining work: official PM acceptance, final submission review, and the
  previously untested fresh GitHub clone and interactive superuser prompts.

## Installation

The local setup uses Python 3.14, Django, Django REST Framework,
django-cors-headers, and SQLite. Dependency versions are in `requirements.txt`.
Clone the backend and install it on macOS or Linux:

```bash
git clone https://github.com/eddyfr3se/kanmind-backend.git
cd kanmind-backend
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
`index.html` with Live Server in the editor, or serve the separate directory
from a second terminal in the backend directory:

```bash
python -m http.server 5500 --bind 127.0.0.1 --directory ../KanMind_Frontend
```

Keep both servers running. The tested frontend address is
http://127.0.0.1:5500/pages/auth/login.html.
The backend's `CORS_ALLOWED_ORIGINS` must allow the frontend's actual origin,
including its hostname and port.

Register a local test user with a new email address, then use that user's
credentials for login. The frontend sends the returned token in
`Authorization: Token <token>` for protected requests. Its preset guest
credentials do not automatically create a local backend user. To use Guest
Log in locally, create your own fictional test user and set `GUEST_LOGIN` in
that separate frontend's `shared/js/config.js` to its credentials. Keep those
local credentials out of public Git exports.

The locally tested frontend also contains a small status-display correction.
In `pages/board/board.js`, inside the successful branch of `modifyTaskStatus`,
add this before `await loadAndRenderTasks()`:

```javascript
if (currentTask && currentTask.id === id) {
    currentTask.status = response.data.status;
}
```

This keeps the open task's status consistent with the backend response when
switching directly from the detail dialog to the edit dialog.

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
For task updates and deletion, follow the Day 7 cases above. Fill the request
placeholders with your task IDs. Use disposable tasks for successful deletion
tests and keep creator, owner, member, and outsider roles distinct.
For personal task lists and board counters, follow the Day 8 cases above.
Adapt the saved baseline assertions to your local task and board IDs and counts.
Run disposable board creation first, then task creation, before using the
counter setup templates' collection variables. Those variable-based setup
scripts were saved after the manual tests and still need a repeatability check.
For comments, follow the Day 9 cases above. Set `comment_task_id` to a local
task accessible to the test member; successful creation can store the returned
ID in `comment_id` for deletion. Use separate authors, other members, owners
and outsiders. Adapt fixture IDs and expected counts, use disposable data for
deletion/cascade checks, and rerun the final variable-based templates before
using them in an automated collection run.
The historical templates above remain local. For a repeatable run, import the
separate Day 11 [regression collection](postman/kanmind-regression.postman_collection.json)
and [environment example](postman/kanmind-local.postman_environment.example.json).
Follow the account setup, saved request order and disposable-fixture cleanup
instructions in [TEST_RESULTS.md](postman/TEST_RESULTS.md). The full local run
passed all 387 assertions. The sanitized export has not been reimported with
a different installation's accounts. The official Academy Postman suite has
not been run against this version.

The central frontend workflows were checked in Safari on Day 10. Day 13 added
successful guest login, the local task-status display correction and a separate
login as a removed member. The removed member no longer saw the test board in
the overview or its data through a direct link. The frontend still renders an
empty placeholder instead of a clear access-denied message for that direct
link. The guest configuration and status-display correction live only in the
separate local frontend; follow the setup notes above on another installation.
These results do not establish an official Academy acceptance pass.

This is a local development setup with `DEBUG = True`. Task creation and
board detail task lists, task PATCH, task DELETE, personal task lists, and actual
board counters are implemented. Comment operations and actual comment counts
are implemented. Task/comment and board/task/comment cascade deletion were
checked on disposable local data. The official PM acceptance suite and final
submission review remain outstanding. Installation from a committed archive
was checked on Day 12; a fresh GitHub clone and interactive superuser creation
remain untested. This project is not yet declared ready for submission.
Global API authentication uses
`Authorization: Token <token>`; registration and login allow unauthenticated
requests.
