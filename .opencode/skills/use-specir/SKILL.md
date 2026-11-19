---
name: use-specir
description: Remission. spec2viz is retired (IR13); diagram specs, renderers, the catalog and generated diagram projections are now handled with specIR's `specir` command and sldb. Load the use-specir skill of the IR repo.
---

# use-spec2viz → use-specir

spec2viz is retired (IR13). This file stays only so that whoever loads the old `use-spec2viz` path
finds where the guidance went. The skill to use is `use-specir`, in the IR repo:
`skills/use-specir/SKILL.md` (sibling checkout: `../IR/skills/use-specir/SKILL.md`). The
command-by-command correspondence is `docs/spec2viz/correspondencia-cli.md` in that repo.

Short map:

- render / validate / lint / schema of a spec → `specir diagram render|validate|lint|schema`
- catalog HTML → `specir catalog build`
- catalog sync / check → `sldb notations sync --catalog [--check]`
- serving the catalog's annotations → `sldb serve`
- spec from a graph or Python source → `sldb notations from-graph`

Deskops conventions that still hold: diagram docs live under `docs/diagrams/`, rendered files are
projections reproducible from their source spec, and durable knowledge goes into atoms/specs first.
