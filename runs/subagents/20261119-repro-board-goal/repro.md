# Reproducción (integrador, 2026-11-19, deskops herramientas 7e0ac345/f04787af)

En un desk nuevo en /dev/shm: `deskops init`; `deskops add task --title "Prueba board" --task-type task.docs --goal "objetivo viejo"`; después `deskops edit task <id> goal "objetivo nuevo"`.
Resultado: desk/tasks/Board.md sigue mostrando `- Prueba board [draft] - objetivo viejo` (viejo=1, nuevo=0). La tarea quedó con el goal nuevo y el Board no se re-renderizó.
Causa probable: la línea sale de la composición task_summaries de BoardDoc (deskops/models/board.py:16-21, plantilla "- {title} [{status}] - {goal}"), que se renderiza al guardar el Board. add task guarda el Board (services/tasks.py alrededor de 118 y 219); edit task no.
