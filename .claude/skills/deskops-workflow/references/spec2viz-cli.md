# spec2viz CLI reference (retired)

spec2viz is retired (IR13). Its command reference no longer lives here: diagrams are rendered,
validated and catalogued with specIR's `specir` command, and the generic parts (syncing specs,
notations, palettes and catalogs into a store, generating specs from a graph or from Python,
serving catalog annotations) with `sldb` directly.

Read instead, in the IR repo (sibling checkout `../IR`):

- `skills/use-specir/SKILL.md` — the skill: who owns what, CLI taxonomy, Python API (`specir.visual`).
- `docs/spec2viz/correspondencia-cli.md` — every old spec2viz command and its equivalent.

Short map:

| Old | Now |
|---|---|
| diagram render | `specir diagram render <spec.yml> --out <dir> [--renderer ...]` |
| diagram validate | `specir diagram validate <spec.yml>` |
| diagram lint / schema | `specir diagram lint`, `specir diagram schema` |
| catalog build / schema | `specir catalog build --config <catalog.yml> --out <out.html>`, `specir catalog schema` |
| catalog sync / validate | `sldb notations sync --catalog [--check]` |
| catalog serve | `sldb serve` |
| diagram generate / from-graph | `sldb notations from-graph` |

Run `specir about` and `specir <group> <command> --help` to confirm flags.
