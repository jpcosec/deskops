REFORMULACION
Propósito: dotar a deskops de un RoleDoc empaquetado `desk-identity` y de su materialización Scion como agente persistente de identidad. Resultado: (1) RoleDoc dato instalable en `desk/roles`; (2) `deskops desk update --apply` lo instala sin pisar existentes y el modo seco lo lista; (3) `deskops runtime template --mode identity` escribe un `agents.md` que nombra la raíz del desk y el proyecto scion, sin worktree ni instrucciones de ejecutor/tester/coordinador. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: no crear el agente en scion, no hook, no repo scion, no mapa de propiedad. Es una tarea `task.code` ejecutable, no un agregado.

AMBIGUEDADES
1. "un cuerpo con estas reglas": enuncia reglas en prosa, no su texto exacto; obliga a inventar redacción, orden y comandos.
2. "junto a las plantillas de deskops/data/templates": no fija ruta ni nombre del archivo empaquetado; obliga a inventar ubicación.
3. "name desk-identity": no fija `id` ni nombre de archivo; obliga a inventar identidad canónica y detección de existente.
4. "con deskops add role por debajo": no da sintaxis ni si el cuerpo va por archivo/stdin; obliga a inventar la integración.
5. "sin worktree por agente (workspace relativo...)": no define texto exacto ni representación del workspace relativo; obliga a inventar contenido y validación.
6. "goldens de ayuda": no identifica ayudas ni salidas esperadas; obliga a inventar goldens.
7. "deskops runtime template desk-identity --mode identity --root <desk temporal>": no aclara si el rol debe estar instalado ni si `<desk temporal>` contiene `desk/roles`; obliga a inventar la precondición.

DRY-RUN
Lecturas: TaskDoc, `desk.py`, `scion.py`, `runtime.py`, tests y declaración de includes. Cambios previstos: añadir el RoleDoc empaquetado; en `desk.py` planificar instalación idempotente vía add role; en `scion.py` añadir modo `identity` con `agents.md` propio y rechazo de modos desconocidos; en `runtime.py` propagar `--mode`; tests y goldens. Dependencias: task de traducción de tools/modelo, `add role` y worktree de dispatch. Validaciones futuras: `test_desk_sync.py`, `test_scion_runtime.py`, `test_output_goldens.py` y suite `-n 4`. Nada ejecutado.

FUTURO
Otro nodo entrega la traducción de tools/modelo; dispatch entrega el worktree para commit; un humano/Governance decide el texto exacto del RoleDoc y aprueba el resultado.
