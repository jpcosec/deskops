## REFORMULACION

**Propósito:** que deskops empaquete un RoleDoc `desk-identity` y lo instale en cualquier desk, y que `runtime template --mode identity` materialice un agente scion persistente de identidad.

**Resultado:** RoleDoc YAML en una carpeta `roles` del paquete; instalación idempotente desde `desk update --apply` e `init`; modo `identity` en `runtime template`; goldens y tests actualizados.

**Repo:** `/mnt/ssd/proyectos/SLDB_1/deskops`.

**Límites:** no crear el agente en scion, ni hook, ni cambios en scion, ni traducción de tools (dependencia).

## AMBIGUEDADES

1. **Instalación con o sin subproceso.** El input dice “con `deskops add role` por debajo” y luego “sin lanzar un subproceso del CLI”. Obliga a inventar si se invoca el CLI o se reutiliza `DeskopsOperations.create_artifact`.
2. **Contenido exacto del RoleDoc para goldens.** Se describen secciones y comandos, pero no el YAML/markdown byte a byte; los goldens exigen hashes. Obliga a inventar frontmatter, orden y redacción exacta.
3. **Patrón de `package-data`.** “un patron para los YAML de esa carpeta roles” no fija el glob. Obliga a inventar `roles/*.yaml` u otro.
4. **Qué significa “workspace relativo”.** “workspace relativo en un proyecto de carpeta sin git” no define el texto ni la configuración concreta del `agents.md`. Obliga a inventar la redacción.
5. **Existencia parcial del rol.** “cualquiera de las tres cuenta como existente” no dice qué hacer si el archivo existe pero no es un RoleDoc válido. Obliga a inventar si se lista divergencia o se ignora.

## DRY-RUN

**Lecturas:** TaskDoc, `pyproject.toml`, `desk.py`, `core.py`, `scion.py`, `registry.py`, tests y goldens citados; dependencia de traducción de tools.

**Cambios previstos:** crear `deskops/roles/desk-identity.yaml`; añadir patrón en `package-data`; función compartida de instalación y llamadas en `desk update`/`InitCLI`; rama `identity` y `_render_identity_agents_md` en `scion.py`; `choices` en `registry.py`; dos tests nuevos; regenerar goldens de ayuda y scaffold.

**Dependencias:** `task-el-runtime-profile-traduce-los-tools...`; `parse_artifact_input`, `DeskopsOperations`, `_example_roots`.

**Validaciones futuras:** los tres pytest indicados y suite completa con `-n 4`; revisar diff de goldens; comprobar que `desk update` en seco lista el rol y que una segunda corrida dice “Desk is up to date.”

## FUTURO

Otro nodo debe entregar la traducción de tools del RoleDoc al vocabulario de claude y el alias de modelo. Un humano/JP debe resolver las ambigüedades 1–5 antes de implementar. El cierre/commit queda para el flujo de closeout; este nodo no ejecuta nada.
