# Copilot instructions for the Yes / No app

This repository ships with a **Graphify code knowledge graph** — a queryable map
of every file, type, and function and how they connect. Use it as your primary
way to orient in the codebase.

## Search the knowledge graph FIRST

Before grepping, opening files at random, or reasoning about how parts of the
code relate, **run a graph query first** and let the results point you to the
relevant files:

```bash
./scripts/graph-query.sh "your natural-language question"
```

Examples:

```bash
./scripts/graph-query.sh "what plays the per-button tap sounds?"
./scripts/graph-query.sh "how does localization get wired into the UI?"
./scripts/graph-query.sh "what does ContentView depend on?"
```

Then open only the files the graph surfaces and read those. This is faster and
more accurate than a blind text search, and it keeps you from missing indirect
connections.

## Keep the graph fresh

The graph lives in `graphify-out/` (git-ignored) and is rebuilt automatically by
a `post-commit` git hook. If it looks stale or is missing, rebuild it:

```bash
./scripts/rebuild-graph.sh
```

First-time setup in a fresh clone:

```bash
./scripts/setup-graphify.sh
```

## Notes

- No MCP server is involved — everything here is plain CLI, so it works inside
  the Copilot coding agent and in local editors alike.
- Graph queries need no network for code-structure questions. Semantic questions
  over docs improve if an `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` / `GEMINI_API_KEY`
  is present in the environment, but are not required.
- The app itself is a tiny SwiftUI iOS app (two full-screen Yes/No buttons, 8
  languages, per-button sounds). Keep changes minimal and match existing style.
