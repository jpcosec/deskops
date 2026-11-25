## REFORMULACION

**Propósito:** registrar que `deskops status` deje de imprimir solo `Deprecated` y entregue un estado rápido del desk: tareas activas, inbox abierto y alertas baratas, sin ejecutar el doctor completo. **Resultado:** la funcionalidad la implementa V1 del frente velocidad-hooks, no este desk; esta tarea la registra y se cierra con `resolved-by` cuando V1 entre. **Repo/superficie:** `deskops/cli/commands` (status), con medición mediante el “benchmark V0 del repo sldb”. **Límites:** sin subprocess de `sldb`; no implementar aquí; validación con benchmark V0; criterio de cierre: menos de 3 s en caliente y salida que no sea solo `Deprecated`. Es un nodo no ejecutable de registro/seguimiento, sin hijos (`atoms: []`, `depends_on: []`).

## AMBIGUEDADES

1. “La implementa V1 del frente velocidad-hooks (supervisor 15-11), no este desk por su cuenta”: no queda claro si el ejecutor debe implementar, verificar o solo esperar; obligaría a inventar su rol.
2. “benchmark V0 del repo sldb”: no define comando, ruta, repo exacto ni métricas; obligaría a inventar el procedimiento.
3. “menos de 3 s en caliente”: no fija umbral en frío ni cómo calentar; obligaría a inventar el criterio completo.
4. “alertas baratas”: no enumera cuáles son; obligaría a inventar el conjunto.
5. “se cierra con resolved-by”: no define formato, responsable ni evidencia; obligaría a inventar el mecanismo de cierre.
6. “sin subprocess de sldb”: no indica de dónde obtiene el estado; obligaría a inventar la fuente de datos.

## DRY-RUN

Lecturas: TaskDoc y la referencia del inbox; no hay especificación de V1 ni benchmark V0 adjuntos. Cambios previstos: ninguno en código; solo registro/seguimiento y, cuando exista V1, eventual actualización de estado/cierre. Dependencias: V1 externa, benchmark V0 y mecanismo `resolved-by`. Validaciones futuras: ejecutar V0 en caliente y frío, comprobar salida distinta de solo `Deprecated` y menos de 3 s en caliente. Al no tener hijos, no hay transferencia interna entre nodos; la validación conjunta queda externalizada en V1 y V0.

## FUTURO

V1 produce la implementación; el benchmark V0 produce las mediciones; un humano o nodo de cierre decide y registra `resolved-by`.
