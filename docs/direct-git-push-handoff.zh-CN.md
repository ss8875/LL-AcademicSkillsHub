# LL-AcademicSkillsHub 直接 Git 推送交接

> 本文是供后续 Codex 对话、维护者和自动化代理读取的项目发布约定。
>
> 用户已明确选择继续沿用项目此前成功使用的上传方式：**使用原生 Git、HTTPS 远程地址和本机 Git 凭据助手，直接推送 `main`；不要求安装 GitHub CLI，不默认创建 Pull Request。**
>
> 生效日期：2026-07-26

## 1. 后续对话应先读取的结论

处理 `D:\daxia\LL-AcademicSkillsHub` 的“上传、发布、推送到线上”请求时：

1. 使用 `git`，不把 `gh` 作为前置条件；
2. 使用已经配置好的 HTTPS 远程仓库；
3. 默认目标为 `origin/main`；
4. 推送前必须检查变更范围并运行项目质量门；
5. 只暂存任务范围内的明确文件；
6. 不提交 `.env`、`dist/`、缓存、日志、凭据或本机工具目录；
7. 提交后执行 `git push origin main`；
8. 推送后比较本地 `HEAD` 与 `origin/main`，确认两者一致；
9. 只有用户明确要求分支、PR、Issue、Release API 或其他 GitHub 管理功能时，才要求额外工具。

这项约定是用户对本项目发布方式的明确选择。不要仅因为缺少 GitHub CLI 就阻止普通源码推送。

## 2. 当前仓库参数

```text
本地目录：D:\daxia\LL-AcademicSkillsHub
远程名称：origin
远程地址：https://github.com/ss8875/LL-AcademicSkillsHub.git
默认分支：main
线上仓库：https://github.com/ss8875/LL-AcademicSkillsHub
```

本机 Git：

```text
Git for Windows
HTTPS remote
Credential helper: helper-selector
```

`helper-selector` 负责选择本机可用的 Git 凭据后端。此前项目已经通过这套配置多次成功推送，因此普通 `git push` 不依赖 `gh`。

## 3. 两类工具的边界

### 原生 Git 能直接完成

- 检查工作区；
- 查看差异；
- 暂存文件；
- 创建提交；
- 拉取和变基；
- 推送分支或标签；
- 比较本地与远程提交。

### GitHub CLI 或网页端主要用于

- 创建和管理 Pull Request；
- 创建 Issue；
- 管理 GitHub Release 及附件；
- 查看 Actions 详细状态；
- 调用 GitHub API；
- 管理仓库设置。

所以“没有安装 `gh`”不等于“不能上传源码”。本项目的默认源码上传只依赖 Git。

## 4. 推送前只读检查

进入仓库：

```powershell
Set-Location -LiteralPath "D:\daxia\LL-AcademicSkillsHub"
```

确认 Git、分支和远程：

```powershell
git --version
git status -sb
git branch --show-current
git remote -v
```

预期结果：

```text
当前分支：main
推送地址：https://github.com/ss8875/LL-AcademicSkillsHub.git
```

同步远程引用：

```powershell
git fetch origin --prune
```

检查本地与远程领先数量：

```powershell
git rev-list --left-right --count main...origin/main
```

输出格式：

```text
本地独有提交数    远程独有提交数
```

如果第二个数字不为 `0`，说明远程出现了本地没有的新提交。此时不要直接推送，应先理解远程变化并处理同步。

## 5. 质量门

LL-AcademicSkillsHub 推送前执行：

```powershell
python scripts/build_catalog.py
python scripts/validate_repo.py
python -m unittest discover -s tests -v
```

正式打包变更还应执行：

```powershell
python scripts/package_release.py
```

通过标准：

- 构建成功；
- 仓库验证结果为 `pass`；
- 全部回归测试为 `OK`；
- 生成文件已同步；
- `git diff --check` 没有空白错误；
- 发行 ZIP 可以打开且许可文件完整。

## 6. 暂存方法

先看变更：

```powershell
git status --short
git diff --stat
git diff
```

优先使用明确路径，不默认使用 `git add -A`：

```powershell
git add -- `
  README.md `
  README.en.md `
  LICENSE `
  COMMERCIAL_LICENSE.md `
  THIRD_PARTY_NOTICES.md `
  CHANGELOG.md
```

根据实际任务继续补充其他明确文件。

暂存后必须复核：

```powershell
git diff --cached --stat
git diff --cached --check
git status --short
```

特别确认以下内容没有进入暂存区：

```text
.env
.env.*
dist/
.tools/
__pycache__/
*.log
任何 Token、密码、私钥或本机凭据
```

## 7. 创建提交

