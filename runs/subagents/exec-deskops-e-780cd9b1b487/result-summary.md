# Result
Changed: AGENTS.md (line 25 -> use-specir), README.md (line 54 no longer cites references/spec2viz-cli.md), git mv .opencode/skills/use-spec2viz -> use-specir (content unchanged).
Validation: drift test passes. Finding: grep use-spec2viz in .opencode still matches 3 lines (SKILL.md of use-specir lines 6,8 - content must stay unchanged per Goal; use-deskops/SKILL.md:159 says "replaces the retired use-spec2viz", out of scope). Supervisor should decide whether to relax the grep.
Note: .claude/skills/deskops-workflow/references/spec2viz-cli.md still exists (out of scope).
