## REFORMULACION

**Propósito:** eliminar de `desk update` la exigencia de `desk/reviews/` como estructura obligatoria, porque git no versiona carpetas vacías y un clon limpio falla en dry-run.

**Resultado:** `deskops desk update --root <clon>` devuelve rc 0 en un clon limpio; `desk/reviews/` se crea al escribir el primer recibo.

**Repo:** `/mnt/ssd/proyectos/SLDB_1/deskops`.

**Límites:** tocar `deskops/cli/commands/desk.py`, `tests/test_cli.py` y, solo si corresponde, `tests/fixtures/golden/scaffold/update.json`. No agregar `.gitkeep` ni ampliar superficie.

## AMBIGUEDADES

1. “Quitar las líneas 231-232” frente a “el código a quitar es el if que agrega 'desk/reviews/'”: los números pueden no coincidir con el archivo actual. Obliga a decidir si manda la ubicación numérica o el bloque lógico.
2. “El golden scaffold/update.json se actualiza solo si su contenido nombra desk/reviews”: no define qué hacer si el golden cambia por otra razón. Obliga a inventar el criterio de actualización.
3. “El primer recibo crea desk/reviews/”: no indica qué comando o fixture representa ese primer recibo. Obliga a inventar la invocación de prueba.
4. “solo se acepta si falla igual ahí”: no define “igual”. Obliga a inventar si basta el mismo test o se exige el mismo error.

## DRY-RUN

Nodo ejecutable de código; no es agregado.

**Lecturas previstas:** bloque de `missing_desk_files` en `desk.py`, creación de carpeta en `review.py`, golden `scaffold/update.json`, tests existentes en `test_cli.py`.

**Cambios previstos:** quitar el añadido condicional de `desk/reviews/`; actualizar el golden solo si nombra esa ruta; añadir un test con `tmp_path`, `git init -b main`, `deskops init`, commit, clon y `desk update --root <clon>` sin `--apply`, esperando rc 0.

**Dependencias:** git, pytest, CLI instalada, `origin/main` para comparar fallas.

**Validaciones futuras:** ejecutar los comandos de `Validation`, incluida la suite completa y la comprobación de fallas en worktree limpio.

## FUTURO

Otro nodo o un humano aportará el repo/base actualizado, ejecutará las validaciones, comparará fallas contra `origin/main` y aceptará el informe final.
