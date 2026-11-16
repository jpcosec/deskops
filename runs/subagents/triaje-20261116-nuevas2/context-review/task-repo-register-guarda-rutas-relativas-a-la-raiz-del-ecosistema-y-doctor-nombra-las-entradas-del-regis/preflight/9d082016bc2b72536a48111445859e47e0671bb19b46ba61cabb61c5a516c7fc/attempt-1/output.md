## REFORMULACION
Nodo ejecutable `task.code` (no agregado) en `/mnt/ssd/proyectos/SLDB_1/deskops`. Propósito: hacer portable el registro del ecosistema y mejorar el diagnóstico de entradas inválidas. Resultado: (1) `deskops repo register` guarda en `path` una ruta relativa a la raíz del repo que contiene el registro, y los lectores siguen aceptando rutas absolutas o con `~`; (2) `deskops doctor` alerta por cada entrada del registro del desk cuyo `path` no resuelve, mostrando id, path guardado y ruta absoluta intentada, sin cambiar el rc. Límites: tocar `repo.py`, resolución del registro, `doctor.py` y tests indicados; no reescribir `~/setup`, no cambiar `RepositoryDoc`, y doctor solo cubre `desk/registry`.

## AMBIGUEDADES
1. “método register alrededor de la linea 32”: no fija la ubicación exacta; obligaría a localizarla por inspección, no a inventar comportamiento.
2. “deskops/doc_access.py (registered_repositories, alrededor de la linea 934) o el modulo que resuelva rutas del registro”: deja abierta la ubicación del cambio, aunque después se concreta en `resolve_registered_root` de `identity.py`.
3. “una entrada con ruta absoluta inexistente da el hallazgo en doctor”: no describe el montaje del registro de prueba; obligaría a inventar el fixture.

## DRY-RUN
Lecturas hipotéticas: `repo.py`, `doc_access.py`, `doctor.py`, `identity.py`, tests citados y atomos. Cambios previstos: calcular `os.path.relpath(destino, raiz_del_registro)` al registrar; centralizar expansión de `~` y resolución relativa en `resolve_registered_root`; añadir hallazgos en doctor con id, path guardado y ruta intentada. Dependencias: entorno `../.venv`, `pytest`, sandbox de desk roots y `origin/main` para comparar fallas. Validaciones futuras: los tres pytest de `test_repo_identity.py`, `test_registry_robustness.py` y `test_message_ecosystem_registry.py`; luego suite completa con `-n 4`, comparando fallas en worktree limpio de `origin/main`. Cierre: los tres casos nuevos pasan y los tests de registro existentes siguen verdes.

## FUTURO
Otro ejecutor implementa y corre las validaciones; un revisor evalúa fallas preexistentes y el informe; el dueño de `~/setup` migra sus entradas con el CLI nuevo; el humano decide commit/entrega.
