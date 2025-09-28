# Security Notes (Addendum)

- `/patches/*` operations should be protected by short-lived tokens and audit logging.
- Keep `ENABLE_MUTATE_EXEC` **disabled** in production unless a full review process exists.
- Consider rotating admin tokens and logging failed attempts with IP/user-agent fingerprinting.
