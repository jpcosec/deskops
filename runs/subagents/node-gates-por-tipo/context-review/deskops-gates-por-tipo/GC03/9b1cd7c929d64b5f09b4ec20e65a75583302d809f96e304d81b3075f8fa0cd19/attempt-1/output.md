REFORMULACION
GC03 es un nodo `delivery` de código en deskops, no un agregado. Encargo: implementar `deskops review` para sustituir los dos scripts de revisión en frío. Resultado: subcomandos `node`, `preflight`, `bundle`, `status` y `dispose`; evidencia bajo `runs/`; `ReviewDoc` con `verdict pending`; perfil pi por defecto; topes y retiro del script de workspace-documental. Repo dueño: deskops. Límites: no toca sldb (solo nota), no implementa Scion, no calcula el hash de ancla (espera GO07) y no ejecuta cierre.

AMBIGUEDADES
1. “con las claves KEEP del script gobernado”: no se enumeran ni se define su contrato; obligaría al ejecutor a inventar qué campos del nodo copiar o a depender de leer un script externo.
2. “status [<task> | <plan-dir>] (compara el hash del input vigente…”: para `<plan-dir>` no se define cuál es el input vigente por nodo ni cómo agregarlo; obligaría a inventar la clave y el hash de status del plan.
3. “archivos que files nombra, menores de 60 KB”: no dice qué hacer si un archivo alcanza o supera 60 KB (omitir, fallar, truncar); obligaría a inventar.
4. “--max-attempts 2 por clave a nivel de plan; para preflight y bundle una por hash de contrato”: no define qué es “clave” ni cómo se combina con `input_sha256`; obligaría a inventar la identidad de los intentos.

DRY-RUN
Lecturas: GC03, GC02, PC01, GC08, GC10, guía y ritual; script gobernado para KEEP; TaskDoc y archivos de `files`. Cambios previstos: `registry.py`, `commands/review.py`, `services/review.py`, `workspace.py`, `desk/runtimes/`, borrado del script, tests, docs y CHANGELOG. Dependencias: `ReviewDoc` de GC02; fixture de `pi`; GO07 para hash futuro. Validaciones futuras: los casos de `acceptance` (cinco archivos, status stale, orden del bundle, ReviewDoc de nodo, dispose, topes, `technical_ok`, grep y docs). Sin ejecutar nada.

FUTURO
GC10 promueve nodos y mantiene `promoted`; GC08 actualiza rituales y manual; GO07 pinnea el subject; el operador dispone veredictos; sldb recibe la nota; `G_RECEIPTS` cierra GC03.
