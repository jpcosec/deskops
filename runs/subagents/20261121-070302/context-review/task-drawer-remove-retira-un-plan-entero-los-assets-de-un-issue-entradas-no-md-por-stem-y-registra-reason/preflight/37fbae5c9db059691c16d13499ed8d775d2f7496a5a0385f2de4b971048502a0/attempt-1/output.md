REFORMULACION
El nodo es una tarea ejecutable (`task.code`), no un agregado. Propósito: corregir `deskops drawer remove` para cubrir cuatro huecos detectados en notas del 2026-11-16. Resultado esperado: (1) retirar un plan completo bajo `desk/drawer/plans/<plan>/`, incluido `dag.yaml`, tracking y bullets del Board; (2) retirar los assets de un issue cuando nadie más los referencie, y permitir que `deskops retire` acepte un asset huérfano; (3) resolver por stem o fragmento entradas `.yml/.yaml`; (4) aceptar `--reason` y `--ref` con el registro que ya usa `retire`. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: tocar `services/drawer.py`, `services/retire.py`, `cli/registry.py`, golden de ayuda y tests nuevos; no tocar `from_drawer` colgante.

AMBIGUEDADES
1. “si nadie mas la referencia”: no define cómo detectar referencias (contenido, grafo, issues, planes) ni qué hacer si alguna existe. Obliga a inventar criterio de seguridad.
2. “por ruta o por nombre del plan”: no aclara qué es “nombre” frente a directorio, planes anidados o nombres ambiguos. Obliga a inventar resolución.
3. “resuelve por stem o fragmento tambien entradas .yml/.yaml”: no fija prioridad frente a `.md`, desempate entre varios `.yml`, ni si aplica a planes. Obliga a inventar reglas.
4. “retire acepta un asset huerfano”: no define forma CLI, ruta esperada ni validación de pertenencia. Obliga a inventar interfaz.
5. “registra reason y ref”: no indica esquema exacto ni visibilidad; “igual que deskops retire” exige inferirlo desde código no incluido aquí.

DRY-RUN
Lecturas hipotéticas: `drawer.py` (resolución y `remove_entry`), `retire.py` (verbos dedicados y registro de `reason/ref`), `registry.py`, golden `deskops_drawer_remove.txt` y tests existentes. Cambios previstos: ampliar resolución a directorios de plan y `.yml/.yaml`; retirar assets; añadir flags; ajustar golden; crear tests temporales. Dependencias: comportamiento actual de `retire`, parser CLI, fixtures y estructura del Board. Validaciones futuras: pytest de gaps, `-k "drawer or retire"`, ayuda y suite completa con criterio de fallo en `origin/main`.

FUTURO
Un humano debe decidir los criterios de referencia de assets, desambiguación de stems/planes y forma CLI del asset huérfano; otro nodo ejecutará la implementación y aportará resultados de tests.
