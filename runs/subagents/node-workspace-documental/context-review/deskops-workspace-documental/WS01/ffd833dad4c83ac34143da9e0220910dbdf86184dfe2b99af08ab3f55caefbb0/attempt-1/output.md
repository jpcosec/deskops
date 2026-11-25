REFORMULACION
Propósito: fijar un brief y glosario autosuficientes para el workspace documental. Resultado: `brief.md` en el repo `deskops`, enlazando `decisiones.md` como registro Pxx completo. Límites: no editar `decisiones.md`; no reescribir si no cambió decisión/contrato; si cambia el encargo, editar solo `brief.md` con acuerdos textuales y vocabulario documento/nodo/vista/renderer/consulta/foco, sin chat invisible. Sin dependencias declaradas. La cobertura documental satisface la elaboración del brief, no el lifecycle cerrado ni autorización de producto.

AMBIGUEDADES
1. «Brief/glosario ya authored y cubiertos por recibo covered_work». No se define qué es el recibo `covered_work`, quién lo produce, dónde está ni cómo se comprueba su hash/alcance; el ejecutor tendría que inventar la evidencia o el criterio de cobertura.
2. «Si cambia realmente el encargo». No se fija quién determina ese cambio ni con qué umbral; el ejecutor tendría que inventar cuándo corresponde editar `brief.md` y cuándo conservarlo.

DRY-RUN
Lecturas previstas: `brief.md`, `decisiones.md`, nodo WS01 y guía de revisión. Cambios previstos: solo `brief.md`, y solo si se acredita cambio real de encargo; verificar enlace a `decisiones.md`, acuerdos textuales con actor/fuente y distinciones del glosario. Dependencias: ninguna directa; comprobar el recibo `covered_work` y hash/alcance si existe. Validaciones futuras: revisión del coordinator comparando reformulación/dry-run con la intención y explicitando hallazgos/disposición; `APTO` no basta. Nada se ejecuta aquí.

FUTURO
El coordinator compara la revisión barata aislada con la intención y registra hallazgos/disposición. La promoción/auditorías verifican hash y alcance del brief. No se deduce autorización de producto, lifecycle cerrado ni permiso de implementación.
