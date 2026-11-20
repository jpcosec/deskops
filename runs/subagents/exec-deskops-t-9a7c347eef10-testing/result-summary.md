PASA

# Resultado de testing — dispatch start sincroniza el template de scion por su ruta

## Entrega verificada

- Commit del ejecutor: `0172198901f0cc92f7255a9887cbc258f837fda5` — *dispatch start syncs the scion template by path*.
- Trailer: `Task-Id: task-dispatch-start-sincroniza-el-template-de-scion-por-su-ruta-no-por-su-nombre-para-que-un-repo-con-su`.
- Archivos del commit:
  - `deskops/dispatch.py`: el `scion templates sync` de `start` pasa `str(target.resolve())` en lugar de `role_name`.
  - `tests/test_dispatch.py`: actualiza las dos aserciones existentes y agrega `test_start_syncs_the_template_by_path_in_a_desk_with_its_own_scion`, que arma un root con `.scion/settings.yaml` propio, verifica que sync recibe la ruta absoluta y que `scion start` sigue usando `--type <nombre>`.
  - `CHANGELOG.md`: entrada en Fixed.
- `git show --check 01721989` no reporta problemas; el diff es acotado y no toca archivos ajenos a la tarea.

## Tests ejecutados

Entorno: `python` no está en PATH y el `.venv` del workspace apunta a un Python 3.12 ausente. Usé `/workspace/sldb/.venv/bin/python` (Python 3.13.18, pytest 9.1.1), desde `/workspace/deskops`.

1. Test nuevo, solo:

       TMPDIR=/tmp /workspace/sldb/.venv/bin/python -m pytest -q -p no:cacheprovider \
         'tests/test_dispatch.py::test_start_syncs_the_template_by_path_in_a_desk_with_its_own_scion'
       -> 1 passed, 1 warning (16.61 s), rc 0

2. Validación de la tarea, archivo completo:

       TMPDIR=/tmp /workspace/sldb/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_dispatch.py
       -> 33 passed, 1 warning (306.91 s), rc 0

No corrí la suite completa (la corre integrate en el host).

## Discriminación del test nuevo

Creé un worktree temporal en `01721989^` (commit padre), copié allí el `tests/test_dispatch.py` nuevo y corrí solo el test nuevo: **falla** porque el argv de sync era `templates sync disp-executor` y no la ruta absoluta. Con `01721989` pasa. El test cubre la regresión pedida.

## Verificación contra el Goal

- `sync` recibe la ruta absoluta del directorio que `materialize_scion_template` acaba de escribir en `target`; deja de resolver el nombre en el grove local del desk.
- El caso con `.scion/settings.yaml` propio (el escenario de IR) está cubierto por el test nuevo.
- `scion start` no cambió: sigue con `--type <role_name>`, tal como resolvió la review de bundle aceptada (el hub del proyecto se consulta antes que el grove local).
- `CHANGELOG.md` documenta el cambio y el alcance de `start`.

## Observaciones

No relancé el dispatch real de la tarea de IR: la review de bundle aceptada establece que la verificación end-to-end la hace el integrador y que un fallo posterior de `scion start` iría en una tarea nueva. El binario `scion` instalado en este contenedor es `scion dev (5601064e)`, anterior a v0.2.21; la review aceptada verificó el contrato de ruta con v0.2.21. Esto no afecta el veredicto sobre el cambio de deskops, que queda cubierto por los tests.

## Conclusión

PASA: el test nuevo pasa, `tests/test_dispatch.py` pasa completo (33/33), el test discrimina contra el commit padre y el cambio implementa exactamente el sync por ruta absoluta solicitado.
