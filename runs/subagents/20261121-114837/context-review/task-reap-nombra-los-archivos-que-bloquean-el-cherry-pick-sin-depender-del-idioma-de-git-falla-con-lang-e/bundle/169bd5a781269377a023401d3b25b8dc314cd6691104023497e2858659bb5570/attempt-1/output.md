REFORMULACION
Propósito: corregir `dispatch reap` para que nombre los archivos locales que bloquean el cherry-pick sin depender del idioma de git (hoy falla con LANG=es_ES del timer y en producción el aviso no nombra archivos). Resultado: reap identifica esos archivos sin parsear mensajes localizados —forzando LC_ALL=C y LANGUAGE= en los subprocess de git, o calculando con `git status --porcelain` más la lista de archivos del commit—; el mensaje sigue nombrando archivos y sugiriendo commitearlos, con rc 8; el test pasa con cualquier locale y se agrega uno en español. Repo: /mnt/ssd/proyectos/SLDB_1/deskops. Límites: dentro deskops/dispatch.py (reap), deskops/runtime si allí corre git, tests/test_dispatch.py y CHANGELOG; fuera el resto.

AMBIGUEDADES
1. "o corre los comandos de git cuya salida parsea con LC_ALL=C y LANGUAGE= en el entorno, o calcula los archivos con git status --porcelain y la lista de archivos del commit": dos implementaciones alternativas sin criterio de elección; obliga a inventar cuál adoptar.
2. "y deskops/runtime si es donde se corre git": condicional sin confirmar; obliga a asumir si git se ejecuta allí.
3. "buscar en deskops/ los sitios que parsean stdout o stderr de git por texto": no acota si se corrigen todos los sitios o solo reap; obliga a inventar el alcance.
4. "del arreglo de RunDoc d42ee663": referencia externa no incluida; obliga a inventar su contenido.
5. "p4: ... commit desde el worktree que dispatch te da": no se especifica ruta ni formato del id; obliga a inventarlos.
6. "CHANGELOG": no se indica archivo ni formato de entrada.
7. "hay locales es_*.utf8 instalados": afirmación de entorno no verificada; obliga a asumir disponibilidad.

DRY-RUN
Lecturas: deskops/dispatch.py (reap), grep de parseos de git en deskops/, tests/test_dispatch.py:514, CHANGELOG. Cambios previstos: test nuevo que reproduce el fallo con LANG/LC_ALL/LANGUAGE=es_ES.UTF-8; ajuste en reap (env LC_ALL=C/LANGUAGE= o porcelain + lista de archivos); conservar mensaje y rc 8; entrada de CHANGELOG; commit con trailer `Task-Id`. Dependencias: locale es_ES.UTF-8, escenario de test existente, worktree de dispatch. Validaciones futuras: pytest con entorno español, con -n 4, y con en_US.

FUTURO
El Board enruta rituales; el nodo de pills/átomos aporta el RunDoc d42ee663 y convenciones. Un humano elige entre las dos implementaciones ambiguas y aprueba el commit/merge. CI ejecuta la validación. Tareas posteriores consumen el cambio.
