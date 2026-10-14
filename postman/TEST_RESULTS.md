# Local Postman regression results

## Executed on 14 October 2026

Tests were executed in the Postman desktop app's local Collection Runner
against the local Django backend. No Postman CLI or external HTTP test runner
was used. These are project tests, not the official Academy PM suite.

| Run | Requests | Assertions | Passed | Failed | Skipped | Execution errors |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Initial setup and validation | 136 | 312 | 311 | 1 | 0 | 0 |
| Corrected missing-board request | 1 | 2 | 2 | 0 | 0 | 0 |
| Permissions and cleanup | 36 | 75 | 75 | 0 | 0 | 0 |
| Complete repeat run | 172 | 387 | 387 | 0 | 0 | 0 |

The initial failure was in the test assertion: missing `board` produced a
controlled HTTP 400 JSON list, while the test expected a JSON object. The
assertion was corrected to check a nonempty list, saved in Postman, and rerun.
No backend source change was required. The full saved collection then passed.

## Scope

- Existing-user login, invalid credentials and registration error cases.
- Authenticated email lookup, invalid input, missing users and authentication.
- Board creation, visibility, details, partial updates, counters and deletion.
- Task creation, assignment validation, partial updates and board immutability.
- Separate assignee/reviewer lists, documented response fields and comment counts.
- Comment creation, chronology, actual authors, empty input and URL/task matching.
- Missing/invalid tokens, outsider access, unsupported methods and missing objects.
- Distinct task creator, board owner and comment author rights, including authors
  and creators removed from membership and owners without membership.
- Empty HTTP 204 bodies, task/comment cascades, board/task/comment cascades,
  repeated deletion and absence of the disposable boards after cleanup.

Successful registration was checked manually through the provided frontend on
Day 10, with password entry and privacy confirmation completed by the user.
The Runner intentionally uses existing test accounts and does not create new
credentials. All collection fixtures were newly created disposable test data;
the API checks for permission changes and deletion target captured fixture IDs.

## Files and reproduction

`kanmind-regression.postman_collection.json` was exported through the Postman
app after the successful full run. Public export metadata and runtime variable
values were cleared, while base URL and fixture configuration were retained.
No actual password or token is included. The environment example is empty.

1. Start Django on `http://127.0.0.1:8001`.
2. Import the collection and environment example into the Postman desktop app.
3. Use existing local fictional test accounts: the owner login request uses
   `erika.tag2@example.com`; the member request uses `max@example.com`.
   Both use `test_password`. Adapt those login requests and the duplicate-email
   registration case if your local account emails differ.
4. Set the private environment's `test_password`, `outsider_token` and
   `outsider_id` to match an existing unrelated third account. Never commit or
   publish an environment export containing these values.
5. Select that environment. Run the complete collection with one iteration
   and Keep variable values enabled. Login captures role IDs/tokens; creation
   captures board/task/comment IDs. Run the requests in their saved order.
6. The second folder intentionally changes memberships and permanently deletes
   only the new fixtures. Do not replace its captured IDs with existing data.
7. Inspect Passed, Failed, Skipped and Errors. A passing request status alone
   is not a substitute for checking the assertions.

The two folders can be run separately, but folder 01 must precede folder 02.
If a run stops before cleanup, inspect the captured fixture IDs and finish
cleanup before starting a new setup run, which resets those variables.

The original successful local run used the unrelated test account with ID 3.
Other installations must supply their own role accounts and IDs; this is not a
zero-configuration test of a fresh database. The sanitized export itself has
not been reimported with a different installation's accounts.

## Remaining acceptance work

- The official Academy PM collection has not been run; the required official
  95% coverage result is not established by these 387 assertions.
- The separate frontend display issue and remaining frontend checks described
  in the main README remain open.
- Clean-checkout installation and full submission checklist checks remain open.
- Postman offered the Runner results JSON export only with a paid upgrade in
  this session. This file records the results observed in the app; it is not
  an exported Runner report. The successful run remains in Postman's run history.
