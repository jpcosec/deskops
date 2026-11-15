# rutas-worker: doctor detecta y repara rutas absolutas

Rama wt/rutas desde main e1f11c23.

## Cambios
- `deskops/absolute_paths.py` (nuevo): escanea el frontmatter de `desk/**/*.md`, resuelve cada ruta absoluta contra los vecinos y aplica la reparación.
- Vecinos: links de `.sldb/store.yaml` leídos con `sldb.api.stores.store_declaration.load_declaration` (fallback `sldb.api.store_links`), más las entradas del registro con ruta relativa. La raíz de un vecino es el padre de su `.sldb`.
- `deskops/cli/commands/doctor.py`: `_check_absolute_paths`; una alerta por ruta, rc sin cambio; con `--repair` escribe con `read_doc`/`write_doc` dentro de `desk_transaction` (transacción de sldb).
- Reglas: bajo la raíz propia -> relativa sin prefijo; existe y cae bajo un vecino -> `../x` en registry `path`, `<repo-id>:<ruta>` en files/references; no existe -> solo si lo que sigue a la carpeta del ecosistema nombra un único vecino (varias apariciones con candidatos distintos = ambigua). Lo demás queda alerta con motivo.
- Tests nuevos: `tests/test_doctor_absolute_paths.py` (13). CHANGELOG y docs/operator-manual.md actualizados.

## Resultados (de a uno, TMPDIR=/dev/shm)
test_doctor_absolute_paths 13 passed; test_doctor_alerts 5; test_doctor_model_registration 8; test_doctor_unmodeled_surfaces 4; test_cli 101; test_output_goldens 7. Ningún golden cambió.

## Dudas
- Los ids `<repo-id>` salen del registro; un vecino con link pero sin entrada de registro queda alerta ("register it with deskops repo register").
- `init` añade un link `deskops` a la fuente del paquete; no se usa para ubicar por sufijo (no cuelga de la carpeta del ecosistema), pero sí cuenta como raíz si la ruta existe aquí.
- Rutas de graph_ui/Chatbot_Infra (no son links) quedarán alerta en los desks reales.
