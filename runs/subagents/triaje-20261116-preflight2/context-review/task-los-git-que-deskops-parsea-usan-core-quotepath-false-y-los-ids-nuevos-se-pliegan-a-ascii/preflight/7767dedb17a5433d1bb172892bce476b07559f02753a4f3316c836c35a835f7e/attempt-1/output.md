REFORMULACION
Propósito: que deskops no dependa de core.quotepath al parsear git y que los ids nuevos derivados de títulos se plieguen a ASCII. Resultado: helper `ascii_slug` en `deskops/slugs.py` compartido por compiler.py, doc_access.py y drawer.py; llamadas git cuya salida se parsea con `-c core.quotepath=false` o `-z`; ids acentuados existentes siguen resolviendo sin renombrarse; test `tests/test_ascii_ids.py`. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: fuera renombrar/migrar ids commiteados, el hook externo de worktrees y cambiar la longitud máxima; auditoría solo de subprocess con argv que empieza por `git` y localizable por grep.

AMBIGUEDADES
1. "cualquier otra llamada git con salida parseada que muestre `grep -rn '"git"' deskops/`": no define qué es salida parseada ni fija el patrón exacto; obliga a inventar el criterio de inclusión.
2. "pasa `-c core.quotepath=false` o usa -z": dos implementaciones alternativas sin preferencia; obliga a elegir por llamada.
3. "Los ids existentes con acentos siguen resolviendo por selector exacto": no dice qué ocurre si el id plegado colisiona con otro existente; obliga a inventar precedencia o rechazo.
4. "Sin fallas nuevas: cada test que falle... solo se acepta si falla igual ahí": "igual" no se define (test, error, causa); obliga a inventar el criterio de comparación.
5. "la longitud maxima de cada llamador se conserva": no aclara si `ascii_slug` trunca o solo pliega; obliga a inventar su firma.

DRY-RUN
Lecturas: task doc, nota de inbox referenciada, compiler.py 155-159, doc_access.py 157-161, drawer.py 288-290, closure.py ~645/695/1555, grep de `git` en deskops/ y tests existentes. Cambios previstos: crear `deskops/slugs.py` con `ascii_slug` (NFKD, descarte de marcas, minúsculas, `re.sub(r'[^a-z0-9]+','-')`, `strip('-')`, sin truncar); sustituir las tres reglas; añadir el flag o `-z` a cada git parseado; crear `tests/test_ascii_ids.py` con los tres casos. Dependencias: stdlib `unicodedata`/`re`, pytest, sandbox de desk, git worktree. Validaciones futuras: los pytest listados, suite completa, `grep quotepath` y comparación en worktree limpio. Nada ejecutado.

FUTURO
Otro nodo o un humano decide `-c` frente a `-z` si no se fija antes, valida la lista de fallas preexistentes del informe y confirma que no se renombran ids.
