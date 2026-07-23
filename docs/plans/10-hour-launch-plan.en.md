# LL-AcademicSkillsHub Initial 10-Hour Delivery Plan

## Objective

Deliver the first local-first release of LL-AcademicSkillsHub in one continuous execution window, with complete Simplified Chinese and English user-facing documentation and catalog interfaces.

The initial release offers only:

1. local deployment from source; and
2. download of the Lianlin Research AI Platform.

It does not promise compatibility with external agent clients, provide a cloud SaaS, or expose content sources as a public-facing architecture layer.

## Ten-hour work packages

### H0–H1: Freeze scope and create the foundation

- Create the repository structure and project policies.
- Define schemas for skills, categories, locales, quality states, and local runtime requirements.
- Establish bilingual documentation, catalog, site, scripts, and test directories.

Acceptance:

- No unprovable “whole web” or “most complete on the internet” claims.
- Only local deployment and platform download are presented as user routes.

### H1–H3: Import and normalize skills

- Import the pinned academic skill bundle already used by the Lianlin research product.
- Remove third-party platform advertising skills.
- Normalize five existing core capabilities as Lianlin core skills.
- Add five identified capability gaps: bilingual evidence reading, lawful full-text acquisition, FAIR data availability, experiment notebook, and research-to-patent.
- Generate bilingual metadata and function cards for every published skill.

Acceptance:

- Every public skill ID is unique.
- Internal fragments, advertisements, and planned items are not counted as available skills.
- Every skill has Chinese and English names, summaries, use cases, inputs, outputs, environment requirements, risk, and maturity.

### H3–H5: Build bilingual catalogs and the local site

- Generate Chinese and English READMEs.
- Generate category pages, complete skill indexes, and skill detail pages.
- Build a searchable local static site with language, category, maturity, and runtime filters.

Acceptance:

- Counts are generated from catalog data.
- Chinese and English catalogs contain identical skill ID sets.
- The built site is usable locally without a remote service.

### H5–H6.5: Local deployment experience

- Implement environment diagnostics, build, and start commands.
- Provide PowerShell and batch entry points.
- Serve the local site with the Python standard library.
- Recommend the Lianlin Research AI Platform when local prerequisites are unavailable.

Acceptance:

- Works from Windows paths containing spaces and Chinese characters.
- Does not modify the user's global Python environment.
- Does not require installing every scientific dependency.

### H6.5–H8: Quality, security, and license gates

- Validate skill structure, frontmatter, metadata, bilingual parity, and links.
- Parse-check Python, JavaScript, and shell scripts.
- Scan for secrets, unsafe downloads, runtime package pulls, CAPTCHA bypasses, and forced third-party advertising.
- Generate machine-readable provenance and license audit results.

Acceptance:

- Zero structural or bilingual parity errors.
- High-risk entries cannot be labeled Verified or Gold.
- Every warning appears in the audit report.

### H8–H9: Full build and remediation

- Build all catalogs, pages, statistics, and site assets.
- Run the full validation suite.
- Fix blockers and rebuild.
- Verify Chinese/English parity and local browsing.

### H9–H10: Release readiness and handoff

- Produce release-readiness, quality, and known-limitations reports.
- Distinguish Lianlin core skills from pinned third-party snapshots.
- Document platform download placeholders.
- Complete final repository and file inventory checks.

## Quality states

- `cataloged`: indexed but not runtime-verified.
- `beta`: usable with known edge cases.
- `tested`: structural and basic behavior checks pass.
- `verified`: dependency, security, runtime, and output checks pass.
- `gold`: real-task comparative evaluation and expert review pass.
- `restricted`: cannot be enabled directly due to license, safety, or runtime constraints.

Publishing every skill in the catalog does not imply that every skill is Verified or Gold.

## Continuous execution

The user explicitly authorized uninterrupted implementation. Automated gates replace intermediate approval checkpoints. Missing real download URLs, QR codes, or original brand assets are represented with explicit placeholders and do not block the repository implementation.
