## REFORMULACION
Propósito: que deskops distribuya la identidad de desk como dato reutilizable. Resultado: (1) RoleDoc `desk-identity` empaquetado junto a `deskops/data/templates` (name `desk-identity`, kind `claude`, tools read/grep/find/ls/bash, cuerpo con reglas de triaje, reenvío, atoms, sin código/dispatch/cola/push, `desk/` y `.sldb/` solo por CLI, `--root` siempre); (2) `deskops desk update --apply` lo instala en `desk/roles` sin pisar existentes (en seco lo lista), apoyado en `deskops add role`; (3) `deskops runtime template --mode identity` escribe `agents.md` de identidad persistente con raíz del desk y proyecto scion, sin worktree ni instrucciones de ejecutor/tester/coordinador. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: no crea el agente en scion, no hook, no repo scion, no mapa de propiedad.

## AMBIGUEDADES
1. "dejar abierto lo que pide decisión de JP y decirlo": no define qué cuenta como decisión de JP ni formato del aviso; obligaría a inventar criterio.
2. "ack con motivo" / "tarea + ack": formato del ack no especificado.
3. "reenviar lo ajeno ... --to <dueño>" frente a "mandar lo sin dueño a su destino": sin criterio para identificar dueño ni destino.
4. "registrar un acuerdo cerrado en un hilo como atom con la referencia del hilo": no define "acuerdo cerrado" ni esquema del atom.
5. "el mensaje de hoy actualizado": no cita el texto actual del error de `--mode` desconocido.
6. "nombra ... el proyecto scion": no dice qué nombre usar.
7. "sin las instrucciones de ejecutor/tester/coordinador": no enumera qué bloques exactos del template se omiten.
8. "deskops desk update --apply (y el modo en seco lo lista)": no aclara si el seco es el comportamiento por defecto ni su formato de salida (goldens).
9. `depends_on` a la tarea de traducción de tools: no dice si esta tarea queda bloqueada hasta que aterrice.

## DRY-RUN
Lecturas: este TaskDoc, la tarea dependiente, la nota de inbox referenciada, `deskops/cli/commands/desk.py`, `deskops/runtime/scion.py`, `deskops/cli/commands/runtime.py`, `tests/test_desk_sync.py`, `tests/test_scion_runtime.py`, `tests/test_output_goldens.py` y plantillas en `deskops/data/templates`. Cambios previstos: RoleDoc nuevo como dato; edición de `desk.py` (instalación en update), `scion.py` y `runtime.py` (`--mode identity`); dos tests nuevos; goldens de ayuda. Dependencias: CLI `add role`, formato RoleDoc existente, tarea de traducción de tools. Validaciones futuras, sin ejecutar: los cuatro comandos pytest listados (incluida suite `-n 4`) y el commit con `git commit -- <rutas>` más trailer `Task-Id`.

## FUTURO
Que aterrice la tarea dependiente de tools; la autorización de Governance sobre el texto base; que JP decida los ítems de inbox abiertos; la ejecución real de la suite y el commit.
