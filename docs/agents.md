# Agents

This document describes the future agent architecture. No agents exist yet.

## Concept

An agent is a role-oriented AI worker. It combines skills, rules, and tools to take on a broader engineering responsibility than a single skill covers. Agents reuse skills rather than duplicating their instructions.

## Intended Roles

Agents will eventually represent engineering roles such as:

- Software Architect
- Backend Engineer
- Frontend Engineer
- Test Engineer
- Debugging Engineer
- DevOps Engineer
- Security Engineer
- Database Engineer

These are planned roles only and have not been created.

## Location

Agents will live in the platform-native directories: `.claude/agents/` for Claude Code and `.github/agents/` for GitHub Copilot.

## Naming

Use lowercase kebab-case, for example `software-architect` or `test-engineer`.
