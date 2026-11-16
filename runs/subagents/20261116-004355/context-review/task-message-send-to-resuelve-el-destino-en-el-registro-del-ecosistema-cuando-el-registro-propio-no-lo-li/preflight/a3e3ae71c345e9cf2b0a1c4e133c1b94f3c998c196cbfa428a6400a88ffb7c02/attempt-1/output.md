## REFORMULACION

Encargo ejecutable (task.code, nodo ritual-execution) en el repo `deskops`: hacer que `message send --to <repo>` resuelva el destino primero en el registro del remitente y, si no aparece, en el registro del ecosistema (`~/setup/desk/registry` o `DESKOPS_ECOSYSTEM_REGISTRY`), incluso desde un repo sin store. Resultado observable: `tests/test_message_ecosystem_registry.py` en verde con CLI real y entrega en `desk/inbox` de deskops desde un repo sin registro propio. Superficie: `deskops/identity.py`, `deskops/cli/commands/message.py`, `deskops/cli/commands/repo.py`, el test citado. Límites: no registrar repos en `~/setup` ni cambiar el modelo `RepositoryDoc`.

## AMBIGUEDADES

1. «o la variable DESKOPS_ECOSYSTEM_REGISTRY»: no define precedencia ni si es directorio o fichero de registro. Obliga a inventar cuál gana y su formato.
2. «las rutas del registro aceptan ~»: no dice qué campos ni si se admiten rutas relativas. Obliga a inventar alcance y normalización.
3. «una raiz registrada que no existe en esta maquina es un error»: no aclara si basta una entrada no relacionada para fallar toda la resolución, ni tipo/mensaje de error. Obliga a inventar política y texto.
4. «no se escribe nada»: no especifica si se refiere solo al inbox del destino o a cualquier escritura. Obliga a inventar el alcance transaccional.
5. «identidad del remitente por raiz en el registro del ecosistema como ultimo recurso»: no define coincidencia de raíz, ni qué identidad se toma, ni comportamiento si tampoco aparece. Obliga a inventar matching y fallback final.
6. «tambien desde un repo sin store»: no dice dónde se escribe ni cómo se comporta sin configuración local. Obliga a inventar el flujo.
7. «entrega en desk/inbox de deskops»: no define ruta absoluta/relativa, nombre de fichero ni creación/append. Obliga a inventar semántica de entrega.
8. «misma resolucion de rutas» en `repo.py`: no identifica comandos afectados. Obliga a inventar alcance.

## DRY-RUN

Lecturas: los cuatro ficheros del scope, registros local/ecosistema y tests existentes. Cambios previstos: helpers en `identity.py`; wiring de destino e identidad en `message.py`; resolución en `repo.py`; test nuevo. Dependencias: HOME, variable de entorno, contenido de registros, pytest. Validaciones futuras: el comando pytest indicado y la prueba manual del Done When. Sin ejecutar nada.

## FUTURO

Un humano decide precedencia del env var, formato de error y semántica de entrega (puntos 1, 3, 4, 7); `deskops repo register` produce los registros; otro nodo ejecutará tests y validación manual.
