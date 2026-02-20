---
name: memory
description: LanceDB-backed memory with automatic consolidation and ExperienceLoop experience learning.
always: true
---

# Memory

## Structure

Memory is stored in **LanceDB** (auto-managed, no manual file operations needed):

| Table | Contents |
|-------|----------|
| `memory` | Long-term facts (`key='long_term'`), conversation history (`type='history'`), task experience (`type='experience'`) |
| `memory_vectors` | Optional semantic embeddings for similarity search (auto-backfilled on first setup) |

## How It Works

- **Long-term memory** is always loaded into your context at conversation start
- **History** is an append-only event log — search it with keywords
- **Experience** stores lessons learned from past tasks — retrieved automatically when similar tasks arise

## Search Past Events

Use the `exec` tool to search history stored in LanceDB. The system handles this internally — just describe what you're looking for and the agent will find relevant context.

## When to Remember

Important facts are captured automatically during conversation consolidation:
- User preferences ("I prefer dark mode")
- Project context ("The API uses OAuth2")
- Relationships ("Alice is the project lead")

For identity/preferences that should persist, update `PERSONA.md` directly using `edit_file`.

## Auto-consolidation

Old conversations are automatically summarized when the session grows large:
- Key facts → long-term memory
- Event summaries → history entries
- Task lessons → experience entries (via ExperienceLoop)

You don't need to manage this manually.

## Experience Lifecycle (ExperienceLoop)

Experience entries follow a closed-loop lifecycle with feedback:

| Phase | Description |
|-------|-------------|
| **Extraction** | After task completion (≥2 tool calls or errors), lessons + search keywords + reasoning trace are automatically extracted |
| **Scoring** | Each experience gets a quality rating (1-5), category, and usage counters (Uses/Successes) |
| **Retrieval** | On similar tasks, results ranked by `quality × time_decay × confidence` and injected into system prompt |
| **Feedback** | Reuse events update Uses/Successes counters; quality auto-adjusts based on success rate after ≥3 uses |
| **Conflict Detection** | When retrieved experiences in the same category have contradicting outcomes, they are flagged with ⚡ |
| **Warnings** | Failed experiences are preserved and surfaced as ⚠️ warnings to prevent repeating mistakes |
| **Cleanup** | Deprecated entries (>30 days) and low-quality entries (quality=1, >90 days) are auto-removed |
| **Merging** | When ≥3 experiences share a category, they are periodically merged into high-level principles |

Experience storage format:
```
[Task] Task description
[Outcome] success/partial/failed
[Category] coding
[Quality] 4
[Uses] 5
[Successes] 4
[Lessons] Reusable strategies and lessons learned
[Keywords] git rebase, merge conflict
[Trace] Reasoning steps taken during the task
```

Confidence = Successes / Uses (calibrated after ≥2 uses).
Time decay: half-life ~35 days, ensuring fresh experiences rank higher.
