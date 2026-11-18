A continuación se presenta la revisión del diff organizada en una lista numerada de hallazgos, cubriendo los cuatro ejes solicitados:

---

### 1. `--back` omite `condition`, reglas `on_transition` (`document`) y asume una única arista manual (`manual[0]`)
* **Archivo:** `deskops/lifecycle.py` (líneas 438–449)
* **Gravedad:** Alta
* **Escenario concreto de fallo:**
  En `advance()`, cuando `back_reason is not None`, se llama a `transitions_from(root, node, manual=True)` sin pasar el documento de la tarea (`document`) y se selecciona incondicionalmente `transition = manual[0]`:
  1. No se evalúa `transition.condition` ni `transition.findings` (reglas `RuleDoc` con `on_transition`), a diferencia del avance normal (y contradiciendo el propio docstring de `advance`). Si una regla `on_transition` o una condición en la arista manual prohíbe la transición para el estado actual de la tarea, `--back` la ignora y fuerza el cambio de nodo.
  2. Tampoco se comprueba si la tarea ya está en un estado cerrado/terminal antes de evaluar la vuelta, ni se itera sobre `manual` buscando la primera arista cuya condición se cumpla si un nodo declara más de una transición manual.

---

### 2. El validador de `history` (`lifecycle_errors`) no distingue aristas manuales de normales al parsear `: <reason>` y puede rechazar la vuelta si `table.edges` excluye manuales o al validar entradas previas
* **Archivo:** `deskops/models/task_lifecycle.py` (líneas 151–156) y `deskops/lifecycle.py` (líneas 398, 446–448)
* **Gravedad:** Alta
* **Escenario concreto de fallo:**
  1. **Construcción de `table.edges`:** Si `table.edges` se puebla usando `lifecycle_transitions()` (que ahora filtra `manual=False` por defecto), `"task_returns_to_execution"` no existirá en `table.edges`. Al ejecutar `apply_effects(payload, ..., model)` en `deskops/lifecycle.py:448`, la validación del modelo `TaskDoc` invocará `lifecycle_errors`, obtendrá `edge is None` y lanzará un error de validación impidiendo cualquier `--back`.
  2. **Entradas históricas no finales (`history[:-1]`):** El cambio solo aplica `.split(": ", 1)[0]` sobre `last` (`history[-1]`). Si `lifecycle_errors` recorre las entradas previas de `history` para validar la cadena completa de transiciones, en cuanto la tarea vuelva a `ritual-execution` y avance de nuevo a `ritual-testing` (o se cierre con `closeout`), `"task_returns_to_execution: <reason>"` dejará de ser `last` y hará fallar la validación de la tarea.
  3. **Falsos positivos en `last`:** `table.edges.get(last.split(": ", 1)[0] if ": " in last else last)` recorta `: <reason>` para **cualquier** arista sin verificar si es manual, y tampoco exige que una arista manual lleve `: <reason>` no vacío. Con esto, `lifecycle_errors` da por válidas:
     - Una transición normal con sufijo arbitrario, p. ej. `"task_activates: texto"`.
     - Una transición manual sin razón (`"task_returns_to_execution"`) o con razón vacía (`"task_returns_to_execution: "`).

---

### 3. `lifecycle_transitions()` oculta silenciosamente las aristas manuales del resto del sistema
* **Archivo:** `deskops/lifecycle.py` (líneas 298–303, 305–321, 398)
* **Gravedad:** Media / Alta
* **Escenario concreto de fallo:**
  `transitions_from()` cambia su firma a `manual: bool = False` y `lifecycle_transitions(root, spec)` hace `[t for node in spec.rituals for t in transitions_from(root, node)]` sin incluir las manuales. Como consecuencia:
  1. Cualquier consumidor de `lifecycle_transitions()` (validación global del grafo, verificación preventiva de `HookDefinitionError` o paquetes en todas las aristas, reportes de topología) deja de ver `testing-task_returns_to_execution`. Un error de configuración en los hooks o atributos de una arista manual pasará desapercibido hasta que alguien ejecute `--back` en tiempo de ejecución.
  2. En `transitions_from(..., snapshot=snapshot, manual=True)` (línea 315), el bloque `if manual:` hace un `return` directo llamando a `sldb.api.edges_from`, ignorando por completo la caché `snapshot` documentada en el docstring.

