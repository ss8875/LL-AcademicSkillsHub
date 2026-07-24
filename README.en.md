<p align="center">
  <img src="./assets/brand/hero-bilingual.svg" alt="LL-AcademicSkillsHub" width="100%">
</p>

<p align="center">
  <strong>Local-first, bilingual, and evidence-tiered academic AI skills</strong><br>
  <a href="./README.md">中文</a> ·
  <a href="./docs/skills.en.md">All skills</a> ·
  <a href="./docs/deployment.en.md">Local setup</a> ·
  <a href="https://github.com/ss8875/LL-AcademicSkillsHub/releases/download/lianlin-ai-v0.3.18/Lianlin-Research-AI-Platform-Setup-0.3.18.exe">Download Research AI Platform</a> ·
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

## Skill Architecture Map

<p align="center">
  <a href="./assets/brand/skill-architecture-map.svg">
    <img src="./assets/brand/skill-architecture-map.svg" alt="Architecture map connecting all 187 LL-AcademicSkillsHub skills" width="100%">
  </a>
</p>

<p align="center"><sub>Seven capability domains connect research discovery, domain computation, data intelligence, research operations, and scholarly communication. Click the image for the scalable full-size map.</sub></p>

<a id="lianlin-platform"></a>

## Don't want to install locally? Use Lianlin Research AI Platform

<p align="center">
  <a href="https://github.com/ss8875/LL-AcademicSkillsHub/releases/download/lianlin-ai-v0.3.18/Lianlin-Research-AI-Platform-Setup-0.3.18.exe">
    <img src="./assets/brand/platform-promo/platform-wechat-banner.png" alt="Download Lianlin Research AI Platform or contact WeChat support" width="100%">
  </a>
</p>

<p align="center">
  <a href="https://github.com/ss8875/LL-AcademicSkillsHub/releases/download/lianlin-ai-v0.3.18/Lianlin-Research-AI-Platform-Setup-0.3.18.exe"><strong>⬇ Download Lianlin Research AI Platform 0.3.18 for Windows</strong></a><br>
  <sub>Approx. 116.75 MB · SHA-256: <code>E502A3422E69A015BFBD56B8A1483C5CE4E1663F08C75D9AE0DE2639CAE280F6</code></sub>
</p>

## Installation

Local use has two separate layers. Choose the one that matches your goal:

| Goal | What to complete | Result |
|---|---|---|
| Browse, search, and read every skill | Deploy the local skill catalog | A private local website covering 18 categories, 187 skills, and their detailed guides |
| Let a local Agent invoke skills | Deploy the catalog, then install skills into the Agent | Complete skill directories in the Agent's skill path, available after the Agent restarts |
| Avoid local configuration | Use the Lianlin Research AI Platform entry above | Integrated access to the research capabilities |

### 1. Prerequisites

| Component | Minimum | Purpose |
|---|---|---|
| Operating system | Windows 10/11, macOS 12+, or a mainstream Linux distribution | Run the local catalog and scripts |
| Python | 3.10 or newer | Build, validate, and serve the catalog |
| Git | Optional | Clone and update the repository; a ZIP download also works |
| Disk | At least 100 MB | Store the repository, catalog data, and guides |
| Node.js | 18 or newer, only for Agent skill installation | Select and copy skills with `npx skills` |

Check installed versions:

```text
python --version
git --version
node --version
npm --version
```

The local catalog itself needs **no Node.js, Docker, database, or third-party Python package**. If Git is unavailable, select `Code → Download ZIP` on GitHub, extract the archive, and continue below.

### 2. Method one: Deploy the local skill catalog

#### 2.1 Download the repository

Git is recommended because it makes later updates simple:

```powershell
git clone https://github.com/ss8875/LL-AcademicSkillsHub.git
cd LL-AcademicSkillsHub
```

For a ZIP download, extract the complete archive and open a terminal in the extracted `LL-AcademicSkillsHub` directory. Run every following command from the repository root, not from a system directory such as `C:\Windows\System32`.

#### 2.2 Automated Windows setup

Open PowerShell in the repository root:

```powershell
.\scripts\setup.ps1
.\scripts\start.ps1
```

`setup.ps1` checks Python 3.10+, creates the local `.env` file on first run, regenerates the bilingual catalog and all 187 guides, then runs the repository audit and environment doctor.

After `Setup complete` appears, run `start.ps1`. If PowerShell blocks script execution, use the supplied batch entry points without changing the system execution policy:

```bat
scripts\setup.bat
scripts\start.bat
```

#### 2.3 macOS or Linux setup

```bash
git clone https://github.com/ss8875/LL-AcademicSkillsHub.git
cd LL-AcademicSkillsHub
cp .env.example .env
python3 scripts/build_catalog.py
python3 scripts/validate_repo.py
python3 scripts/doctor.py
python3 scripts/serve.py
```

The first three Python commands generate the catalog, audit the repository, and check the environment. The last command starts the local website.

#### 2.4 Open, stop, and restart

A successful start prints:

