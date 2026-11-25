# Propuesta: agente de coherencia del desk (para revisar si sirve)

Fecha: 2026-11-25. Estado: propuesta, sin decisión. Pedido de JP: "deja una propuesta, después revisamos si sirve de
algo hacer esto". Base: `diagnostico.md` (capa 2) y la decisión D4 (deskops exige git).

## Qué problema resuelve

Hoy la coherencia entre el desk y el código se revisa solo bajo demanda y por piezas sueltas (`doctor`, `graph
missing`, `drift`, `stores build --check`), y nada reacciona a una mutación. Además `doctor` marca mutaciones normales
como errores (220 en un clon limpio de main), así que su señal no sirve.

## Dos partes, separadas por costo

1. **Chequeo determinista (sin modelo de lenguaje).** Barato, corre siempre:
   - qué cambió: `git status --porcelain` y `git diff --name-only <último commit revisado>` (35-70 ms medidos);
   - el store frente al árbol: lo que hoy hace `sldb stores build --check`, separando mutación (alerta) de rotura (error);
   - referencias rotas: archivos que nombran tareas, átomos o anclas de código y ya no existen;
   - cambios fuera de su tarea: archivos tocados que aparecen en `files` de una tarea activa distinta a la del commit
     (trailer `Task-Id`);
   - las reglas `on_check` del desk (`sldb rules check`).
2. **Revisión con juicio (con modelo, opcional).** Cara, corre solo cuando la parte 1 lo pide o a demanda: si un doc o
   un átomo sigue diciendo lo que el código hace, después de un cambio en el código que lo materializa. Se despacha con
   el mismo mecanismo flexible de despacho (claude, pi o scion, según el perfil de runtime del desk).

## Cuándo corre (configurable por desk, en `desk/config.json`)

| Disparador | Para qué | Por defecto |
|---|---|---|
| Hook `post-commit` | avisar al que commitea | parte 1, solo avisa |
| Hook `pre-push` | no subir un desk roto | parte 1, bloquea solo errores |
| CI | la verdad compartida | parte 1 completa, bloquea errores |
| A demanda (`deskops check` o similar) | revisión completa | partes 1 y 2 |
| Proceso que vigila (opcional) | sesiones largas con agentes | parte 1, avisa |

## Qué hace ante una mutación (configurable)

- **Avisar** (por defecto): imprime y, si el desk lo pide, deja una nota en el inbox.
- **Registrar solo lo inocuo**: una mutación de texto sin cambio de datos (`benign_mutation`) actualiza el store sola.
- **Bloquear**: solo errores reales (documento que el modelo rechaza, referencia rota, store que no corresponde al
  árbol en CI o pre-push), nunca una mutación.
- **Abrir trabajo**: una deriva entre doc y código abre una nota o una tarea en el drawer, no una corrección automática.

## Qué no hace

No corrige código ni docs por su cuenta, no cierra tareas y no reemplaza los gates del workflow (esos son del núcleo).

## Lo que habría que decidir

1. Si vale el costo de la parte 2 o basta con la parte 1.
2. Si la parte 1 es un comando nuevo o la versión corregida de `doctor` más hooks.
3. Qué disparadores vienen activados por defecto en un desk nuevo.
