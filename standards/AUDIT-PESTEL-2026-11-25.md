# PESTEL quality audit — 2026-11-25

Codex behavioral acceptance: **19/20**, **95/100**, no observed critical methodological failures.

Initial run: 13/20. Focused questions did not consistently select/read the skill; one proposed-rule answer omitted jurisdiction. Metadata and the jurisdiction instruction were clarified. Three ambiguous prompts were explicitly situated in a PESTEL review instead of expecting a macro skill for standalone law, survey or forecast questions. The original prompts, answers and verdicts remain in local audit artifacts. All twenty final cases were executed anew; criteria were not weakened.

Final scenario 14 failed: it rejected an objective interpretation of 92/100 but mentioned a mockup label without proposing the required alternative qualitative priorities or transparent separate judgment scales. The limitation remains recorded rather than counted as a pass.

Tests use actual ephemeral, read-only Codex CLI 0.171.0-alpha.13.2 runs in an isolated project. Entry-point reads and selected-skill metadata are verified. Default model identity was not emitted in JSON events; no model identity is inferred. A separate Codex invocation reviewed saved answers against prewritten Outcome, Process, Style and Efficiency criteria, not just successful process exits. This is not independent human assessment.

Primary basis: CIPD's scope/source/analysis/options/monitoring process, UCLA's ETPS history and institutional PESTEL definitions. Source boundaries and unavailable readers are documented in [sources](../skills/pestel-analysis/references/sources.md). No current legal/market claims or proprietary forecasting formula are asserted.

| Criterion | Maximum | Awarded |
| --- | ---: | ---: |
| Task clarity | 8 | 8 |
| Activation | 8 | 8 |
| Methodology | 12 | 12 |
| Procedure | 10 | 9 |
| Inputs | 7 | 7 |
| Truthfulness | 10 | 10 |
| Output | 8 | 7 |
| Examples | 6 | 6 |
| Edge cases | 7 | 7 |
| Tools/security | 7 | 7 |
| Architecture | 5 | 5 |
| Testing | 8 | 7 |
| Portability | 4 | 2 |

Procedure and output each lose one point for the recorded omitted alternative; testing loses one for a single final run per case, no ablation or human-independent review. Portability loses two because Claude Code/Cursor execution was unavailable. Installation is checked separately after publication and does not certify behavior in those agents. There are no runtime code dependencies; PyYAML is needed only by the temporary authoring validator.

Nine structural tests and the official skill quick validator passed. Other five project skills and external JTBD/AJTBD were not modified. Exact tested file hashes and per-case evidence: [BEHAVIOR-PESTEL-2026-11-25.json](BEHAVIOR-PESTEL-2026-11-25.json). Public main, SHA and installation are independently verified after publication; absence of those records must not be read as a successful install.
