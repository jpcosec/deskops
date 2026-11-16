## REFORMULACION

El nodo debe migrar DeskOps para que ninguna pieza versionada instruya a invocar `spec2viz`, salvo `deskops/graph/desk_graph.py:75`, cubierto por otra tarea. El resultado esperado es reemplazar las menciones en las skills `.claude` y `.opencode`, la referencia `spec2viz-cli.md` y, condicionalmente, `render_diagram.py`, usando la correspondencia CLI de IR. Repo principal: DeskOps; se consulta IR en solo lectura. Límites: no tocar el repo IR, `desk_graph.py` ni `.pi/skills`. El cierre exige comprobador de IR sin hallazgos de DeskOps —salvo `desk_graph.py:75`—, dos tests concretos y respuesta a IR con el hash del commit.

## AMBIGUEDADES

1. «se borra o queda como remision a use-specir»: obliga a inventar qué opción elegir para `.opencode/skills/use-spec2viz/SKILL.md`; requiere decisión humana o criterio no incluido.
2. «si el plan sigue existiendo (si JP lo retiro, no hay nada que hacer ahi)»: obliga a inventar cómo verificar la existencia y quién es JP o cómo constatar su retiro.
3. «Reescribir cada mencion con la tabla del goal»: obliga a inventar el tratamiento de menciones en prosa que no correspondan exactamente a un comando CLI.
4. «Correr los tests de skills»: no identifica un comando único; obliga a inventar si bastan los dos tests de Validation o hay otro conjunto.

## DRY-RUN

Lecturas previstas: los cinco archivos de `files`, la nota de inbox referenciada, `IR/docs/spec2viz/correspondencia-cli.md` y `skills/use-specir/SKILL.md`. Cambios previstos: sustituir comandos según la tabla; reemplazar o borrar `spec2viz-cli.md`; resolver `use-spec2viz`; ajustar `use-deskops`; editar líneas 7 y 9 de `render_diagram.py` si existe. Dependencias: acceso de lectura a IR, decisión sobre borrado/remisión, decisión sobre el plan de JP. Validaciones futuras: `specir retirement check --path deskops=...`; `pytest -q tests/test_skill_cli_drift.py`; `pytest -q tests/test_closeout_skill_links.py`. No se ejecuta nada.

## FUTURO

Un humano decide borrar o convertir `use-spec2viz` en remisión y confirma si JP retiró el plan. Otro nodo o el ejecutor produce el commit, su hash y el mensaje a IR; IR recibe y valida la respuesta.
