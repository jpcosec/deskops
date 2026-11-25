FILE:desk/tasks/task-deskops-atoms-citations-queda-declarado-como-comando-que-modifica-en-el-test-del-registro-de-comando.md
---
sldb:
  by: agent
  at: '2026-11-16T23:00:31Z'
  authority: generated
  via: create_document
id: task-deskops-atoms-citations-queda-declarado-como-comando-que-modifica-en-el-test-del-registro-de-comando
status: draft
summary: ''
tags:
- host:robocop2
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- tests/test_command_registry.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-un-archivo-de-codigo-cita-los-atomos-que-implementa-y-deskops-atoms-citations-lo-comprueba
---

# deskops atoms citations queda declarado como comando que modifica en el test del registro de comandos

## Rationale

_Explain why this task exists or the business driver behind it._

La integracion de wA:p1 sobre 12c5c2ce dio 1113 passed y 1 failed: tests/test_command_registry.py::test_mutating_commands_are_declared_explicitly. La tarea de atoms citations (996becef, closeout 8b0aae02) agrego el comando deskops atoms citations, que con --write crea y borra RelationDoc en el desk; su entrada en deskops/cli/registry.py ya lleva mutates=True, pero el conjunto esperado MUTATING_COMMANDS del test no lo lista, y el test compara igualdad exacta.

## Goal

_Describe the concrete result this task must produce._

tests/test_command_registry.py pasa: ('atoms', 'citations') esta en MUTATING_COMMANDS junto a los demas subcomandos de atoms que modifican, y la entrada del registro sigue declarando mutates=True.

## Scope

_State what is in scope and what is out of scope._

Entra: agregar la tupla ('atoms', 'citations') al conjunto MUTATING_COMMANDS de tests/test_command_registry.py, en el bloque de los subcomandos de atoms. Sale: deskops/cli/registry.py (ya declara mutates=True; solo se lee para confirmarlo), el comportamiento del comando y cualquier otro test.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Correr tests/test_command_registry.py y confirmar que la unica falla es ('atoms', 'citations'). 2) Confirmar en deskops/cli/registry.py que la entrada path=('atoms', 'citations') tiene mutates=True. 3) Agregar la tupla a MUTATING_COMMANDS. 4) Correr la Validation.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_command_registry.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_atom_citations.py

## Done When

_Name the observable condition that makes the task complete._

tests/test_command_registry.py y tests/test_atom_citations.py pasan y git diff solo toca tests/test_command_registry.py.

FILE:desk/atoms/workflow-model/atom-code-changes-close-with-tests-and-commit.md
---
id: atom-code-changes-close-with-tests-and-commit
title: Code changes close with tests and commit
five_wh_one_plus: when
tags:
- system:deskops
- topic:testing
- topic:git
- topic:closeout
---

# Code changes close with tests and commit

## Answer

A task that modifies code is not closed until relevant tests pass and the completed change is recorded in a descriptive git commit.

FILE:desk/atoms/atom-un-archivo-de-codigo-cita-los-atomos-que-implementa-y-deskops-atoms-citations-lo-comprueba.md
---
sldb:
  by: agent
  at: '2026-11-16T22:30:24Z'
  authority: generated
  via: create_document
id: atom-un-archivo-de-codigo-cita-los-atomos-que-implementa-y-deskops-atoms-citations-lo-comprueba
title: Un archivo de codigo cita los atomos que implementa y deskops atoms citations
  lo comprueba
five_wh_one_plus: how
tags:
- system:deskops
- topic:atoms
provenance: tests/test_atom_citations.py
---

# Un archivo de codigo cita los atomos que implementa y deskops atoms citations lo comprueba

## Answer

Un modulo Python cita los atomos que implementa con un bloque Atoms: en su docstring de modulo (un id atom-... por linea, en columna 0, hasta una linea vacia); cualquier otro archivo versionado usa comentarios '# Atom: <id>'. deskops atoms citations recorre git ls-files, reporta las citas, las citas rotas (atomo inexistente) y los atomos sin cita; --check sale 1 si hay una cita rota; --write registra cada cita como un RelationDoc cited_by (archivo -> AtomDoc) y deskops show atom muestra 'Cited by:'. Limitacion vigente de sldb (2026-11-16): una ruta de archivo no es extremo valido de RelationDoc, asi que la cita es un documento y no una arista recorrible, y sldb edges check da un error por cita.

