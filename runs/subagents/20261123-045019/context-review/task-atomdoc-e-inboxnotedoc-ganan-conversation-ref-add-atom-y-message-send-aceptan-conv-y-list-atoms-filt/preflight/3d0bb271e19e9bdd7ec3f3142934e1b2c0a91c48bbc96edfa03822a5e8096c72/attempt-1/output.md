## REFORMULACION
Encargo: implementar en el repo `deskops` el campo `conversation_ref` en `AtomDoc` e `InboxNoteDoc`, aceptar `--conv` en `add atom` y `message send`, filtrar `list atoms --conv`, y rechazar duplicados en `add atom`. Resultado: cuatro tests nuevos pasan, goldens actualizados, modelos actualizados en `.sldb`, y sin errores nuevos en `doctor` ni `stores check`. Límites: no crear `add agreement` ni migrar atoms antiguos con la referencia en `provenance`; incluye modelos, CLI, goldens, store, tests, suite completa y commit con `Task-Id`.

## AMBIGUEDADES
1. “los goldens de contrato y de ayuda” — no identifica rutas ni nombres; obligaría a inventar qué ficheros actualizar.
2. “sldb models update de los dos modelos en el store del desk” y “en .sldb” — no aclara el comando exacto, root ni formato; obligaría a inventar invocación.
3. “un --conv que ya tiene otro atom” — no define si compara ref exacta, hilo, prefijo `<hilo>/`, ni si excluye el propio atom; obligaría a inventar semántica.
4. “avisa en stderr … y no crea un duplicado” — no precisa formato exacto del mensaje ni si el aviso precede o sustituye otros errores; obligaría a inventar salida contractual.
5. “<hilo>/<id de mensaje> o solo <hilo>” y ejemplo `"#acuerdos-sldb1/1234"` — no aclara si `#` forma parte canónica ni validación; obligaría a inventar normalización.
6. “vacío no se escribe” — no define si vacío significa `None`, `""` o whitespace; obligaría a inventar tratamiento.
7. `message send --conv` no menciona duplicados ni validación; obligaría a inventar comportamiento.
8. No se especifica comportamiento de `list atoms --conv` con refs antiguas en `provenance`; obligaría a inventar compatibilidad.

## DRY-RUN
Lecturas: modelos, comandos, tests y goldens citados. Cambios previstos: añadir campo opcional a ambos modelos; añadir opción `--conv` a `add atom` y `message send`; persistir solo si no está vacío; implementar filtro por igualdad o prefijo `<hilo>/`; detectar duplicado y salir 1; actualizar JSON, goldens, ayuda y snapshots; actualizar modelos en `.sldb`. Dependencias: CLI existente, serialización/modelos, fixtures de tests, store. Validaciones futuras: ejecutar los cuatro tests, snapshot de contrato, suite `-n 4`, `doctor`, `stores check` y commit con trailer.

## FUTURO
Un ejecutor implementa y ejecuta validaciones; otro nodo o un humano decide rutas de goldens, semántica exacta de duplicados, normalización de `--conv` y comando de actualización del store.
