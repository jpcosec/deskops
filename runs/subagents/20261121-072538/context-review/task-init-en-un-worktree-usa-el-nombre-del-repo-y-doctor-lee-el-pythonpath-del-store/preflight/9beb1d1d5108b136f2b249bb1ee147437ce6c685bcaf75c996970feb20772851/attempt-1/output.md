REFORMULACION
Propósito: corregir dos conductas de deskops. Resultado: (1) `deskops init` dentro de un git worktree debe derivar `project_identity` del repo principal —git common dir o remoto—, no de la carpeta del worktree; (2) `deskops doctor` debe usar el `pythonpath` declarado en el store para hallar los modelos del proyecto. Superficie: `deskops/workspace.py` (init) y doctor, más un test nuevo con `git worktree add` real. Repo: deskops (`/mnt/ssd/proyectos/SLDB_1/deskops`). Límites: solo init y doctor; el pythonpath se lee por la API de sldb, sin parsear `store.yaml` a mano. No es agregado ni paquete: es una tarea ejecutable, hoy `status: draft` y `current_node: ritual-execution`.

AMBIGUEDADES
1. «git common dir o remoto»: no fija precedencia, ni qué hacer sin remoto o si ambos difieren; obliga a inventar fuente, normalización y fallback.
2. «usa el pythonpath que declara el store»: no define clave, formato (lista/string), resolución relativa/absoluta ni precedencia sobre `PYTHONPATH`; obliga a inventar el contrato.
3. «se lee por la API de sldb»: no nombra función, módulo ni versión; obliga a inventar el punto de integración.
4. «test nuevo de deskops (nombre a fijar al promover) con git worktree add real»: no fija ubicación, nombre, fixture ni limpieza; obliga a inventar el arnés.
5. «doctor carga modelos del pythonpath del store»: no define qué es “cargar” ni el comportamiento ante ruta inválida; obliga a inventar validación y error esperado.

DRY-RUN
Lecturas: TaskDoc, nota de inbox referenciada, `workspace.py`, doctor y API de sldb para el store. Cambios previstos: resolver identidad desde git common dir/remoto con fallback; inyectar el pythonpath del store en doctor vía API sldb; añadir test con worktree real. Dependencias: git disponible, API sldb que exponga el store, arnés de tests de deskops. Validaciones futuras: ejecutar el test nuevo, suite existente y comprobación manual en worktree. Nada ejecutado.

FUTURO
Un nodo de ejecución producirá el diff y el test; el promotor fijará el nombre del test y cambiará el estado; un humano o CI decidirá la aceptación. La API de sldb debe proveer el acceso al store.
