# API work list

Source: [KanMind API specification](https://cdn.developerakademie.com/courses/Backend/EndpointDoku/index.html?name=kanmind), checked 2026-10-01.
**Registration is implemented and tested.** All other operations are pending. Paths start with `/api/` and end in `/`.
Errors shown are the documented client errors. The specification also lists
500 for server failures; it is not a validation response to implement deliberately.

## Response field groups

- **User**: id, email, fullname.
- **Auth**: token, fullname, email, user_id.
- **Board summary**: id, title, member_count, ticket_count, tasks_to_do_count, tasks_high_prio_count, owner_id.
- **Task detail**: id, title, description, status, priority, assignee, reviewer, due_date, comments_count.
- **Task list/create**: Task detail plus board.
- **Task update**: Task detail without comments_count.
- **Comment**: id, created_at, author, content.

Assignee and reviewer are nested User objects or null. Comment author is a
string. Request assignee_id/reviewer_id values are IDs, not nested objects.

| Method | Path | Request | Response | Success | Errors | Access |
| --- | --- | --- | --- | --- | --- | --- |
| POST | registration/ | fullname, email, password, repeated_password | Auth | 201 | 400 | Public |
| POST | login/ | email, password | Auth | 200 | 400 | Public |
| GET | boards/ | — | Board summary list | 200 | 401 | Authenticated; owner/member boards only |
| POST | boards/ | title, members (IDs) | Board summary | 201 | 400, 401 | Authenticated |
| GET | boards/{board_id}/ | — | id, title, owner_id, members (User list), tasks (Task detail list) | 200 | 401, 403, 404 | Owner/member |
| PATCH | boards/{board_id}/ | title, members (IDs), partial | id, title, owner_data (User), members_data (User list) | 200 | 400, 401, 403, 404 | Owner/member |
| DELETE | boards/{board_id}/ | — | Empty | 204 | 401, 403, 404 | Owner |
| GET | email-check/?email=... | email query | User | 200 | 400, 401, 404 | Authenticated |
| GET | tasks/assigned-to-me/ | — | Task list/create list | 200 | 401 | Current assignee |
| GET | tasks/reviewing/ | — | Task list/create list | 200 | 401 | Current reviewer |
| POST | tasks/ | board, title, description, status, priority, assignee_id, reviewer_id, due_date | Task list/create | 201 | 400, 401, 403, 404 | Board member |
| PATCH | tasks/{task_id}/ | title, description, status, priority, assignee_id, reviewer_id, due_date; partial | Task update | 200 | 400, 401, 403, 404 | Board member |
| DELETE | tasks/{task_id}/ | — | Empty | 204 | 400, 401, 403, 404 | Creator/board owner |
| GET | tasks/{task_id}/comments/ | — | Comment list, chronological | 200 | 401, 403, 404 | Board member |
| POST | tasks/{task_id}/comments/ | content | Comment | 201 | 400, 401, 403, 404 | Board member |
| DELETE | tasks/{task_id}/comments/{comment_id}/ | — | Empty | 204 | 400, 401, 403, 404 | Comment author |

## Checks to add during implementation

- Registration: password confirmation, email format and unique account mapping.
- Login and protected requests: valid, missing and invalid tokens.
- Boards: no duplicate list entries; PATCH replaces the supplied members list.
- Tasks: creator is taken from the request user; board cannot change on PATCH.
- Assignee/reviewer must belong to the board; omitted assignments stay empty.
- Comments: author comes from authentication; nested IDs must refer to the same task.
- DELETE responses have no body; board deletion removes tasks and comments.
- Test owner, member, outsider, creator and author as distinct roles.

The text for assigned-to-me has an inconsistent success description mentioning
reviewers. Use its endpoint description and permissions: filter by assignee only.
