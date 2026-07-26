# Contributing

Contributions must include:

- a kebab-case skill ID and one clear responsibility;
- `SKILL.md` with only `name` and `description` frontmatter;
- bilingual `locales/zh-CN.md` and `locales/en.md`;
- a catalog record with inputs, outputs, environment, risk, quality, provenance, and license status;
- deterministic tests or fixtures when code is included;
- no fabricated citations, hidden advertising, credential collection, or unconditional execution instructions.

Run `python scripts/validate_repo.py` before submitting a change. A skill enters the catalog as `cataloged` or `beta`; promotion to `tested`, `verified`, or `gold` requires recorded evidence.

## Contribution licensing

The repository is source-available under PolyForm Noncommercial License 1.0.0 for first-party materials. By submitting a contribution, you represent that you have the right to submit it and grant the applicable project copyright holder a perpetual, worldwide, non-exclusive, royalty-free copyright license to use, reproduce, modify, prepare derivative works from, publicly display, distribute, and sublicense the contribution. This grant permits the project copyright holder to:

- distribute the contribution as part of this project under PolyForm Noncommercial License 1.0.0;
- offer the contribution under separate commercial terms.

Submission also requires that:

- third-party material must be clearly identified and may be included only when its upstream license permits the intended distribution;
- a contribution must not remove or weaken existing copyright, license, provenance, trademark, or Required Notice information.

If you cannot grant both the noncommercial project license and the right for the project copyright holder to offer separate commercial terms, do not submit the material as a contribution without first obtaining a separate written agreement.
