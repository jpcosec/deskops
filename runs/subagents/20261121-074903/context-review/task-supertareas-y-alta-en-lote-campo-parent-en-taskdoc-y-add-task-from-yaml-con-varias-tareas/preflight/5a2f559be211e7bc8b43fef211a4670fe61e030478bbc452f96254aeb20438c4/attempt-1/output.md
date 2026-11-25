## REFORMULACION

Nodo ejecutable `task.code`, no agregado. Propósito: que `TaskDoc` represente jerarquía mediante `parent` y que el alta desde YAML sea masiva y atómica. Resultado: un YAML con una supertarea y tres hijas crea cuatro tareas con `parent`; si falla la tercera, no queda ninguna. Repo: `deskops`. Límites: `deskops/models` (TaskDoc), `deskops/services/tasks.py`, CLI `add task`; la relación se apoya en la API de aristas de `sldb`, sin grafo propio. Validación futura: test nuevo de `deskops` con ese YAML.

## AMBIGUEDADES

1. “deskops add task --from-yaml acepta una lista de tareas”: no define esquema del YAML, claves de `parent`, orden ni sintaxis CLI. Obliga a inventar formato de entrada y compatibilidad.
2. “parent (id de otra tarea)”: no aclara validación de existencia, autociclos, jerarquías profundas ni comportamiento ante `parent` inválido. Obliga a inventar reglas.
3. “relacion por la API de aristas de sldb, sin grafo propio”: no concreta API, tipo de arista, dirección ni metadatos. Obliga a inventar el mapeo `parent`→arista.
4. “doctor y el tablero respetan”: no define qué significa “respetar” ni si doctor/tablero están en alcance; el Scope no los lista. Obliga a inventar comportamiento o cambios fuera de alcance.
5. “un error en la tercera no deja ninguna”: no especifica mecanismo transaccional, errores cubiertos ni atomicidad ante fallos de aristas. Obliga a inventar estrategia de rollback.
6. “test nuevo de deskops (nombre a fijar al promover)”: no fija nombre, ubicación ni comando. Obliga a inventar convención de test.

## DRY-RUN

Lecturas previstas: modelo `TaskDoc`, `services/tasks.py`, CLI `add task`, tests existentes y API de aristas de `sldb`. Cambios previstos: campo `parent` y validaciones; carga YAML de lista; creación transaccional; test supertarea+tres hijas. Dependencias: parser YAML, API de aristas, fixtures. Validaciones futuras: alta completa, rollback al fallar la tercera, compatibilidad con una sola tarea y respeto por doctor/tablero. Sin ejecutar nada.

## FUTURO

Un nodo de implementación escribirá código y test; un humano fijará el nombre del test al promover y decidirá el esquema YAML si no se especifica antes.
