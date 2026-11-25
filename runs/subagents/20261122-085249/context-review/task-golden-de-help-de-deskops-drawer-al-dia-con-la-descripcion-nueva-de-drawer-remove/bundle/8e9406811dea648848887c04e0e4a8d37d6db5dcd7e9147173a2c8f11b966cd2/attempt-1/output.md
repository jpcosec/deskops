## REFORMULACION
Nodo ejecutable `task.code`. **Propósito:** restaurar la consistencia del golden de ayuda del grupo `drawer` tras el cambio de descripción de `drawer remove`. **Resultado:** `tests/fixtures/golden/help/deskops_drawer.txt` coincide con la salida actual de `deskops drawer --help` con `COLUMNS=80`; solo cambia ese archivo y se registra en un commit con `Task-Id`. **Repo:** `deskops`, en el worktree que entregue dispatch. **Límites:** dentro, únicamente ese golden; fuera, el código de `drawer` y cualquier otro golden; no se ejecuta la suite completa, la corre integrate.

## AMBIGUEDADES
1. «con `COLUMNS=80`. Se regenera con el mecanismo del propio test (`pytest ... --update-golden`)»: el comando no fija `COLUMNS=80`; obligaría a inventar si debe exportarse o si el test ya lo controla.
2. «commit desde el worktree que dispatch te da»: el bundle no incluye su ruta; obligaría a inventar el worktree.
3. «se revierten y se explica por qué»: no se indica dónde debe quedar esa explicación; obligaría a inventar el soporte (commit, nota o informe).

## DRY-RUN
**Lecturas:** TaskDoc, `tests/test_output_goldens.py`, golden afectado y golden de `drawer_remove`, y estado git del worktree. **Cambios previstos:** ejecutar la regeneración en el worktree; revisar `git status`; revertir cualquier golden distinto de `deskops_drawer.txt`; repetir el test sin `--update-golden`; commitear solo el archivo indicado con el trailer. **Dependencias:** worktree de dispatch, entorno Python/pytest y git operativos, y el mecanismo del test para fijar el ancho. **Validaciones futuras:** `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_output_goldens.py`, más la comprobación de que el commit solo toca el golden objetivo.

## FUTURO
Dispatch aporta el worktree. El nodo de integrate ejecutará la suite completa. Otro nodo o un humano revisará el commit y la explicación de goldens revertidos, si los hubo.
