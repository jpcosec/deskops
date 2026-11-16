## REFORMULACION
**Propósito:** documentar en deskops qué es configuración sobre sldb y cómo se declara un tipo de tarea o una vista. **Resultado:** `docs/configuration.md` con el mapa (modelos/tipos, `ReviewDoc`/recibos, `RelationDoc`/`attributes`, `RuleDoc`, `ViewDoc`, grafo, semillas y plantillas) y recetas ejecutables; enlaces desde `operator-manual` y `workflow-policy-reference`; FAQ; rituales vía deskops; test de receta; CHANGELOG. **Repo dueño:** deskops. **Límites:** nodo de docs, no cambia comportamiento ni escribe en sldb; no suple reglas con Python; depende de CC31–CC34 y CC36; el formato del desk y la gramática del CLI no cambian. CC53 es delivery ejecutable, no agregado.

## AMBIGUEDADES
1. “los rituales que nombran comportamiento cambiado se actualizan vía deskops”. No enumera rituales ni fija qué cuenta como “comportamiento cambiado”; la aceptación tampoco los verifica. Obliga a inventar el conjunto de rituales y el criterio de terminado.
2. “los ejemplos de ayuda de la CLI siguen pasando (test_cli_help_examples.py)”. Contradice `alcance.md`, que ancla los goldens de ayuda en “test_output_goldens.py:316 test_help_goldens”. Obliga a decidir cuál es la prueba autoritativa o a crear/renombrar una; no es solo un nombre diferido al TaskDoc, porque la aceptación ya lo fija.

## DRY-RUN
**Lecturas:** `dag.yaml`, `brief.md`, `alcance.md`, `decisiones.md`, docs actuales, tests y goldens, y salidas de CC31–CC34/CC36. **Cambios previstos:** crear `docs/configuration.md`; enlazarlo desde `operator-manual` y `workflow-policy-reference`; añadir las preguntas a `docs/faq.md` y `deskops/data/faq.md`; actualizar rituales con deskops; añadir el test de receta en desk temporal; CHANGELOG. **Dependencias:** CC31 (lifecycle), CC32 (reglas), CC33 (recibos), CC34 (vistas) y CC36 (plantillas) ya en main; `requires: []`. **Validaciones futuras:** ejecutar el test de receta, comprobar `test_cli_help_examples.py` o el golden equivalente, enlaces, FAQ/rituales, suite y `doctor` en los 6 desks. Sin ejecutar nada.

## FUTURO
El TaskDoc fija el nombre exacto del test de receta y, si se corrige la ambigüedad 2, la prueba de ayuda autoritativa; el supervisor corre la suite integrada; CC51/CC52 miden y validan los 6 desks y el Board; el dueño revisa la publicación de `configuration.md`. Nada de esto es ambigüedad del nodo.
