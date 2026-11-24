# Framework Skills quality contract

Scope: the original skills in skills/, including newly authorized framework skills. The external JTBD/AJTBD skill is not part of this repository and must not be copied, revised, or attributed to us.

Before creating a skill or changing one explicitly requested by the user, read standards/AI_SKILL_QUALITY_STANDARD.md in full. It is the project's acceptance contract. Preserve existing skill names and public installation paths; add a new name only for an explicitly requested new skill. Keep domain instructions separate from publishing/SEO work.

Research primary methodology sources before writing; keep the compact entrypoint, source-aware procedure, evidence distinctions, useful examples, negative routing cases, and honest limitations. Each skill has 20 behavioral scenarios. Structural tests alone do not satisfy behavioral acceptance. Report actual platform/runtime/model, scenario results, and source/code hashes. Require >=90/100 and >=19/20 with no critical methodological failures for full acceptance on a tested platform. If a runtime is unavailable, explicitly mark its acceptance incomplete; never infer a pass from installation.

Run python3 scripts/validate_skills.py before publication. Review the exact diff; do not modify seo/, src/, unrelated workflows, or other skills. Publish only after available checks; verify public main and the exact installed files. Keep the supplied standard unchanged; document any future amendments explicitly.
