**REFORMULACION**
Propósito: que el cierre de una nota del desk conserve el motivo del ack. Resultado: `deskops message ack <selector> --reason <texto>` marca la nota como acknowledged y guarda el texto en un campo opcional `ack_reason`; sin `--reason`, el ack funciona como hoy y `ack_reason` queda vacío; `deskops message read` muestra `ack_reason` cuando existe. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops` (deskops). Límites: tocar el modelo, el registro/CLI de `message`, la salida de `read` y tests; no migrar notas existentes ni afectar otros desks; esta revisión no ejecuta nada. Validación prevista: los tres pytest indicados en el TaskDoc.

**AMBIGUEDADES**
1. “y lo que el store necesite para declararlo”: no enumera archivos ni esquema del store; obligaría a inventar si hay cambios fuera de `deskops/models/inbox.py`.
2. “ack_reason queda vacio”: no define si será campo ausente, `null` o cadena vacía; obligaría a inventar el contrato de render/roundtrip y el efecto en notas viejas.
3. “message read muestra ack_reason cuando existe”: no fija si aplica a texto, JSON o ambos, ni dónde aparece; obligaría a inventar el formato exacto.
4. “Correr test_command_registry.py y los goldens de ayuda”: esos archivos no están en `files`; obligaría a inventar qué goldens se actualizan y si `tests/test_command_registry.py` ya existe.

**DRY-RUN**
Lecturas hipotéticas: `deskops/models/inbox.py`, `deskops/cli/registry.py`, `deskops/cli/commands/message.py`, `tests/test_message_cli.py`, más patrones de campos opcionales y ayuda. Cambios previstos: añadir `ack_reason` opcional con default vacío y su marcador de plantilla; declarar `--reason` en `ack`; en `_ack_note`, persistir el motivo junto con `acknowledged_by/at`; en `read`, incluir `ack_reason` en detalle/texto; añadir tests de ack con/sin razón y nota vieja. Dependencias: validación roundtrip de SLDB, tracking del store, ayuda CLI y goldens. Validaciones futuras: ejecutar los tres pytest de la sección Validation y registrar el cambio en un commit descriptivo, según el átomo de cierre.

**FUTURO**
El ejecutor implementará, correrá los tests y hará el commit. Revisión/CI y merge quedan fuera de este nodo. La migración de notas viejas y otros desks quedan explícitamente fuera; un humano decidirá cualquier ampliación de alcance si el store exige cambios no previstos.