```text
LL-AcademicSkillsHub: http://127.0.0.1:8765/site/
Press Ctrl+C to stop.
```

Open `http://127.0.0.1:8765/`; the root URL redirects to `/site/`. Keep the terminal open while using the site. Press `Ctrl+C` to stop it safely, then run `scripts\start.ps1` or `python3 scripts/serve.py` to restart.

#### 2.5 Change the port or bind address

Local settings live in `.env`:

```dotenv
LL_HOST=127.0.0.1
LL_PORT=8765
```

If the port is busy, change `LL_PORT` to `9000` or run:

```powershell
.\scripts\start.ps1 --port 9000
```

`127.0.0.1` allows access only from the same computer. Do not change it to `0.0.0.0` unless firewall rules, access control, a reverse proxy, and TLS are already configured.

#### 2.6 Verify the deployment

Windows:

```powershell
python scripts\doctor.py
python -m unittest discover -s tests -v
```

macOS / Linux:

```bash
python3 scripts/doctor.py
python3 -m unittest discover -s tests -v
```

`"ready": true` in the doctor output confirms that the catalog and site exist; the tests should finish with `OK`. The browser should let you search skills, switch among 18 categories, and open detailed guides.

#### 2.7 Update the repository

For a Git installation:

```powershell
git pull
.\scripts\setup.ps1
```

On macOS or Linux, rerun the generation and validation commands above after `git pull`. ZIP users should download and extract the new version; back up a customized `.env` first.

### 3. Method two: Install skills into a local Agent

Installable units live under `skills/<category>/<skill-name>/` and retain their complete `SKILL.md` directories. The repository has been tested with `npx skills`, which discovers all **187 skills**.

#### 3.1 List available skills

Install Node.js 18 or newer, then run:

```powershell
npx skills add ss8875/LL-AcademicSkillsHub --list
```

A successful scan prints `Found 187 skills` and names such as `ll-paper-search`, `ll-paper-analysis`, `scanpy`, and `scientific-writing`.

#### 3.2 Install every skill globally for Codex

```powershell
npx skills add ss8875/LL-AcademicSkillsHub --global --agent codex --skill '*' --yes --copy
```

`--global` makes the skills available to all local projects; `--agent codex` selects the target Agent; `--skill '*'` selects every skill; and `--copy` preserves each complete skill directory.

#### 3.3 Install one skill for the current project

Omit `--global` for a project-scoped installation:

```powershell
npx skills add ss8875/LL-AcademicSkillsHub --agent codex --skill ll-paper-search --yes --copy
```

Replace `ll-paper-search` with any exact name returned by `--list`.

#### 3.4 Install a research workflow

For example, install paper search, close reading, and citation audit together:

```powershell
npx skills add ss8875/LL-AcademicSkillsHub --global --agent codex `
  --skill ll-paper-search `
  --skill ll-paper-analysis `
  --skill ll-citation-audit `
  --yes --copy
```

On macOS or Linux, replace the PowerShell continuation character `` ` `` with `\`, or place the command on one line.

#### 3.5 Check, update, and activate

```powershell
npx skills list --global --agent codex --json
npx skills update --global --yes
```

After installation or update, **fully close and reopen the Agent session** so it rescans its skill directories. The installer copies skill files; configure any specialized Python/R packages, external programs, models, or API credentials only when the selected detailed guide requires them.

### 4. Troubleshooting

| Symptom | Cause | Resolution |
|---|---|---|
| `python` is not recognized | Python is missing or not on PATH | Install Python 3.10+; select `Add Python to PATH` on Windows, then reopen the terminal |
| `git` is not recognized | Git is missing | Install Git or use GitHub's `Download ZIP` |
| `winget` is not recognized | Windows Package Manager is unavailable | This project does not require `winget`; use the official Python, Git, or Node.js installers |
| PowerShell blocks scripts | Execution policy restriction | Use `scripts\setup.bat` and `scripts\start.bat` |
| `npx` is not recognized | Node.js/npm is missing or the terminal is stale | Install Node.js 18+, then reopen the terminal |
| Port 8765 is busy | Another process uses the port | Run `scripts\start.ps1 --port 9000` or edit `.env` |
| The browser cannot connect | The service is stopped or the URL is wrong | Restart the service and open `http://127.0.0.1:8765/` |
| The Agent cannot see a new skill | The Agent started before installation | Exit the Agent completely, reopen it, and check the skill list |
| An installed skill fails at runtime | A specialized dependency is missing | Open that skill's detailed guide and configure the required dependency or credential |

See the [local deployment document](./docs/deployment.en.md) for the compact system reference.


## Quality and provenance

`cataloged → beta → tested → verified → gold` are evidence levels; inclusion is not verification. Pinned third-party instructions remain upstream work and carry separate provenance and license-review status. See the [quality model](./docs/quality-model.en.md), [third-party notices](./THIRD_PARTY_NOTICES.md), and generated [audit report](./reports/audit.en.md).

## License

Lianlin first-party code and original documentation are Apache-2.0. Third-party skills remain under their upstream terms and do not become Apache-2.0 merely by inclusion.
