# 发布审计报告

结论：**通过**

- 技能: 187
- 分类: 18
- 阻断错误: 0
- 复核警告: 19
- 信息项: 1
- 目录 SHA-256: `5443cfc3b3f41c1bd63b78f5228cb5c8e7ee2a655f9e3e1a1a525e1248984ab4`

## 检查矩阵

| 检查 | 结果 |
|---|---|
| `catalogSchema` | `{"records": 187, "uniqueIds": 187, "categories": 18}` |
| `skillStructure` | `{"diskSkills": 187, "catalogSkills": 187}` |
| `bilingualParity` | `{"locales": ["zh-CN", "en"], "skills": 187, "generatedArtifacts": 9}` |
| `codeSyntax` | `{"pythonFiles": 236, "pythonWarnings": 0, "jsFiles": 1, "jsFailures": 0}` |
| `securityStaticScan` | `{"files": 1603, "findings": {"dynamic-python": 15, "shell-pipe-exec": 2, "shell-true": 2}}` |
| `brandAndScope` | `{"publicFiles": 5, "firstReleaseRoutes": 2, "platformVersion": "0.3.18", "platformDownloadLinkedFiles": 7}` |
| `licenseProvenance` | `{"statusCounts": {"metadata-declared": 177, "first-party": 10}}` |
| `releaseContract` | `{"skills": 187, "categories": 18, "firstParty": 10, "thirdParty": 177}` |

## 阻断错误

无。

## 复核警告

- `security.dynamic-python`: 15
- `security.shell-pipe-exec`: 2
- `security.shell-true`: 2

警告主要来自固定第三方代码或原始元数据，表示后续运行/许可证复核队列，不影响目录结构发布；具体明细见 `reports/audit.json`。

## 解释

本报告证明双语目录、路径、元数据、站点构建与常见静态风险检查无阻断错误；它不证明 177 项第三方技能已经完成真实 API、领域科学有效性或逐文件法律验证。
