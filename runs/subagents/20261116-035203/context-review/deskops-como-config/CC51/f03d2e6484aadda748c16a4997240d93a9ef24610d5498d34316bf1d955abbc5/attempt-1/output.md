## REFORMULACION

**Propósito**: documentar la medición código vs configuración del plan completo y justificar lo que quedó como código. **Resultado**: `docs/config-vs-code.md` con (a) líneas Python de `deskops/deskops` por directorio de primer nivel en la base `827f3db7` y en el commit de cierre, (b) inventario de configuración con su ubicación, (c) lista archivo por archivo de lo que queda como código, con justificación (P4, hechos de git de CC33, agents de CC34 en el CLI) o marcada como deuda con nodo/inbox que la retire; más `CHANGELOG`. **Repo dueño**: deskops. **Límites**: nodo de docs/medición, no escribe en sldb ni suple reglas con Python; no cambia el formato del desk ni la gramática del CLI; parte de CC30–CC38 cerrados; N la fija el dueño (DA3) antes de promover.

## AMBIGUEDADES

1. "las líneas totales del commit de cierre" (acceptance): no se identifica cuál es ese commit; el ejecutor debe inventar si es el commit del propio CC51, el de cierre de PF4 ya integrado o HEAD de main al medir. Afecta la comprobación `< N`.
2. "inventario de configuración (modelos, …)" junto a "lista de lo que quedó como código, archivo por archivo": no dice cómo clasificar archivos que son modelo declarativo en Python (`deskops/models/*.py`), a la vez configuración y líneas contadas; obliga a inventar si van en el inventario, en la lista de código o en ambas para que "cada archivo aparece" sea comprobable.
3. "en la base (827f3db7: 18,732; …)": esa base no es el punto de partida real del plan (G_P0 y G_GATES_FROZEN integran código antes de CC30); no dice si se re-mide en el main de promoción ni qué cifra prevalece si el comando difiere de las dadas.

## DRY-RUN

**Lecturas previstas**: `dag.yaml` (CC51, PF4), brief/alcance (§límite, P4, invariante), `decisiones.md` (DA3, DK6), árbol de `827f3db7` y del commit de cierre, `docs/` y `CHANGELOG` existentes, salidas nominales de CC30–CC38. **Cambios**: crear `docs/config-vs-code.md`; editar `CHANGELOG.md`; nada en `desk/` ni `.sldb/`. **Dependencias**: N del dueño; CC30–CC38 integrados; worktree limpio del coordinador. **Validaciones futuras**: ejecutar `find deskops/deskops -name "*.py" | xargs wc -l` agrupado por directorio en base y cierre; verificar que todo archivo aparece en la lista o en directorio P4 nombrado; total del cierre < N; inventario con ubicaciones existentes; CHANGELOG actualizado; sin goldens de CLI afectados.

## FUTURO

El dueño fija N tras CC30 y antes de promover CC51 (DA3). Los nodos CC30–CC38 entregan lo que este nodo inventaría; cualquier deuda marcada la retira otro nodo o un inbox. La aprobación del documento medido corresponde al supervisor/operador del desk.
