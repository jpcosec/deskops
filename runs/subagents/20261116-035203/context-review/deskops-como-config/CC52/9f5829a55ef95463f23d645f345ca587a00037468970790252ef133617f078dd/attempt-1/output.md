## REFORMULACION
Propósito: verificación final (P5) de que la migración a configuración deja deskops y los 6 desks verdes y el Board rápido. Resultado: registro en la Validation del TaskDoc y sección de verificación en `docs/config-vs-code.md` con tabla de los 6 desks y tiempos frío/caliente. Repo dueño: deskops. Límites: no cambia código salvo arreglos que la verificación delate; no corre las suites completas (las corre el supervisor, regla 3); no escribe en sldb; no toca P4. Depende de CC30–CC38.

## AMBIGUEDADES
1. Cita: "sin cambio de código salvo arreglos que la verificación delate (cada arreglo es un commit con su test)" frente a output_scope "tests/ (solo arreglos), docs/config-vs-code.md (sección verificación)". Si el arreglo cae en `deskops/operations.py` o similar, ¿está permitido? Obliga a inventar si los arreglos de código pertenecen al nodo o se derivan.
2. Cita: "deskops desk update --apply (dry-run primero, resultado en la Validation)". No dice si se aplica sobre los desks reales o copias; aplicarlo escribe en seis repos ajenos al output_scope. Obliga a inventar el destino y si esas escrituras están permitidas.
3. Cita: "3 corridas en frío (caché del usuario borrada) y 3 en caliente, mediana, en robocop2." No fija qué caché ni si se borra antes de cada corrida fría; obliga a inventar el procedimiento de medición reproducible.

## DRY-RUN
Lecturas: `dag.yaml` (CC52 y aristas), `alcance.md` (reglas 3 y 6), esta guía, la versión integrada de CC30–CC38, `docs/config-vs-code.md` y CHANGELOG. Cambios previstos: ninguno de código; escritura de la sección de verificación en `docs/config-vs-code.md` y de la tabla en la Validation; sobre los 6 desks: dry-run y luego apply, doctor, view board, `sldb stores check` y `rules check`; benchmark 3+3 con mediana. Dependencias: CC30–CC38 integrados, sldb pinneado y robocop2. Validaciones futuras: mediana caliente < 1 s, fría registrada, doctor/view board/stores/rules por desk, suite del supervisor registrada, y grep de arreglos con test. Sin ejecutar.

## FUTURO
El supervisor corre las suites completas de deskops y sldb sobre el resultado integrado y entrega el veredicto que CC52 solo registra. Un humano o el coordinador decide si un arreglo delatado fuera del output_scope se promueve como nodo aparte. La versión integrada y el pin de sldb dependen de que CC30–CC38 hayan cerrado.
