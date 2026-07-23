<p align="center">
  <img src="./assets/brand/hero-bilingual.svg" alt="LL-AcademicSkillsHub" width="100%">
</p>

<p align="center">
  <strong>Local-first, bilingual, and evidence-tiered academic AI skills</strong><br>
  <a href="./README.md">中文</a> ·
  <a href="./docs/skills.en.md">All skills</a> ·
  <a href="./docs/deployment.en.md">Local setup</a> ·
  <a href="./docs/quality-model.en.md">Quality model</a> ·
  <a href="https://github.com/ss8875/LL-AcademicSkillsHub/actions">Quality workflow</a>
</p>

# LL-AcademicSkillsHub

LL-AcademicSkillsHub organizes research skills into a searchable, installable, and auditable bilingual catalog. The first release contains **187 skills** across **18 categories**: **10 Lianlin first-party core skills** and **177 pinned third-party skills**.

## What you can do

- Find capabilities by research task in the [complete skill and function catalog](./docs/skills.en.md).
- Inspect inputs, outputs, runtime, network, credentials, risk, source, and quality status.
- Run the searchable local site on Windows, macOS, or Linux using only the Python standard library.
- Choose the integrated Lianlin Research AI Platform route if individual skill setup is inconvenient.

## Quick start

```powershell
./scripts/setup.ps1
./scripts/start.ps1
```

Open `http://127.0.0.1:8765/`. Windows users may also run `scripts\setup.bat` and `scripts\start.bat`.

> The first release deliberately supports only local deployment or the Lianlin Research AI Platform download route. It does not promise compatibility with a particular agent client. Third-party runtimes, API credentials, and data permissions still follow each function card.

## Brand and promotion boundary

Lianlin Research AI Platform appears only on explicit surfaces such as the README, documentation site, download page, and release notes. It is not an always-running skill and never interrupts research workflows. Until an official URL is supplied, the site states that it is unconfigured instead of inventing a link or QR code.

## Quality and provenance

`cataloged → beta → tested → verified → gold` are evidence levels; inclusion is not verification. Pinned third-party instructions remain upstream work and carry separate provenance and license-review status. See the [quality model](./docs/quality-model.en.md), [third-party notices](./THIRD_PARTY_NOTICES.md), and generated [audit report](./reports/audit.en.md).

## License

Lianlin first-party code and original documentation are Apache-2.0. Third-party skills remain under their upstream terms and do not become Apache-2.0 merely by inclusion.
