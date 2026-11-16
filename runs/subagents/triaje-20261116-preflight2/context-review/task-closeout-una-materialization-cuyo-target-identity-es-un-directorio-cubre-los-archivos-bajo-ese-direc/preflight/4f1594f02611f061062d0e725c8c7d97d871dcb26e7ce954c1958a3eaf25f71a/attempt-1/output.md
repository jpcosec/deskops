REFORMULACION
Propósito: que en deskops un archivo cambiado quede cubierto por una materialization de la tarea cuando su target_identity sea el archivo o un directorio que lo contenga. Resultado: helper de cobertura por prefijo en deskops/services/closure.py, uso en la lógica de cobertura, test de directorio vs archivo y nota a sldb si `deskops graph missing` marca missing_declared_target para un directorio. Repo: /mnt/ssd/proyectos/SLDB_1/deskops. Límites: no modificar sldb ni la compuerta de átomos; rutas POSIX relativas, sensibles a mayúsculas, sin symlinks ni barra final; el directorio no necesita existir; esta tarea no espera respuesta de sldb. Nodo de tarea ejecutable, no agregado/paquete.

AMBIGUEDADES
1. "la funcion se llama target_covers(target, path)" frente a "1) Funcion covers(target, path)". Obliga a inventar el nombre definitivo del helper.
2. "Si `deskops graph missing` reporta missing_declared_target para un target que es directorio" y "cuerpo con la salida de graph missing": no fija formato/alcance exacto de la salida que debe copiarse en la nota. Obliga a inventar qué fragmento se adjunta.
3. "exito = nota entregada": no define evidencia verificable de entrega. Obliga a inventar si vale el stdout de `message send` o hace falta recibo.

DRY-RUN
Lecturas hipotéticas: TaskDoc, pill de contratos, closure.py junto a cobertura, test file, fixtures de sandbox y ayuda de graph/message. Cambios previstos: helper target_covers (o nombre que se resuelva) con normalización indicada; sustituir búsqueda exacta por cobertura; añadir test `pkg/sub` cubre `pkg/sub/a.py` y no `pkg/subzero.py`. Dependencias: API interna de closure, fixtures de test, sandbox desk, CLI graph/message. Validaciones futuras: pytest del test, closeout_gates, closeout; suite completa; fallas comparadas en worktree limpio de origin/main. Sin ejecutar.

FUTURO
El nodo ejecutor implementará y correrá pruebas; producirá commit/informe con fallas baseline y, si aplica, nota enviada citada. sldb decide si acepta directorios; su respuesta no bloquea. Un humano/revisor valida cierre y merge.
