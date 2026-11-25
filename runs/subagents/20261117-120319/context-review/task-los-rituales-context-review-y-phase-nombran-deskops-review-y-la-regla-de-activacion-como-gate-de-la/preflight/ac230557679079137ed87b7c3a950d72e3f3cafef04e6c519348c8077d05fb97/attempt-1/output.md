REFORMULACION
Propósito: actualizar los rituales `context-review` y `phase` para que describan la revisión de contexto mediante `deskops review preflight|bundle|dispose` y el gate mediante `rule-activation-<tipo>`, sin instruir `pi` manual. Resultado: ambos rituales actualizados, sin referencias operativas a `pi --provider` ni `preflight.md`, con `doctor` sin hallazgos nuevos y `tests/test_skill_cli_drift.py` pasando. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`; archivos: `desk/rituals/context-review.md` y `desk/rituals/phase.md`. Límites: solo esos pasos; fuera otros rituales, reglas de `desk/lifecycle`, `docs/` y el plan `gates-por-tipo`. Cambios exclusivamente con `deskops edit ritual`, nunca a mano. Es una tarea documental ejecutable, no un agregado.

AMBIGUEDADES
1. «Reescribir los pasos afectados con deskops edit ritual» no identifica campo, paso ni texto exacto: obliga a inventar el mapeo entre la redacción del manual y los campos del ritual.
2. «su recibo en desk/reviews/<tarea>/» no fija nombre ni formato del recibo: documentarlo obligaría a inventar su estructura.
3. «sin 'pi --provider' ni 'preflight.md' como instruccion» no aclara si prohíbe toda mención o solo el uso como instrucción: obliga a decidir el criterio de inspección.
4. «sin hallazgos nuevos sobre rituales» no define baseline: obliga a inventar contra qué ejecución comparar.

DRY-RUN
Lecturas: TaskDoc; `desk/rituals/context-review.md`; `desk/rituals/phase.md`; `docs/operator-manual.md`; reglas `rule-activation-*` de `desk/lifecycle`; `dag.yaml` solo como referencia. Inspección prevista con `deskops show ritual context-review` y `deskops show ritual phase`. Cambios previstos con `deskops edit ritual <id> <campo> <valor> --root .`: sustituir pasos de `pi` manual/`preflight.md` por `deskops review preflight|bundle|dispose`, `--engine` y default `runtime-pi-deepseek-flash`; nombrar `rule-activation-<tipo>` en `phase`. Dependencias: CLI `deskops`, nombres reales de campos, perfil y reglas existentes. Validaciones futuras, sin ejecutar: `show` sin instrucción `pi`/`preflight.md`; `doctor` sin hallazgos nuevos; pytest indicado.

FUTURO
La retirada del plan `gates-por-tipo` corresponde a otro nodo. Un humano o nodo de cierre decidirá si las validaciones y el recibo bastan para cerrar; otro nodo ejecutará la revisión de contexto con `deskops review`.
