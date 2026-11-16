REFORMULACION

Propósito: que el registro del ecosistema sea portable entre máquinas, sin rutas absolutas atadas a robocop2. Resultado: (1) `repo register` escribe en `path` una ruta relativa y la lectura tolera entradas viejas absolutas o con `~`; (2) `doctor` emite, por cada entrada no resoluble, un hallazgo con id, path guardado y ruta resuelta, además del mensaje actual de store enlazado. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: toca `repo.py`, `doc_access.py`, `doctor.py`, `tests/test_repo_identity.py` y `tests/test_registry_robustness.py`; quedan fuera reescribir `~/setup` y cambiar el formato `RepositoryDoc`. Es una tarea de código ejecutable, no un agregado.

AMBIGUEDADES

1. "guarda en path la ruta relativa a la raiz del repo que contiene el registro" contrasta con el título "rutas relativas a la raiz del ecosistema" y con "register calcula os.path.relpath(destino, raiz_del_registro)": hay tres bases posibles (repo, ecosistema, directorio del registro); obliga a inventar cuál.
2. "acepta leer entradas viejas con ruta absoluta o con ~" y "con ~ expandido solo al resolver": no dice qué función expande `~` ni si `doctor` también debe expandirlo; obliga a inventar el punto de resolución.
3. "un hallazgo con el id del repo, el path guardado y la ruta resuelta, ademas del mensaje actual del store enlazado": no fija severidad (error/alerta) ni efecto en el exit code, que `doctor.py` distingue; obliga a inventar.
4. "el path guardado y la ruta resuelta": si la entrada no resuelve no existe ruta resuelta; obliga a inventar si se reporta la intentada.

DRY-RUN

Lecturas: `RepoCLI.register` y `_resolve_registered_root`; `registered_repositories`/`repository_root`; `load_repository_registry`, `resolve_registered_root`; `doctor.py` y `doctor_findings`; los dos tests nombrados. Cambios previstos: calcular `relpath` del destino contra la base elegida al escribir; normalizar `~` y absolutas al leer; añadir el hallazgo en el chequeo de registro de `doctor`; tests de ruta relativa, absoluta inexistente y absoluta válida. Dependencias: `sldb.api.transaction`, `render_model_markdown`, `select_documents`, `Findings`. Validaciones futuras: los cuatro comandos `pytest` indicados; las fallas de la suite completa se replican en worktree limpio de `origin/main` antes de aceptarlas.

FUTURO

El dueño de `~/setup` reescribe sus entradas con el CLI nuevo; un humano decide la severidad si se eleva; el cierre produce el commit descriptivo y el informe con la lista de fallas baseline.
