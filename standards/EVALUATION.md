# Reproducible acceptance

The unchanged project contract is [AI_SKILL_QUALITY_STANDARD.md](AI_SKILL_QUALITY_STANDARD.md). Its 90/100 and 19/20 requirements are release gates, not guarantees of model correctness.

## Distinct checks

1. `python3 scripts/validate_skills.py`: entrypoints, relative resources, case contracts, and deterministic arithmetic. This does not prove behavior.
2. The bundled Codex skill-creator validator: `python3 /path/to/skill-creator/scripts/quick_validate.py skills/NAME`. Its validation environment needs PyYAML; this is not a dependency of using the skills.
3. `python3 scripts/run_skill_evals.py --project /tmp/marketing-skill-evals --output /tmp/marketing-skill-results`: 20 independent real Codex tasks per skill (80 total), isolated read-only task project, no external data transmission. Requires installed authenticated Codex CLI. The harness copies only entrypoints/references/scripts, not expected answers, into the task project.
4. `python3 scripts/grade_skill_evals.py --skill NAME --output /tmp/marketing-skill-results`: independent review of saved actual outputs against prewritten criteria. Keep supporting quotes and concrete failures; review the judgments. Skill selection is recorded separately from the user deliverable; its transport line must not fail a one-word answer. Positive routing also requires a trace of reading the project entrypoint, not an unverified claim of activation.
5. Fix demonstrated failures, retain the earlier results, and rerun affected scenarios. The execution fingerprint includes skill resources, prompt, and case, so changed instructions invalidate prior runs. Never grade an absent answer as a pass.
6. Confirm public default branch, exact resource hashes, and installation from GitHub in temporary Codex/Claude Code/Cursor project locations. Installation verifies packaging, not execution compatibility.

Record the actual CLI/model, timestamp, tested source hashes, pass counts, reviewer limitations, and unresolved platform status. Claude Code and Cursor runtime acceptance require actual sessions on those hosts; directory installation alone is insufficient. A quality score cannot override an untested-platform limitation.

Keep raw synthetic execution artifacts outside published skill folders. Publish the scenario definitions, tools, and an honest summary; do not publish auth/config files or unrelated user context. Grade Outcome, Process, Style, and Efficiency; a neat format or runtime exit cannot compensate for a critical methodological failure.

The website's four original skills must include all linked resources in downloads. Preserve the external JTBD/AJTBD author's skill and installation command unchanged. Do not deploy unrelated site changes as a side effect of a skill revision.
