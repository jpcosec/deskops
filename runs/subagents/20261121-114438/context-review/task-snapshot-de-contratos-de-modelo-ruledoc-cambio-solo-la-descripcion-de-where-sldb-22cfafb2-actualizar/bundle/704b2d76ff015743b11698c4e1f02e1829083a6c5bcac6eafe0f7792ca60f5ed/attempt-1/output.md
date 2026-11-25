## REFORMULACION

Propósito: actualizar el snapshot de contratos de modelo de deskops tras el cambio en sldb 22cfafb2, que solo modificó la `description` del campo `where` de `RuleDoc`. Resultado: `tests/fixtures/model_contract_hashes.json` con el hash nuevo de `RuleDoc`, recalculado con la función del propio test; evidencia de `sldb stores check` en el run dir; entrada en CHANGELOG; commit con trailer `Task-Id`. Repo: deskops (`/mnt/ssd/proyectos/SLDB_1/deskops`), consultando sldb (`/mnt/ssd/herramientas/sldb`). Límites: dentro, solo la entrada `RuleDoc` del fixture y CHANGELOG; fuera, el test, otros hashes y sldb. Es una tarea `task.code` ejecutable, no un agregado.

## AMBIGUEDADES

1. “sldb stores check sobre el store de deskops y el de sldb”: no se dan rutas ni identificadores de store; obligaría a inventarlos.
2. “anotar la salida en el run dir”: no se especifica qué run dir; obligaría a inventar la ruta.
3. “CHANGELOG”: no se indica archivo, sección ni formato; obligaría a inventar ubicación y estilo de entrada.
4. “no da hallazgos nuevos de RuleDoc”: “nuevos” exige una línea base no definida; obligaría a inventar el criterio de comparación.
5. “commit desde el worktree que dispatch te da”: el bundle no incluye esa ruta; obligaría a inventarla o a esperar a dispatch.

## DRY-RUN

Un ejecutor futuro leería el TaskDoc, `tests/test_model_contract_snapshot.py` —en especial `FIXTURE_UPDATE`—, el fixture, CHANGELOG y la salida de `git show 22cfafb2 -- src/sldb/models/rule_doc.py`. Ejecutaría `sldb stores check` sobre ambos stores y guardaría la salida en el run dir. Actualizaría únicamente el hash de `RuleDoc` mediante el procedimiento indicado por el test, añadiría la entrada de CHANGELOG y no tocaría test, otros hashes ni sldb. Dependencias: commit y CLI de sldb disponibles, stores accesibles, worktree y run dir proporcionados por dispatch. Validaciones futuras: ejecutar el pytest indicado, revisar que el diff solo afecte `RuleDoc`, confirmar ausencia de hallazgos nuevos y verificar el commit con `Task-Id`.

## FUTURO

Dispatch entrega el worktree; si `stores check` muestra hallazgos de `RuleDoc`, un humano decide si corresponde migrar o escalar; CI y revisión validan el commit.
