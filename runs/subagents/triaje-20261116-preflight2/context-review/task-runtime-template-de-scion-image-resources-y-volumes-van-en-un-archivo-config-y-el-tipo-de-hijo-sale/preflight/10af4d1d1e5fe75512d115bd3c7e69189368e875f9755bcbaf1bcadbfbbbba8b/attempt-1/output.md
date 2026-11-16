REFORMULACION
Nodo ejecutable (`task.code`), no agregado. Propósito: separar de `scion-agent.yaml` las claves de entorno de scion y escribirlas en `scion-env.yaml`, usando `--config` al lanzar. Resultado: `runtime template` genera ambos archivos, `scion_start_argv` añade `--config`, el `agents.md` del coordinador usa ese archivo y los flags `--executor-role`/`--tester-role` fijan rol y `--type` de los hijos. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: no tocar el repo scion, no lanzar scion, no cambiar la imagen ni el engine de review.

AMBIGUEDADES
1. “con `--executor-role ir-executor` el agents.md generado nombra ir-executor”: el flag parece recibir el id sin `role-`, mientras el default es `role-deskops-executor`; no se aclara si acepta ambos formatos ni si elimina `role-` solo cuando existe. Obligaría a inventar normalización o validación.
2. “sus goldens de ayuda”: no se nombran archivos concretos; obligaría a inventar cuáles actualizar si no se localizan por el test.
3. “scion-env.yaml se escribe en el mismo directorio de salida que scion-agent.yaml”: no se define cómo se obtiene ese directorio ni qué hacer si no existe; obligaría a inventar creación o error.
4. “alrededor de las lineas 84-135, 266-300, 440-463 y 588-607”: son rangos aproximados; obligaría a inventar límites exactos si el código difiere.

DRY-RUN
Lecturas: task doc, referencia de inbox, `deskops/runtime/scion.py`, `deskops/cli/commands/runtime.py`, `tests/test_scion_runtime.py`, `tests/test_runtime_profiles.py`, `tests/test_output_goldens.py` y goldens de ayuda. Cambios previstos: extraer image/resources/volumes/kubernetes/telemetry presentes; escribir `scion-env.yaml` junto al template y sobrescribirlo; pasar su ruta a `scion_start_argv`; añadir `--config` y roles al `agents.md`; definir flags con defaults. Dependencias: generador actual, constructor de argv, goldens y pytest. Validaciones futuras: los tres pytest específicos, suite completa con `-n 4`, y comparación de fallas en worktree limpio de `origin/main`. Sin ejecutar.

FUTURO
Otro nodo ejecutará los cambios, tests y commit. Un humano decidirá la aceptación de fallas preexistentes y la revisión final.
