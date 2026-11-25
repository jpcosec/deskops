## REFORMULACION

Propósito: añadir a `deskops` un modo `pr` en `IntegrateConfig` para que el ciclo dispatch start/reap/integrate termine en un PR hacia `integrate.branch`, sin push directo ni merge local a la base. Resultado: campo `mode` (`push` por defecto, `pr`); en `pr`, reap crea `task/<task-id>` desde la base, el closeout se commitea ahí, integrate corre compuertas, empuja la rama y crea/actualiza el PR con `gh`, imprimiendo su URL. Repo: `deskops` (código en `deskops/`, tests en `tests/`, docs y CHANGELOG). Límites: no migrar rutas de máquina de deskops/sldb ni configurar desks de heyantonia; `push` debe quedar igual.

## AMBIGUEDADES

1. «título = el de la tarea»: el TaskDoc no tiene campo título y `summary` está vacío; obliga a inventar si sale del heading, del `id` o de otro sitio.
2. «el closeout si hace falta para commitear en la rama de la tarea»: no define qué artefacto es el closeout ni cuándo “hace falta”; obliga a inventar su contrato.
3. «Si el PR ya existe, solo empuja»: no indica cómo detectarlo (`gh pr view`, `gh pr list`) ni qué hacer con varios PRs; obliga a inventar el criterio.
4. «task/<task-id>, creada desde la base»: no aclara si `task-id` es el id completo ni qué ocurre si la rama ya existe o la base avanzó; obliga a inventar reset/rebase/ff.
5. «las mismas compuertas»: no enumera cuáles ni sobre qué diff se aplican; obliga a inventar el conjunto.
6. «un gh falso en PATH, un script que registra sus argumentos y devuelve una URL»: no fija formato de URL ni argumentos esperados; obliga a inventar el contrato del fake.
7. «start (simulado)»: no define cómo simularlo ni qué estado deja; obliga a inventar la fixture.
8. «desk/config.local.json … que está en .gitignore»: no aporta evidencia de que esté ignorado; obliga a asumirlo.

## DRY-RUN

Lecturas: `deskops/config.py`, `deskops/dispatch.py`, `deskops/integrate.py`, `tests/test_integrate.py`, `tests/test_dispatch.py`, docs de configuración, CHANGELOG y `.gitignore`. Cambios previstos: `IntegrateConfig.mode`; reap a rama de tarea; commit del closeout; push de `task/<id>` y `gh pr create`/actualización; tests de remoto protegido y regresión de `push`; documentación. Dependencias: remoto bare con hook que rechaza `dev`, `gh` falso, git y pytest. Validaciones futuras: el comando pytest indicado, suite completa `-n 4`, PR simulado con `--base dev`, `dev` intacta y modo `push` sin regresiones. Sin ejecutar nada.

## FUTURO

El coordinador migrará rutas de máquina a `config.local.json`; Governance configurará los desks de heyantonia; un humano aportará credenciales/`gh` autenticado y decidirá la estrategia de ramas si la base avanza; revisión y merge del PR quedan fuera de este nodo.
