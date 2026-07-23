# Lianlin Scholarly Citation Audit

Verify DOI, authors, venue, year, volume, issue, pages, and consistency between in-text citations and references.

## Main capabilities

- Parse in-text citations and the reference list
- Match authoritative metadata by DOI, title, and author
- Classify verified, partial, conflicting, and unresolved records
- Check missing, orphaned, duplicate, ordering, and style issues
- Never fabricate fields for unresolved records
- Return a per-item audit table, fixes, and open questions

## Inputs

- Manuscript, reference list, and target citation style

## Outputs

- Citation audit table, corrected references, and unresolved list

## Local-use note

Read the root `SKILL.md` and its referenced files first, then check the catalog record for runtime, credential, network, risk, and license status. This profile does not replace upstream instructions for third-party skills.

Quality status: `beta`; source kind: `lianlin-first-party`.
