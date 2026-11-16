## REFORMULACION
Nodo ejecutable (`task.code`), no agregado. **Propósito:** sustituir en deskops las emulaciones H1/H2 de capacidades que sldb ya ofrece. **Resultado:** la configuración de `project_graph` en `deskops/graph/desk_graph.py` usa `closed:` con la condición equivalente a `_closed_issue` y declara `declared_file_targets` para archivos existentes no-documento; desaparecen `_closed_issue` y `declared_target_is_a_file`; `deskops graph missing --root .` conserva su resultado. **Repo:** `/mnt/ssd/proyectos/SLDB_1/deskops`. **Límites:** solo `desk_graph.py`, `checks.py` y los dos tests listados; no cambiar sldb ni editar a mano `.sldb/store.yaml`; guardar la salida previa de `graph missing`.

## AMBIGUEDADES
1. “declara declared_file_targets para los archivos existentes que no son documento”: no se indican campos, globs ni nodos esperados; obliga a inventar el esquema concreto de declaración.
2. “con la misma condicion que hoy evalua _closed_issue”: la condición no está incluida; obliga a inferirla del código citado o inventar su traducción a `closed:`.
3. “Si algun destino […] no se puede declarar […] se manda deskops message send --to sldb con el caso”: no define cuándo se considera no declarable, qué contenido exacto enviar ni si bloquea el cierre; obliga a inventar criterio y formato.
4. “runs/subagents/<run>/graph-missing-antes.txt”: `<run>` no está concretado; obliga a inventar el directorio de ejecución.
5. “misma lista de faltantes” frente a “misma salida que graph-missing-antes.txt”: no aclara comparación exacta byte a byte o por conjunto; obliga a elegir el criterio.

## DRY-RUN
Lecturas previstas: este TaskDoc, los archivos de sldb citados (`document_surface.py`, `project_texts.py`, `project_graph_config*.py`, `declared_file_targets.py`, `declared_target_nodes.py`, test de `project_graph`) y `desk_graph.py:180-215`, `checks.py:55-90`, tests indicados. Cambios previstos: capturar salida de `graph missing`; reemplazar `closed_document=_closed_issue` por `closed:`; construir `declared_file_targets`; borrar código viejo; ajustar tests. Dependencias: API de sldb disponible, frontmatter/globs existentes, entorno `../.venv` y CLI `deskops`. Validaciones futuras: pytest de ambos archivos, comparación de `graph missing`, grep vacío y suite completa con baseline en worktree de `origin/main`. Sin ejecutar nada.

## FUTURO
El ejecutor futuro producirá el diff, la salida previa, resultados de tests y, si aplica, el mensaje a sldb. Un revisor o humano decidirá la aceptación y el tratamiento de fallas no nuevas; otro nodo podrá corregir sldb si se reporta un destino no declarable.
