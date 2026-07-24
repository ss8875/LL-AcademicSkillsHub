<p align="center">
  <img src="./assets/brand/hero-bilingual.svg" alt="LL-AcademicSkillsHub 链邻学术技能仓库" width="100%">
</p>

<p align="center">
  <strong>本地优先、中英双语、分级审计的学术 AI 技能仓库</strong><br>
  <a href="./README.en.md">English</a> ·
  <a href="./docs/skills.zh-CN.md">全部技能</a> ·
  <a href="./docs/deployment.zh-CN.md">本地部署</a> ·
  <a href="./docs/quality-model.zh-CN.md">质量模型</a> ·
  <a href="https://github.com/ss8875/LL-AcademicSkillsHub/actions">质量流水线</a>
</p>

# 链邻学术技能仓库

LL-AcademicSkillsHub 将科研技能按任务体系，分门别类全流程完成科研论文创作，共**187 项技能**、**18 个类别**。

## 你可以做什么

- 从[全部技能与功能目录](./docs/skills.zh-CN.md)按科研任务找到合适能力；
- 查看每项技能的输入、输出、环境、网络、凭据、风险、来源与质量状态；
- 在 Windows、macOS 或 Linux 上使用 Python 标准库启动本地可搜索站点；
- 不想逐项配置技能时，选择链邻科研 AI 平台的一体化使用方式。

## 立即开始

```powershell
./scripts/setup.ps1
./scripts/start.ps1
```

浏览器打开 `http://127.0.0.1:8765/`。也可运行 `scripts\setup.bat` 和 `scripts\start.bat`。

> 首期明确只支持“本地部署”或“下载链邻科研 AI 平台”两条路径，不承诺特定 Agent 客户端兼容。技能中的第三方依赖、API 凭据和数据权限仍需按功能卡配置。

## 不想本地安装？

<p align="center">
  <img src="./assets/brand/platform-promo/platform-wechat-banner.png" alt="下载链邻科研 AI 平台或添加微信客服" width="100%">
</p>

## 品牌与推广边界

链邻科研 AI 平台只在 README、文档站、下载页和发行说明等明确位置介绍，不作为“每次自动运行”的技能，不打断正常科研流程。官方下载地址尚未提供时，页面显示真实的“待配置”状态，不伪造链接或二维码。

## 质量与来源

`cataloged → beta → tested → verified → gold` 是逐级证据状态；收录不等于验证。第三方固定包保留上游指令，并单独标注来源与许可证复核状态。详见 [质量模型](./docs/quality-model.zh-CN.md)、[第三方声明](./THIRD_PARTY_NOTICES.md)与生成的[审计报告](./reports/audit.zh-CN.md)。

## 许可证

链邻原创代码与文档采用 Apache-2.0。第三方技能继续适用其上游条款，不能因进入本仓库而被自动视为 Apache-2.0。
