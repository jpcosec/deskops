## REFORMULACION

Encargo documental ejecutable (no es paquete ni agregado): corregir la skill, el ritual `drawer-triage`, la ayuda de `promote inbox-to-drawer-task` y el manual para que una nota del inbox que es trabajo se convierta en tarea con `deskops add task`, `references` hacia la nota y `deskops message ack`; si no es trabajo, solo ack. Resultado: ninguno de esos textos manda notas de trabajo al drawer y la ayuda de promote advierte que borra la nota de origen. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: no retirar promote ni cambiar atoms; editar el ritual solo con `deskops edit ritual`; conservar ejemplos correctos.

## AMBIGUEDADES

1. “texto canonico (en el idioma de cada archivo)”: no define la traducción exacta por archivo; obligaría a inventar la redacción inglesa/española de SKILL.md, vocabulary y operator-manual.
2. “5) Tests.”: no concreta tests adicionales; obligaría a inventar alcance distinto de los tres tests listados en Validation.
3. “Se conservan los ejemplos que sigan siendo correctos.”: exige juicio no objetivado; obligaría a inventar el criterio para conservar o eliminar ejemplos.
4. “solo menciones que advierten que no es el camino para notas que son trabajo” frente a “El grep solo muestra advertencias”: no fija el texto aceptable; obligaría a inventar qué formulaciones cuentan como advertencia.

## DRY-RUN

Lecturas: los cinco archivos de `files`, la nota de inbox y el brief referenciados, y `grep -rn 'inbox-to-drawer'` sobre `.claude`, `docs`, `deskops/cli/registry.py` y `desk/rituals`. Cambios previstos: reescribir menciones en SKILL.md, vocabulary y operator-manual; sustituir el paso 1 del ritual mediante `deskops edit ritual`; actualizar el help en `registry.py`; regenerar `tests/fixtures/golden/help/deskops_promote_inbox-to-drawer-task.txt`. Dependencias: CLI `deskops`, ritual existente, golden y `pytest --update-golden`. Validaciones futuras: los tres pytest indicados y el grep final. Sin ejecutar nada.

## FUTURO

Un ejecutor aplicará los cambios y dejará evidencia de comandos y tests. JP decide, en otra tarea, si se retira promote. La aceptación humana/CI verifica que el grep solo contenga advertencias y que los tests pasen.
