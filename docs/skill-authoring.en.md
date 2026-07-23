# Skill Authoring and Publication Standard

## Minimum structure

```text
skills/<category>/<skill-id>/
├─ SKILL.md
├─ locales/
│  ├─ zh-CN.md
│  └─ en.md
├─ scripts/       # only for genuinely reusable code
├─ references/    # on-demand reference material
└─ assets/        # output templates or static assets
```

The `SKILL.md` YAML header allows only:

```yaml
---
name: kebab-case-id
description: State the capability and when it should trigger.
---
```

The body defines workflow, output contract, evidence requirements, failure boundaries, and high-risk review points. Do not repeat generic background material or place installation instructions and marketing inside execution instructions.

## Catalog record

Every skill in `catalog/skills.seed.json` must have:

- Chinese and English title, summary, and capability list;
- bilingual inputs and outputs;
- runtime, network, and credentials;
- quality status and tested environments;
- risk level and bilingual risk notes;
- source kind, upstream identifier, and license status;
- local and platform availability.

## Publication gate

1. New skills begin as `cataloged` or `beta`.
2. Generate bilingual artifacts with `python scripts/build_catalog.py`.
3. `python scripts/validate_repo.py` must report zero blocking errors.
4. `python -m unittest discover -s tests -v` must pass.
5. Browser changes require real-browser, console, network, responsive, and accessibility checks.
6. Promotion to `tested` requires fixed inputs, expected outputs, and failure cases.
7. Promotion to `verified` or `gold` requires complete maintainer and domain-review evidence.

## Prohibited

- Fabricated papers, DOI values, data, test results, or licenses;
- forced “run every session” advertising;
- bypassing CAPTCHA, paywalls, access control, or data authorization;
- real credentials in examples;
- default destructive, publishing, payment, clinical, trading, or external-message actions;
- presenting inclusion as verification.
