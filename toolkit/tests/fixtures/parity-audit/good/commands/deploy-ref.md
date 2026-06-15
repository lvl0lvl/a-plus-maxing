---
description: fixture exercising BUG-22f placeholder-skip + the anchor mapping
---

# Deploy Ref (fixture)

Illustrative placeholder paths must be SKIPPED (BUG-22f), not resolved:
`~/.claude/skills_library/roles/...` and `~/.claude/.../anything`.

The anchor must resolve against --lib, not the deploy root: the architect role at
`~/.claude/skills_library/roles/architect/agent.md` exists in this lib's roles/.
