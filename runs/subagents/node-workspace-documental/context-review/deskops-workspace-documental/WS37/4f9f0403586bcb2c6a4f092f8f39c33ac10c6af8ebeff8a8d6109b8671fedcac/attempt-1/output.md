## REFORMULACION

**Propósito:** validar con un agente real el flujo UF06 (pregunta, intervención, corrección, evidencia, decisión y cierre mediante el handoff de WS28), con un actor humano.
**Resultado:** acta de validación humana que satisface `G_HUMAN_DELEGATE`, guardada en el repo dueño.
**Repo:** `graph_ui`.
**Límites:** no sustituir la integración por mocks ni dar por completado lo que solo es aprobación; el `output_scope` se restringe a `runs/subagents/workspace-documental-acceptance/delegacion/`; no bloquea WS31. Requiere `G_EXEC` y `G_SCION`.

## AMBIGUEDADES

1. «UF06 real: pregunta/intervención/corrección/evidencia/decisión» — el input no define UF06 ni nombra quién lo produce; obligaría a inventar el recorrido, sus pasos y el resultado esperado para poder validarlo.
2. «protocolo de validacion-humana.md (guion, acta en runs/subagents/workspace-documental-acceptance/delegacion/)» — no se suministra el protocolo ni se identifica su productor; obligaría a inventar guion, criterios y formato del acta.

## DRY-RUN

Sin ejecutar:
- **Lecturas:** `dag.yaml` (WS37, gates `G_EXEC`/`G_SCION`, `G_HUMAN_DELEGATE`), protocolo `validacion-humana.md`, evidencia de cierre/handoff de WS28, salida de WS36 (adaptador WS34 y registro WS33.2), `autorizaciones/scion.md`.
- **Cambios previstos:** crear el acta en `graph_ui:runs/subagents/workspace-documental-acceptance/delegacion/` con actor humano, versión, guion, resultado y soportes; registrar el recibo de `G_HUMAN_DELEGATE`.
- **Dependencias:** WS36 y WS30 completos y conformes; `G_EXEC` autorizado por el solicitante/designee y `G_SCION` verificado por WS44. Si falta contrato, API o permiso: detenerse y registrar el hueco, sin sustituto.
- **Validaciones futuras:** recorrido UF06 real sin mocks; evidencia enlazada de WS33.1/WS33.2; errores de API/permisos visibles; `completed` no equivale a aprobación.

## FUTURO

WS38 documentará la operación usando el acta de WS37 y enlazará átomos de WS31. `G_HUMAN_DELEGATE` quedará resuelto por WS37; `G_SCION` por WS44; `G_EXEC` por el resolutor externo. WS31 no depende de WS37.
