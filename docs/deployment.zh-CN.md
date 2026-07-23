# 本地部署

## 环境

- Windows 10/11、macOS 12+ 或常见 Linux 发行版；
- Python 3.10 或更高版本；
- Git 可选，仅用于克隆和版本管理；
- 约 100 MB 可用磁盘空间（不含各技能后续安装的模型、数据库和依赖）。

目录站点本身只使用 Python 标准库，不要求 Node.js、Docker 或数据库。某个具体技能需要的 Python/R/Node、API 密钥、网络和数据权限，应以该技能功能卡与 `SKILL.md` 为准。

## Windows

```powershell
git clone https://github.com/ss8875/LL-AcademicSkillsHub.git
cd LL-AcademicSkillsHub
./scripts/setup.ps1
./scripts/start.ps1
```

没有配置 PowerShell 执行权限时，可双击或运行：

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

浏览器打开 `http://127.0.0.1:8765/site/`。

## 配置

复制 `.env.example` 为 `.env`。`LL_HOST` 与 `LL_PORT` 控制监听地址和端口。只有在获得官方链接后才设置 `LIANLIN_PLATFORM_DOWNLOAD_URL`；未配置时页面必须显示“待配置”，不能生成虚假链接或二维码。

默认绑定 `127.0.0.1`，只供本机访问。若改为 `0.0.0.0`，请自行配置防火墙、反向代理、TLS 与访问控制。