FILE:tests/test_command_registry.py
"""The declared command registry must match the frozen CLI surface.

The help goldens were captured from the hand-built parser by
task-rw-f1-output-golden-files, so comparing registry paths against that
directory catches both dropped commands and accidental new ones.
"""

from __future__ import annotations

from pathlib import Path

from deskops.cli.registry import command_registry


HELP_GOLDENS = Path(__file__).resolve().parent / "fixtures" / "golden" / "help"


def _golden_command_paths() -> set[tuple[str, ...]]:
    paths: set[tuple[str, ...]] = set()
    for path in HELP_GOLDENS.glob("deskops_*.txt"):
        if path.name == "deskops.txt":
            continue
        paths.add(tuple(path.stem.split("_")[1:]))
    return paths


def test_registry_paths_match_help_goldens() -> None:
    declared = {command.path for command in command_registry()}

    assert declared == _golden_command_paths()


def test_registry_paths_are_unique_and_have_parents() -> None:
    commands = command_registry()
    paths = [command.path for command in commands]

    assert len(paths) == len(set(paths))
    declared = set(paths)
    for path in paths:
        assert path
        if len(path) > 1:
            assert path[:-1] in declared


MUTATING_COMMANDS: set[tuple[str, ...]] = {
    ("doctor",),
    ("bootstrap",),
    ("init",),
    ("inbox",),
    ("message",),
    ("message", "send"),
    ("message", "ack"),
    ("review",),
    ("review", "node"),
    ("review", "preflight"),
    ("review", "bundle"),
    ("review", "dispose"),
    ("review", "record"),
    ("promote",),
    ("promote", "inbox-to-drawer-task"),
    ("drawer",),
    ("drawer", "remove"),
    ("issue",),
    ("issue", "close"),
    ("add",),
    ("add", "task"),
    ("add", "pill"),
    ("add", "ritual"),
    ("add", "board"),
    ("add", "atom"),
    ("add", "materialization"),
    ("add", "repository"),
    ("add", "inbox-note"),
    ("add", "faq-doc"),
    ("add", "step"),
    ("add", "role"),
    ("add", "runtime-profile"),
    ("edit",),
    ("edit", "task"),
    ("edit", "pill"),
    ("edit", "ritual"),
    ("edit", "board"),
    ("edit", "atom"),
    ("edit", "materialization"),
    ("edit", "repository"),
    ("edit", "review"),
    ("edit", "inbox-note"),
    ("edit", "faq-doc"),
    ("edit", "step"),
    ("edit", "role"),
    ("edit", "runtime-profile"),
    ("bind",),
    ("bind", "pill"),
    ("advance",),
    ("advance", "task"),
    ("repo",),
    ("repo", "register"),
    ("repo", "remove"),
    ("retire",),
    ("desk",),
    ("desk", "install"),
    ("desk", "migrate"),
    ("desk", "replace"),
    ("desk", "update"),
    ("atoms",),
    ("atoms", "add-namespace"),
    ("atoms", "reorganize"),
    ("atoms", "create"),
    ("atoms", "delete"),
    ("atoms", "split"),
    ("atoms", "merge"),
    ("atoms", "crossroad"),
    ("atoms", "proto"),
    ("atoms", "type"),
    ("graph",),
    ("graph", "build"),
    ("graph", "reflect"),
    ("materialize",),
    ("closeout",),
    ("closeout", "commit"),
    ("closeout", "supersede"),
    ("closeout", "retire"),
    ("closeout", "resolved-by"),
    ("runtime",),
    ("runtime", "init"),
    ("runtime", "stop"),
    ("runtime", "template"),
}


def test_mutating_commands_are_declared_explicitly() -> None:
    """Every command that writes desk files, the store, or git must say so."""
    declared = {command.path for command in command_registry() if command.mutates}

    assert declared == MUTATING_COMMANDS

FILE:instruccion
Cold-bundle de la tarea task-deskops-atoms-citations-queda-declarado-como-comando-que-modifica-en-el-test-del-registro-de-comando: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_command_registry.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_atom_citations.py

