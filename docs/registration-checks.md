# Registration checks

Run on 2026-10-01 using Python 3.14.7, Django 5.2.17 and DRF 3.18.1.

## Postman collection

`postman/registration.postman_collection.json` was executed with Newman 6.2.1
against a local server on port 8001 with a separate temporary SQLite database.

Result: 23 requests, 71 assertions, no failures on the final run.

Cases include successful registration, exact response fields, duplicate email
(including different case), missing/empty/null fields, invalid email, mismatched
passwords, whitespace-only names, malformed JSON and unsupported GET requests.
Long names and email addresses, extra permission fields and registration with
a stale token header are included as well.

An initial run found a test-script variable name conflict. The script was
corrected and the entire collection rerun successfully.

## Django tests

`python manage.py test auth_app`: seven tests passed in an isolated database.

- Password is hashed and significant whitespace is preserved.
- Returned token belongs to the created user.
- Duplicate email does not create a second user or token.
- Invalid registration does not write an account.
- A client cannot grant itself admin permissions.
- Failed token creation rolls back the account.
- A duplicate introduced after validation returns a field error.
- Admin account list and creation form can be opened by a superuser.

`python manage.py check` reports no issues. `makemigrations --check --dry-run`
reports no missing migrations. The initial migrations were applied locally.

The academy's official PM tests and frontend integration have not been run.
These results cover registration only.
