# GitHub 项目发布与维护操作手册

> 以 LL-AcademicSkillsHub 的真实发布方式为案例，整理成可复制到其他项目的通用流程。
>
> 适用范围：Windows、macOS、Linux；新项目首次上传、已有项目迁移、日常更新、版本发行、大文件发布与交接。
>
> 最后核对日期：2026-07-24

## 1. 这份手册解决什么问题

把一个本地项目放到 GitHub，不只是执行一次 `git push`。可靠的发布流程至少需要同时处理：

1. 哪些内容应该进入源码仓库；
2. 哪些内容必须排除，例如密钥、缓存、日志和本机构建产物；
3. 如何建立本地 Git 历史并连接远程仓库；
4. 如何安全完成首次推送和后续更新；
5. 如何发布 ZIP、安装程序等下载文件；
6. 如何用自动化检查避免把损坏或未同步的内容推到公开仓库；
7. 如何让其他维护者接手后仍能重复构建、验证和发布。

本文给出两层内容：

- **项目实录**：LL-AcademicSkillsHub 实际采用了什么结构；
- **通用模板**：其他项目只需替换项目名、目录、仓库地址和验证命令即可复用。

---

## 2. LL-AcademicSkillsHub 的实际发布架构

### 2.1 当前仓库

| 项目 | 实际值 |
|---|---|
| GitHub 仓库 | `https://github.com/ss8875/LL-AcademicSkillsHub` |
| 可见性 | Public |
| 默认分支 | `main` |
| 源码版本标签 | `v0.1.0` |
| 平台安装包标签 | `lianlin-ai-v0.3.18` |
| 自动化检查 | `.github/workflows/quality.yml` |
| 本地发行包 | `dist/LL-AcademicSkillsHub-local.zip` |
| 发行校验清单 | `dist/manifest.json` |
| 链邻原创部分许可 | PolyForm Noncommercial License 1.0.0；商业使用须事先书面授权 |
| 第三方内容 | 继续适用各自上游条款，不由仓库级许可覆盖 |

### 2.2 三层发布模型

这个项目没有把所有文件不加区分地提交到 GitHub，而是采用三层模型：

| 层级 | 放什么 | 放在哪里 | 原因 |
|---|---|---|---|
| 源码层 | README、文档、技能、脚本、测试、目录数据、网站源码 | Git 仓库 | 需要版本记录、审查和协作 |
| 构建层 | 本地 ZIP、构建清单、临时检查结果 | 本地 `dist/` 或 CI 工作区 | 可由源码重新生成，不应反复污染 Git 历史 |
| 发行层 | 用户实际下载的 ZIP、清单、Windows 安装程序 | GitHub Releases | 面向用户分发，避免把大型二进制写入 Git 历史 |

这套划分可以直接用于桌面软件、数据工具、模型应用、文档产品和网站项目。

### 2.3 为什么安装程序放 Release，不放源码仓库

链邻科研 AI 平台安装程序约为 116.75 MB，超过 GitHub 普通 Git 对象 100 MiB 的硬限制，因此没有提交到 `main` 分支，而是上传到独立 Release：

```text
Tag: lianlin-ai-v0.3.18
File: Lianlin-Research-AI-Platform-Setup-0.3.18.exe
Size: 122,424,791 bytes
SHA-256: E502A3422E69A015BFBD56B8A1483C5CE4E1663F08C75D9AE0DE2639CAE280F6
```

适合放入 Release 的文件：

- `.exe`、`.msi`、`.dmg`、`.AppImage` 等安装程序；
- 用户下载使用的 ZIP 或离线包；
- 模型、资源包或数据库快照；
- 需要同时公布版本、大小和校验值的交付物。

适合使用 Git LFS 的文件：

- 必须跟随分支和提交版本变化的大型二进制源文件；
- 设计源文件、训练权重、音视频素材等需要团队共同修改的文件；
- 不能仅作为某个版本下载附件存在的二进制资产。

如果文件只是用户下载的成品，优先选 Release；如果它是开发过程的一部分并需要版本化，才考虑 Git LFS。

### 2.4 本项目当前采用的源码推送方式

LL-AcademicSkillsHub 已由用户明确指定继续采用此前验证成功的发布方式：

```text
原生 Git + HTTPS remote + 本机 Git 凭据助手
→ 检查与测试
→ 明确暂存文件
→ 创建提交
→ git push origin main
→ 比较 HEAD 与 origin/main
```

普通源码推送不依赖 GitHub CLI。只有创建 Pull Request、操作 Issue、管理 Release 或调用 GitHub API 时，才需要 GitHub CLI、GitHub App 或网页端。

