## REFORMULACION
**Propósito:** corregir `extend_tip` en `deskops/integrate.py` para que extienda el tip a HEAD cuando HEAD ya contiene un merge de la rama remota y los commits posteriores al closeout solo afectan a `desk/`, `.sldb/` o `runs/`.

**Resultado:** cambio en `extend_tip` —y, si hace falta, en cómo recibe la ref remota—, dos tests nuevos en `tests/test_integrate.py`, entrada en `CHANGELOG`, y validación mediante pytest.

**Repo:** `deskops`, bajo `/mnt/ssd/proyectos/SLDB_1/deskops` según el cwd indicado.

**Límites:** dentro, `deskops/integrate.py`, `tests/test_integrate.py` y `CHANGELOG`; fuera, el resto de pasos de `integrate`.

## AMBIGUEDADES
1. «cfg.remote/cfg.branch, la misma que usa el paso fast-forward» no define la API/config real para obtener la ref remota; obligaría a inventar nombres, atributos o función existente.
2. «son solo de desk/, .sldb/ o runs/» no precisa el criterio de rutas: prefijo, directorio exacto, normalización o rutas anidadas; obligaría a inventar la regla de pertenencia.
3. «los archivos que cambian los commits de tip..HEAD que no están en la rama remota» frente a `HEAD ^tip ^<remoto>` admite lecturas distintas del rango; obligaría a inventar la semántica exacta.
4. «extend_tip devuelve HEAD cuando…» no indica qué debe devolver si no se cumplen las condiciones; obligaría a inventar el fallback.
5. «commit desde tu worktree con 'git commit -- <rutas>' y trailer Task-Id» no fija worktree ni formato exacto del trailer; obligaría a inventar ambos.

## DRY-RUN
**Lecturas:** `deskops/integrate.py`, `tests/test_integrate.py`, `CHANGELOG`, configuración remota y salidas de `git log`/`git diff`.

**Cambios previstos:** añadir test del merge remoto con commits posteriores solo de desk; añadir test de commit local de código que no debe extender; implementar comprobación de ancestro remoto y filtro de archivos; ajustar `extend_tip`; actualizar changelog.

**Dependencias:** repo git con remoto configurado, fixtures de tests, pytest.

**Validaciones futuras:** ejecutar `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_integrate.py` y comprobar que pasan los dos tests nuevos y el resto del archivo.

## FUTURO
Otro nodo o un humano deberá ejecutar la validación, revisar el commit y su trailer `Task-Id`, y decidir la integración/publicación del cambio.
