# Things to consider

## API Versioning Discussion

### Context

- Endpoint versioning allows for breaking changes without disrupting existing clients.
- Common approach is to prefix endpoints with `/api/v1/`, `/api/v2/`, etc.

### Concerns

- Mixing `v1` and `v2` endpoints can lead to confusion and maintenance overhead.
- Prefer migrating the entire API to a new version when any breaking change is introduced.

### Points for Team Discussion

- Should we version endpoints individually or migrate the whole API at once?
- How do we handle deprecation and communication with clients?
- What tooling or patterns can help keep migrations DRY and maintainable?
- How do we document version changes and migration paths?

### Next Steps

- Gather feedback from all developers.
- Decide on a versioning strategy before introducing breaking changes.
- Document the chosen approach in the README and API docs.

## Database Migration Discussion

### Context

- Database schemas change over time; manual SQL updates can be error-prone and hard to track.
- Migration tools (e.g., Alembic, Yoyo, Flyway) help version, apply, and roll back schema changes safely.

### Options

- Continue with manual SQL files and document changes/versioning.
- Adopt a migration tool (Alembic for SQLAlchemy, Yoyo for raw SQL, etc.) for automated schema management.

### Points for Team Discussion

- When is the right time to introduce a migration tool?
- Which tool best fits our stack and workflow?
- How do we handle migrations in CI/CD and production?
- How do we document and communicate schema changes?

### Next Steps

- Gather feedback from all developers.
- Decide on a migration strategy before the schema evolves further.
- Document the chosen approach in the README and developer docs.
