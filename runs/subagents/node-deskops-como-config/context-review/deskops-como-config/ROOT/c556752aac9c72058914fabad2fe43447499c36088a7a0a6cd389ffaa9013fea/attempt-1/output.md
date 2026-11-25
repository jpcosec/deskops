REFORMULACION
ROOT es el agregado del plan: deskops deja de tener motor propio y pasa a ser configuración sobre sldb —ciclo de vida, gates, vistas, escrituras y plantillas—, conservando formato del desk, gramática del CLI y autoridad de cierre. Resultado sustantivo: cuatro paquetes integrados: base (fachada limpia y plantillas como datos), reglas (invariantes, ciclo de vida, activación, cierre y consistencia), lecturas/escrituras vía sldb y cierre medido. Repo dueño: deskops. Límites: no escribir en sldb, no suplir reglas con Python, no tocar P4, no cambiar formato/CLI, no migrar desks ajenos. ROOT no ejecuta: termina cuando cierran sus hijos.

AMBIGUEDADES
ninguna.

DRY-RUN
ROOT no es ejecutable. Hipotéticamente: PF1 lee main con G_P0/G_GATES_FROZEN y GD26; entrega fachada sin lógica, specs duplicados eliminados y plantillas como datos, y transfiere una base limpia a PF2/PF3. PF2 lee PF1 más GO06/GO08/GO09 y DK6; entrega validadores de modelo, ciclo de vida con efectos, activación por RuleDoc/G_CONSUMER, cierre por recibos y validador de TaskDoc; transfiere contratos de configuración a PF3/PF4. PF3 lee PF2 más GD25 y GD22–GD24; entrega ViewDoc servidas por sldb serve y escrituras por transacción, borrando desk_view.py y doc_io.py; transfiere superficies migradas a PF4. PF4 lee todo lo anterior; entrega inventario config/código, 6 desks verdes, Board <1 s caliente y documentación. Validación conjunta: hijos cerrados, G_CONSUMER informado, invariante probado por hijo, CHANGELOG/docs al día, goldens y suite/doctor/Board sin regresiones; grep de código viejo vacío.

FUTURO
El supervisor promueve hijos y dispone revisiones; sldb entrega gates; el dueño fija N de CC51 (DA3); seguimientos DO2/DO3 y correcciones de TaskDoc los deciden operador/overlord.
