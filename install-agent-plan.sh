#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
if [ ! -f AGENTS.md ]; then
  printf '# SkillForge agent instructions\n\n' > AGENTS.md
fi
if ! grep -Fq '## SkillForge mandatory plan tracking' AGENTS.md; then
  printf '\n' >> AGENTS.md
  cat AGENTS-plan-section.md >> AGENTS.md
  echo 'Added plan tracking policy to AGENTS.md'
else
  echo 'AGENTS.md already includes plan tracking policy; no changes made'
fi
