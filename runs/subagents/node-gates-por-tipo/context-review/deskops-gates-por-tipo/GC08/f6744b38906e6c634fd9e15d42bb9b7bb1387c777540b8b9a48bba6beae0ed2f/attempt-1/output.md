REFORMULACION

GC08 es un nodo `delivery` de documentación en deskops, no un agregado ni un paquete no ejecutable. Propósito: alinear rituales, manual y guía de workflow con tipos de tarea, `ReviewDoc` y `deskops review`. Resultado: `execution.md`, `context-review.md` y `phase.md` editados vía `deskops edit ritual`; `workflow-policy-reference.md` con tabla de tipos, reglas por tipo, contrato y campos no editables; `operator-manual.md` y `quickstart.md` con el flujo; `CHANGELOG`. Repo dueño: deskops. Límites: solo `output_scope`; depende de GC03, GC05 y GC06; no toca sldb ni implementa código.

AMBIGUEDADES

1. “review dispose como la disposición del coordinador”: “coordinador” no está definido; las fuentes dicen “quien opera el desk”. Obligaría a inventar si la disposición corresponde al coordinador, al dueño o al operador.
2. “paso 8 nombra los dos kinds”: no se dice cuáles; GC03 define cinco (`preflight`, `bundle`, `reproduction`, `goldens`, `owner`). Obligaría a elegir dos sin criterio explícito.
3. “el gate de la fase es la regla de activación de cada tipo, no un paso manual”: “gate de la fase” no está definido en las fuentes; obligaría a inventar qué transición o regla documentar en `phase.md`.

DRY-RUN

Sin ejecutar: leería brief, alcance, decisiones, salidas de GC01/GC05/GC06, rituales y docs actuales, y `CHANGELOG`. Editaría los tres rituales con `deskops edit ritual`; actualizaría `workflow-policy-reference.md`, `operator-manual.md`, `quickstart.md` y `CHANGELOG`. Dependencias: GC03 (comando, `runs/`, `ReviewDoc`, perfil), GC05 (reglas y explicación), GC06 (campos rechazados). Validaría extracción ida y vuelta por `RitualDoc` y `deskops doctor` sin alertas nuevas; greps de `preflight.md` y `deskops review`; coincidencia de la tabla con `brief.md`; `test_cli_help_examples.py`; entrada en `CHANGELOG`.

FUTURO

GC01 entrega tabla/modelos de tipos; GC05, reglas por tipo y contenido de workflow; GC06, campos no editables y golden de help; GC03, comando `deskops review`, layout de `runs/` y `ReviewDoc`. El dueño autoriza el plan y quien opera el desk escribe la disposición de aceptación.
