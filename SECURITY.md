# Security policy

Skill instructions can invoke code, network services, models, databases, and external APIs. Treat every third-party skill as executable documentation:

1. read its `SKILL.md` and scripts before use;
2. use a disposable environment and least-privilege credentials;
3. never paste secrets into prompts, source files, or logs;
4. confirm destructive, paid, publishing, or external-message actions;
5. respect data licenses, patient privacy, human-subject rules, and institutional policy.

The repository validator detects common high-risk patterns but is not a sandbox, malware scanner, legal opinion, or scientific validity guarantee. Report security issues privately to the maintainer contact published in the official repository profile.