后续维护者和 Codex 对话应优先阅读[直接 Git 推送交接](./direct-git-push-handoff.zh-CN.md)。

---

## 3. 发布前的四项决策

在创建仓库前，先明确以下内容。

### 3.1 仓库身份

填写这组变量，后面的命令可以直接替换：

```text
PROJECT_NAME      = YOUR_PROJECT_NAME
PROJECT_DIR       = D:\path\to\YOUR_PROJECT_NAME
GITHUB_OWNER      = YOUR_GITHUB_USERNAME
REPOSITORY_NAME   = YOUR_REPOSITORY_NAME
DEFAULT_BRANCH    = main
REMOTE_URL        = https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY_NAME.git
```

仓库名建议：

- 只用英文字母、数字、短横线；
- 名称能直接表达项目用途；
- 不随意加入日期或临时版本号；
- 中文品牌名写在 README，不建议作为仓库 URL。

### 3.2 公开还是私有

| 选择 | 适用情况 | 发布前必须检查 |
|---|---|---|
| Public | 开源项目、产品展示、公共文档 | 许可证、第三方许可、密钥、个人信息、商业素材 |
| Private | 未公开产品、内部项目、客户项目 | 成员权限、组织策略、敏感数据、依赖授权 |

“Private”不能替代安全治理。密钥、身份证件、客户数据和生产数据库仍不应直接写入 Git 历史。

### 3.3 许可证

公开仓库最好在首次发布前明确许可证。常见选择：

- Apache-2.0：允许商业使用，并包含专利授权条款；
- MIT：简洁宽松；
- GPL：要求衍生发行保持同类开源义务；
- 专有许可证：仅允许查看或在特定条件下使用。

如果项目包含第三方代码、技能、模型或素材，需要额外维护：

- `THIRD_PARTY_NOTICES.md`
- 来源地址和固定版本；
- 上游许可证；
- 修改说明；
- 不适用于本项目统一许可证的例外。

不要因为把第三方文件复制进自己的仓库，就把它们自动声明成自己的许可证。

### 3.4 源码、生成物与发行物边界

发布前建立一张表：

| 文件类型 | Git 仓库 | Release | 忽略 |
|---|---:|---:|---:|
| 源代码、脚本、测试 | 是 | 可选 | 否 |
| README、许可证、贡献说明 | 是 | 否 | 否 |
| `.env.example` | 是 | 否 | 否 |
| `.env`、令牌、私钥 | 否 | 否 | 是 |
| 缓存、日志、临时文件 | 否 | 否 | 是 |
| 可重复生成的构建目录 | 通常否 | 可选 | 是 |
| 安装程序、交付 ZIP | 通常否 | 是 | 是 |
| 小型品牌图片 | 是 | 可选 | 否 |
| 大型可版本化素材 | Git LFS | 可选 | 否 |

---

## 4. 安装 Git 与选择认证方式

### 4.1 Windows

推荐顺序：

