# Format and platform boundaries — 2026-11-21

Checked primary documentation:

- Agent Skills specification: https://agentskills.io/specification
- OpenAI local skill authoring/discovery: https://learn.chatgpt.com/docs/build-skills
- Anthropic Agent Skills overview: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview

Entrypoints use required `name` and `description` only, portable Markdown, and relative resources. Detailed materials load progressively. The ODI calculator needs Python 3 only when used; the other procedures are instruction-only. No MCP/API/secret is required by these four skills.

Codex discovers repository skills under `.agents/skills`; Claude Code uses `.claude/skills`; deployment through the Skills CLI can create the relevant agent locations. Do not assume same-name global skills are merged or replaced: test the actual installed path and record which file the host reads.

The current behavioral harness exercises Codex, not Claude Code or Cursor. These other hosts remain unverified at runtime unless a dated acceptance report states an actual run. Filesystem layout and specification conformance are necessary but insufficient for claiming compatibility.
