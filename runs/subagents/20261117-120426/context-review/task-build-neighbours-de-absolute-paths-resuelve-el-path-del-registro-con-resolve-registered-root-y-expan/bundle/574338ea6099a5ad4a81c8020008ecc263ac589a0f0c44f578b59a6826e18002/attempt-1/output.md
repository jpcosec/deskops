## REFORMULACION

Encargo: en `deskops/absolute_paths.py`, `build_neighbours` debe resolver el `path` de cada entrada del registro con `deskops.identity.resolve_registered_root` (que expande `~` y resuelve relativas contra la raíz del repo del registro), en lugar de resolverlo a mano. Resultado observable: una entrada con `~` o relativa produce el mismo directorio vecino por `build_neighbours` y por `doc_access.repository_root`, y `doctor` deja de reportarla dos veces (caso Chatbot_Infra). Repo: `deskops`. Límites: solo `build_neighbours` y tests en `tests/test_doctor_absolute_paths.py`; fuera: formato de `RepositoryDoc`, `repo register` y el chequeo de registro de doctor (ya cerrados). Es una tarea de código ejecutable; cierra con tests y commit (átomo).

## AMBIGUEDADES

1. "resuelve cada entrada del registro con resolve_registered_root" — el input no da firma ni semántica de `resolve_registered_root` (parámetros, base, retorno, excepciones). Obliga a inventar cómo se invoca y qué hacer ante fallo.
2. "resuelve rutas relativas contra la raiz del repo del registro" — no queda claro si la base es `root` (repo bajo estudio) o la raíz del repo al que pertenece el documento de registro. Obliga a elegir una.
3. "una entrada de registro con la virgulilla (HOME apuntado al sandbox)" — no se especifica cómo se fija `HOME` en el test (monkeypatch, env) ni si `resolve_registered_root` usa `expanduser`. Obliga a inventar el mecanismo.
4. "planned" — no dice si los valores de `planned` también pasan por `resolve_registered_root`. Obliga a decidir el orden de resolución.
5. "igual que doc_access.repository_root" — no aclara si se comparte helper o se duplica la llamada. Obliga a elegir estrategia.

## DRY-RUN

Lecturas: `build_neighbours` y `_registry` en `absolute_paths.py`; `doc_access.repository_root`; `identity.resolve_registered_root`; `models.RepositoryDoc`; fixture `_register/_eco` en el test.
Cambios previstos: sustituir el bloque `if Path(value).is_absolute()...` por la llamada a `resolve_registered_root` (aplicada también a valores `planned`), preservando `own_ids`, `roots` e `ids`; añadir test con `~` y relativa comparando contra `repository_root`.
Dependencias: que `resolve_registered_root` exista y acepte `~`; `HOME` redirigible; `desk_transaction` intacto.
Validaciones futuras: los dos pytest de Validation más el test nuevo; `doctor` sin doble alerta.

## FUTURO

Otro nodo ejecuta edición, tests y commit descriptivo; un humano decide si conviene refactor compartido entre `doc_access` y `absolute_paths`; el closeout registra el commit.
