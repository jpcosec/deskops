## REFORMULACION

CC35a es un nodo `delivery` de deskops, parte (1) de CC35. Encargo: sustituir todo uso de `doc_io.DocTransaction` por `sldb.api.transaction` (GD24), con `expected_source_hash` en updates; incluir `message send/ack` sin rollback manual; borrar `doc_io.py`. Resultado: grep vacío de `doc_io|DocTransaction`, rollback comprobable ante fallo inyectado en atoms merge, conflicto por hash viejo, goldens idénticos, tests verdes, `doctor` sin hallazgos nuevos en 6 desks, líneas antes/después y CHANGELOG. Límites: solo la superficie de transacción; no toca código de sldb, no sustituye reglas con Python, no deja dos caminos y conserva formato del desk y gramática del CLI. Depende de CC30, CC36 y CC38; `G_GD24` está satisfecho.

## AMBIGUEDADES

1. “revierte el atom, los referrers y el índice”. No se define qué es “el índice” ni cómo comprobarlo; obligaría a inventar si se refiere a un índice propio de átomos, a los shards de sldb o a otra estructura. La frase siguiente (“hash de archivos y sldb stores check iguales antes y después”) no lo nombra expresamente.

## DRY-RUN

Lecturas: guía, brief, alcance, decisiones, nodo CC35a y gate `G_GD24`. Cambios previstos, sin ejecutar: reemplazar llamadas en `operations.py`, `services/`, `message.py` y `runtime/scion.py`; añadir `expected_source_hash`; borrar `doc_io.py`; ajustar tests y CHANGELOG. Dependencias: CC30, CC36 y CC38 integrados; GD24 pinneado. Validaciones futuras: grep de aceptación, fallo inyectado en atoms merge, escritura con hash viejo, goldens de ayuda/salida, tests de archivos tocados, `doctor` en 6 desks, líneas antes/después; la suite completa queda al supervisor.

## FUTURO

El TaskDoc fijará archivos, tests y líneas base, y probablemente el texto exacto del conflicto. La promoción y el preflight los decide el operador/supervisor. La suite integrada la corre el supervisor. CC35b, CC35c y CC35d continúan después. GD24 es contrato suministrado por sldb, no decisión de este nodo.
