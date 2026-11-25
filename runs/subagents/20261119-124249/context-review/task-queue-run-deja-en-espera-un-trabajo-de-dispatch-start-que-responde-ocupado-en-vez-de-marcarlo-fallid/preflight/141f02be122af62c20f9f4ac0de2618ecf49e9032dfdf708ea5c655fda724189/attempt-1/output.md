## REFORMULACION

Encargo: en el repo deskops, hacer que `queue run` no marque `failed` un trabajo cuyo comando de dispatch sale con código 3 ("ocupado"), sino que lo deje `pending` para la próxima corrida, imprimiendo "en espera: <id> ocupado" y continuando con el resto (o deteniéndose sin fallar), análogo a los gates de memoria; cualquier otro código distinto de 0 sigue siendo fallo. Resultado: `queue.py` con un campo opcional `retry_exit_codes` por tipo de trabajo en `queue_jobs` (lista de enteros, default vacío), configurado con `[3]` en los desks dispatch-executor y dispatch-tester, más tests, `docs/operator-manual.md` (Host queue) y CHANGELOG. Límites: no se cambian los códigos de dispatch.

## AMBIGUEDADES

1. "sigue con el resto (o se detiene sin fallar)" — dos comportamientos incompatibles; obliga a inventar cuál implementar.
2. "igual que con los gates de memoria" — sin contexto del comportamiento de esos gates; obliga a inventar su semántica.
3. "en la configuración de los desks dispatch-executor y dispatch-tester con [3]" frente a "el integrador agrega retry_exit_codes a los config.json de deskops, sldb e IR" — no queda claro dónde se define ni qué desks/work types llevan `[3]`; obliga a inventar el mapeo.
4. "sin nota unclear" — no define formato ni criterio exacto de la nota; obliga a inventar qué se comprueba.
5. "queue run --all corrió..." frente a "queue run lo deja en pending" — no aclara si el comportamiento aplica a `--all`, a un id o a ambos; obliga a inventar el alcance del flag.

## DRY-RUN

Lecturas: `deskops/queue.py` (flujo de `queue run`, manejo actual de `failed`/nota y de gates), esquema/definición de `queue_jobs`, `tests/test_queue.py` y configs de los desks citados. Cambios previstos: p1 test nuevo (exit 3 + `retry_exit_codes [3]` → pending sin nota; otro código → failed) que falla antes; p2 rama en `queue.py` que consulta `retry_exit_codes` y emite "en espera"; p3 docs y CHANGELOG; p4 commit con rutas y Task-Id. Dependencias: existencia del campo en `queue_jobs` y su lectura desde config; que el integrador añada la config tras integrar. Validaciones futuras: `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_queue.py` y suite completa de deskops.

## FUTURO

El integrador agrega `retry_exit_codes` a los `config.json` de deskops, sldb e IR después de integrar. Un humano debe decidir entre "seguir" o "detenerse sin fallar" y resolver el mapeo de desks antes de implementar. La integración valida la suite completa.
