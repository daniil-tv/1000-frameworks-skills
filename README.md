# 1000 Frameworks Skills

Source-aware AI skills for the strategy pages of 1000 Frameworks:

| Page | Skill |
| --- | --- |
| Outcome-Driven Innovation | `odi-outcome-research` |
| Customer Development | `customer-development` |
| Switch Interview | `switch-interview` |
| Business Model Canvas | `business-model-canvas` |
| Value Proposition Canvas | `value-proposition-canvas` |
| PESTEL / PESTLE | `pestel-analysis` |
| Porter's Five Forces | `porters-five-forces` |

The JTBD page points to Ivan Zamesin's separate [Next Move Theory Canon & Skills](https://github.com/zamesin/Next-Move-Theory-Canon-and-Skills) repository. That author's AJTBD / Next Move Theory skills are not copied into this collection or represented as generic JTBD.

Each skill takes real research inputs, keeps evidence separate from hypotheses, and refuses to invent interviews, numerical findings, or examples. Sources for the methodologies are linked in the individual files.

Install a skill with the [Skills CLI](https://github.com/vercel-labs/skills/blob/main/docs/commands.md), for example:

```bash
npx skills add daniil-tv/1000-frameworks-skills --skill odi-outcome-research -a codex -y
```

Replace the skill name with one from the table above. Use `-a claude-code` or `-a cursor` for those agents. The website offers installation commands only after the published files and installation have been checked.

## Quality and acceptance

The project contract is [AI Skill Quality Standard](standards/AI_SKILL_QUALITY_STANDARD.md). Every new skill and explicitly requested revision follows it. Each original skill bundles a compact procedure, primary-source notes, three clearly synthetic calibration examples, and 20 behavioral scenarios. Only ODI includes a deterministic calculator; it requires Python 3 when used.

Run and interpret checks as described in [EVALUATION.md](standards/EVALUATION.md). Structural validation, installation, and behavioral acceptance are distinct. Platform status and actual results belong in the dated quality audit; never infer Claude Code/Cursor runtime compatibility from filesystem installation alone. See [platform notes](standards/PLATFORM_NOTES.md).

Install the whole skill folder, including references and scripts. A standalone copy of SKILL.md is not a complete package. The external JTBD/AJTBD skill remains unchanged and outside this audit.

The dated [audit and remaining limitations](standards/AUDIT-2026-11-23.md) records actual Codex behavioral results and the rubric score. Claude Code and Cursor runtime acceptance is incomplete; their installation options above do not imply runtime certification.

The new Value Proposition Canvas skill has a separate [2026-11-24 quality audit](standards/AUDIT-VPC-2026-11-24.md) with its actual behavioral results and platform limitations.

The PESTEL skill has a separate [2026-11-25 quality audit](standards/AUDIT-PESTEL-2026-11-25.md) with actual results and platform limitations.

The Five Forces skill has a separate [2026-11-26 quality audit](standards/AUDIT-PORTER-2026-11-26.md) with actual behavioral results and platform limitations.
