## REFORMULACION
Propósito: evitar que ejecutor y tester validen entregas que la suite completa de integrate rechaza por gates estructurales. Resultado: `desk/config.json`, bloque `dispatch`, admite `quick_gates` (argv) opcional; si existe, `dispatch start` incluye en el `prompt.md` del ejecutor la exigencia de rc 0 antes del commit y en el del tester un FALLA si el rc no es 0; sin el campo, el prompt no cambia. Repo: `deskops` (config, dispatch, tests, docs, CHANGELOG). Límites: no tocar configs reales de desks; el integrador declarará después `quick_gates` en sldb (`bash tools/check.sh --fast`) y en deskops; commit sin push.

## AMBIGUEDADES
1. «quick_gates (argv)» no define esquema: ¿lista de argv, cadena de shell, uno o varios comandos? Obliga a inventar el tipo y la validación en `DispatchConfig`.
2. «el prompt.md que escribe dispatch start» frente a «los textos de prompt.md por rol en deskops/dispatch.py»: no se indica la ruta exacta ni si hay plantillas separadas. Obliga a inventar ubicación y mecanismo de composición.
3. «Los quick_gates corren con el python del venv del contenedor (/tmp/ws-venv…)»: no aclara si se antepone el intérprete, se sustituye en el argv, ni cwd/env. Obliga a inventar la invocación.
4. «un FALLA si da distinto de 0»: no fija el texto exacto ni el formato del veredicto del tester. Obliga a inventar redacción y criterio de inserción.
5. El cold-bundle dice incluir «las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra», pero el TaskDoc trae `pills: []`, `atoms: []`, `files: []`. No hay ambigüedad del encargo, sino ausencia de material adicional; no obliga a inventar contenido, pero impide verificar detalles.
6. «la suite completa de deskops» no nombra comando; la validación solo cita `tests/test_dispatch.py`. Obliga a inferir el comando global.

## DRY-RUN
Lecturas: `deskops/config.py` (`DispatchConfig`), `deskops/dispatch.py` (prompts por rol), `tests/test_dispatch.py`, `docs/operator-manual.md`, `CHANGELOG`. Cambios previstos: test previo fallido con y sin `quick_gates`; campo opcional y armado condicional de prompts; documentación y entrada de CHANGELOG; commit con rutas y `Task-Id`. Dependencias: python del venv `/tmp/ws-venv`, flujo `dispatch start`. Validaciones futuras: el pytest indicado y la suite completa en integrate.

## FUTURO
El integrador declarará `quick_gates` en sldb y deskops; los desks reales decidirán si lo declaran. Un humano revisará y hará merge/push.
