# Maintained patches to pinned third-party skills

The importer preserves third-party source files by default. A release audit may identify a minimal blocker that makes a pinned skill syntactically unusable. Such changes are recorded here.

| Skill | File | Change | Reason |
|---|---|---|---|
| `brenda-database` | `scripts/brenda_queries.py` | Repaired an invalid nested conditional for activator mechanism | Python could not parse the upstream snapshot, so the skill could not run at all |

These patches do not transfer authorship or change the upstream license. Future snapshot updates must re-evaluate whether the patch is still needed.
