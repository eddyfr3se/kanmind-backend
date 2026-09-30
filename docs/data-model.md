# Data model plan

This is the initial plan. These models have not been implemented or migrated.
SQLite is used locally. `auth_app` handles accounts; `kanban_app` handles the
three project entities below.

| Entity | Planned fields and relationships |
| --- | --- |
| User | Start from Django's standard User. The API needs email, fullname and a securely hashed password. |
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

## Account decision before migrations

Prefer the standard Django User unless there is a concrete reason for a custom
model. Before registration is implemented, settle how `fullname` is stored and
how email login maps to a unique account. The default email field is not unique;
username and name fields also have length limits. Do not silently shorten names
or reject valid email addresses because of an internal mapping. A related profile
is an option for fullname. No database migrations have been applied yet, so the
choice can still be made without converting existing user data.

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
