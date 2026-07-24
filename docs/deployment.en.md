# Local Deployment

If you prefer not to deploy or debug a local environment, [download Lianlin Research AI Platform 0.3.18 for Windows](https://github.com/ss8875/LL-AcademicSkillsHub/releases/download/lianlin-ai-v0.3.18/Lianlin-Research-AI-Platform-Setup-0.3.18.exe).

## Environment

- Windows 10/11, macOS 12+, or a mainstream Linux distribution;
- Python 3.10 or newer;
- Git is optional and only needed for cloning and version control;
- roughly 100 MB free disk space, excluding models, databases, and dependencies installed by individual skills.

The catalog site uses only the Python standard library. It does not require Node.js, Docker, or a database. Python/R/Node runtimes, API credentials, network access, and data permissions for an individual skill follow that skill's function card and `SKILL.md`.

## Windows

```powershell
git clone https://github.com/ss8875/LL-AcademicSkillsHub.git
cd LL-AcademicSkillsHub
./scripts/setup.ps1
./scripts/start.ps1
```

If PowerShell execution policy blocks direct scripts, run:

```bat
scripts\setup.bat
scripts\start.bat
```

## macOS / Linux

```bash
git clone https://github.com/ss8875/LL-AcademicSkillsHub.git
cd LL-AcademicSkillsHub
python3 scripts/build_catalog.py
python3 scripts/validate_repo.py
python3 scripts/doctor.py
python3 scripts/serve.py
```

Open `http://127.0.0.1:8765/site/`.

## Configuration

Copy `.env.example` to `.env`. `LL_HOST` and `LL_PORT` control the bind address and port. `LIANLIN_PLATFORM_DOWNLOAD_URL` already points to the current official installer; override it only for a new release or an internal mirror.

The default bind address is `127.0.0.1` for local access only. If you change it to `0.0.0.0`, configure firewall, reverse proxy, TLS, and access control yourself.
