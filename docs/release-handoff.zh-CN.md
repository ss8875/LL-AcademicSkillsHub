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

## 仍需维护者提供的真实资产

这些不是代码阻断项，但发布到公开 GitHub 前必须替换：

1. 链邻科研 AI 平台官方 HTTPS 下载地址；
2. 如需宣传，经过验证的客服/社群/微信二维码；
3. 维护者安全联系地址；
4. 最终品牌 Logo 或备案后的商标素材。

在正式地址缺失时，站点会明确显示“待配置”，不会生成假链接或二维码。平台宣传只位于 README、文档站、下载页和发行说明，不进入技能执行指令。

## 交接入口

- 中文首页：`README.md`
- 英文首页：`README.en.md`
- 全部技能：`docs/skills.zh-CN.md` / `docs/skills.en.md`
- 最终架构：`docs/architecture.zh-CN.md`
- 质量模型：`docs/quality-model.zh-CN.md`
- 审计报告：`reports/audit.zh-CN.md`
- 发行包：`dist/LL-AcademicSkillsHub-local.zip`
- 校验清单：`dist/manifest.json`
