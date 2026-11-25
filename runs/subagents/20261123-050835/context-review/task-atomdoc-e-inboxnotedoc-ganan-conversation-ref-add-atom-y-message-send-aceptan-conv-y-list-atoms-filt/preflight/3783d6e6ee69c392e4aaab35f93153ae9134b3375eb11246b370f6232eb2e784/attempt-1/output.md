## REFORMULACION

Encargo ejecutable de código en el repo `deskops` (worktree que dará dispatch). Propósito: dar a `AtomDoc` e `InboxNoteDoc` un campo `conversation_ref: str | None` para la referencia `<hilo>/<id>` o `<hilo>`, y exponerlo en CLI. Resultado: (1) modelos con el campo, vacío = no escrito; (2) `add atom --conv` y `message send --conv` lo rellenan; (3) `list atoms --conv <hilo>` filtra por igualdad o prefijo `<hilo>/` e incluye el campo en JSON; (4) `add atom` rechaza duplicado exacto con stderr `"ya existe <atom id> con conversation_ref <ref>"` y código 1. Límites: no toca `deskops/cli/commands/atoms.py`, no crea verbo `add agreement`, no migra atoms antiguos. Incluye tests, hashes de contrato, tres goldens de ayuda y `sldb models update` de ambos modelos.

## AMBIGUEDADES

1. «deskops message send --conv <ref> lo llenan» frente a «flags ("--conversation-ref", "--conv")»: no se dice si `message send` también acepta `--conversation-ref` o solo `--conv`; obligaría a inventar el nombre largo.
2. «sldb models update AtomDoc --store .sldb --pythonpath .»: no se aclara si reescribe documentos existentes añadiendo `conversation_ref: null` o solo el esquema; obligaría a inventar el efecto sobre atoms viejos.
3. «regenerar goldens ... --update-golden»: se asume que ese flag de pytest existe; no consta en el input; obligaría a inventar el mecanismo de regeneración.
4. «vacío = None o solo espacios, no se escribe»: no se dice si aplica también a `list --conv` o a `message send`; obligaría a inventar el comportamiento del filtro con `--conv ""`.
5. «duplicado = otro atom con conversation_ref exactamente igual (tras strip)»: no se acota el universo (todo el store vs. mismo hilo); aunque la frase sugiere global, obligaría a inventar el alcance.

## DRY-RUN

Lecturas: los 14 ficheros listados, `parse_input.py`, `doc_access`, configuración de goldens. Cambios previstos: campo en dos modelos; flags en `_add_subject_commands` y `_list_subject_commands`; filtro en `DeskopsOperations.list_atoms`/`AtomsService.list_atoms`; chequeo de duplicado en rama `add`; `_deliver_note` añade el campo; cuatro tests; hashes y tres goldens; `sldb models update` ×2. Dependencias: `create_artifact`, generador de flags por campos, plugin de goldens, CLI `sldb`. Validaciones futuras: los cuatro pytest de Validation, más `deskops doctor --root .` y `sldb stores check --store .sldb`. Nada ejecutado.

## FUTURO

Dispatch entrega worktree y revisa el commit con trailer `Task-Id`; un humano valida el diff de goldens y el mensaje de stderr; CI ejecuta la suite completa.
