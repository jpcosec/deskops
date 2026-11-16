## REFORMULACION

**Propósito:** que `deskops message send --to <repo>` resuelva el destino primero en el registro del remitente y, si no lo lista, en el registro del ecosistema (`$DESKOPS_ECOSYSTEM_REGISTRY` o `~/setup/desk/registry`), también desde un repo sin store.
**Resultado:** `identity.py` con `ecosystem_registry_dir`, `load_ecosystem_registry`, `find_registered_desk` y `expanduser` en `resolve_registered_root`; `message.py` resolviendo destino e identidad del remitente con esas piezas; `repo.py` usando la misma `resolve_registered_root`; `tests/test_message_ecosystem_registry.py` en verde.
**Repo:** deskops.
**Límites (p1–p8):** gana la variable si está definida y no vacía; `~` se expande solo en `path` de `RepositoryDoc`; raíz inexistente del repo pedido → `SLDBStoreError` con `"does not exist on this machine"` y rc 1; orden del remitente: registro propio, `desk/config.json`, ecosistema; sin store solo cambia la búsqueda; entrega y formato de nota intactos; en `repo.py` solo cambia `_resolve_registered_root`. Fuera: registrar repos en `~/setup` y cambiar `RepositoryDoc`.

## AMBIGUEDADES

1. **p4 vs p6/p7.** p4: *"no se escribe nada en ningun lado: ni inbox ni directorios del destino, ni la nota"*; p6: *"la nota se escribe en el inbox del destino igual que hoy"*. ¿p4 aplica solo al caso de raíz inexistente (error) o a todo `send`? Leerlo literal anularía la entrega; obliga a inventar el alcance del "no escribir".
2. **Conflicto de identidad del remitente.** Orden p5: *"registro propio, desk/config.json, ecosistema"*; pero también *"la raiz del remitente (find_context_root) se compara con resolve_registered_repo_by_root sobre las entradas del ecosistema; se toma el id de esa entrada"*. Si el registro propio y el ecosistema dan ids distintos para la misma raíz, no se dice cuál gana. Obliga a inventar precedencia.
3. **Alcance de la comprobación de existencia.** p3: *"solo cuenta la entrada del repo pedido"*. No aclara si el chequeo de raíz inexistente vale también para entradas del registro propio o solo del ecosistema.

## DRY-RUN

**Lecturas:** los cuatro archivos nombrados y `instruccion`.
**Cambios previstos:** `identity.py` (expandir `~` en `resolve_registered_root`; funciones de ecosistema); `message.py` (`_resolve_repo_desk` → `find_registered_desk`; `_sender_project` con último recurso por raíz); `repo.py` (delegar en `resolve_registered_root`); test nuevo.
**Dependencias:** `pytest`, `sldb`, `HOME` temporal de conftest, CLI real en subproceso.
**Validaciones futuras:** `TMPDIR=/dev/shm python -m pytest -q -p no:cacheprovider tests/test_message_ecosystem_registry.py`; comprobar los seis casos (ecosistema, sin store, prioridad local, variable, raíz ausente, id desconocido) y el `send --to deskops` manual. Nada ejecutado.

## FUTURO

Otro nodo/humano debe: registrar los repos en `~/setup` con `deskops repo register` (fuera de alcance); completar el contenido real del registro del ecosistema en cada máquina; revisar y mergear el diff; confirmar que MEPU (prioridad alta) queda desbloqueado.
