REFORMULACION

Nodo ejecutable (`task.code`), no agregado. Propósito: evitar que ejecutor y tester de dispatch aprueben entregas que la suite completa de integrate rechaza por gates estructurales, porque solo corren tests de archivos tocados. Resultado: `DispatchConfig` con `quick_gates` opcional; el `prompt.md` del executor exige rc 0 antes del commit y el del tester marca FALLA si rc≠0, solo si el desk lo declara; tests, docs y CHANGELOG; commit con rutas nombradas y Task-Id, sin push. Repo: deskops (`deskops/config.py`, `deskops/dispatch.py`, `tests/test_dispatch.py`, `docs/operator-manual.md`). Límites: no tocar configs reales; el integrador declarará `quick_gates` después en sldb y deskops.

AMBIGUEDADES

1. "un campo opcional quick_gates (argv)": no define tipo ni forma JSON; obliga a inventar lista de cadenas frente a cadena, anidamiento exacto en el bloque `dispatch` y ejemplo.
2. "contienen el comando y la regla" frente a "quick_gates": singular/plural contradictorio; obliga a decidir uno o varios comandos y cómo representarlos.
3. "Los quick_gates corren con el python del venv del contenedor (/tmp/ws-venv...)": no aclara si el argv ya incluye el intérprete o si dispatch lo antepone; obliga a inventar la invocación exacta.
4. "el prompt.md ... exige correrlo con rc 0": no distingue instrucción textual de verificación en runtime; obliga a decidir si dispatch comprueba el rc o solo redacta.
5. "(un FALLA si da distinto de 0)": no fija plantilla ni literalidad del veredicto; obliga a inventar la redacción exacta.

DRY-RUN

Lecturas: `deskops/config.py`, `deskops/dispatch.py`, `tests/test_dispatch.py`, `docs/operator-manual.md`, `CHANGELOG`; identificar serialización de config y armado de prompt por rol. Cambios previstos: test primero con desk de prueba con y sin `quick_gates`; campo opcional en `DispatchConfig`; bloque condicional en prompts de executor y tester; docs y CHANGELOG; commit con rutas y Task-Id. Dependencias: `/tmp/ws-venv`, pytest y estructuras existentes de config/prompt. Validaciones futuras: el pytest indicado, luego la suite completa vía integrate; comprobar que sin campo el prompt no cambia. Nada ejecutado.

FUTURO

El integrador declarará `quick_gates` en sldb (`bash tools/check.sh --fast`) y en deskops; integrate ejecutará la suite completa; un humano revisará y fusionará el commit.
