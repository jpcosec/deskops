FALLA

# Veredicto del tester

El commit del ejecutor cumple el renombrado de la carpeta y el test de drift pasa, pero no cumple la Validation ni el Done When: el token `use-spec2viz` sigue presente en `.opencode`.

## Commit evaluado

- Commit: `eee49b8993879f4c54ac3720fbc1eaf7524cfdbb`
- Mensaje: `Route AGENTS/README to use-specir and rename opencode skill folder`
- Trailer: `Task-Id: task-agents-md-readme-md-y-la-carpeta-de-la-skill-de-opencode-dejan-de-nombrar-use-spec2viz-y-pasan-a-use`
- Archivos:
  - `.opencode/skills/use-spec2viz/SKILL.md` -> `.opencode/skills/use-specir/SKILL.md` (rename 100%)
  - `AGENTS.md`
  - `README.md`

## Pruebas ejecutadas

En un worktree limpio del commit (`/tmp/deskops-test-eee49b89`), con Python 3.13.18 y pytest 9.1.1 de `/mnt/ssd/proyectos/SLDB_1/sldb/.venv/bin/python`:

- `PYTHONPATH=$PWD TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_skill_cli_drift.py`
  - Resultado: **2 passed**, exit 0.
- El commit no toca archivos `tests/*.py` ni módulos de código, así que no hay otros tests del commit que ejecutar.

## Chequeo de Validation que falla

```text
$ grep -rn use-spec2viz AGENTS.md README.md .opencode
.opencode/skills/use-specir/SKILL.md:6:# use-spec2viz → use-specir
.opencode/skills/use-specir/SKILL.md:8:spec2viz is retired (IR13). This file stays only so that whoever loads the old `use-spec2viz` path
.opencode/skills/use-deskops/SKILL.md:159:- Load `use-specir` (IR repo, `skills/use-specir/SKILL.md`; replaces the retired `use-spec2viz`) for structured diagram specs and generated diagram projections.
exit 0 (3 coincidencias)
```

La Validation pide `rc 1` sin coincidencias y el Done When repite que el grep en `AGENTS.md`, `README.md` y `.opencode` no debe dar nada. Hay tres coincidencias, todas dentro de `.opencode`.

## Por qué no aplica la excepción de “menciones históricas”

La aceptación registrada de la tarea (preflight-1 y bundle-1, ambas `accepted`) precisa el criterio:

- No debe quedar el token `use-spec2viz` en `AGENTS.md`, `README.md` ni `.opencode`; solo se quedan menciones históricas de `spec2viz` sin ese token.
- El título del `SKILL.md` movido puede cambiar para no usar el token (por ejemplo, “antes la skill de spec2viz de opencode”); el resto del contenido no cambia.
- Si el grep encuentra el token en otras skills de `.opencode`, también se cambian y se informa.

Por tanto, la referencia histórica permitida es `spec2viz`, no el identificador `use-spec2viz`. `use-specir/SKILL.md` conserva el token en el título y en el cuerpo, y `use-deskops/SKILL.md:159` lo conserva en la frase de reemplazo. El ejecutor lo reportó como fuera de alcance, pero la aceptación lo pone explícitamente dentro de alcance.

## Corrección necesaria

Quitar el token `use-spec2viz` de las tres líneas manteniendo el sentido histórico (p. ej. título `# use-specir (antes la skill de spec2viz de opencode)`, “la ruta anterior de spec2viz” y “replaces the retired spec2viz”), sin cambiar el resto del contenido del `SKILL.md` renombrado. Después, repetir el grep y `tests/test_skill_cli_drift.py`.

## Entorno

El `.venv` de `/mnt/ssd/proyectos/SLDB_1` está roto en este contenedor: sus binarios apuntan a un Python 3.12 ausente (y `python` resuelve a 3.11 sin pytest). No modifiqué el repositorio para la validación; usé el worktree temporal anterior y el Python 3.13 de `sldb/.venv`, que ejecuta el test correctamente.
