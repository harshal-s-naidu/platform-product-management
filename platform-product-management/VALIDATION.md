# Validation record

Package version: 1.0.1. Validation is local and read-only except for generated editions, manifest and transfer archive.

Checks performed:

- `scripts/validate_state.py data/state.json` — starter state passes with 0 errors and 0 warnings.
- `scripts/validate_state.py examples/sample-state.json` — fictional fixture passes with 0 errors and 0 warnings.
- `python3 -m unittest discover -s scripts -p 'test_*.py' -v` — 21 tests pass, covering malformed records, dates, IDs, links, versions, stale stores, decisions, risks and dependency cycles.
- `scripts/build_editions.py` — generates assembled Markdown/plain-text editions, checks local links and writes an allowlisted manifest/archive.
- `scripts/build_editions.py --check` — confirms generated editions and manifest are reproducible after packaging.
- A dependency-free frontmatter check confirms `SKILL.md` has the required `name`/`description`, valid lowercase hyphenated name, no unfinished TODO scaffold, and no disallowed frontmatter keys. The bundled `quick_validate.py` could not run because its optional PyYAML dependency is not installed; no package installation was required.

Limits:

- The state validator intentionally implements the subset of JSON Schema needed by this package and selected cross-record rules. It is not a general Draft 2020-12 validator.
- No live Snowflake account, Cortex session, Copilot tenant, work document, authentication, multi-user concurrency or deployment was exercised.
- The sample dataset is fictional and must remain separate from work state.
