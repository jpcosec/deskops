## REFORMULACION

El nodo es un TaskDoc ejecutable (`task.code`), no un agregado ni paquete no ejecutable. Encargo: en el repo `/mnt/ssd/proyectos/SLDB_1/deskops`, modificar el camino de `deskops init` que llama a `sldb.api.init_store` dentro de `_init_store` (`deskops/bootstrap.py`, alrededor de la línea 348) para que, tras `init_store`, el `.gitignore` de la raíz del repo git contenga idempotentemente una línea `.deskops.log`, creándolo si no existe. Resultado observable: la línea aparece una sola vez, un segundo init no la duplica, un `.gitignore` previo se preserva y `git status` no muestra `.deskops.log` como no trackeado. Añadir o ajustar el test en `tests/test_gitignore_policy.py`. Límites: no mover el log fuera de la raíz ni cambiar `sldb`; solo el camino de init en `bootstrap.py` y ese test. Validación futura: pytest de `tests/test_gitignore_policy.py`, `tests/test_runtime_initializer.py` y suite completa, comparando fallas con `origin/main` limpio.

## AMBIGUEDADES

1. Cita: “contiene una linea .deskops.log (una sola vez, sin duplicarla si ya estaba)” y “asegurar idempotentemente la linea .deskops.log”. No define si la comparación es línea exacta o entrada equivalente (espacios, CRLF, comentario). Obliga a inventar el criterio de idempotencia y normalización.
2. Cita: “un .gitignore previo con la linea queda igual”. No precisa si “igual” es byte a byte o solo contenido. Obliga a decidir preservación de newline final y orden.

## DRY-RUN

Un ejecutor futuro leería `deskops/bootstrap.py` y `tests/test_gitignore_policy.py`; localizaría `_init_store` y el flujo posterior a `init_store`. Cambios previstos: helper idempotente que cree el `.gitignore` raíz si falta y agregue `.deskops.log` solo si no está; invocación tras `init_store`; tests con repo temporal para primer init, segundo init y `.gitignore` previo. Dependencias: comportamiento existente de `sldb.api.init_store`, pytest y repositorios temporales. Validaciones futuras: los tres comandos pytest indicados, sin ejecutarlos ahora.

## FUTURO

Otro nodo ejecutor aplicará el cambio y correrá las validaciones; CI/merge decidirá la integración; un humano revisará el diff y aceptará el resultado, incluyendo cualquier falla preexistente comparada contra `origin/main`.
