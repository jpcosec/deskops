REFORMULACION
PF1 es un nodo agregado (`node_role: aggregate`) del plan deskops-como-config; no se ejecuta: termina cuando terminan CC30 y CC36. Propósito: agrupar la base que no espera capacidades nuevas de reglas. Resultado: `operations.py` como fachada sin lógica y sin specs YAML duplicados (CC30), y plantillas del desk como datos escritos por el scaffold de sldb (CC36, tras GD26). Repo dueño: deskops. Límites: invariante de formato del desk y gramática del CLI; no escribe en sldb; no suple reglas con Python; no toca P4. Aceptación conjunta: grep de `spec/artifacts` y `spec/fields` vacío; `workspace.py` sin strings de plantilla; `deskops init` temporal con mismo árbol y bytes.

AMBIGUEDADES
1. "workspace.py sin strings de plantilla": PF1 no define qué cuenta como plantilla y CC36 solo exige greps de `_write_if_missing`, `scaffold_desk`, `guess_model_for_path` y `"_template("`. Validar el agregado obligaría a inventar el criterio; se resuelve leyendo la aceptación como esos greps.

DRY-RUN
No ejecutable. Hipotéticamente: CC30 lee `operations.py`, `services/`, `specs/`, `model_introspection.py`; mueve helpers a `doc_access.py`, deja la fachada, unifica duplicados y borra specs; depende de G_P0 y G_GATES_FROZEN; valida goldens, greps y tests. Transfiere a CC36 una base sin YAML duplicados y modelos con `__artifact__`. CC36, ya con CC30, captura golden de `init`, mueve plantillas a `data/templates/`, declara `desk_declaration.yaml`, usa `scaffold_store` (GD26), borra `scaffold_desk`/`_write_if_missing`; valida sha256, idempotencia y goldens de ayuda. Validación conjunta: ambas aceptaciones, greps del agregado, `init` y segunda corrida de `desk update --apply` sin cambios; el supervisor corre suite completa y `doctor`/`view board` en los 6 desks.

FUTURO
El agregado nunca se promueve: se promueven CC30 y CC36 por separado. sldb debe cerrar GD26 y deskops pinnear versión. El supervisor corre la suite integrada; CC34 retirará los alias de graph_ui que CC30 conserva; CC31 reducirá `task_lifecycle.yaml`.
