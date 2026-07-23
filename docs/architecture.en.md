# Final Architecture

## Design principle

The public architecture starts from the LL-AcademicSkillsHub brand and research tasks. It has no “whole-web sources” layer. Provenance, license, and community contribution remain visible per-skill governance fields without overriding the brand or user workflow.

```text
LL-AcademicSkillsHub
├─ Brand and user entry
│  ├─ Chinese README / English README
│  ├─ Searchable local site
│  └─ Local deployment / Lianlin Research AI Platform
├─ Academic capability catalog
│  ├─ 18 research-task categories
│  ├─ 187 bilingual function cards
│  └─ Inputs, outputs, environment, risk, and quality
├─ Skill implementations
│  ├─ 10 Lianlin first-party core skills
│  └─ 177 pinned third-party skills
├─ Trust governance
│  ├─ Provenance and license status
│  ├─ cataloged → beta → tested → verified → gold
│  ├─ Static security scan and regression tests
│  └─ Machine-readable audit report
└─ Local runtime
   ├─ build / validate / doctor / serve
   ├─ Windows PowerShell and batch entry points
   └─ Dependency-free Python static server
```

## Single sources of truth

- `catalog/categories.seed.json`: 18 stable categories;
- `catalog/skills.seed.json`: authoritative bilingual records for 187 skills;
- `scripts/build_catalog.py`: generates READMEs, category tables, full skill tables, and site data;
- `scripts/validate_repo.py`: checks structure, bilingual parity, syntax, security, brand boundaries, provenance, and release contract;
- `site/data/catalog.json`: published browser data and never hand-edited.

## Skill boundary

Lianlin first-party skills provide complete, independent, bilingual evidence workflows. Pinned third-party skills retain upstream `SKILL.md`, scripts, and assets; Lianlin adds bilingual function cards and governance metadata. Any audit-driven edit to a third-party file must be recorded in `docs/upstream-patches.md`.

## Local server boundary

The local server exposes `site/`, `skills/`, `docs/`, `assets/`, and a small public root-file allowlist. It blocks `.env`, `.git`, `scripts/`, `catalog/`, and `reports/`, and binds to `127.0.0.1` by default.

## First-release non-goals

No specific agent-client compatibility promise, cloud multi-user system, automatic installation of all scientific dependencies, access-control bypass, or claim that every third-party skill has completed live API or scientific-validity verification.