---

### 4. `--back` oculta `LifecycleGraphMissing` en desks existentes sin actualizar y marca erróneamente el resultado como terminal cuando no hay arista manual
* **Archivo:** `deskops/lifecycle.py` (líneas 438–452)
* **Gravedad:** Media
* **Escenario concreto de fallo:**
  1. **Orden de comprobación de `LifecycleGraphMissing`:** El bloque `if back_reason is not None:` se ejecuta **antes** de `transitions = transitions_from(root, node); if not transitions: raise LifecycleGraphMissing(...)` (línea 450). Si el grafo de ciclo de vida falta en `.sldb` (o si un nodo aún no tiene aristas cargadas tras actualizar el código sin correr `deskops desk update --apply`), `--back` no lanza `LifecycleGraphMissing` con las instrucciones de remediación, sino que devuelve silenciosamente `"no hay transicion de vuelta desde <node>"`.
  2. **Flag booleano invertido en `TransitionResult`:** En la línea 441:
     ```python
     return TransitionResult(node, status, False, True, f"no hay transicion de vuelta desde {node}")
     ```
     El cuarto argumento posicional (que representa estado terminal/bloqueo final; compárese con `TransitionResult(..., True, False, ...)` en la línea 449) se pasa como `True`. Si un usuario ejecuta `--back` desde `ritual-execution` (donde no hay arista manual), el resultado reporta falsamente ese estado como terminal/bloqueado, además de devolver el mensaje en español mientras que todo el resto de la CLI y `lifecycle.py` emite mensajes en inglés.

---

### 5. Falta validación de `back_reason` vacío o solo espacios fuera de la CLI
* **Archivo:** `deskops/lifecycle.py` (línea 438), `deskops/services/tasks.py` (línea 297) y `deskops/operations.py` (línea 220)
* **Gravedad:** Baja / Media
* **Escenario concreto de fallo:**
  La validación `if back and not (reason or "").strip():` solo existe en la capa CLI (`deskops/cli/commands/operations.py:208`). Tanto `DeskopsOperations.advance_task`, `TasksService.advance_task` como `lifecycle.advance` comprueban únicamente `if back_reason is not None:`. Si cualquier llamador interno, test o integración invoca `operations.advance_task(task_id, back_reason="")` o `back_reason="   "`, se ejecutará la transición manual en lugar del avance normal y se persistirá en `history` la entrada inválida `"task_returns_to_execution: "`.

---

### 6. Post-hooks y rollback al volver a `ritual-execution`
* **Archivo:** `deskops/lifecycle.py` (líneas 445–449), `deskops/services/tasks.py` (líneas 312–316) y `desk/lifecycle/testing-task_returns_to_execution.md`
* **Gravedad:** Media
* **Escenario concreto de fallo:**
  1. **Ejecución de post-hooks y rollback en `TasksService.advance_task`:** `lifecycle.advance` con `back_reason` devuelve un `TransitionResult(progressed=True, ..., transition=transition)` idéntico al de un avance normal. En `TasksService.advance_task`, todo el flujo posterior (persistencia del documento, ejecución de post-hooks de `result.transition.hooks` y eventual rollback si un hook falla) se comparte sin distinguir si fue un avance o una vuelta. Si el rollback o el registro de ejecución asume que el movimiento fue hacia adelante (o si `execution-task_activates` tenía efectos secundarios al entrar en `ritual-testing` que no se deshacen al volver a `ritual-execution`, como artefactos/runs de Scion abiertos), la vuelta solo cambia `current_node: RitualDoc:ritual-execution` y `status: active` en el documento de la tarea sin limpiar ni revertir el estado externo creado al salir de ejecución.
  2. **Mutación in-place de `payload` antes de persistir:** En `deskops/lifecycle.py:448`, `payload.update(apply_effects(...))` muta el diccionario recibido antes de que `TasksService.advance_task` ejecute los post-hooks; si el llamador reutiliza `payload` en memoria tras un fallo posterior, queda con el estado mutado.
