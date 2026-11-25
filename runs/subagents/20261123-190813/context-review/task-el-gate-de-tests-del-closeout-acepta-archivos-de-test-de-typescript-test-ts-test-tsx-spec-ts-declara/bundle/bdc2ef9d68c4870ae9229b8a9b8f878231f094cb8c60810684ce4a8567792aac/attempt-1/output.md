REFORMULACION  
Este nodo es una tarea ejecutable (`task.code`), no un agregado. Propósito: que el gate de tests del closeout reconozca evidencia de tests TypeScript/vitest. Resultado: `reference_points_to_test` acepta archivos existentes `.test.ts`, `.test.tsx`, `.spec.ts` y `.spec.tsx` dentro del repo, fuera de `node_modules` y directorios ocultos, ubicados en un directorio de tests o declarados en `files`; el rechazo `--test` nombra los sufijos. Repo: `deskops`; superficie: `deskops/services/closeout_gates.py` y tests del closeout. Límites: no ejecutar tests JS desde deskops; fuera de alcance correr vitest/surface.

AMBIGUEDADES  
1. Cita: “(*.test.ts, *.test.tsx, *.spec.ts)”; Goal añade “.spec.tsx”. Obliga a inventar el conjunto final de sufijos.  
2. Cita: “en un directorio de tests o declarados en files”. No define directorio de tests para TS (`tests/`, `__tests__/`, `src/`). Obliga a inventar la lista.  
3. Cita: “fuera de node_modules y directorios ocultos”. No aclara si “ocultos” son nombres con punto ni si se excluye cualquier nivel. Obliga a inventar la regla.  
4. Cita: “El mensaje de rechazo nombra los sufijos aceptados”. No fija el texto exacto. Obliga a inventar la redacción.  
5. Cita: “deskops/services/closeout_gates.py:166” frente a “tests/test_closeout_test_paths.py”. La raíz del repo no queda explícita. Obliga a inventar cwd/layout.

DRY-RUN  
Sin ejecutar: leería TaskDoc, `closeout_gates.py:166` y `tests/test_closeout_test_paths.py`, `tests/test_closeout_gates.py`; localizaría helper de sufijos y fixtures. Cambios previstos: ampliar predicado de sufijos, aplicar exclusiones `node_modules`/ocultos, actualizar mensaje y añadir tests con `.test.ts` declarado y en `node_modules`. Dependencias: layout real del repo, fixtures existentes, pytest/TMPDIR. Validaciones futuras: los dos pytest indicados; además, `closeout verify` de una tarea con commit vitest como prueba de aceptación.

FUTURO  
Un nodo ejecutor implementará y correrá pytest; un humano decidirá sufijos/directorios/mensaje si persisten. El closeout real de la tarea vitest aportará validación end-to-end; el Board/gobernanza aceptará o rechazará el cambio.
