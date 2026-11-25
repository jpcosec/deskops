## REFORMULACION
WS44 es un nodo de validación, no un agregado. Encargo: comprobar, mediante probe read-only, el acceso público a Scion para el ramal E y satisfacer G_SCION. Resultado: `auditoria/scion-probe.md` con respuesta pública real, identidad del operador, Hub, fecha y capabilities. Repo dueño: deskops. Límites: no crear agentes, enviar mensajes, cambiar configuración ni mostrar secretos; sin registro en `autorizaciones/scion.md` no hay probe; si `auditoria/scion.md` no mapea capabilities requeridas por WS32/WS33, se detiene y registra el hueco. Depende de WS05 y WS07; requiere G_PRODUCT.

## AMBIGUEDADES
1. «verifica capacidades/identidad necesarias para intento y mensajes» frente a «Sin crear agentes, enviar mensajes». No se define qué llamada read-only demuestra la capacidad de mensajes ni qué respuesta cuenta como éxito; obligaría a inventar el criterio o a exceder el límite.
2. «El operador indica el Hub desde la configuración existente». No se nombra archivo, clave ni qué hacer si esa configuración no contiene Hub; obligaría a inventar la fuente o el fallback.

## DRY-RUN
Lecturas: `auditoria/scion.md` de WS05, `decisiones.md`/`owner-decisions.json` de WS07, `autorizaciones/scion.md`, configuración Scion sin secretos y API pública documentada. Cambios previstos: solo `auditoria/scion-probe.md`. Dependencias: designación del operador y registro de acceso por el solicitante, Hub indicado por el operador, mapeo de capabilities por WS32/WS33 en el inventario, y G_PRODUCT. Validaciones futuras: ejecutar probe real read-only; comprobar identidad del operador, Hub, fecha y capabilities; no exponer secretos; si falta contrato, acceso o mapeo, detenerse y registrar el hueco; tras cambio de Hub/API/credencial, repetir e invalidar recibo previo. Sin ejecutar nada.

## FUTURO
El solicitante designa operador y registra su acceso; WS05 produce inventario y mapeo de capabilities; WS32/WS33 los consumen. WS44 produce el recibo de probe y un humano o verificador lo acepta; solo entonces G_SCION puede cambiar. Nada de eso se decide en esta revisión.
