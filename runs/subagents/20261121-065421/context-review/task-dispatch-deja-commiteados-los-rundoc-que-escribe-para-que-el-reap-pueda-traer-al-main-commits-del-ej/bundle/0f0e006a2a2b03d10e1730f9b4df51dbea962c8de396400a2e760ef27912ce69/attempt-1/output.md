REFORMULACION
Propósito: que el reap cherry-pickee a main commits del ejecutor sin chocar con el store sin commitear que escribe dispatch start (record_scion_run). Resultado: start commitea con pathspec solo el store tocado ('run: <agente>', [skip ci]); reap commitea RunDocs pendientes antes del cherry-pick; si otro cambio local choca, el error nombra archivos y sugiere commitearlos. Repo: deskops. Límites: solo deskops/dispatch.py (start y reap) o deskops/runtime/scion.py (record_scion_run), tests/test_dispatch.py y CHANGELOG; fuera el resto.

AMBIGUEDADES
1. "deskops/dispatch.py (start y reap) o deskops/runtime/scion.py (record_scion_run)": no fija archivo ni helper compartido; obligaría a inventar ubicación y granularidad.
2. "commitea en la rama principal": no nombra la rama ni cubre detached HEAD/worktrees; obligaría a inventar destino.
3. "solo los archivos del store que record_scion_run tocó": no enumera rutas ni patrón del shard; obligaría a inventar el pathspec.
4. "mensaje 'run: <agente>'": no define el formato de <agente>; obligaría a inventar el identificador.
5. "[skip ci]": no fija posición ni formato exactos; obligaría a inventar la línea de mensaje.
6. "cualquier RunDoc pendiente de sus agentes": no define cómo detectarlos ni si se limita a RunDocs; obligaría a inventar la lógica.
7. "Si queda otro cambio local que choca, el mensaje de error nombra los archivos": no dice quién detecta, cuándo ni la redacción; obligaría a inventar parsing y texto.
8. "trailer Task-Id": no fija valor/formato ni si aplica a ambos commits; obligaría a inventarlo.

DRY-RUN
Lecturas: TaskDoc, dispatch.py, runtime/scion.py, tests/test_dispatch.py, CHANGELOG y estado git. Cambios previstos: helper que ejecute `git commit -- <rutas>` con mensaje y trailer; invocarlo en start tras record_scion_run y en reap antes del cherry-pick; precheck de cambios locales con error descriptivo; test de regresión. Dependencias: git disponible, store y shards localizables, rama principal. Validaciones futuras: el pytest indicado y revisar que el commit no arrastre archivos ajenos.

FUTURO
Deciden humano/revisión: rama destino, conjunto exacto de rutas y formato de mensaje/trailer. Otro nodo produce el CHANGELOG y el commit final con Task-Id. No es ambigüedad.
