REFORMULACION
- Propósito: disponer de una utilidad que informe cuántas palabras contiene README.md.
- Resultado: el archivo scripts/wc.py, que al ejecutarse con `python scripts/wc.py` imprime un entero (conteo de palabras de README.md).
- Repo: el repositorio git de trabajo (/dev/shm/tester-806c-sbx); los únicos archivos afectados son scripts/wc.py (creación) y, como lectura, README.md.
- Límites: solo scripts/wc.py; no tocar otros archivos. Sin criterio explícito de cómo se define "palabra".

AMBIGUEDADES
1. "Un script que imprime cuantas palabras tiene README.md." — No se define qué cuenta como palabra (separación por espacios, tokens alfanuméricos, exclusión de markdown como `#`, enlaces o bloques de código). Obligaría a inventar la regla de tokenización.
2. "Escribir scripts/wc.py que lee README.md y imprime el conteo." — No se indica la ruta de README.md (¿relativa al cwd o al propio script?) ni qué hacer si no existe. Obligaría a elegir comportamiento ante archivo ausente y base de rutas.
3. "python scripts/wc.py imprime un entero." — No se especifica el formato de salida (solo número, o texto como "N palabras") ni si debe terminar con salto de línea. Obligaría a decidir el formato exacto.
4. "Validation: python scripts/wc.py" — No se define qué valor esperado se verifica ni cómo comprobar corrección del conteo; no hay criterio para validar que el número es correcto. Obligaría a inventar un caso de prueba.
5. "scripts/" — No consta si el directorio scripts/ existe ya; el input no dice si debe crearse. Obligaría a decidir si crear el directorio (esto afecta al límite "solo scripts/wc.py").

DRY-RUN
- Lecturas previstas: README.md (para contar palabras); posiblemente el directorio scripts/ para comprobar su existencia.
- Cambios previstos: crear scripts/wc.py con lectura de README.md, conteo de palabras e impresión de un entero. Sin tocar otros archivos.
- Dependencias: Python disponible en el entorno; README.md presente en la ruta que resuelva el script.
- Validaciones futuras: ejecutar `python scripts/wc.py` y comprobar que la salida es un único entero; comprobar que git status solo muestra scripts/wc.py como nuevo archivo. Un ejecutor real debería resolver las ambigüedades 1–5 antes de implementar.

FUTURO
- Decidir la definición de "palabra" y el formato de salida (ambigüedades 1 y 3).
- Decidir la base de ruta de README.md y el comportamiento ante archivo ausente (ambigüedad 2).
- Confirmar si scripts/ existe o debe crearse (ambigüedad 5).
- Definir un caso de prueba con conteo esperado, si se desea validación de corrección (ambigüedad 4).
