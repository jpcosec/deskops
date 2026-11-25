## REFORMULACION
El nodo es una tarea de código ejecutable: deskops debe empaquetar un RoleDoc `desk-identity` como YAML en `deskops/data/roles/`, instalarlo mediante `desk update --apply` e `init` sin sobrescribir uno existente, y añadir `--mode identity` a `runtime template` para generar un `agents.md` persistente que nombre la raíz del desk y el proyecto scion, sin worktree ni instrucciones de ejecutor/tester/coordinador. Resultado: rol instalable, modo identity funcional, tests y goldens actualizados. Límites: no crear el agente scion, no hook, no tocar repo scion, mapa de propiedad ni traducción de tools.

## AMBIGUEDADES
1. «lo que pide decisión de JP y decirlo» / «queda abierta si pide una decision de JP»: no hay criterio para distinguir una decisión de JP de una nota accionable; obligaría a inventar una política de clasificación.
2. «el destino de lo sin dueño que declare el desk»: no se especifica dónde ni con qué formato se declara ese destino; obligaría a inventar esquema y precedencia.
3. «un acuerdo cerrado en un hilo» y «la referencia del hilo»: no se define qué cierra un acuerdo ni el formato de referencia; obligaría a inventar ambos.
4. «si ningun RoleDoc de desk/roles tiene name desk-identity» frente a «un desk/roles/role-desk-identity.md existente, aunque tenga otro cuerpo, no se pisa»: no queda claro si la detección es por `name` o por ruta; obligaría a inventar la precedencia.

## DRY-RUN
Hipotético, sin ejecutar: leer el TaskDoc y los archivos listados; escribir primero los tests de `test_desk_sync.py` y `test_scion_runtime.py`; añadir el YAML, `package-data`, la función compartida de instalación en `desk.py`/`core.py`, la rama identity en `scion.py` y `choices` en `registry.py`; actualizar goldens con pytest y correr validaciones indicadas. Dependencia: `task-el-runtime-profile-traduce-los-tools...`. Validaciones futuras: los cuatro comandos pytest del apartado Validation.

## FUTURO
La tarea dependiente produce la traducción de tools y el alias de modelo. Otro nodo crea el agente scion y su hook. JP decide, al operar la identidad, las notas que requieren su decisión y el destino de lo sin dueño.
