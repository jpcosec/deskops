REFORMULACION

El nodo debe corregir el template Scion del harness `pi`: en `deskops/runtime/scion.py`, `_command_args` debe emitir cada opción y su valor como elementos separados (`"--tools", "read,grep,find,ls,bash"`) cuando el `RuntimeProfileDoc` sea de kind `pi`; para los demás harness conserva `opcion=valor`. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Resultado: template `--harness pi` con `command_args` separados y `--harness claude` sin cambios, probado por tests. Nodo ejecutable, no agregado. Límites: solo `deskops/runtime/scion.py`, `tests/test_scion_runtime.py` y mención en `docs/operator-manual.md` si procede; fuera scion, imagen de pi y otros flags; checkout principal, sin worktree ni rama, sin `git add` ni `git commit`.

AMBIGUEDADES

1. Cita: “Checkout principal, sin worktree ni rama, sin git add ni git commit.” Frente al átomo: “not closed until relevant tests pass and the completed change is recorded in a descriptive git commit.” Obligaría a inventar si el cierre exige commit, quién lo hace y si el límite del TaskDoc prevalece.

2. Cita: “y la mencion en `docs/operator-manual.md` si el manual describe la forma de command_args.” El archivo no está en el input. Obligaría a inventar si existe tal mención y qué texto corregir.

DRY-RUN

Lecturas: TaskDoc, `deskops/runtime/scion.py` (`_command_args`, `scion_template_files`, `materialize_scion_template`), `deskops/materializers/runtime_profiles.py` (`build_agent_spec_args`), `tests/test_scion_runtime.py` y, si existe, `docs/operator-manual.md`.

Cambios previstos: en `_command_args`, ramificar por `profile.get("kind")`: para `pi`, devolver `list(args)` con pares separados; para el resto, mantener `f"{flag}={value}"`. Extender tests: template pi con tools produce `["--tools", "read,grep,find,ls,bash"]`; claude conserva `["--allowedTools=Read", ...]`. Actualizar manual solo si ya describe `command_args`.

Dependencias: orden de `build_agent_spec_args`, presencia de `kind` en el perfil y formato aceptado por pi 0.73.1. Validación futura: `TMPDIR=/dev/shm pytest -q tests/test_scion_runtime.py`; comprobar el “Done When”. Sin ejecutar nada; sin `git add`/`git commit` según scope.

FUTURO

Otro nodo de closeout o un humano debe resolver el conflicto entre el átomo y el límite de no commit, y ejecutar o autorizar el commit si corresponde. Un revisor valida el diff y el resultado conjunto; un humano confirma si el manual requería cambio.
