# AI Skills

Публичный каталог AI Skills для маркетинга, стратегии и исследований. Каждый Skill решает отдельную профессиональную задачу и устанавливается целиком.

## Каталог

| Skill | Задача | Файлы |
|---|---|---|
| Business Model Canvas | Описание бизнес-модели | [Открыть](skills/business-model-canvas/) |
| Customer Development | Исследование клиентов | [Открыть](skills/customer-development/) |
| Outcome-Driven Innovation | Исследование желаемых результатов | [Открыть](skills/odi-outcome-research/) |
| PESTEL | Анализ макросреды | [Открыть](skills/pestel-analysis/) |
| Porter's Five Forces | Анализ отрасли | [Открыть](skills/porters-five-forces/) |
| STP | Сегментация, таргетинг, позиционирование | [Открыть](skills/stp-strategy/) |
| Switch Interview | Исследование смены решения | [Открыть](skills/switch-interview/) |
| Value Proposition Canvas | Ценностное предложение | [Открыть](skills/value-proposition-canvas/) |

## Установка

Нужны Node.js и установленный AI-клиент. Пример для PESTEL:

**Claude Code**

```bash
npx skills add daniil-tv/1000-frameworks-skills --skill pestel-analysis -a claude-code
```

**Codex**

```bash
npx skills add daniil-tv/1000-frameworks-skills --skill pestel-analysis -a codex
```

Замените pestel-analysis на имя каталога выбранного Skill. Установить можно также вручную: скопируйте весь каталог Skill в .claude/skills/ или .agents/skills/ проекта. Не копируйте только SKILL.md.

## Качество и ограничения

Структурная проверка, установка и поведенческие испытания — разные виды проверки. Подробные результаты и ограничения платформ: [стандарт качества](standards/AI_SKILL_QUALITY_STANDARD.md), [протокол оценки](standards/EVALUATION.md), [отчёты](standards/). Не считать наличие команды установки подтверждением работы на всех платформах.

The JTBD page points to Ivan Zamesin's separate [Next Move Theory Canon & Skills](https://github.com/zamesin/Next-Move-Theory-Canon-and-Skills) repository. That author's AJTBD / Next Move Theory skills are not copied into this collection or represented as generic JTBD.

The dated [audit and remaining limitations](standards/AUDIT-2026-11-23.md) records actual Codex behavioral results and the rubric score. Claude Code and Cursor runtime acceptance is incomplete; their installation options above do not imply runtime certification.

The new Value Proposition Canvas skill has a separate [2026-11-24 quality audit](standards/AUDIT-VPC-2026-11-24.md) with its actual behavioral results and platform limitations.

The PESTEL skill has a separate [2026-11-25 quality audit](standards/AUDIT-PESTEL-2026-11-25.md) with actual results and platform limitations.

The Five Forces skill has a separate [2026-11-26 quality audit](standards/AUDIT-PORTER-2026-11-26.md) with actual behavioral results and platform limitations.

The STP skill has a separate [2026-11-26 quality audit](standards/AUDIT-STP-2026-11-26.md) with actual behavioral results and platform limitations.

## AI-сотрудники

[AIEmployee — отдельный каталог профессиональных сотрудников](https://github.com/daniil-tv/1000-frameworks-employees).
