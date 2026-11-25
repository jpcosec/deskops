REFORMULACION
Propósito: que `deskops init` y `desk update --apply` instalen el merge driver de sldb en el repo git del desk, usando `install_merge_driver`, de forma idempotente, sin efecto fuera de git y avisando por stderr si git falla, para que doctor no muestre `stores/merge_driver_missing` y el golden no cambie. Resultado: cambios en bootstrap y en el camino de update, tests, docs y CHANGELOG. Repo: deskops. Límites: sldb queda fuera; si `install_merge_driver` no se puede importar, se omite sin error.

AMBIGUEDADES
1. “deja .gitattributes con las tres líneas merge=sldb”: no se enumeran las tres líneas ni sus patrones; obliga a inventar globs y formato exacto.
2. “si git falla avisa por stderr sin romper”: no se define mensaje, nivel ni comportamiento de salida; obliga a inventar el contrato de aviso.
3. “cuando el desk es un repo git”: no se fija el criterio de detección (`rev-parse`, `.git`, worktree); obliga a inventar casos límite.
4. “desk.py:200 update y lo que llame”: la cadena de llamada no se nombra; obliga a inventar el punto de inserción.
5. “commit con rutas nombradas y Task-Id”: no se especifica formato; obliga a inventar la convención.

DRY-RUN
Lecturas: `deskops/bootstrap.py`; `deskops/cli/commands/desk.py` (update); `tests/test_lifecycle_seed_drift.py` y goldens; `docs/operator-manual.md`; `CHANGELOG`; API `sldb.api.stores.merge_driver_install`. Cambios previstos: helper que detecte repo git e invoque `install_merge_driver` sobre el store; llamada en `init_local_store` y en `update --apply`; tests de init, update y no-git; docs y CHANGELOG. Dependencias: sldb con `install_merge_driver`, binario git y repos temporales. Validaciones futuras: el pytest indicado, la suite completa por integrate, comprobar `.gitattributes` y `merge.sldb.driver`, y el no-op fuera de git.

FUTURO
La disponibilidad de un sldb con el alert y su versión la aporta el entorno u otro nodo; integrate ejecuta la suite completa; un humano decide commit/advance y valida el mensaje de aviso si se considera contrato.
