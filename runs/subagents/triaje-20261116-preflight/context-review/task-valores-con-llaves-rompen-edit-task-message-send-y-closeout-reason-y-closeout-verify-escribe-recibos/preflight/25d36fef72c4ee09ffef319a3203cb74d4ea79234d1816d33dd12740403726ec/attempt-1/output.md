REFORMULACION
Propósito: reproducir y corregir en `deskops` tres fallos: `closeout verify` escribe recibos pese a su ayuda; `closeout commit --reason` con llaves imprime “Missing required field” tras commitear y deja una evidencia sin commitear; `edit task` y `message send` fallan con `TemplateSyntaxError` ante dobles llaves. Resultado: recibo de reproducción de (a), (b) y (c), correcciones y tests; si (c) se origina en el render de sldb, mensaje a sldb y test `xfail` que cite la nota. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: incluye `closure.py`, ayuda de `closeout.py`, caminos hasta sldb y tests; excluye modificar sldb. No es agregado: es una tarea ejecutable.

AMBIGUEDADES
1. “verify no escribe nada o su ayuda dice exactamente que escribe”: disyuntiva; obliga a inventar cuál contrato adoptar.
2. “Si (c) nace en el render de sldb”: no define cómo atribuir el origen; obliga a inventar el criterio.
3. “un --reason con llaves queda literal en el commit”: no aclara si deben preservarse exactamente las llaves o solo evitar el error; obliga a inventar la semántica.
4. “sin fallas nuevas respecto de main”: no fija baseline ni estado de main; obliga a asumir la comparación.
5. “registrar el recibo de reproduccion”: no define contenido/esquema, aunque sugiere `review record`; obliga a inventar el formato.

DRY-RUN
Lecturas: TaskDoc, nota referenciada, `closure.py` (incluida línea 788), `closeout.py`, tests citados. Cambios previstos: crear sandbox con `deskops init`; ejecutar comandos mínimos y guardar `runs/<run>/repro-*.log`; registrar evidencia; corregir escritura/ayuda de verify y formateo seguro de `--reason`; rastrear (c); añadir tests. Dependencias: render de sldb, entorno `.venv`, `TMPDIR`, sandbox. Validaciones futuras: los cuatro pytest indicados, recibos presentes, tests verdes o `xfail` citando la nota.

FUTURO
sldb decide/corrige su render; un humano resuelve el contrato de verify y el baseline de main; revisión/aceptación del recibo.
