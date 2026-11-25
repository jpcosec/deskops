## REFORMULACION

Propósito: documentar para qué sirve `desk/hitl` y el resto de carpetas de `desk/`, y que `doctor` detecte archivos de agentes en `hitl/`. Resultado: `deskops about` y `deskops faq` describen cada carpeta de `desk/` (incluida `hitl/`); `doctor` emite una alerta cuando `desk/hitl` contiene archivos que no son para el humano; el criterio de "para el humano" queda declarado como dato. Repo: paquete `deskops` (`deskops/about.py`, faq del paquete, `deskops doctor`) en workspace `desk`. Límites: no se fija aquí el conjunto de carpetas, el formato del dato ni la severidad de la alerta; tampoco se incluye corregir el enrutado `--to deskops`.

## AMBIGUEDADES

1. "deskops about y deskops faq describen cada carpeta de desk/" — no se enumeran las carpetas ni dónde vive la faq. Obligaría a inventar el listado y el artefacto.
2. "criterio de 'para el humano' declarado como dato, no a mano en el codigo" — sin ruta, formato ni esquema. Obligaría a inventar la configuración.
3. "doctor emite una alerta" — sin severidad, texto, código de salida ni canal. Obligaría a inventar el contrato.
4. "test nuevo de deskops (nombre a fijar al promover)" — nombre y ubicación indeterminados. Obligaría a inventar path y nombre.
5. "un archivo de agente y uno humano en desk/hitl" — no define qué rasgo distingue cada fixture. Obligaría a inventar el criterio operativo.
6. "Origen: ... --to deskops no resolvia" — no aclara si arreglarlo entra en alcance. Obligaría a inventar el límite.

## DRY-RUN

Hipotético, sin ejecutar: lecturas de `about.py`, fuente de la faq, módulo `doctor`, tests existentes y árbol de `desk/`; cambios previstos: contenido de about y faq, dato del criterio, comprobación en `doctor`, test nuevo; dependencias: enumeración de carpetas y esquema del dato; validaciones futuras: ejecutar suite y `doctor` con fixtures agente/humano.

## FUTURO

Humano decide lista de carpetas, criterio "para el humano" y severidad; nodo de promoción fija el nombre del test; otro nodo redacta el contenido de about/faq.
