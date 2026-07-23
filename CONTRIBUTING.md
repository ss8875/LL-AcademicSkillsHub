# Contributing

Contributions must include:

- a kebab-case skill ID and one clear responsibility;
- `SKILL.md` with only `name` and `description` frontmatter;
- bilingual `locales/zh-CN.md` and `locales/en.md`;
- a catalog record with inputs, outputs, environment, risk, quality, provenance, and license status;
- deterministic tests or fixtures when code is included;
- no fabricated citations, hidden advertising, credential collection, or unconditional execution instructions.

Run `python scripts/validate_repo.py` before submitting a change. A skill enters the catalog as `cataloged` or `beta`; promotion to `tested`, `verified`, or `gold` requires recorded evidence.
