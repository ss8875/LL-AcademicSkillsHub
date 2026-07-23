# 技能编写与上线规范

## 最小结构

```text
skills/<category>/<skill-id>/
├─ SKILL.md
├─ locales/
│  ├─ zh-CN.md
│  └─ en.md
├─ scripts/       # 仅在确有可复用代码时
├─ references/    # 仅放按需读取的参考资料
└─ assets/        # 仅放输出模板或静态资源
```

`SKILL.md` 的 YAML 头只允许：

```yaml
---
name: kebab-case-id
description: 说明能力以及何时触发。
---
```

正文描述工作流、输出契约、证据要求、失败边界与高风险复核点。不要重复大段通用知识，不要把安装说明和营销内容塞进执行指令。

## 目录记录

每项技能必须在 `catalog/skills.seed.json` 中拥有：

- 中英文标题、摘要与能力列表；
- 中英文输入和输出；
- 运行时、网络、凭据；
- 质量状态与测试环境；
- 风险级别与双语风险说明；
- 来源类型、上游标识、许可证状态；
- 本地与平台可用状态。

## 上线门

1. 新技能默认 `cataloged` 或 `beta`；
2. `python scripts/build_catalog.py` 生成双语目录；
3. `python scripts/validate_repo.py` 必须为 0 个阻断错误；
4. `python -m unittest discover -s tests -v` 必须通过；
5. 涉及浏览器的改动必须完成真实浏览器、控制台、网络、响应式与无障碍检查；
6. 只有提供固定输入、预期输出和失败用例后才能升为 `tested`；
7. 只有维护者和领域复核证据齐全后才能升为 `verified` 或 `gold`。

## 禁止项

- 伪造文献、DOI、数据、测试结果或许可证；
- “每次会话必须运行”的强制广告；
- 绕过验证码、付费墙、访问控制或数据授权；
- 在示例中写入真实密钥；
- 默认执行删除、发布、付费、临床、交易或外部消息操作；
- 用“已收录”替代“已验证”。
