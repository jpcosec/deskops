# Result summary

run_id: run-deskops-t-2af89ce8b87d
task: task-deskops-dispatch-lanza-y-recoge-por-scion-al-ejecutor-y-al-tester-de-una-tarea-sin-coordinador-agent
veredicto: PASS

## Evidencia principal

- tests/test_dispatch.py (nuevo): 10 passed. Cubre start executor, start tester con run_dir -testing,
  ocupado -> 3 sin start, intento 2 y tercero -> 5, reap por los tres motivos + vivo -> 4, y falta de
  dispatch -> 2 en ambos subcomandos.
- Guardianes CLI: test_cli_grammar.py + test_command_registry.py 5 passed; test_cli.py -k
  help_uses_deskops_name 1 passed; test_output_goldens.py -k help 1 passed.
- Sin regresiones: test_scion_runtime.py 40 passed, test_packaging.py 6 passed, test_config.py +
  test_supervise.py 12 passed. test_queue.py 14 passed tras corregir solo el entorno del subproceso de
  test (el fallo inicial era ModuleNotFoundError: sldb.store porque ese test lanza python -m deskops con
  PYTHONPATH solo al repo y HOME redirigido; no toca dispatch). Workaround temporal eliminado.
- Prueba manual real con desk desechable creado por `deskops init` bajo /dev/shm, roles/tarea creados por
  el CLI, config dispatch y un scion falso propio primero en PATH (registra argv y responde list con JSON;
  nunca se ejecutó el scion real):
  - start executor: exit 0, argv list -> templates sync -> start con nombre/tipo/proyecto/workspace/
    etiquetas/--config, frase con ruta absoluta de prompt.md; template, RunDoc y prompt.md creados.
  - start tester: exit 0, nombre sin -testing, run_dir exec-<nombre>-testing, sin --config.
  - agente running: `ocupado: busy-agent`, exit 3, sin start.
  - intento 2 -> nombre -a2; tercer intento -> `sin intentos: <task> executor`, exit 5.
  - reap: phase:stopped, activity:blocked y result-summary detenidos+borrados; vivo conservado; exit 4.
    Solo terminados -> exit 0.
  - sin campo dispatch: ambos subcomandos y reap -> mensaje exacto y exit 2, sin llamar a scion.
  - Desk desechable borrado al terminar.

## Revisión

- Todas las llamadas a scion pasan por `_scion` (subprocess.run).
- Tests con scion falso en PATH; sin mocks ni monkeypatch sobre funciones del módulo.
- Sin cambios del tester, sin commits, sin editar desk/ ni .sldb/ del repo. Cambios ajenos ignorados.

## Veredicto

PASS en todos los puntos de Validation y Done When.