提交消息应简洁说明完整变化：

```powershell
git commit -m "docs: add noncommercial licensing and publishing guides"
```

提交后检查：

```powershell
git show --stat --oneline HEAD
git status -sb
```

如果提交后仍有计划内文件未提交，应先判断遗漏原因，不要直接推送半成品。

## 8. 直接推送 main

本项目默认命令：

```powershell
git push origin main
```

如果本机尚未缓存 GitHub 凭据，Git 可能弹出浏览器或账号选择窗口。登录有仓库写入权限的 `ss8875` 账号即可。

禁止把 Token 写入远程 URL：

```text
错误：https://TOKEN@github.com/ss8875/LL-AcademicSkillsHub.git
正确：https://github.com/ss8875/LL-AcademicSkillsHub.git
```

## 9. 推送后验证

刷新远程引用：

```powershell
git fetch origin
```

比较提交：

```powershell
$LocalCommit = git rev-parse HEAD
$RemoteCommit = git rev-parse origin/main

Write-Output "local=$LocalCommit"
Write-Output "remote=$RemoteCommit"

if ($LocalCommit -ne $RemoteCommit) {
    throw "本地 HEAD 与 origin/main 不一致，推送验证失败。"
}
```

检查状态：

```powershell
git status -sb
```

预期：

```text
## main...origin/main
```

不应再显示领先、落后或未提交的计划内文件。

线上检查：

```text
https://github.com/ss8875/LL-AcademicSkillsHub
https://github.com/ss8875/LL-AcademicSkillsHub/commits/main
https://github.com/ss8875/LL-AcademicSkillsHub/actions
```

至少核对：

- 最新提交标题正确；
- README 正常显示；
- 新增文档链接可打开；
- LICENSE 和商业授权说明在线可见；
- Actions 已触发且最终通过。

## 10. 常见失败

### `Authentication failed`

检查远程：

```powershell
git remote -v
```

确认使用 HTTPS 且账号有写入权限。必要时在 Windows 凭据管理器中删除错误的 GitHub 凭据，让 Git 重新弹出登录。

### `Repository not found`

检查：

- 远程 OWNER 是否为 `ss8875`；
- 仓库名是否为 `LL-AcademicSkillsHub`；
- 登录账号是否有权限；
- 网络是否能访问 GitHub。

### `non-fast-forward`

远程比本地新。不要强制推送：

```powershell
git fetch origin
git log --oneline --left-right main...origin/main
git pull --rebase origin main
```

解决冲突并重新运行质量门后，再推送。

### 大文件超过限制

不要把安装程序提交到 Git 历史。源码仓库继续忽略 `dist/`，大型安装程序通过 GitHub Release 网页上传。

### Actions 失败

推送已经完成不代表发布质量通过。读取失败日志，修复后重新运行本地测试，再创建新的修复提交并推送。

## 11. 何时不能直接推送 main

遇到以下情况应停下并请求用户决定：

- 工作区包含明显无关的用户修改；
- 远程 `main` 有本地没有的新提交；
- 需要重写历史或强制推送；
- 需要删除远程分支、标签或 Release；
- 自动化测试失败；
- 发现密钥、个人数据、第三方许可不明或大型二进制误入；
- 用户明确要求 Pull Request 审核流程。

`git push --force`、`git push --force-with-lease` 和删除远程引用不属于本项目默认发布方式。

## 12. 可供其他对话直接使用的任务说明

后续对话可以复制下面这段：

```text
请先读取：
D:\daxia\LL-AcademicSkillsHub\docs\direct-git-push-handoff.zh-CN.md

本项目上传源码不依赖 GitHub CLI。使用原生 Git、HTTPS 远程地址和本机
credential helper，按文档完成质量检查、明确文件暂存、提交、
git push origin main，并在推送后确认本地 HEAD 与 origin/main 完全一致。
不要提交 .env、dist、缓存、日志或凭据；不要强制推送。
```

## 13. 最短安全流程

```powershell
Set-Location -LiteralPath "D:\daxia\LL-AcademicSkillsHub"

git fetch origin --prune
git status -sb
git remote -v

python scripts/build_catalog.py
python scripts/validate_repo.py
python -m unittest discover -s tests -v

git status --short
git diff --stat

# 使用明确文件列表暂存
git add -- <本次任务文件>

git diff --cached --stat
git diff --cached --check

git commit -m "<准确的提交说明>"
git push origin main

git fetch origin
git rev-parse HEAD
git rev-parse origin/main
git status -sb
```

核心原则：

```text
检查范围 → 运行质量门 → 明确暂存 → 提交 → 直接推送 main → 验证远程一致
```