1. 从 [Git for Windows 官方页面](https://git-scm.com/download/win)下载安装；
2. 或安装 [GitHub Desktop](https://desktop.github.com/download/)，它适合不熟悉命令行的用户；
3. 如果电脑有 `winget`，也可以用包管理器安装；
4. 如果系统提示“无法识别 winget”，直接改用官方下载方式，不需要先修复 `winget`。

安装完成后关闭并重新打开 PowerShell：

```powershell
git --version
git config --global user.name "YOUR_NAME"
git config --global user.email "YOUR_GITHUB_EMAIL"
git config --global init.defaultBranch main
```

Git for Windows 通常会同时安装 Git Credential Manager。第一次通过 HTTPS 推送时，会打开浏览器完成 GitHub 登录，不需要把密码或令牌写进命令。

### 4.2 macOS

```bash
git --version
git config --global user.name "YOUR_NAME"
git config --global user.email "YOUR_GITHUB_EMAIL"
git config --global init.defaultBranch main
```

如果没有 Git，可以安装 Xcode Command Line Tools、Homebrew Git 或 GitHub Desktop。

### 4.3 Linux

通过发行版的软件包管理器安装 Git，然后配置用户名、邮箱和默认分支。使用 HTTPS 时，可以安装 Git Credential Manager；也可以使用 SSH 密钥。

### 4.4 HTTPS、SSH 与 GitHub CLI 怎么选

| 方式 | 推荐人群 | 特点 |
|---|---|---|
| HTTPS + Git Credential Manager | 大多数 Windows 用户 | 浏览器登录，配置最少 |
| SSH | 熟悉密钥管理的开发者 | 长期稳定，适合多仓库 |
| GitHub CLI `gh` | 需要命令行创建仓库和 Release 的用户 | 可自动化，但需要额外安装 |
| GitHub Desktop | 不熟悉命令行的用户 | 图形化提交、推送和分支管理 |

本文的主流程使用 **HTTPS + Git Credential Manager**，因为最容易在其他项目中复制。

---

## 5. 项目进入 Git 前的安全检查

### 5.1 先写 `.gitignore`

通用起点：

```gitignore
# Secrets
.env
.env.*
!.env.example
*.pem
*.key

# Python
__pycache__/
*.py[cod]
.venv/

# Node
node_modules/

# Build outputs
dist/
build/
coverage/

# Logs and caches
*.log
.cache/
.audit-cache/

# Operating system
.DS_Store
Thumbs.db
```

不要机械复制全部规则。某些项目需要跟踪 `dist/`，某些项目必须提交锁文件。应根据项目的构建和交付方式调整。

LL-AcademicSkillsHub 的关键规则是：

```gitignore
.env
.env.*
!.env.example
dist/
.tools/
.audit-cache/
```

含义：

- 真正的 `.env` 永不提交；
- 可公开的配置示例 `.env.example` 必须保留；
- 本地发行包和工具缓存不进入源码历史。

### 5.2 配置 `.gitattributes`

跨 Windows、macOS、Linux 的项目建议统一文本换行：

```gitattributes
* text=auto eol=lf
*.bat text eol=crlf
*.ps1 text eol=crlf

*.png binary
*.jpg binary
*.jpeg binary
*.gif binary
*.pdf binary
*.zip binary
```

这样可以减少“文件内容没变，但整份文件都显示变化”的换行问题。

### 5.3 检查大文件

PowerShell：

```powershell
$ProjectPath = "D:\path\to\YOUR_PROJECT"

Get-ChildItem -LiteralPath $ProjectPath -Recurse -File |
  Where-Object { $_.FullName -notmatch '\\.git\\' } |
  Sort-Object Length -Descending |
  Select-Object -First 30 FullName, Length
```

专门查找超过 50 MiB 的文件：

```powershell
Get-ChildItem -LiteralPath $ProjectPath -Recurse -File |
  Where-Object {
    $_.FullName -notmatch '\\.git\\' -and
    $_.Length -ge 50MB
  } |
  Select-Object FullName, Length
```

决策规则：

- 小于 50 MiB：通常可进入 Git，但仍要判断是否必要；
- 50–100 MiB：GitHub 会警告，优先考虑压缩、Release 或 LFS；
- 大于 100 MiB：不能作为普通 Git 对象推送；
- 浏览器直接上传的单文件限制更低，不适合批量项目发布。

### 5.4 检查密钥和个人信息

重点查找：

- `API_KEY`、`TOKEN`、`SECRET`、`PASSWORD`；
- 云服务凭据和私钥；
- 数据库连接串；
- 微信、手机号、邮箱等不准备公开的信息；
- 客户数据、实验受试者数据、内部合同；
- 本地绝对路径和用户名。

确认忽略规则：

```powershell
git check-ignore -v .env
git status --ignored --short
```

如果项目还没有初始化 Git，可以先手工检查目录，再在初始化后执行第二次检查。

### 5.5 检查嵌套仓库

项目内部如果意外包含另一个 `.git`，`git add` 时可能变成子模块或无法完整上传。

```powershell
Get-ChildItem -LiteralPath $ProjectPath -Recurse -Force -Directory -Filter ".git"
```

正常情况下只应看到项目根目录的一个 `.git`。确实需要子模块时，必须使用 `git submodule` 明确管理。

---

## 6. GitHub 网页端创建空仓库

登录 GitHub 后：

1. 右上角点击 `+`；
2. 选择 `New repository`；
3. 填写仓库名；
4. 选择 Public 或 Private；
5. 填写简介；
6. **如果本地项目已经有 README、许可证或 `.gitignore`，网页端不要再次初始化这些文件**；
7. 点击 `Create repository`。

为什么要创建空仓库：

- 本地已有完整文件时，网页端再生成 README 会产生两套无关历史；
- 第一次推送容易出现 `non-fast-forward` 或 `unrelated histories`；
- 空仓库能让本地首个提交直接成为远程 `main` 的起点。

如果已经误选了 README，也不需要删除仓库，参见“常见故障”中的历史合并方案。

---

## 7. 首次上传：可直接复制的 PowerShell 流程

先替换变量：

```powershell
$ProjectPath = "D:\path\to\YOUR_PROJECT"
$GitHubOwner = "YOUR_GITHUB_USERNAME"
$RepositoryName = "YOUR_REPOSITORY_NAME"
$RemoteUrl = "https://github.com/$GitHubOwner/$RepositoryName.git"
```

进入项目：

```powershell
Set-Location -LiteralPath $ProjectPath
```

### 7.1 初始化与身份确认

```powershell
git init
git branch -M main
git config user.name
git config user.email
```

如果最后两个命令没有输出，先配置：

```powershell
git config --global user.name "YOUR_NAME"
git config --global user.email "YOUR_GITHUB_EMAIL"
```

### 7.2 首次暂存前检查

```powershell
git status --short
git add .
git status --short
git diff --cached --stat
```

重点确认：

- `.env` 没有出现；
- 安装程序、数据库、构建缓存没有误入；
- README、LICENSE、`.gitignore`、源码和必要文档已经出现；
- 没有意外的数万个文件；
- 没有嵌套仓库警告。

如果文件误入暂存区：

```powershell
git rm --cached -- "path\to\file"
```

首次提交尚未建立时使用 `git rm --cached`。已经有提交历史的仓库也可以使用：

```powershell
git restore --staged "path\to\file"
```

然后把规则加入 `.gitignore`，再次检查。这两个命令只把文件移出暂存区，不会删除本地工作文件。

### 7.3 创建首次提交

```powershell
git commit -m "feat: initial project release"
```

### 7.4 连接远程仓库

```powershell
git remote add origin $RemoteUrl
git remote -v
```

如果已经存在 `origin`：

```powershell
git remote set-url origin $RemoteUrl
git remote -v
```

### 7.5 推送

```powershell
git push -u origin main
```

第一次推送时，Git Credential Manager 可能打开浏览器。确认登录的是目标 GitHub 账号，并授权访问。

成功后，`-u` 会建立跟踪关系。以后只需：

```powershell
git push
```

### 7.6 首次推送后验证

```powershell
git status
git branch -vv
git remote -v
git log -5 --oneline --decorate
```

GitHub 网页端检查：

- 默认分支是 `main`；
- README 正常显示；
- 图片和相对链接可以打开；
- LICENSE 被 GitHub 正确识别；
- Actions 已启动；
- 不存在敏感文件；
- 仓库简介、官网和 Topics 已填写。

---

## 8. 首次上传：Bash 版本

macOS、Linux 或 Git Bash 可以使用：

```bash
PROJECT_PATH="/path/to/YOUR_PROJECT"
GITHUB_OWNER="YOUR_GITHUB_USERNAME"
REPOSITORY_NAME="YOUR_REPOSITORY_NAME"
REMOTE_URL="https://github.com/${GITHUB_OWNER}/${REPOSITORY_NAME}.git"

cd "$PROJECT_PATH"
git init
git branch -M main
git add .
git status --short
git diff --cached --stat
git commit -m "feat: initial project release"
git remote add origin "$REMOTE_URL"
git remote -v
git push -u origin main
```

仍然必须先完成 `.gitignore`、大文件和密钥检查，不能因为命令少就跳过发布前审计。

---

## 9. 日常更新的标准流程

不要形成“改完直接 `git add . && git push`”的习惯。推荐每次按下面顺序：

```powershell
Set-Location -LiteralPath "D:\path\to\YOUR_PROJECT"

git status --short
git diff
```

只暂存本次相关文件：

```powershell
git add README.md docs scripts
```

检查即将提交的内容：

```powershell
git diff --cached --stat
git diff --cached
```

提交：

```powershell
git commit -m "docs: add GitHub publishing guide"
```

推送前同步远程：

```powershell
git pull --rebase origin main
git push origin main
```

最后确认：

```powershell
git status
```

### 9.1 推荐的提交消息

```text
feat: add new user-facing capability
fix: correct broken download link
docs: add installation guide
test: add catalog regression coverage
build: update release packaging
ci: strengthen repository validation
chore: refresh generated catalog
```

一个提交应尽量表达一个完整目的。不要把无关格式化、素材替换和功能修改混在同一个提交里。

### 9.2 多人协作时使用分支

```powershell
git switch -c docs/github-publishing-guide
git add docs/github-publishing-guide.zh-CN.md
git commit -m "docs: add reusable GitHub publishing guide"
git push -u origin docs/github-publishing-guide
```

然后在 GitHub 创建 Pull Request，等待检查通过和评审后再合并到 `main`。

---

## 10. 自动化质量检查

### 10.1 LL-AcademicSkillsHub 当前做法

仓库中的 `.github/workflows/quality.yml` 在以下场景运行：

- 推送到 `main`；
- 创建或更新 Pull Request。

检查矩阵：

- Ubuntu 与 Windows；
- Python 3.10 与 3.12。

执行内容：

1. 重建技能目录；
2. 验证仓库结构与元数据；
3. 运行回归测试；
4. 确认生成文件已同步提交。

其中最后一步很关键：

```bash
git diff --exit-code
```

如果生成器运行后改变了仓库文件，说明开发者只改了源数据，却没有把生成结果一起提交，CI 会直接失败。

### 10.2 可复用的 GitHub Actions 模板

将下面文件保存为 `.github/workflows/quality.yml`，再替换项目自己的安装和测试命令：

```yaml
name: quality

on:
  push:
    branches: [main]
  pull_request:

permissions:
  contents: read

jobs:
  validate:
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, windows-latest]
        python: ["3.10", "3.12"]

    runs-on: ${{ matrix.os }}

    steps:
      - uses: actions/checkout@v7

      - uses: actions/setup-python@v7
        with:
          python-version: ${{ matrix.python }}

      - name: Install dependencies
        run: python -m pip install -r requirements.txt

      - name: Validate
        run: python scripts/validate_repo.py

      - name: Test
        run: python -m unittest discover -s tests -v
```

如果项目没有 `requirements.txt`，删除安装步骤；如果是 Node.js、Java、Rust 或其他技术栈，应改成对应的官方 setup action 和测试命令。

### 10.3 合并保护建议

在仓库 Settings 中建立 Ruleset 或分支保护：

- 合并前必须通过状态检查；
- 禁止强制推送到 `main`；
- 多人项目要求 Pull Request；
- 重要项目要求至少一名评审者；
- 对发布标签限制创建权限。

个人项目早期可以允许直接推送，但正式发布前仍应以 CI 通过作为发布门槛。

---

## 11. 版本号、标签和 Release

### 11.1 版本号

推荐语义化版本：

```text
MAJOR.MINOR.PATCH
```

- `PATCH`：兼容性修复；
- `MINOR`：向后兼容的新功能；
- `MAJOR`：不兼容变化。

示例：

```text
v0.1.0  首个可用版本
v0.1.1  修复文档或安装问题
v0.2.0  增加一批新能力
v1.0.0  稳定公开版本
```

### 11.2 发布前门

创建标签前至少确认：

```powershell
git status
git pull --rebase origin main
```

然后执行项目测试，例如：

```powershell
python scripts/build_catalog.py
python scripts/validate_repo.py
python -m unittest discover -s tests -v
python scripts/package_release.py
```

确认工作区无未提交变化：

```powershell
git status --short
```

### 11.3 计算发行文件校验值

Windows：

```powershell
Get-FileHash `
  -LiteralPath ".\dist\YOUR_PROJECT-v1.0.0.zip" `
  -Algorithm SHA256
```

macOS/Linux：

```bash
shasum -a 256 ./dist/YOUR_PROJECT-v1.0.0.zip
```

在 Release Notes 同时公布：

- 文件名；
- 文件大小；
- SHA-256；
- 系统要求；
- 是否代码签名；
- 已知限制。

### 11.4 创建并推送标签

```powershell
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

检查标签指向：

```powershell
git show v1.0.0 --stat
```

### 11.5 网页端创建 Release

1. 打开仓库的 `Releases`；
2. 点击 `Draft a new release`；
3. 选择刚推送的标签；
4. 填写清楚的标题；
5. 编写新增、变化、修复、安装方法和已知限制；
6. 上传 ZIP、安装程序、校验清单等资产；
7. 等待上传完成；
8. 发布后逐个点击资产，确认真实可下载；
9. 把最终下载链接更新到 README 和下载文档。

不要在文件尚未上传成功时先写一个猜测出来的下载链接。

### 11.6 直接下载链接结构

GitHub Release 资产链接通常为：

```text
https://github.com/OWNER/REPOSITORY/releases/download/TAG/FILE_NAME
```

通用示例：

```text
https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY/releases/download/v1.0.0/YOUR_PROJECT-v1.0.0.zip
```

LL-AcademicSkillsHub 安装程序：

```text
https://github.com/ss8875/LL-AcademicSkillsHub/releases/download/lianlin-ai-v0.3.18/Lianlin-Research-AI-Platform-Setup-0.3.18.exe
```

文件名、标签大小写和空格编码必须与 Release 资产完全一致。

---

## 12. 大文件处理决策树

```text
文件是否必须进入版本历史？
├─ 否
│  ├─ 用户需要下载 → GitHub Release
│  └─ 只是缓存/构建物 → .gitignore
└─ 是
   ├─ 文件较小且适合差异比较 → 普通 Git
   └─ 大型二进制、模型、媒体 → Git LFS
```

### 12.1 Git LFS 基本流程

安装 Git LFS 后：

```powershell
git lfs install
git lfs track "*.bin"
git lfs track "*.psd"
git add .gitattributes
git add path\to\large-file.bin
git commit -m "build: track large assets with Git LFS"
git push
```

注意：

- LFS 有存储和带宽额度；
- 协作者也需要支持 Git LFS；
- `.gitattributes` 必须提交；
- 已经进入普通 Git 历史的大文件不能只靠新增 `git lfs track` 自动迁移；
- 对模板仓库和 GitHub Pages 等场景，应先核对 GitHub 当前限制。

### 12.2 文件已误提交但尚未推送

从暂存区移除：

```powershell
git restore --staged "path\to\large-file.exe"
```

如果已经进入最近一次本地提交但尚未推送：

```powershell
git rm --cached "path\to\large-file.exe"
Add-Content -LiteralPath ".gitignore" -Value "*.exe"
git add .gitignore
git commit --amend --no-edit
```

执行前确认这个提交尚未共享。已推送的历史不要随意改写。

### 12.3 大文件已经进入远程历史

需要使用 `git filter-repo` 或 `git lfs migrate` 清理历史。这个操作会重写提交 ID，影响所有协作者。

处理原则：

1. 先停止其他人继续推送；
2. 备份仓库；
3. 明确要清理的路径；
4. 执行历史重写；
5. 受控强制推送；
6. 通知所有协作者重新克隆或重置；
7. 更新 Release 或 LFS 方案。

不要在不了解影响时直接运行强制推送命令。

---

## 13. README 和仓库首页的发布标准

一个可用的公开仓库首页至少应包含：

1. 项目名称和一句话定位；
2. 主视觉或截图；
3. 功能清单；
4. 快速开始；
5. 安装或部署说明；
6. 系统要求；
7. 下载入口；
8. 文档索引；
9. 质量或测试状态；
10. 许可证和第三方声明；
11. 安全问题报告入口；
12. 贡献方式。

LL-AcademicSkillsHub 还提供：

- 中文和英文 README；
- 18 类、187 项能力清单；
- 本地部署文档；
- 质量模型；
- 发布交接；
- 平台下载说明；
- CI 质量流水线；
- 第三方来源和许可边界。

### 13.1 仓库设置建议

在 GitHub 仓库首页右侧 `About` 区域配置：

- Description：一句话说明项目；
- Website：项目官网；
- Topics：5–12 个稳定关键词；
- Releases：允许用户从固定入口下载；
- Issues：项目是否接受公开问题；
- Discussions：是否需要社区问答。

仓库简介不要堆砌营销词，应让用户一眼看懂它是什么、解决什么问题。

---

## 14. 发布前审计清单

### 14.1 内容

- [ ] README 能在 GitHub 首页正常显示；
- [ ] 中英文入口和相对链接有效；
- [ ] 所有图片路径区分大小写；
- [ ] 安装命令可以从全新目录执行；
- [ ] `.env.example` 只包含占位符；
- [ ] 没有本地绝对路径；
- [ ] 没有个人账户、客户数据或实验敏感数据；
- [ ] 版本号、发布日期和下载文件一致。

### 14.2 Git

- [ ] 默认分支为 `main`；
- [ ] `git status` 干净；
- [ ] `origin` 指向正确仓库；
- [ ] 提交消息能解释本次变化；
- [ ] 没有嵌套 `.git`；
- [ ] 没有超过策略限制的大文件；
- [ ] 标签指向经过验证的提交。

### 14.3 安全与许可

- [ ] 未提交 `.env`、Token、私钥或密码；
- [ ] 已检查第三方许可证；
- [ ] 已准备 LICENSE；
- [ ] 已准备 SECURITY.md；
- [ ] 发行二进制公布 SHA-256；
- [ ] 未签名安装程序已明确说明；
- [ ] 密钥由 GitHub Secrets 管理，不写在 workflow 中。

### 14.4 自动化

- [ ] Push 和 Pull Request 会触发检查；
- [ ] CI 使用最小权限；
- [ ] 测试失败会阻止发布；
- [ ] 生成文件一致性已检查；
- [ ] Windows/Linux 或目标平台已覆盖；
- [ ] Actions 页面没有被忽略的红色失败任务。

### 14.5 Release

- [ ] Release 标签和标题正确；
- [ ] 发行说明包含变化和已知限制；
- [ ] 每个资产上传完成；
- [ ] 文件名、大小、校验值一致；
- [ ] 从无登录浏览器测试下载；
- [ ] README 下载链接已更新；
- [ ] 旧版本仍可追溯。

---

## 15. 常见故障与处理

### 15.1 `git` 无法识别

原因：Git 未安装，或安装后终端没有重启。

处理：

1. 安装 Git for Windows；
2. 关闭并重新打开 PowerShell；
3. 执行 `git --version`；
4. 如果仍失败，检查 Git 是否加入 PATH。

### 15.2 `winget` 无法识别

这不影响 GitHub 发布。直接从 Git for Windows 官方页面下载安装，或使用 GitHub Desktop。

### 15.3 `remote origin already exists`

```powershell
git remote -v
git remote set-url origin "https://github.com/OWNER/REPOSITORY.git"
```

不要在未检查旧地址前直接删除远程。

### 15.4 `Repository not found`

依次检查：

- OWNER 和仓库名是否拼写正确；
- 当前登录账号是否有权限；
- 仓库是否为 Private；
- Git Credential Manager 是否缓存了错误账号；
- 远程地址是否包含多余空格。

```powershell
git remote -v
```

Windows 可以在“凭据管理器”中删除错误的 GitHub 凭据，再次推送并重新登录。

### 15.5 `Authentication failed`

GitHub 不再接受账号密码作为 Git HTTPS 推送密码。应使用：

- Git Credential Manager 浏览器登录；
- GitHub CLI 登录；
- SSH；
- 必要时使用具备最小权限的 Personal Access Token。

不要把令牌直接写进远程 URL、脚本、聊天记录或 README。

### 15.6 `non-fast-forward`

远程已有本地没有的提交：

```powershell
git fetch origin
git pull --rebase origin main
git push origin main
```

先查看远程变化，不要直接强制推送。

### 15.7 网页端误创建 README，出现 unrelated histories

最安全的方案是保留双方历史并人工解决冲突：

```powershell
git fetch origin
git merge origin/main --allow-unrelated-histories
```

解决 README、LICENSE 或 `.gitignore` 冲突后：

```powershell
git add .
git commit
git push -u origin main
```

如果远程仓库刚创建且没有任何需要保留的内容，也可以删除后重新创建空仓库，但必须先确认没有其他人的提交。

### 15.8 文件超过 100 MiB

不要反复重试推送。选择：

- 从提交中移除并作为 Release 资产发布；
- 使用 Git LFS；
- 将可重新生成的文件加入 `.gitignore`。

如果大文件已经进入较早的提交，普通删除无法减小历史，需要历史清理。

### 15.9 推送很慢或中断

检查：

- 是否误提交 `node_modules`、虚拟环境、缓存或构建目录；
- 是否包含大量二进制；
- 单次推送是否过大；
- 网络代理或防火墙；
- GitHub 状态页。

先执行：

```powershell
git count-objects -vH
git status --short
```

不要把“调大缓冲区”当成首选修复，先确认仓库内容是否合理。

### 15.10 README 图片不显示

常见原因：

- 相对路径错误；
- 文件名大小写不同；
- 图片没有提交；
- 路径含空格但没有正确编码；
- 使用了本机绝对路径。

推荐：

```markdown
![项目截图](./assets/project-screenshot.png)
```

### 15.11 Actions 在 Windows 通过、Linux 失败

重点检查：

- 路径大小写；
- `\` 与 `/`；
- 默认编码；
- 换行符；
- shell 差异；
- 依赖是否只在本机存在。

这正是跨平台 CI 的价值：在发布前暴露本地环境掩盖的问题。

### 15.12 敏感信息已经推送

立即按顺序处理：

1. **撤销或轮换密钥**，不要先忙着改 Git；
2. 检查访问日志和异常使用；
3. 从当前版本删除敏感文件；
4. 使用官方建议的方法清理历史；
5. 检查 Fork、缓存、Release 和 Actions 日志；
6. 通知受影响协作者；
7. 增加 secret scanning 和发布前检查。

仅删除最新文件并不能让秘密从历史中消失。

---

## 16. 可复制的项目发布记录模板

把下面内容复制到新项目的 `docs/release-handoff.md`：

````markdown
# PROJECT_NAME 发布交接

## 仓库

- GitHub：REPOSITORY_URL
- 默认分支：main
- 当前版本：vX.Y.Z
- 发布日期：YYYY-MM-DD

## 交付范围

- 源码：
- 文档：
- 测试：
- 构建产物：
- Release 资产：

## 环境

- 操作系统：
- 运行时：
- 包管理器：
- 必需依赖：
- 可选依赖：

## 构建

```shell
BUILD_COMMAND
```

## 验证

```shell
LINT_COMMAND
TEST_COMMAND
PACKAGE_COMMAND
```

## Release

- 标签：
- 提交：
- 文件名：
- 文件大小：
- SHA-256：
- 下载地址：
- 是否代码签名：

## CI

- Workflow：
- 必需检查：
- 支持平台：

## 已知限制

- LIMITATION_1
- LIMITATION_2

## 后续更新

1. 更新版本号；
2. 更新 CHANGELOG；
3. 运行构建和测试；
4. 确认工作区干净；
5. 创建并推送标签；
6. 上传 Release 资产；
7. 核对下载链接和校验值。
````

---

## 17. 可复制的最小项目文件清单

```text
YOUR_PROJECT/
├─ .github/
│  └─ workflows/
│     └─ quality.yml
├─ docs/
│  ├─ deployment.md
│  └─ release-handoff.md
├─ scripts/
│  ├─ build.*
│  └─ validate.*
├─ tests/
├─ .env.example
├─ .gitattributes
├─ .gitignore
├─ CHANGELOG.md
├─ CONTRIBUTING.md
├─ LICENSE
├─ README.md
├─ SECURITY.md
└─ THIRD_PARTY_NOTICES.md
```

不是每个项目都必须有全部文件，但公开发布的软件或工具项目至少应具备：

- README；
- LICENSE；
- `.gitignore`；
- 环境变量示例；
- 安装和验证说明；
- 变更记录；
- 安全问题报告方式。

---

## 18. 一页式执行清单

首次发布：

```text
□ 明确仓库名、可见性和许可证
□ 划分源码、生成物和发行物
□ 创建 .gitignore 与 .gitattributes
□ 扫描密钥、个人信息和大文件
□ 在 GitHub 创建空仓库
□ git init
□ git branch -M main
□ git add .
□ 检查暂存区
□ git commit
□ git remote add origin
□ git push -u origin main
□ 检查 GitHub 首页、链接和 Actions
□ 建立标签
□ 生成 SHA-256
□ 上传 Release 资产
□ 验证无登录下载
□ 更新 README 下载链接
```

日常更新：

```text
□ git status
□ git diff
□ 运行构建和测试
□ 只暂存相关文件
□ git diff --cached
□ git commit
□ git pull --rebase
□ git push
□ 检查 Actions
```

版本发行：

```text
□ 更新版本号和 CHANGELOG
□ 完成全量测试
□ 确认工作区干净
□ 生成发行文件
□ 计算大小与 SHA-256
□ 创建并推送标签
□ 发布 Release
□ 测试资产下载
□ 更新项目文档
□ 保存发布交接
```

---

## 19. 官方参考

- [GitHub：创建新仓库](https://docs.github.com/repositories/creating-and-managing-repositories/creating-a-new-repository)
- [GitHub：使用命令行添加本地项目](https://docs.github.com/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github)
- [GitHub：通过 Git Credential Manager 缓存凭据](https://docs.github.com/get-started/git-basics/caching-your-github-credentials-in-git)
- [GitHub：普通仓库中的大文件限制](https://docs.github.com/repositories/working-with-files/managing-large-files/about-large-files-on-github)
- [GitHub：Git Large File Storage](https://docs.github.com/repositories/working-with-files/managing-large-files/about-git-large-file-storage)
- [GitHub：管理 Releases](https://docs.github.com/repositories/releasing-projects-on-github/managing-releases-in-a-repository)
- [LL-AcademicSkillsHub 仓库](https://github.com/ss8875/LL-AcademicSkillsHub)
- [LL-AcademicSkillsHub Releases](https://github.com/ss8875/LL-AcademicSkillsHub/releases)

---

## 20. 最终原则

可持续的 GitHub 发布不是“把文件传上去”，而是建立一条可以反复执行的链路：

```text
本地内容审计
→ Git 版本记录
→ 远程协作
→ 自动化验证
→ 标签冻结
→ Release 分发
→ 校验与交接
```

源码负责可追踪，CI 负责可验证，Release 负责可下载，交接文档负责可延续。其他项目只要保留这四个边界，再替换项目变量和验证命令，就能直接复用本手册。
