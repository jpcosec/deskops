## REFORMULACION

**Propósito:** desbloquear los integrate de deskops actualizando el snapshot de contratos de modelo tras un cambio solo de descripción en `RuleDoc`. **Resultado:** `tests/fixtures/model_contract_hashes.json` con el hash nuevo de `RuleDoc`, calculado por la función del propio test; `CHANGELOG`; y un commit que explique que es cambio solo de descripción, sin migración de stores. **Repo:** deskops, en el worktree que entregue dispatch; se inspecciona el repo sldb en `/mnt/ssd/herramientas/sldb`. **Límites:** tocar solo la entrada `RuleDoc` del fixture y `CHANGELOG`; no tocar el test, otros hashes ni sldb. Es una tarea ejecutable, no un agregado.

## AMBIGUEDADES

1. «sldb stores check sobre el store de deskops y el de sldb»: no da rutas, identificadores ni sintaxis de los stores; obligaría a inventar comandos y ubicaciones.
2. «anotar la salida en el run dir»: no define qué run dir; obligaría a inventar la ruta de salida.
3. «commit desde el worktree que dispatch te da»: no indica ruta, rama ni forma de obtenerlo; obligaría a inventar el worktree.
4. «CHANGELOG»: no especifica archivo, sección ni formato; obligaría a inventar dónde y cómo documentarlo.
5. «Si el test permite marcar cambios solo de descripción sin migración [...] seguir ese camino»: no define el criterio ni el camino alternativo si no lo permite; obligaría a inventar el fallback.
6. «pytest ... contra el sldb de `/mnt/ssd/herramientas/sldb`»: no dice cómo apuntar el test a ese sldb (env, `PYTHONPATH` u otro); obligaría a inventar el mecanismo.

## DRY-RUN

**Lecturas:** TaskDoc, `tests/test_model_contract_snapshot.py` (incluido `FIXTURE_UPDATE`), fixture actual, `CHANGELOG`, `git -C /mnt/ssd/herramientas/sldb show 22cfafb2 -- src/sldb/models/rule_doc.py`, configuración de stores. **Cambios previstos:** solo la entrada `RuleDoc` del fixture, con hash regenerado por la función del test; `CHANGELOG`; commit con trailer `Task-Id`. **Dependencias:** worktree de dispatch, sldb con 22cfafb2, stores accesibles, git y pytest. **Validaciones futuras:** `sldb stores check` en ambos stores con salida en run dir; `pytest` indicado; `git diff` limitado a fixture y CHANGELOG. Sin ejecutar.

## FUTURO

Dispatch entrega worktree y `Task-Id`; CI/integración ejecuta la suite completa; un revisor humano confirma que el cambio es solo de descripción y que no requiere migración.
