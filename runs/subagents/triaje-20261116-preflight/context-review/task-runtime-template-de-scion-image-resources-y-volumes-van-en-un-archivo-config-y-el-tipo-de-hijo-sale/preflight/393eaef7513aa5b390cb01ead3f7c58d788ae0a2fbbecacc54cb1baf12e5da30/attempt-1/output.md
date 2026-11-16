REFORMULACION
Nodo ejecutable `task.code`, no agregado. Propósito: corregir `deskops runtime template` para que scion reciba la configuración de entorno mediante un archivo `--config` y permitir configurar roles y `--type` de hijos. Resultado: cambios en `deskops/runtime/scion.py` y `deskops/cli/commands/runtime.py`; `scion-env.yaml` contiene image, resources, volumes, kubernetes y telemetry; `scion-agent.yaml` deja de contenerlos; `scion_start_argv` añade `--config <ruta>`; el agents.md del coordinador usa ese `--config` y los roles recibidos; flags `--executor-role` y `--tester-role`; tests y goldens de ayuda actualizados. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: no modificar el repo scion, no lanzar scion, no tocar la imagen del contenedor ni el engine de review.

AMBIGUEDADES
1. “scion-env.yaml, junto al template”: no define directorio exacto, ruta relativa, política de sobrescritura ni si se genera siempre. Obliga a inventar la ubicación y el ciclo de vida.
2. “el agents.md del coordinador usa ese --config al lanzar hijos”: no indica qué archivo o plantilla contiene ese agents.md ni si lo genera `runtime template`. Obliga a inventar ubicación y mecanismo de generación.
3. “Los ids de rol y el --type del ejecutor y del tester salen de dos flags nuevos… (--executor-role y --tester-role, por defecto los de deskops)”: no aclara cómo se deriva `--type` desde el rol; los defaults citados son `role-deskops-executor`/`role-deskops-tester`, pero los tipos son `deskops-executor`/`deskops-tester`. Obliga a inventar el mapeo, el prefijo y si dos flags cubren ambos valores.
4. “image, resources, volumes, kubernetes y telemetry”: no define el esquema YAML exacto ni si se trasladan únicamente esas claves. Obliga a inventar la estructura de `scion-env.yaml`.

DRY-RUN
Lecturas: zonas citadas de `scion.py`, `runtime.py`, tests de scion/runtime/goldens y ayuda de `runtime template`. Cambios previstos: separar claves de entorno, escribir `scion-env.yaml`, añadir `--config` al argv, ajustar plantilla de agents.md, añadir flags y tests. Dependencias: contrato CLI actual, goldens, pytest y `.venv`. Validaciones futuras: los cuatro comandos pytest indicados, incluida la suite completa. Sin ejecutar.

FUTURO
Un ejecutor futuro implementará y validará los cambios. Un humano deberá resolver las ambigüedades previas y decidir la aceptación del baseline `main` si hay fallas preexistentes.
