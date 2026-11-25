REFORMULACION
Propósito: inventariar las superficies concretas de Deskops y todas sus operaciones públicas, con evidencia comprobable. Resultado: `auditoria/deskops.md`, una fila por superficie, con ubicación, operaciones que la leen/mutan o «dato pasivo», y estado comprobado/no comprobado con causa. Repo dueño: deskops. Límites: archivos de categorías enumeradas bajo `desk/` de este checkout, comandos CLI públicos y métodos de `DeskopsOperations`, modelos registrados que sirven esas superficies y store local `.sldb`; no inventariar binarios ajenos ni inferir modelo por carpeta. Es un nodo de planificación/auditoría, no un agregado ni una implementación.

AMBIGUEDADES
1. «firmas públicas, efectos Git y cierre.» El alcance define «cierre» (`deskops closeout verify|commit`) pero no qué cuenta como «efecto Git». Obligaría a inventar si incluye commits, staging, estado, hooks u otras mutaciones, y dónde buscarlas; una omisión o ampliación alteraría el inventario.

DRY-RUN
El ejecutor leería el nodo y el brief/glosario de WS01; recorrería los archivos de las categorías bajo `desk/`, la ayuda/comandos públicos de Deskops, `DeskopsOperations`, `sldb models list` y el store local `.sldb`. Cambios previstos: crear/editar solo `auditoria/deskops.md`; no tocar código, store ni otros repos. Dependencia directa: WS01. Validaciones futuras: cada fila con ubicación y lista completa de operaciones; evidencia `archivo:línea`, hash/listado read-only o salida de comando; marcar «no comprobado» con causa; no inferir modelo por carpeta; no incluir binarios ajenos.

FUTURO
WS01 aporta el brief/glosario. WS06 y WS10 consumen la auditoría para reconciliación y manual; el coordinador revisa el encargo. Ninguna decisión humana de producto corresponde a WS02; la falta de store se reporta, no se resuelve aquí.
