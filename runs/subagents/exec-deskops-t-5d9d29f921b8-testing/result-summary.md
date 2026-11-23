PASA

# Tester — despertar la identidad scion al llegar una nota (identity.wake)

- Task: `task-al-llegar-una-nota-al-inbox-de-un-desk-deskops-despierta-a-la-identidad-scion-de-ese-desk-si-su-conf`
- Commit revisado: `465b442bd9437b4e4bd4538a755678ebda94c602` (`deskops message: despertar la identidad scion del desk al llegar una nota (identity.wake)`), con el trailer `Task-Id` correcto.
- Archivos del commit: `deskops/config.py`, `deskops/wake.py` (nuevo), `deskops/cli/commands/message.py`, `deskops/cli/registry.py`, goldens de ayuda, `tests/test_config.py`, `tests/test_message_cli.py`, `tests/test_message_delivery.py`. Todos dentro del scope declarado.

## Veredicto: PASA

Los cinco tests nuevos pasan y los tests existentes de mensajería siguen verdes sin cambios funcionales.

## Evidencia de tests (de a un archivo, TMPDIR=/tmp)

| Archivo | Resultado |
|---|---|
| `tests/test_message_delivery.py` | **9 passed** (incluye los 4 nuevos de wake; 204 s) |
| `tests/test_message_cli.py` | **17 passed** (221 s) |
| `tests/test_config.py` | **6 passed** (incluye `test_load_takes_identity_from_config_local_json`) |
| `tests/test_output_goldens.py` | **7 passed** (goldens de ayuda y salidas; 442 s) |
| `tests/test_command_registry.py` | **3 passed** (registry tocado) |
| `tests/test_queue.py` | **18 passed** en venv limpio (comprobación adicional del enqueue/gate) |
| Nuevos tests aislados en venv limpio (`-k 'wake or identity'`) | **6 passed** |

## Comprobaciones de contrato

- `IdentityConfig` tiene `scion_project`, `agent`, `wake=False` por defecto, `command` con factory y el argv por defecto del encargo; `DeskConfig.load` mezcla `config.local.json` con `_deep_merge_dicts`.
- `wake_identity(root, note_name)` no hace nada sin identity o con `wake=false`; consulta `queue.wait_reason(config)` y devuelve `bloqueado: <motivo>`; ejecuta argv sin shell (`subprocess.run` sin `shell=True`), `stdin=DEVNULL`, timeout 60 s; devuelve `despertado` / `fallo: <rc>` (incluye timeout y `OSError`).
- `message send` llama al wake después de escribir/validar la nota, captura cualquier excepción y nunca cambia el rc del send. Un bloqueo/fallo imprime aviso en stderr. Smoke manual con `command=["sh","-c","exit 7"]`: send rc 0, nota entregada, `Warning: ... (fallo: 7)` en stderr.
- Con gate bloqueado y `queue_jobs` declarando `wake-identity`, encola un trabajo pendiente `wake-identity` (test de integración); sin identity el comportamiento no cambia (tests previos verdes).
- `deskops message wake --root <desk> [--note <id>]` existe con ayuda/golden, ejecuta `wake_identity` y sale con rc 3 cuando el gate bloquea (`retry_exit_codes: [3]`).

## Notas de entorno (no afectan al veredicto)

- El venv del repo (`/workspace/.venv`, mismo path que `/mnt/ssd/proyectos/SLDB_1/.venv`) tenía los symlinks de `python3`/`python3.12` rotos (apuntaban a un `/usr/bin/python3` que ahora es 3.11), por lo que `python -m pytest` no encontraba pytest. Para verificar se usó un CPython 3.12.16 gestionado por uv (`/dev/shm/tester-venv`) con las dependencias instaladas desde `pyproject.toml`, y `TMPDIR=/tmp`.
- Un primer `tests/test_queue.py` falló con `ModuleNotFoundError: sldb.store` porque ese test reemplaza `PYTHONPATH` en sus subprocesos y el workaround inicial dependía del entorno; en el venv limpio con `sldb` instalado pasó 18/18. No es un fallo del commit.
- No se corrió la suite completa, siguiendo la instrucción del rol tester; la integración completa queda para el host. No se modificó código, desk ni `.sldb` durante la revisión.

Detalle crudo de comandos y resultados: `runs/subagents/exec-deskops-t-5d9d29f921b8-testing/validation.log`.
