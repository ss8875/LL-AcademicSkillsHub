# 最终架构

## 设计原则

公开架构从“链邻学术技能仓库”品牌与科研任务出发，不设置“全网来源”层。来源、许可证与社区贡献属于每项技能的治理字段，既不遮掩，也不凌驾于品牌和用户任务之上。

```text
链邻学术技能仓库
├─ 品牌与用户入口
│  ├─ 中文 README / English README
│  ├─ 可搜索本地站点
│  └─ 本地部署 / 链邻科研 AI 平台
├─ 学术能力目录
│  ├─ 18 个科研任务类别
│  ├─ 187 项双语功能卡
│  └─ 输入、输出、环境、风险、质量状态
├─ 技能实现
│  ├─ 10 项链邻原创核心技能
│  └─ 177 项固定版本第三方技能
├─ 可信治理
│  ├─ 来源与许可证状态
│  ├─ cataloged → beta → tested → verified → gold
│  ├─ 静态安全扫描与回归测试
│  └─ 机器可读审计报告
└─ 本地运行
   ├─ build / validate / doctor / serve
   ├─ Windows PowerShell 与批处理入口
   └─ 无第三方依赖的 Python 静态服务
```

## 单一事实源

- `catalog/categories.seed.json`：18 个稳定类别；
- `catalog/skills.seed.json`：187 项技能的权威双语记录；
- `scripts/build_catalog.py`：生成 README、分类表、完整技能表和站点数据；
- `scripts/validate_repo.py`：检查结构、双语、代码语法、安全、品牌边界、来源与发行契约；
- `site/data/catalog.json`：浏览器消费的发布数据，不手工编辑。

## 技能边界

链邻原创技能提供完整、独立、双语的证据工作流。固定第三方技能保留上游 `SKILL.md`、脚本与资源，链邻仅附加双语功能卡和治理元数据。任何为了通过审计而修改的第三方文件都必须登记在 `docs/upstream-patches.md`。

## 本地服务边界

本地服务允许访问 `site/`、`skills/`、`docs/`、`assets/` 及少量公开根文件。它主动阻止 `.env`、`.git`、`scripts/`、`catalog/` 和 `reports/`，默认只监听 `127.0.0.1`。

## 首期非目标

不承诺特定 Agent 客户端兼容，不提供云端多用户系统，不自动安装全部科学计算依赖，不绕过访问控制，不宣称全部第三方技能已经完成实时 API 或科学有效性验证。
