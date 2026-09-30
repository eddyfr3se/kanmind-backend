# Data model plan

The user model is implemented and migrated. Board, Task and Comment remain planned.
SQLite is used locally. `auth_app` handles accounts; `kanban_app` handles the
three project entities below.

| Entity | Planned fields and relationships |
| --- | --- |
| User | auth_app.User extends AbstractUser with unique email, fullname and a 254-character username. Password hashing and permissions are inherited. |
| Board | id, title, owner (User), members (many-to-many User) |
| Task | id, board, creator (User), title, description, status, priority, assignee (nullable User), reviewer (nullable User), due_date |
| Comment | id, task, author (User), content, created_at |

Board deletion cascades to tasks and their comments. Task deletion cascades
to comments. User deletion behavior must be chosen when implementing the
relationships; nullable assignee/reviewer relations can use SET_NULL.
Each user relationship needs its own `related_name`.

Counts are computed from related objects rather than stored in extra fields.
Task status is one of `to-do`, `in-progress`, `review`, `done`; priority is
`low`, `medium`, or `high`.

## Account decision

`auth_app.User` inherits from Django's `AbstractUser`. This small extension
provides database uniqueness for email and stores fullname without splitting
or truncating it. The unchanged Django User does not provide these fields
in this form. A separate profile would add a second table for account data.

For API registrations, username is the normalized email as well. Its length
is 254 to avoid imposing the standard username limit of 150 on email
addresses. This keeps Django's existing manager and password methods usable.
The forthcoming API login must look up normalized email, then authenticate
with the stored username; admin-created usernames can differ from email.

The serializer lowercases email and checks existing addresses with `iexact`.
Database uniqueness also rejects simultaneous API registrations of the same
normalized address. Admin users should use lowercase email addresses; direct
admin edits do not apply the API serializer's normalization.

`fullname` uses a TextField because the contract specifies no maximum length.
Blank and null names are rejected. Registration fields are explicitly listed,
so clients cannot set staff status, superuser status or groups.

`create_user()` hashes the password. A database transaction saves the account
and its token together, rolling both back if creation fails. The transaction
exists to avoid half-finished registrations.

References: [Django user customization](https://docs.djangoproject.com/en/5.2/topics/auth/customizing/)
and [transactions](https://docs.djangoproject.com/en/5.2/topics/db/transactions/).

## Access rules

| Operation | Allowed user |
| --- | --- |
| List/read/update board | Owner or member |
| Create board | Any authenticated user |
| Delete board | Owner |
| Create/update task | Board member |
| Delete task | Task creator or board owner |
| Assigned tasks | Current assignee |
| Reviewing tasks | Current reviewer |
| Read/create comment | Board member |
| Delete comment | Comment author |

Ownership does not automatically add membership. Assignment does not make a
user the task creator. Store the creator separately. The comment author is
returned as a full name, not as a nested user object.

## Resolve with the relevant endpoint

- Required, blank and nullable fields, including due dates.
- Existing task assignments after removing a board member.
- Duplicate member IDs.
- Missing objects versus existing objects without access (404 versus 403).

The API specification is authoritative. These open questions must not become
extra permission grants or arbitrary validation rules.
