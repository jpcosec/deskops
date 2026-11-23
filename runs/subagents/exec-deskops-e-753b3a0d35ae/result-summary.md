# Resultado
Modo `pr` implementado.
- deskops/config.py: IntegrateConfig.mode ('push' por defecto | 'pr').
- deskops/dispatch.py: en modo pr reap crea task/<id> desde la base, la deja checked out en el checkout principal (el closeout cae en ella) y trae ahi los commits del ejecutor; la base no se toca. start acepta estar en task/*, y el worktree sale de HEAD.
- deskops/integrate.py: en modo pr mismas compuertas sobre el tip; empuja task/<id>, `gh pr list` y si no hay PR abierto `gh pr create --base <branch> --head task/<id>`; imprime `PR: <url>`; dry-run no empuja; tools_checkout no se toca.
- tests/test_integrate.py (3 tests: remoto con pre-receive que rechaza dev + gh falso; PR existente; dry-run), tests/test_dispatch.py (reap en pr), docs/operator-manual.md (modos y config.json vs config.local.json), CHANGELOG.md.
Limite: el test de integrate arranca desde un repo ya cerrado con la rama task/<id> en el tip; no ejecuta el closeout real sobre task/<id> (cae en HEAD por construccion).
Validacion: ver validation.log. test_integrate.py bajo -n 4 dio errores de fixture por carga; en serie 28 passed. La falla de la suite completa es el test corregido despues de que arrancara; pasa suelto.
Revisar: elección de `gh pr list` para detectar PR existente; push sin force.
