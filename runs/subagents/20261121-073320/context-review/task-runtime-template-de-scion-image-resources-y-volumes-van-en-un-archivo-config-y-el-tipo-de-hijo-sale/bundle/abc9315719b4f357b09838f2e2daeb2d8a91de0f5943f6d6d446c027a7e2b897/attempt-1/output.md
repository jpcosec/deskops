REFORMULACION

El encargo pide modificar el materializador de plantillas Scion en `deskops/runtime/scion.py` y `deskops/cli/commands/runtime.py`: image, resources, volumes, kubernetes y telemetry deben dejar de escribirse en `scion-agent.yaml` y pasar a un `scion-env.yaml` hermano, sobrescrito en cada corrida; `scion_start_argv` debe añadir `--config <ruta>`; el `agents.md` del coordinador debe usar ese `--config`; y se añaden `--executor-role`/`--tester-role` (defaults `role-deskops-executor`/`role-deskops-tester`), derivando el `--type` del hijo al quitar el prefijo `role-`. Resultado observable: pasan los tests de scion, runtime profiles y goldens de ayuda, y la suite completa no añade fallas nuevas. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: no tocar el repo scion, no lanzar scion, no cambiar la imagen ni el engine de review.

AMBIGUEDADES

1. «reciben un id de RoleDoc completo (con prefijo role-)» frente a «con --executor-role ir-executor el agents.md generado nombra ir-executor»: ¿se exige o se tolera el prefijo? Obliga a inventar validación/normalización.
2. «scion_start_argv agrega --config <ruta de scion-env.yaml>»: la firma actual recibe `template: str`, no una ruta; obliga a inventar de dónde se deriva.
3. «el agents.md del coordinador usa ese --config»: no se da la forma literal ni el origen de la ruta en el texto generado; obliga a inventar el fragmento.
4. «solo image, resources, volumes, kubernetes y telemetry (las que esten presentes)»: el código actual solo emite `env`, `volumes` y `resources` desde `context`; no existen image, kubernetes ni telemetry; obliga a inventar su origen.
5. «sus goldens de ayuda»: no nombra el archivo golden concreto; obliga a inventar cuál actualizar.

DRY-RUN

Lecturas: `scion.py` (zonas 84-135, 266-300, 440-463, 588-607), `runtime.py`, `tests/test_scion_runtime.py` y los goldens de ayuda de runtime template. Cambios previstos: separar las claves de entorno del dict del template, escribir `scion-env.yaml` junto a `scion-agent.yaml`, pasar la ruta a `scion_start_argv` y añadir `--config`, actualizar la plantilla del coordinador, añadir los dos flags con defaults y ajustar tests/goldens. Dependencias: RoleDocs, RuntimeProfileDocs y parser CLI. Validaciones futuras: los tres pytest indicados y la suite completa, comparando fallas en worktree limpio de `origin/main`.

FUTURO

Un ejecutor implementará y correrá las validaciones; un humano decide las ambigüedades 1-4 (prefijo de rol, origen de image/kubernetes/telemetry y forma del `--config`) antes del despacho.
