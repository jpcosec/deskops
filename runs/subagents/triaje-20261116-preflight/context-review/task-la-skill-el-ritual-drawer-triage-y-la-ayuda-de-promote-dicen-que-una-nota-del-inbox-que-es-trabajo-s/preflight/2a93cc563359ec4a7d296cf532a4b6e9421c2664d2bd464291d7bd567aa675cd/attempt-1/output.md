## REFORMULACION
**Propósito:** corregir la skill, el ritual y la ayuda que afirman que una nota del inbox que es trabajo se promueve al drawer, alineándolos con los atoms y el camino confirmado por JP: si es trabajo, `deskops add task` con references a la nota y `deskops message ack`; si no, solo ack y razón en el informe de triaje.  
**Resultado:** SKILL.md, vocabulary.md, ritual-drawer-triage, ayuda de promote y su golden, y operator-manual describen ese camino; promote advierte que borra la nota y que no sirve para notas-trabajo.  
**Repo:** `/mnt/ssd/proyectos/SLDB_1/deskops`.  
**Límites:** no retirar promote ni cambiar atoms; editar el ritual solo con `deskops edit ritual`.  
El nodo es un TaskDoc ejecutable, no un agregado ni paquete no ejecutable.

## AMBIGUEDADES
1. «el help de promote en deskops/cli/registry.py y su golden»: no nombra el archivo golden ni el comando de regeneración; obligaría a inventar ambos.
2. «Reescribir cada mención.»: no fija la redacción ni si se conservan ejemplos; obligaría a inventar el texto exacto.
3. «deskops edit ritual ritual-drawer-triage steps '[...]' --root .»: el literal `[...]` no define el array; obligaría a inventar pasos, orden y formato exactos.
4. «`deskops add task` con references hacia la nota»: no especifica la sintaxis de references; obligaría a inventar flags o formato documental.

## DRY-RUN
**Lecturas:** nota del inbox, brief, atoms citados, SKILL.md, vocabulary.md, ritual, registry.py, golden(s) de ayuda, operator-manual y tests mencionados.  
**Cambios previstos:** reescribir menciones en skill/vocabulary/operator-manual; actualizar ayuda de promote; editar el ritual vía CLI con un array de pasos; regenerar golden.  
**Dependencias:** CLI `deskops` disponible, `--root .`, venv y golden regenerable; orden lógico: localizar menciones, editar ritual, ajustar ayuda, regenerar golden, ejecutar tests.  
**Validaciones futuras:** los tres pytest indicados y el grep final; comprobar que solo quedan advertencias. No se ejecuta nada.

## FUTURO
El ejecutor futuro aplicará los cambios y correrá los tests. JP decidirá en otra tarea si se retira promote. El ack y el informe de triaje pertenecen al flujo de triaje, no a este TaskDoc.
