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

You do not need to memorize 187 skill names. The easiest way to begin is to **state your research goal and available materials, then let your local Agent select the right skill or skill sequence from the catalog.** If you already know a skill name, mention it directly.

### Step 1: Choose how to use the project

#### Option A: Run it locally

From the repository root:

```powershell
./scripts/setup.ps1
./scripts/start.ps1
```

Open `http://127.0.0.1:8765/` to search categories, skills, and functions. Windows users may also run `scripts\setup.bat` and `scripts\start.bat`; see the [local deployment guide](./docs/deployment.en.md) for other systems and environment checks.

After finding a skill, open its detailed guide and check its use cases, required materials, workflow, outputs, references, and boundaries before connecting the skill directory to your local Agent Skill environment.

#### Option B: Use Lianlin Research AI Platform

If you do not want to install skills, configure dependencies, or debug the environment one by one, use the integrated Lianlin Research AI Platform. The download and WeChat support entry is in “[Don't want to install locally? Use Lianlin Research AI Platform](#lianlin-platform)”.

### Step 2: Start with one complete request

A useful request has five parts: **research goal, available materials, task scope, expected output, and quality requirements**. Copy and adapt this template:

> Select the most suitable skill or skill sequence from LL-AcademicSkillsHub. My research goal is [the question to solve]. My available materials are [papers, data, code, images, protocols, or drafts]. The scope is [population, time range, language, method, target journal, or exclusions]. Produce [a table, report, code, figure, manuscript, or audit checklist]. Preserve evidence sources and key parameters, distinguish facts from inferences and uncertainty, do not invent missing information, and list the decisions that require my confirmation.

Incomplete materials are acceptable. Ask the Agent to check input sufficiency first and return missing items, risks, and a proposed plan before execution.

### Step 3: Enter through the research workflow

| Research stage | Start with these categories | Typical outcome |
|---|---|---|
| Topic selection and planning | Academic Core · Research Methods & Scientific Reasoning | Map trends and gaps, form research questions, propose hypotheses, and assess novelty and feasibility |
| Search and evidence acquisition | Literature Search & Management · Scientific Databases | Build queries, search across databases, deduplicate and screen records, and acquire metadata or lawful full text |
| Close reading and knowledge organization | Academic Core · Document Processing & Data Tools | Parse PDFs and documents, perform bilingual close reading, locate evidence, and create reading cards or evidence matrices |
| Study design and experiment execution | Research Methods & Scientific Reasoning · Laboratory Automation & Integration · Platform & Infrastructure | Design studies, identify bias, draft protocols, connect laboratory workflows, and configure compute resources |
| Data processing and modeling | Data Analysis & Statistical Modeling · Machine Learning & AI | Clean data, perform inference, train models, diagnose errors, interpret results, and preserve reproducibility records |
| Manuscript writing and submission | Scientific Writing & Communication · Document Processing & Data Tools | Draft papers, grants, and reports; improve language; apply templates; and prepare submission files |
| Figures and research communication | Academic Presentation & Visualization | Create paper figures, mechanism diagrams, posters, slide decks, and editable visual assets |
| Review, revision, and governance | Academic Core · Scientific Writing & Communication | Simulate peer review, prepare point-by-point responses, audit citations, and check data-availability or compliance boundaries |

### Step 4: Enter through your research domain

| Research domain | Relevant categories | Common work |
|---|---|---|
| Life science and medicine | Bioinformatics & Genomics · Clinical & Precision Medicine · Protein Engineering & Structural Biology | Sequence and omics analysis, single-cell workflows, medical imaging, clinical evidence, and protein structure or function |
| Chemistry, drug discovery, and materials | Cheminformatics & Drug Discovery · Materials Science & Computational Physics | Molecular processing, property prediction, virtual screening, structure design, materials simulation, and physics computation |
| Finance, economics, and spatial research | Finance & Economics Data · Geospatial & Remote Sensing | Market and macroeconomic data, company research, GIS, remote-sensing imagery, and spatial analysis |
| Cross-disciplinary computational research | Scientific Databases · Data Analysis & Statistical Modeling · Machine Learning & AI · Platform & Infrastructure | Data acquisition, normalization, statistical or AI modeling, cloud computing, and workflow orchestration |

### Step 5: Copy a real task to begin

| Goal | Example request |
|---|---|
| Analyze a research topic | “Search representative work from the past five years on [topic], separate active trends, solved problems, and evidence-backed gaps, then propose three feasible topics scored for novelty, data, methods, ethics, and resources.” |
| Run a reproducible literature search | “Split [research question] into concept blocks and synonyms, build reproducible queries for [databases], record dates, filters, and hit counts, deduplicate the results, and screen them with [criteria].” |
| Read Chinese and English papers closely | “Read these PDFs and build a bilingual terminology list. Extract the question, methods, sample, results, and limitations, and attach a page, figure, table, or section locator to every key claim.” |
| Build a systematic-review evidence table | “Create an evidence matrix for these papers, comparing design, sample, variables, methods, results, and risk of bias. Keep author claims separate from evidence demonstrated in the paper.” |
| Design a study | “Using [question and existing evidence], specify hypotheses, units of analysis, sampling, controls, measurements, exclusions, missing-data handling, primary outcomes, reproducibility plan, and any ethics-review requirements.” |
| Analyze research data | “Audit variables, missingness, outliers, distributions, and collection quality first. Then choose suitable statistical methods and return runnable code, effect sizes, uncertainty, diagnostics, and sensitivity analyses.” |
| Perform domain-specific analysis | “This is [sequence, clinical, molecular, materials, finance, or spatial] data. Confirm versions, units, reference systems, and method suitability before selecting the relevant domain skills and proposing validation.” |
| Draft a paper section or manuscript | “Draft the [abstract, introduction, methods, results, or discussion] from these sources, results, and figures. Preserve facts, numbers, and citations; separate results from interpretation; flag unsupported statements.” |
| Create figures and a presentation | “Design a submission-ready multi-panel figure from these data and conclusions, with editable source files, captions, and data mappings; then turn the central evidence into a lab-meeting deck.” |
| Simulate peer review | “Review this manuscript for the question, novelty, methods, statistics, figures, reporting completeness, and reproducibility. Return major issues, minor issues, and actionable revisions.” |
| Audit citations and references | “Check consistency between in-text citations and references, then verify DOI, authors, journal, year, and pages. Classify each item as verified, partial match, conflict, or unverifiable; do not invent fields.” |
| Respond to reviewers | “Decompose every reviewer comment, map it to manuscript locations and revision evidence, and draft a courteous, specific, verifiable response. Explain any declined request with evidence and list decisions still requiring the authors.” |

### Step 6: Combine skills when the task is complex

Complex research usually requires skills to hand off explicit artifacts:

- **Topic to paper:** topic analysis → reproducible search → full-text close reading → study design → data analysis → scientific figures → manuscript writing → citation audit.
- **Systematic review:** search strategy → deduplication and screening → evidence extraction → bias assessment → statistical synthesis → PRISMA flow and review writing.
- **Data paper:** data and variable audit → domain analysis → statistics or machine learning → visualization → methods and results writing → data-availability statement.
- **Submission and revision:** journal template → pre-submission audit → simulated peer review → revised manuscript → point-by-point response → citation, figure, and supplement checks.

You can say: “First propose the skill sequence, the input and output of each step, and the human checkpoints; execute it in stages after I provide the materials.” Staged review makes evidence gaps and methodological errors easier to detect than one-shot generation.

<a id="lianlin-platform"></a>

## Don't want to install locally? Use Lianlin Research AI Platform

<p align="center">
  <img src="./assets/brand/platform-promo/platform-wechat-banner.png" alt="Download Lianlin Research AI Platform or contact WeChat support" width="100%">
</p>

## Brand and promotion boundary

Lianlin Research AI Platform appears only on explicit surfaces such as the README, documentation site, download page, and release notes. It is not an always-running skill and never interrupts research workflows. Until an official URL is supplied, the site states that it is unconfigured instead of inventing a link or QR code.

## Quality and provenance

`cataloged → beta → tested → verified → gold` are evidence levels; inclusion is not verification. Pinned third-party instructions remain upstream work and carry separate provenance and license-review status. See the [quality model](./docs/quality-model.en.md), [third-party notices](./THIRD_PARTY_NOTICES.md), and generated [audit report](./reports/audit.en.md).

## License

Lianlin first-party code and original documentation are Apache-2.0. Third-party skills remain under their upstream terms and do not become Apache-2.0 merely by inclusion.
