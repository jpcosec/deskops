REFORMULACION
Propósito: documentar en `docs/configuration.md` qué es la configuración de deskops y cómo se declara un tipo de tarea nuevo, con receta ejecutable, más otra para una vista. Resultado: doc nuevo, enlaces desde `operator-manual.md` y `workflow-policy-reference.md`, entradas en ambas FAQ, `tests/test_docs_recipes.py`, posible ajuste condicional de rituales y `CHANGELOG.md`. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: no cambiar código de deskops; tocar solo archivos listados; rituales solo vía `deskops edit ritual` y solo si el grep detecta textos obsoletos; mantener pruebas de ayuda existentes y suite sin fallas nuevas respecto de `main`. No es agregado ni paquete: es una tarea documental ejecutable.

AMBIGUEDADES
1. “se corrige con deskops solo el ritual cuyo texto nombre algo que ya no existe (`grep -rln ...`)” — el grep halla coincidencias, no prueba que nombren algo inexistente ni indica reemplazo; obligaría a inventar el criterio de invalidación y el texto corregido.
2. “y otra para una vista nueva.” — no define contenido, comandos ni resultado esperado de esa receta; obligaría a inventar sus pasos y validación.
3. “sin fallas nuevas respecto de main” — no fija el estado/base de `main` ni cómo comparar; obligaría a inventar la línea base y el método de comparación.

DRY-RUN
Lecturas: TaskDoc; `docs/configuration.md`, `operator-manual.md`, `workflow-policy-reference.md`, `docs/faq.md`, `deskops/data/faq.md`, `CHANGELOG.md`; `deskops/models`, `deskops/data/rules`; documentación de `sldb rules`; salida del grep en `desk/rituals`. Cambios previstos: redactar configuration.md con mapa de configuración y ambas recetas; enlazar desde manual y referencia; ampliar FAQ; crear test de receta con desk temporal; ajustar rituales solo si el grep no está vacío; anotar en CHANGELOG. Dependencias: CC31–CC34 y CC36 cerradas, CLI deskops y entorno virtual disponibles. Validaciones futuras: las cinco órdenes pytest indicadas, incluida la suite completa con `-n 4`.

FUTURO
Un nodo de CI/verificación ejecutará la suite y comparará contra `main`; un humano revisará y aceptará el contenido documental y decidirá el cierre/merge. Eso no resuelve las ambigüedades anteriores.
