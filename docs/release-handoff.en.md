# 0.1.0 Release Handoff

## Delivery result

The first local-deployment release is complete and passes the publication gate. The repository contains 187 skills, 18 categories, 10 Lianlin first-party core capabilities, and 177 pinned third-party capabilities. Chinese and English catalogs share one source of truth, and the site supports search, category filtering, and quality filtering.

## Verified

- Build, deep audit, environment doctor, and nine regression tests pass.
- Catalog, disk, and site each contain the same 187 skill IDs.
- Chinese/English switching, search, category, and quality filters pass in real Chrome.
- Desktop and 390px mobile layouts have no horizontal overflow.
- Browser console has zero errors and warnings; no resource requests fail.
- `.env`, `.git`, `scripts/`, `catalog/`, and `reports/` are unreachable from the local server.
- The release ZIP is complete and has a SHA-256 manifest.

## Quality interpretation

- 10 Lianlin first-party skills are `beta`.
- 177 third-party skills are `cataloged`.
- The release audit has zero blocking errors.
- Nineteen non-blocking warnings come from dynamic execution or pipe-install patterns in third-party source; the itemized list is in `reports/audit.json`.
- All 177 third-party skills still rely on collection-level license metadata from the pinned bundle and need per-skill confirmation before commercial redistribution.

## Key commands

```powershell
./scripts/setup.ps1
./scripts/start.ps1
./scripts/build.ps1
```

Individual commands:

```powershell
python scripts/build_catalog.py
python scripts/validate_repo.py
python -m unittest discover -s tests -v
python scripts/package_release.py
```

## Lianlin Research AI Platform installer

The Windows 0.3.18 installer is published as a GitHub Release asset:

- [Direct installer download](https://github.com/ss8875/LL-AcademicSkillsHub/releases/download/lianlin-ai-v0.3.18/Lianlin-Research-AI-Platform-Setup-0.3.18.exe)
- Size: 122,424,791 bytes (approximately 116.75 MB)
- SHA-256: `E502A3422E69A015BFBD56B8A1483C5CE4E1663F08C75D9AE0DE2639CAE280F6`

The installer is not currently Windows code-signed, so the release page and download documentation explain checksum verification. For later versions, update version, direct asset URL, size, and digest in `catalog/platform-release.json`, then run the complete build.

## Handoff entry points

- Chinese home: `README.md`
- English home: `README.en.md`
- All skills: `docs/skills.zh-CN.md` / `docs/skills.en.md`
- Final architecture: `docs/architecture.en.md`
- Quality model: `docs/quality-model.en.md`
- Audit: `reports/audit.en.md`
- Release package: `dist/LL-AcademicSkillsHub-local.zip`
- Checksum manifest: `dist/manifest.json`
