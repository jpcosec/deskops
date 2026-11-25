REFORMULACION
Encargo ejecutable (task.code, no agregado; sin hijos). Propósito: que `build_neighbours` de `deskops/absolute_paths.py` resuelva cada entrada del registro con el mismo criterio que `doc_access.repository_root`, usando `deskops.identity.resolve_registered_root`. Resultado: una entrada con virgulilla o relativa produce el mismo directorio por ambos caminos y doctor deja de reportarla dos veces. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: solo `deskops/absolute_paths.py` y `tests/test_doctor_absolute_paths.py`; fuera el formato de `RepositoryDoc`, `repo register` y el chequeo de registro de doctor.

AMBIGUEDADES
1. «resuelve cada entrada del registro con resolve_registered_root, igual que doc_access.repository_root»: no se define firma, argumentos ni valor de retorno de `resolve_registered_root`; obligaría a inventar su contrato de llamada.
2. «una entrada vieja escrita a mano con la virgulilla»: no se especifica el esquema del registro (claves, formato, ubicación); obligaría a inventar cómo crear esa entrada en el sandbox.
3. «HOME apuntado al sandbox»: no se indica si se parchea la variable de entorno, `Path.home()` u otra fuente; obligaría a elegir el mecanismo.
4. «resuelve rutas relativas contra la raiz del repo del registro»: no se aclara qué raíz exacta ni cómo se obtiene; obligaría a inferirla.
5. «dan el mismo directorio»: no se define igualdad (string, `resolve()`, symlinks); obligaría a fijar el criterio de comparación.
6. «Reemplazar la resolucion a mano por resolve_registered_root»: se desconoce el código actual de `build_neighbours`; obligaría a imaginar su estructura.

DRY-RUN
Lecturas: `deskops/absolute_paths.py` (`build_neighbours`), `deskops/identity.py` (`resolve_registered_root`), `doc_access.repository_root`, `tests/test_doctor_absolute_paths.py` y el registro de prueba. Cambios previstos: sustituir la resolución manual por la llamada compartida y añadir un test en `tmp_path` con entrada con virgulilla y relativa, comparando ambos caminos. Dependencias: entorno `../.venv`, `PYTHONPATH`, `TMPDIR=/dev/shm`. Validaciones futuras: los dos pytest indicados en `Validation`.

FUTURO
Un humano o nodo posterior confirma la firma real de `resolve_registered_root` y el esquema del registro; el ejecutor solo implementa y valida.
