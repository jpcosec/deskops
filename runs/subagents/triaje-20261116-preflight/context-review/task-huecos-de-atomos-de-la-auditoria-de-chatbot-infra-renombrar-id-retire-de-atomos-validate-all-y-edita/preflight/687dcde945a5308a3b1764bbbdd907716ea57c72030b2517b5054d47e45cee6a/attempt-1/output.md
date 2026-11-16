## REFORMULACION
Encargo ejecutable, no agregado. Propósito: cerrar los huecos 1, 3, 4, 5 y 6 de la auditoría de Chatbot_Infra en el repo `deskops`. Resultado: por hueco, recibo de reproducción o constancia de no reproducción con comando y salida; si se reproduce, corrección con test. Alcance: `deskops/services/atoms.py`, `deskops/cli/registry.py`, `deskops/cli/commands/doctor.py` y tests; un desk sandbox por hueco. Fuera: citas código→átomo y repos de AntonIA. Límites: commits separados por corrección; validaciones pytest indicadas; aquí no se ejecuta nada.

## AMBIGUEDADES
1. «`deskops atoms rename <id> <nuevo-id>` que reescribe referrers con la API de sldb»: no define qué referrers, formato de id, colisiones ni atomicidad; obliga a inventar el contrato.
2. «retire acepta atomos o hay un verbo de retiro de atomos»: dos alternativas sin criterio; obliga a elegir interfaz.
3. «Sin verificar: 'atoms validate --all' marca toda la provenance como no resoluble (falso positivo masivo)»: no da comando reproducible ni salida esperada; obliga a inventar el escenario.
4. «un desk sandbox por hueco»: no indica creación, ruta ni aislamiento; obliga a inventar el procedimiento.
5. «doctor resuelve el store enlazado de deskops aunque se mueva el workspace»: no especifica movimiento permitido ni resultado esperado; obliga a inventar la prueba.
6. La validación no incluye test de doctor, rename, retire ni pills; «sin fallas nuevas respecto de main» no define la comparación.

## DRY-RUN
Lecturas: TaskDoc, `atoms.py`, `registry.py`, `doctor.py`, tests citados, comandos existentes y API sldb. Cambios previstos: reproducir cada hueco en sandbox; añadir rename; aceptar átomos en retire o nuevo verbo; corregir `validate --all`; verbo para `contexts/pills.md`; resolver store enlazado en doctor; test por hueco. Dependencias: CLI deskops, API sldb, desk sandbox y fixtures. Validaciones futuras: los cuatro pytest listados y comprobación manual de doctor; un commit por corrección.

## FUTURO
Un ejecutor produce recibos, parches, commits y tests. Un humano decide el contrato de rename/retire, acepta no reproducciones y valida la suite. Otro nodo puede revisar los commits.
