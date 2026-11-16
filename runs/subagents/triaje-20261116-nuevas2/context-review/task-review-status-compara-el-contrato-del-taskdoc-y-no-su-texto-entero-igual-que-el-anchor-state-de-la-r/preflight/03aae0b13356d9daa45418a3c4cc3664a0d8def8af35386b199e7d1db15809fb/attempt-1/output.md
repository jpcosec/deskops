REFORMULACION

Propósito: corregir `deskops review status` para que no marque `stale` cuando solo cambian metadatos del TaskDoc (`sldb`, tags, status, current_node, history, references). Resultado: el estado se calculará comparando un `contract_sha256` del contrato del TaskDoc, guardado en el ReviewDoc, más las demás fuentes del bundle; los recibos antiguos conservarán la comparación actual por `input_sha256`. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`, archivos `deskops/services/review.py` y `tests/test_review_command.py`. Límites: no cambiar `input.md`, el `input_sha256` registrado ni las reglas de activación; mantener un estado por clave y la agregación actual.

AMBIGUEDADES

1. Fuente exacta del digest: “el contract_sha256 del TaskDoc que sldb calcula sobre __contract__… se ubica con grep”. Si no existe una función reutilizable o su semántica difiere, habría que inventar algoritmo, normalización y compatibilidad.
2. Composición del hash de bundle: “las demas fuentes… siguen entrando al hash como hoy; solo la parte del TaskDoc se reemplaza”. No se define orden, concatenación ni si `files` del TaskDoc se cuenta también como archivo enlazado; obligaría a inventar el esquema.
3. Persistencia del campo: “si el ReviewDoc no lo guarda, se agrega el campo al escribir el recibo”. No se precisa formato/versionado ni valor por defecto; obligaría a inventar la representación y migración.
4. Cobertura exacta de tests: “editar tags y status… deja status accepted; editar goal lo deja stale”. No indica aserciones, fixtures ni el estado inicial completo; obligaría a inventarlos.

DRY-RUN

Lecturas: `review.py:440-520` y `740-800`; búsqueda de `__contract__`/`contract_sha256`; definición de ReviewDoc; tests de review. Cambios previstos: helper de digest contractual; escritura del campo en recibos nuevos; comparación con fallback a `input_sha256`; tests de tags/status/goal. Dependencias: disponibilidad del digest en sldb, serialización del ReviewDoc y comportamiento del bundle. Validaciones futuras: los tres comandos pytest indicados, incluida la suite completa y comparación de fallas en worktree limpio.

FUTURO

Otro nodo implementará y ejecutará pruebas; un humano decidirá si las fallas preexistentes son aceptables, revisará el commit y dará por cerrada la tarea.
