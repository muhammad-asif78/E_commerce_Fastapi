# CLAUDE.md

## Project Overview
This repository is an e-commerce backend built with FastAPI, SQLAlchemy, Alembic, and bearer-token authentication.

Main areas of the app:
- Authentication
- Admin
- Users
- Products
- Orders
- Cart
- Todos
- Email

Important files and folders:
- `app/main.py` -> app entrypoint and router registration
- `app/auth.py` -> authentication, token creation/validation, current user/admin dependencies
- `app/config.py` -> environment variable loading
- `app/database.py` -> database setup and session handling
- `app/model.py` -> SQLAlchemy models
- `app/router/` -> API routes
- `app/schemas/` -> request/response schemas
- `alembic/` -> database migrations

## Working Rules
When making changes in this repository, always follow these rules:

1. Do not break existing API behavior unless explicitly requested.
2. Prefer small, focused changes over large refactors.
3. Keep FastAPI router logic clean and readable.
4. Put validation in Pydantic schemas when possible.
5. Put database logic in a structured, maintainable place.
6. Reuse existing auth and dependency patterns before introducing new ones.
7. Keep naming consistent with the current codebase.
8. Avoid adding unnecessary libraries.

## Security Rules
This project handles authentication, user data, admin access, orders, and email-related flows. Security is a top priority.

Always enforce the following:

### Secrets and Config
- Never hardcode secrets, tokens, passwords, or credentials.
- Always use environment variables for sensitive config.
- Do not introduce shared default secrets for convenience.
- If a required secret such as `SECRET_KEY` is missing, prefer failing fast over using an insecure fallback.
- If a secret fallback is insecure, recommend removing it rather than expanding it.
- Do not commit real `.env` values.
- Prefer setup helpers or bootstrap scripts over insecure hardcoded defaults.

### Authentication and Authorization
- All protected routes must clearly enforce the correct dependency:
  - user-only routes -> user dependency
  - admin-only routes -> admin dependency
  - superadmin-only routes -> superadmin dependency
- Do not expose admin functionality to normal users.
- Do not trust client-provided identity fields without server-side verification.
- For user-linked resources such as orders, carts, todos, and similar records, always enforce ownership checks or explicit admin authorization.
- Never rely on caller-provided `user_id` or similar identifiers alone for access control decisions.
- Token validation changes must be reviewed carefully.
- Do not add auth bypasses, temporary shortcut access, or insecure developer backdoors.
- Admin bootstrap or privileged account initialization must be deployment-safe and must not be publicly claimable.

### Input Validation
- Validate request input with Pydantic schemas.
- Reject unexpected or malformed input.
- Add type-safe validation instead of manual unchecked parsing where possible.

### Database Safety
- Avoid risky query patterns.
- Prevent accidental overexposure of records.
- Be careful with update/delete operations.
- Preserve migration safety when changing models.

### API Safety
- Do not leak sensitive internal errors to clients.
- Use clear HTTP status codes.
- Avoid returning secrets, password hashes, raw tokens, or internal-only fields in API responses.

### Logging
- Never log passwords, tokens, secret keys, or sensitive personal data.
- Do not enable verbose SQL or debug logging in environments where sensitive values or query parameters may be exposed.
- Keep logs useful but safe.

## Code Style Guidance
- Use clear function names.
- Keep functions focused on one responsibility.
- Prefer explicit logic over clever shortcuts.
- Maintain consistency with existing file structure.
- Add comments only when they improve understanding.

## FastAPI / Project Conventions
- New endpoints should usually live in the appropriate router file.
- Request and response models should go in schemas.
- Database model changes must consider Alembic migrations.
- Auth-related changes should align with `app/auth.py`.
- Config changes should align with `app/config.py`.

## When Reviewing Code
When asked to review code in this repo, focus on:
1. Authentication correctness
2. Authorization boundaries
3. Secret handling
4. Input validation
5. Unsafe defaults
6. Database safety
7. API response safety
8. Migration impact
9. Maintainability and consistency

## High-Risk Areas
Pay extra attention to:
- `app/auth.py`
- login flows
- admin creation and admin-only routes
- token generation and verification
- secret loading and fallback behavior
- config/env handling
- model changes affecting migrations
- order/cart/todo/email flows that affect ownership or access control
- any route accepting `user_id`, `admin_id`, or similar identity-linked fields

## Safe Change Process
For non-trivial changes, follow this order:
1. Understand the existing route / schema / model flow
2. Identify auth and security impact
3. Make the smallest safe change
4. Check whether schema changes require migration changes
5. Verify no sensitive data is exposed
6. Summarize what changed and any risks

## What To Avoid
- Do not introduce hardcoded secrets
- Do not introduce insecure fallback secrets
- Do not bypass auth dependencies
- Do not accept public bootstrap of privileged accounts
- Do not trust client-controlled ownership fields for protected resources
- Do not mix unrelated refactors with security fixes
- Do not return database objects blindly without checking exposed fields
- Do not weaken token validation
- Do not add hidden magic behavior without explanation

## Preferred Assistant Behavior
When helping in this repository:
- First explain what you are changing
- Then make the change
- Mention any security or migration implications
- If something is risky or unclear, say so explicitly
- Prefer safe defaults