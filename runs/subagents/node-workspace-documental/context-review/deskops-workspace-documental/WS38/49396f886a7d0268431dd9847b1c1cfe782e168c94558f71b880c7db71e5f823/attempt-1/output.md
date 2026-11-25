## REFORMULACION
WS38 es un nodo `delivery` documental, no un agregado. Su propósito es publicar en el manual la operación de delegación y la revisión trazable tal como quedaron demostradas en WS37. El resultado esperado es una actualización de `docs/workspace-user-manual.md` y átomos vinculados en `desk/atoms/`. Repo dueño: `deskops`. Límites: documentar solo lo ocurrido en WS37; cada paso debe remitir al acta y a operaciones reales; deben documentarse los fallos registrados; cada acuerdo durable debe quedar vinculado a un átomo, reutilizando uno de WS31 si cubre la regla o creándolo solo si no existe equivalente; no atomizar permisos de una sola sesión; indicar que G_EXEC es necesario para operar. Depende de WS37 y WS31, y requiere G_HUMAN_DELEGATE.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
Un ejecutor futuro leería el nodo WS38, la guía, `brief.md`, `alcance.md`, `decisiones.md`, el acta de WS37 en `runs/subagents/workspace-documental-acceptance/delegacion/acta.md`, el manual y los átomos existentes de WS31, y el estado de G_HUMAN_DELEGATE. Cambios previstos: ampliar `docs/workspace-user-manual.md` con el capítulo de delegación y revisión trazable; enlazar cada paso al acta y a operaciones reales; documentar los fallos del acta; buscar átomos de WS31 por regla durable, enlazar/actualizar el equivalente o crear uno nuevo; indicar la necesidad de G_EXEC. Dependencias: acta y gate producidos por WS37; manual básico y átomos de WS31. Validaciones futuras: links resolubles, remisiones verificables al acta, fallos cubiertos, átomo vinculado por acuerdo durable, ausencia de átomos de permisos de sesión y mención explícita de G_EXEC.

## FUTURO
WS37 produce el acta de delegación y resuelve G_HUMAN_DELEGATE; WS31 produce el manual básico y los átomos reutilizables; un actor externo decide G_EXEC; la promoción fijará la redacción exacta y los archivos concretos dentro de la aceptación.
