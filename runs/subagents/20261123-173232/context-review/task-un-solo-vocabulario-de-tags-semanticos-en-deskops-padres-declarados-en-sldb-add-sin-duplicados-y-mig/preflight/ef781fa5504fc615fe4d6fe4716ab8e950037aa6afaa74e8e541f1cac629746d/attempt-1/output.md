REFORMULACION
Propósito: unificar el vocabulario de tags semánticos de deskops, eliminando duplicados y tags planos sin padre. Resultado: tags con padre o equivalente declarado en sldb; `deskops add/edit` sin duplicados; documentos del desk migrados por CLI; `semantic_dag.yaml` sin tags planos injustificados; informe con mapeo y conteo antes/después. Repo: desk de deskops. Límites: solo ese desk, no otros desks ni el lector de surface; prohibido editar `.sldb` a mano; si falta operación masiva, avisar a sldb y migrar lo permitido. Es una tarea individual (`task.code`), no un agregado.

AMBIGUEDADES
1. “padre declarado con sldb semantic parent o es equivalente declarado (sldb semantic equivalent)” no fija sintaxis, comandos ni criterio para comprobar equivalencia; obligaría a inventar la interfaz real de sldb.
2. “los documentos existentes del desk de deskops” no precisa ruta, selección ni exclusión; obligaría a inventar el conjunto migrable.
3. “cambios en los templates o validadores de deskops que escriben tags” no nombra archivos ni punto de validación; obligaría a inventar la superficie de código.
4. “siguiendo los tags de modelo con puntos como canonicos” no resuelve colisiones concretas ni jerarquías; obligaría a inventar el mapeo tag viejo→nuevo.
5. “Si a sldb le falta una operacion” no define cómo detectarlo; obligaría a inventar el criterio de carencia.

DRY-RUN
Lecturas: esta tarea, nota de inbox referenciada, store semántico, `semantic_dag.yaml`, comandos `add/edit`, templates, validadores y tests. Cambios previstos: informe con inventario y tabla de mapeo; declaraciones de padres/equivalentes vía sldb; ajustes de escritura de tags con tests; migración CLI del desk; regeneración de caché; conteos antes/después. Dependencias: capacidades reales de sldb y deskops. Validaciones futuras: `TMPDIR=/tmp pytest -q` de tests tocados, `deskops doctor --root .` y conteo de tags planos sin padre.

FUTURO
Otro nodo produce la implementación, tests y migración; sldb podría aportar una operación masiva. Un humano decide el mapeo canónico si hay colisiones y acepta el informe y el resultado final.
