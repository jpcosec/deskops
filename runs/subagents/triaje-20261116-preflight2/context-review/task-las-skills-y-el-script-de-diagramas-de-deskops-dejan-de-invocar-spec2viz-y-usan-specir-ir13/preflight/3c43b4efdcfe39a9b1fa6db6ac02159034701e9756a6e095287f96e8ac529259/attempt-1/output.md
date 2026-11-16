## REFORMULACION
El nodo debe migrar las dependencias versionadas de deskops que aún invocan `spec2viz` hacia `specir`/SLDB, en el repo deskops. Resultado: ninguna instrucción versionada de deskops menciona `spec2viz` como herramienta invocable, salvo `deskops/graph/desk_graph.py:75`, cubierto por otra tarea. Alcance: `.claude/skills/deskops-workflow/SKILL.md`, su referencia `spec2viz-cli.md` (reemplazada por remisión a `skills/use-specir/SKILL.md` del repo IR), `.opencode/skills/use-spec2viz/SKILL.md` (remisión corta, no borrado), `.opencode/skills/use-deskops/SKILL.md` y, solo si existe, `render_diagram.py`. Fuera: `desk_graph.py`, `.pi/skills`, repo IR. Debe aplicar la tabla de correspondencia, ejecutar validaciones y enviar a IR el hash del commit. No es agregado ni paquete: es un TaskDoc ejecutable por un ejecutor futuro.

## AMBIGUEDADES
1. “Menciones historicas (p. ej. 'spec2viz se archiva') se dejan”: no define el límite entre mención histórica y mención operativa; obligaría a inventar un criterio de clasificación.
2. “Reescribir cada mencion con la tabla del goal”: la tabla no cubre toda frase posible sobre `spec2viz`; obligaría a inventar redacción para casos no mapeados.
3. “.opencode/skills/use-deskops/SKILL.md”: no se cita ningún fragmento concreto ni el cambio esperado; obligaría a inferir qué menciones contiene.
4. “no lista nada de deskops salvo deskops/graph/desk_graph.py:75”: no fija el formato exacto de salida aceptable; obligaría a inventar el criterio de comparación.

## DRY-RUN
Lecturas previstas: los cinco archivos del campo `files`, la nota de IR, `IR/docs/spec2viz/correspondencia-cli.md` y `skills/use-specir/SKILL.md`. Cambios previstos: buscar `spec2viz`; editar menciones operativas en skills; reemplazar la referencia CLI por remisión; convertir `use-spec2viz` en remisión; ajustar `use-deskops`; con `test -f`, cambiar líneas 7 y 9 de `render_diagram.py` si existe. Dependencias: archivos presentes, repo IR y su `.venv`, `specir retirement check`, pytest, y que JP no haya retirado el plan. Validaciones futuras: `specir retirement check --path deskops=...`; `pytest tests/test_skill_cli_drift.py`; `pytest tests/test_closeout_skill_links.py`; envío del mensaje a IR con el hash.

## FUTURO
JP decide si el plan `workspace-documental` sigue existiendo. El repo IR y su comprobador producen la señal de aceptación. El ejecutor genera el commit y su hash; IR recibe y verifica la respuesta.
