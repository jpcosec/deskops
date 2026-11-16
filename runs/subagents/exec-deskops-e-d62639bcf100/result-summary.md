# Result summary — exec-deskops-e-d62639bcf100

- run_id: run-deskops-e-d62639bcf100
- task: task-deskops-atoms-citations-escanea-las-citas-codigo-atomo-reporta-citas-rotas-y-atomos-sin-cita-y-las-l
- session: scion://agent/deskops-e-d62639bcf100 (claude); session_sha256: not available to the executor
- Nothing committed.

## What changed

| File | In `files`? | Why |
|---|---|---|
| `deskops/services/atoms.py` | yes | Citation grammar and scan: `docstring_citations` (ast, `Atoms:` block in the module docstring, ids `^atom-[a-z0-9-]+$` in column 0, ends at an empty line, a non-id line or the end of the docstring), `comment_citations` (`# Atom: <id>`), `scan_citations` (`git ls-files -z`, skips non-UTF-8 or missing files), `citation_doc_name`. `AtomsService.atom_citations(write=)` reports citations, broken citations and orphan atoms. `--write` creates the `cited_by` RelationTypeDoc if the store has none, plus one RelationDoc per valid (file, atom) citation (source_id = file path, target_id = `AtomDoc:<id>`) under `desk/citations/`, through `doc_access.create_doc` (the sldb transaction). It deletes cited_by RelationDocs that no file backs any more and is idempotent. `AtomsService.cited_by(atom_id)` reads those RelationDocs. |
| `deskops/cli/registry.py` | yes | New `deskops atoms citations [--root] [--check] [--write]` verb, with help, a description of the grammar and examples. |
| `deskops/cli/commands/atoms.py` | **no** | The `AtomsCLI` handler for the new subcommand (`_run_citations`). Every `atoms` verb's handler lives here, so the verb cannot run without this file. `--check` exits 1 when at least one citation is broken, even if there are also orphans. Orphans alone exit 0 with a `Warning:` list. |
| `deskops/cli/commands/operations.py` | **no** | `show atom` is served by the generic `show <artifact>` path here. The scope asks for the "Cited by:" section, so it is added when the atom has citers (in both text and JSON as `cited_by`). An atom without citers prints exactly as before, so the show/atoms_show goldens are unchanged. |
| `tests/test_atom_citations.py` | yes | Grammar unit tests plus three sandbox cases on the `lifecycle_desk` fixture (tmp_path): a valid citation (check exit 0, then `--write`, then `show atom` lists "Cited by:", idempotent, stale citation removed), a broken citation (exit 1 even with an orphan present), and an orphan atom (warning, exit 0). |
| `tests/fixtures/golden/help/deskops_atoms.txt` | **no** (help goldens, done_when "goldens de ayuda al día") | Adds the new subcommand. |
| `tests/fixtures/golden/help/deskops_atoms_citations.txt` | **no** (same) | New help golden. |

`--update-golden` also re-wrapped the usage line in `deskops_add/edit/list/show.txt`. The comparison already unwraps usage (`_unwrap_usage`), so that was noise and I reverted it with `git checkout` on those 4 files only.

Not touched: `deskops/graph/checks.py`. The scope says "si graph missing debe reportar citas rotas", which is optional, and `--check` already covers broken citations.

## Validation (validation.log)

- tests/test_atom_citations.py: 5 passed, rc=0
- tests/test_output_goldens.py: 7 passed, rc=0
- tests/test_cli_help_examples.py: 13 passed, rc=0
- tests/test_graph_checks.py: 4 passed, rc=0
- Full suite `pytest -n 4 -q tests`: **not run, left for the integrator** (brief order). Failures compared against origin/main: none to report, since the full suite was not run.
- Read-only run on the real repo: `deskops atoms citations --check --root .` gives 0 citations and 170 orphan atoms, rc=0. Deskops does not cite atoms in its code yet. I did not run `--write` on the real repo.

## Risks / gap to route (sldb)

- **sldb drops edges whose endpoint is not a tracked document.** The contract asks for a RelationDoc with source = the file path. sldb's edge index (`store/edge_index/resolve.py::_authored`) reports each one as `relation 'cite-…': source '<path>' is not a tracked document` (`check_edges` errors, `EdgeIndex.problems`) and leaves it out of the edge index. `edges_to(AtomDoc:<id>, "cited_by")` therefore returns nothing.
  - What I did: `show atom` reads the cited_by **RelationDoc documents** (`select_documents(model=RelationDoc)` plus a read of each payload) instead of the edge index. The contract says "leída de esas RelationDoc", and done_when is met.
  - `sldb stores check` still PASSes with these docs (checked in the sandbox).
  - Consequence: the citations live in the store as documents but are **not traversable edges** of the KGDB/sldb graph. Running `--write` on a repo adds one `check_edges` error per citation.
  - Suggested gap for the sldb inbox, routed by the coordinator: a node class for versioned files (e.g. `file:<path>`) that is valid as a RelationDoc endpoint. Alternatively, decide whether the citation should hang from another node.
- `desk/citations/` as the location of the RelationDocs and `cite-<sha1(path\0atom)[:12]>` as their name are my reversible choices; the contract did not fix them.
- `scan_citations` also scans docs and Markdown. A `# Atom: atom-x` example in a versioned doc would count as a citation (and as broken if the atom does not exist), as the contract specifies.
- On a loaded machine, `deskops init` in a sandbox took about 57 s real time. The tests reuse the session `lifecycle_desk` fixture, so the file takes about 25–30 s.

- `deskops graph missing --root .` (graph.txt): rc=1, 35 pre-existing missing findings from other tasks, none related to this change.
