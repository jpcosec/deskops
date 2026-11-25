REFORMULACION

Propósito: corregir dispatch start para que el commit del RunDoc incluya también el run.md del run dir del agente vivo. Resultado: `_run_store_paths` añade ese archivo si existe (incluida la variante `-testing` de testers) y `_commit_run_store` lo commitea con pathspec; así el gate de store de integrate acepta commits con agentes vivos y el closeout posterior no se rompe. Repo: deskops. Límites: solo `deskops/dispatch.py` (`_run_store_paths`, `_commit_run_store`), `tests/test_dispatch.py` y CHANGELOG; queda fuera el gate de store de integrate. Es un nodo ejecutable `task.code`, no un agregado.

AMBIGUEDADES

1. Cita: “runs/subagents/exec-<nombre>/run.md, y -testing para testers, el mismo de _run_dir_for”. Falta la definición de `_run_dir_for`; obligaría a inventar si `-testing` sustituye o se añade a `<nombre>` y de dónde sale `<nombre>`.
2. Cita: “después de dispatch start (simulado)”. No se especifica cómo simularlo; obligaría a inventar fixture, mock o ejecución real.
3. Cita: “el mismo chequeo que corre integrate”. No se nombra la función o módulo del gate; obligaría a inventar su localización o a replicar el chequeo.
4. Cita: “si existe”. No aclara si debe probarse el caso ausente; obligaría a inventar cobertura adicional no pedida.

DRY-RUN

Sin ejecutar: leería `deskops/dispatch.py` (funciones citadas y línea 186), `tests/test_dispatch.py`, `tests/test_integrate.py`, CHANGELOG y el chequeo de store de integrate. Cambios previstos: en `_run_store_paths`, calcular el run.md con la misma lógica que `_run_dir_for` y añadirlo solo si existe; en `_commit_run_store`, incluirlo en el pathspec del commit `run: <agente>`. Añadiría tests: el commit tras dispatch start contiene shard y run.md; el chequeo de store pasa; y el closeout no falla por run.md ya trackeado. Dependencias: helpers existentes, fixtures de git y locale es_ES. Validación futura: ejecutar el comando pytest indicado y, según p4, con LANG/LC_ALL/LANGUAGE es_ES.UTF-8; después CHANGELOG y commit con trailer `Task-Id`.

FUTURO

El nodo de implementación producirá el parche, tests y commit. El nodo de integrate ejecutará el gate de store y la suite; el closeout commiteará el run dir completo. Un humano decidirá aceptación o cierre si los tests y el gate pasan.
