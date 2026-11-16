## REFORMULACION

**Propósito:** documentar en `docs/configuration.md` el mapa de configuración de deskops (modelos y tipos de tarea, ReviewDoc/recibos, RelationDoc con attributes, RuleDoc, ViewDoc, grafo, semillas y plantillas) y ofrecer recetas ejecutables para declarar un tipo de tarea nuevo y una vista nueva.

**Resultado:** `configuration.md` con ambas recetas; `tests/test_docs_recipes.py` que ejecuta la receta del tipo nuevo en un desk temporal (bloqueo y activación) y la de vista (responde); enlaces desde `operator-manual.md` y `workflow-policy-reference.md`; entradas FAQ en `docs/faq.md` y `deskops/data/faq.md`; corrección mínima de rituales obsoletos; `CHANGELOG.md`.

**Repo:** `/mnt/ssd/proyectos/SLDB_1/deskops`.

**Límites:** no cambiar código de deskops; rituales solo si el grep `spec/artifacts\|desk_graph.py\|doc_io\|advance task .* --to` da coincidencias con referencias muertas y solo vía `deskops edit ritual`; deben seguir pasando `test_output_goldens.py` y `test_cli_help_examples.py`; suite completa sin fallas nuevas (comparadas en worktree limpio de `origin/main`).

## AMBIGUEDADES

1. "el archivo o comando nombrado no existe hoy" — no define cómo aislar el token «nombrado» dentro de una línea del grep. Obliga a inventar un criterio de parseo.
2. "la frase se reemplaza por el comando o archivo vigente que hace lo mismo" — no delimita qué es «la frase». Obliga a inventar los límites del reemplazo.
3. "solo via deskops edit ritual" — no da sintaxis ni parámetros del comando. Obliga a inventar la invocación.
4. "la tarea queda bloqueada y luego activada segun su regla" — no indica cómo se observa (exit code, mensaje, estado). Obliga a inventar las aserciones del test.
5. "que ejecuta sldb en cada caso" frente a «deskops» en el resto — no aclara si `sldb` es binario distinto o alias. Obliga a inventar la terminología.
6. "una subclase en desk/models/*.py" — no indica clase base, registro ni nombre de módulo. Obliga a inventar la API.
7. "verla con deskops view <nombre> --root ." — placeholder sin valor concreto.

## DRY-RUN

**Lecturas:** `deskops/models`, `deskops/data/rules`, doc de `sldb rules`, `docs/` y `deskops/data/faq.md`, `desk/rituals` (vía grep), tests existentes y goldens.
**Cambios previstos:** los siete archivos listados más rituales solo si el grep confirma referencias muertas.
**Dependencias:** CC31–CC34 y CC36 cerradas; CLI `deskops`/`sldb`; `.venv` en `../.venv`.
**Validaciones futuras:** los cinco comandos pytest del apartado Validation, incluida la suite completa con comparación contra `origin/main`.

## FUTURO

Un humano decide si una falla es preexistente aceptable y aprueba el contenido documental y el formato del CHANGELOG; otro nodo ejecuta la implementación y el ritual de cierre.
