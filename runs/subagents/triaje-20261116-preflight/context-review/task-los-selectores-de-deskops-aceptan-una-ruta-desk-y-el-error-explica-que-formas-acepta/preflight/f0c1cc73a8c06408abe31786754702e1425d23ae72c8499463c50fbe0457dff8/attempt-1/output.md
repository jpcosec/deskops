## REFORMULACION
Encargo ejecutable (no agregado): en el repo `/mnt/ssd/proyectos/SLDB_1/deskops`, hacer que los selectores de deskops acepten una ruta relativa al repo (`desk/...`) o absoluta dentro del desk y resuelvan al mismo artefacto que su stem. Si no resuelven, el error debe enumerar las formas aceptadas: id exacto, nombre de archivo, stem, fragmento único y ruta `desk/...`. También debe añadirse un ejemplo con un item del drawer en la ayuda de `edit task`. Entra: `deskops/desk_paths.py`, `deskops/doc_access.py`, ayuda en `deskops/cli/registry.py`, goldens y tests citados. No entra: legibilidad de `promote inbox-to-drawer-task`. Límite: esta revisión no ejecuta nada.

## AMBIGUEDADES
1. «si contiene '/', resolver contra la raiz del repo» frente a «ruta relativa al repo (desk/...) o absoluta dentro del desk»: no queda claro cómo tratar rutas absolutas, `..`, symlinks o rutas fuera de `desk/`; obligaría a inventar la normalización exacta.
2. «fragmento unico»: no se define unicidad ni qué ocurre si hay colisión; obligaría a inventar criterio de desambiguación.
3. «actualizar goldens de ayuda» y «La ayuda de edit task trae un ejemplo con un item del drawer»: no se especifica texto exacto, golden afectado ni item de ejemplo; obligaría a inventar la salida esperada.
4. «sin fallas nuevas respecto de main»: no se define cómo obtener/comparar `main`; obligaría a inventar el baseline.

## DRY-RUN
Lecturas: TaskDoc, `desk_paths.py`, `doc_access.py`, `cli/registry.py`, tests y goldens. Cambios previstos: normalización compartida de selectores con `/`; resolución contra raíz del repo y reducción a stem dentro de `desk/`; mensaje de error común; ayuda de `edit task`; tests y goldens. Dependencias: convención de raíz del repo, resolución existente de artefactos y formato de goldens. Validaciones futuras: los cinco comandos pytest listados, incluida suite completa. Sin ejecutar.

## FUTURO
Un ejecutor implementará y correrá tests. Un humano o revisor decidirá texto exacto del error/ayuda y aceptación del baseline. Otro nodo validará goldens y suite completa.
