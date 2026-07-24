# 0.1.0 发布交接

## 交付结论

首期本地部署版已经完成并通过发布门。当前仓库包含 187 项技能、18 个分类、10 项链邻原创核心能力和 177 项固定第三方能力。中文与英文目录来自同一事实源，站点可搜索、可按分类和质量状态筛选。

## 已验证

- 构建、深度审计、环境诊断和 9 项回归测试全部通过；
- 目录、磁盘与站点均为 187 项，ID 集合完全一致；
- 真实 Chrome 中中文/英文切换、搜索、分类与质量筛选通过；
- 桌面与 390px 移动端无横向溢出；
- 浏览器控制台 0 错误、0 警告，资源请求无失败；
- `.env`、`.git`、`scripts/`、`catalog/`、`reports/` 均不可从本地服务器访问；
- 发行 ZIP 完整，可通过 SHA-256 校验。

## 质量解释

- 10 项链邻原创技能状态为 `beta`；
- 177 项第三方技能状态为 `cataloged`；
- 发布审计为 0 个阻断错误；
- 19 个非阻断警告来自第三方源码中的动态执行或管道安装模式，完整清单保存在 `reports/audit.json`；
- 177 项第三方技能仍使用固定包的集合级许可证元数据，商业再发布前需要继续逐项确认。

## 关键命令

```powershell
./scripts/setup.ps1
./scripts/start.ps1
./scripts/build.ps1
```

单独执行：

```powershell
python scripts/build_catalog.py
python scripts/validate_repo.py
python -m unittest discover -s tests -v
python scripts/package_release.py
```

## 链邻科研 AI 平台安装包

Windows 安装版 0.3.18 已作为 GitHub Release 附件发布：

- [直接下载安装包](https://github.com/ss8875/LL-AcademicSkillsHub/releases/download/lianlin-ai-v0.3.18/Lianlin-Research-AI-Platform-Setup-0.3.18.exe)
- 大小：122,424,791 字节（约 116.75 MB）
- SHA-256：`E502A3422E69A015BFBD56B8A1483C5CE4E1663F08C75D9AE0DE2639CAE280F6`

安装包目前未进行 Windows 代码签名，发布页和下载文档已明确说明校验方式。后续版本应沿用 `catalog/platform-release.json` 更新版本、附件直链、大小和摘要，再运行完整构建。

## 交接入口

- 中文首页：`README.md`
- 英文首页：`README.en.md`
- 全部技能：`docs/skills.zh-CN.md` / `docs/skills.en.md`
- 最终架构：`docs/architecture.zh-CN.md`
- 质量模型：`docs/quality-model.zh-CN.md`
- 审计报告：`reports/audit.zh-CN.md`
- 发行包：`dist/LL-AcademicSkillsHub-local.zip`
- 校验清单：`dist/manifest.json`
