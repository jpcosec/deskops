# Veredicto — tester deskops-t-a8ebbb84ed77

Tarea: task-repo-register-guarda-rutas-relativas-a-la-raiz-del-ecosistema-y-doctor-nombra-las-entradas-del-regis
Entrega: run-deskops-e-ae9a07e468ed (diff sin commitear en repo.py, doc_access.py, doctor.py, tests/test_registry_robustness.py)

**APROBADO**

## Contrato vs diff
- (1) `repo register` guarda `os.path.relpath(destino, raíz del repo del registro)` (deskops/cli/commands/repo.py:59, helper :191). La raíz es el abuelo de `<desk>/registry`; `_desk_root` (repo.py:169) siempre es `project_root(store)/desk`, así que coincide con el `root` contra el que resuelven los lectores (`load_repository_registry(desk, root)`; para ~/setup, `load_ecosystem_registry` usa `desk_root.parent` = ~/setup). El destino se resuelve con `resolve_registered_root` (expande `~`). Precisión del preflight cumplida.
- Entradas viejas absolutas / con `~` siguen resolviendo: `resolve_registered_root` (identity.py:324) ya expandía `~`; test nuevo lo cubre para identity y doc_access.
- (2) doctor: `_check_registry_paths` (doctor.py:148) una alerta por entrada de desk/registry que no resuelve a un dir, con id, path guardado y ruta intentada; va a `findings.alerts` (no cambia rc). Solo desk/registry, como pide el preflight.
- Archivos dentro de `files`; tests/test_repo_identity.py no se tocó (pre-autorizado sin uso: podar `files` antes del cierre).

## doc_access.repository_root (doc_access.py:960)
Antes: absoluto -> resolve; relativo -> root/path. Ahora delega en `resolve_registered_root`: idéntico para absolutos y relativos; path vacío sigue -> root.resolve(); única diferencia: `~/x` ahora se expande (antes daba `<root>/~/x`, inexistente). Su único llamador es `list_repo_task_routes` (doc_access.py:1012). `message send --to` (message.py usa `load_ecosystem_registry`) y la evidencia `<repo-id>:<sha>` de closeout_gates (vía `load_repository_registry`) NO pasan por `repository_root`; ya usaban `resolve_registered_root`. Sin cambio para ellos; test_message_ecosystem_registry, test_closeout_gates, test_closeout_resolved_by(_xrepo) verdes.

## Evidencia
- 7 archivos de a uno, sin lock, PYTHONPATH al checkout: 8+8+6+5+12+25+12 passed, todos rc=0 (validation.log).
- doctor real (solo lectura, desk/ sin cambios): alerta solo `Chatbot_Infra` (/home/jp/... no existe aquí); las 5 relativas existen y no alertan. Correcto. rc=1 de doctor es por errores previos ajenos (ReviewDoc lost).
- HEAD: 4 failed / 4 passed con los tests nuevos -> los tests discriminan.
- Suite completa no corrida (por brief).

## Riesgos (no bloquean)
- deskops/absolute_paths.py `build_neighbours` (fuera de files) resuelve `path` del registro a mano sin expandir `~`; solo afecta entradas viejas escritas a mano con `~`. Candidato a drawer (el propio ejecutor lo señala).
- Para Chatbot_Infra doctor da dos líneas (absolute_paths + registry); ruido menor.
- `register` usa `.resolve()` antes de relpath (symlinks -> rutas reales).
- La comprobación de duplicado en register (repo.py:85) resuelve con `root`; equivalente porque desk_root = root/desk.
