## REFORMULACION

Propósito: restaurar la copia empaquetada de la FAQ tras el integrate fallido de drawer-triage. Resultado: `deskops/data/faq.md` idéntica byte a byte a `docs/faq.md`, con `tests/test_packaging.py` y `tests/test_large_doc_materialization.py` en verde. Repo: deskops, según las rutas del encargo. Límites: solo se modifica `deskops/data/faq.md`; `docs/faq.md` y cualquier otro archivo quedan fuera. El camino indicado es copiar, comparar, ejecutar los dos módulos de test, commitear solo ese archivo con trailer `Task-Id` y ejecutar `deskops advance`.

## AMBIGUEDADES

1. “No cambia ningún otro archivo.” frente a “y deskops advance.”: no queda claro si los metadatos de workflow que pueda escribir `advance` cuentan como excepción y si deben commitearse. Obligaría a inventar el tratamiento del TaskDoc y del estado de workflow.
2. “commit solo de deskops/data/faq.md con ‘git commit -- deskops/data/faq.md’ y el trailer ‘Task-Id: <id de esta tarea>’, y deskops advance.”: no explicita el orden exacto ni si `advance` va después del commit. Obligaría a inventar la secuencia operativa.

## DRY-RUN

Lecturas: TaskDoc, `docs/faq.md`, `deskops/data/faq.md`, los dos módulos de test y estado git. Cambios previstos: sobrescribir `deskops/data/faq.md` con `cp docs/faq.md deskops/data/faq.md`; ningún otro cambio de contenido; commit únicamente de esa ruta con `Task-Id`; `deskops advance`. Dependencias: `docs/faq.md` correcto, permiso de escritura, Python/pytest con `TMPDIR=/tmp`, git y CLI `deskops`. Validaciones futuras: `cmp` sin salida; pytest indicado; commit limitado a la ruta y con trailer; avance de workflow. Nada se ejecuta ahora.

## FUTURO

El ejecutor producirá el diff de `deskops/data/faq.md`, la salida de `cmp`, el resultado de pytest y el commit. CI o un humano validará y aceptará el cambio; `deskops advance` moverá el estado del nodo.
