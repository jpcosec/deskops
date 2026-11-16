# Veredicto del tester deskops-t-9da54e09a30a

- task: task-la-regla-de-desk-graph-sobre-specs-deja-de-nombrar-spec2viz-y-reconoce-los-specs-yaml-sincronizados
- role: tester (independiente, agente claude, sesión fresca)
- run_id: run-deskops-t-9da54e09a30a · session: scion://agent/deskops-t-9da54e09a30a · session_sha256: (no disponible desde dentro de la sesión)
- entrega verificada: cambios sin commitear del ejecutor deskops-e-4ba5a0d9443c

## VEREDICTO: APROBADO

## Hallazgos

1. Diff conforme al contrato (scope + precisión 1 del preflight-1):
   - deskops/graph/desk_graph.py:75: la única línea cambiada; `path_prefixes` pasa de
     `("spec", "docs/architecture/spec2viz")` a `("spec", "docs/architecture")`. `suffixes=_SPEC`
     (.md/.yaml/.yml) y el orden de FILE_RULES no cambian. Ningún otro cambio en el archivo.
   - tests/test_graph_extract_sources.py:45-58: test nuevo
     `test_extract_source_file_nodes_reads_spec_yaml_under_docs_architecture` (nombre al estilo
     del archivo, precisión 1 del bundle-1), sobre un sandbox `tmp_path`;
     `docs/architecture/diagrams/desk-flow.yaml` sale con kind `spec` y file_kind `spec`, y
     `spec/artifacts/atom.yaml` sigue en file_kind `spec`. Ningún test existente se tocó.
   - Nada fuera de `files` del TaskDoc: no se tocaron test_graph_snapshot.py ni
     test_graph_missing_existing_files.py (precisión 3 del bundle-1); los cambios de `.sldb/` y
     `runs/subagents/2026*` del git status vienen de antes, del lanzador.
2. Validación (corrida por mí, un archivo cada vez, TMPDIR=/dev/shm, sin lock):
   extract_sources 17 passed · snapshot 10 passed · missing_existing_files 7 passed ·
   extract_docs 2 passed · checks 4 passed; todos rc 0.
   `grep -n spec2viz deskops/graph/desk_graph.py`: sin coincidencias, rc 1.
3. Reproducción: copia de HEAD (git archive) más el test nuevo en /dev/shm. El test nuevo
   FALLA (1 failed, 16 passed; falta `spec:docs/architecture/diagrams/desk-flow.yaml`) y el
   import sale de la copia (se verificó `__file__`). El test discrimina el cambio. La copia
   se borró después.
4. Grafo real: `deskops graph missing --root .` → "36 missing, 0 informational" (sin cambios).
   deskops no tiene docs/architecture/, así que la regla no altera los nodos reales.
5. Done When cumplido: grep vacío, el YAML del sandbox bajo docs/architecture se extrae como
   nodo de file_kind spec, y los tres archivos de la Validation pasan.

## Riesgos y notas (no bloquean)

- Ensanchamiento intencional (precisión 1 del preflight-1): cualquier .md/.yaml/.yml bajo
  docs/architecture/ se convierte en nodo `spec` por la FileRule. En los repos que tengan
  Markdown narrativo ahí podrían aparecer nodos spec nuevos. Hoy no afecta a deskops.
- No se corrieron la suite completa ni `stores build --check`, por orden del integrador wA:p1.
  Quedan para el integrador.
- Ruido en validation.log: probé `deskops graph missing --format json` y falló (no es una opción
  válida, la salida no es JSON). No influye en el veredicto; el conteo sale de la salida en texto.
