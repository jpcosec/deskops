## REFORMULACION
- **Propósito:** no indicado ("Not provided.").
- **Resultado:** un comando nuevo que cuente las líneas de README.md, validado con pytest.
- **Repo:** no identificado en el input.
- **Límites:** "Solo README.md y un script nuevo". No tocar otros archivos.

## AMBIGUEDADES
1. "Agregar un comando que cuente las lineas de README.md": no define nombre, interfaz ni formato de salida. Obligaría a inventarlos.
2. "un script nuevo": no indica ruta, lenguaje ni si el script es el propio comando. Obligaría a elegir ubicación y tecnología.
3. "Solo README.md y un script nuevo": no dice qué cambiar en README.md. Obligaría a decidir su contenido.
4. "## Implementation Path" está vacío. Obligaría a inventar la superficie afectada.
5. "- pytest": no indica qué tests escribir ni dónde. Obligaría a inventar casos y archivos.
6. "contar las lineas": no define si se cuentan líneas en blanco o si la última línea sin salto cuenta. Obligaría a fijar la semántica.
7. "## Done When" está vacío. Obligaría a inventar el criterio de cierre.

## DRY-RUN (hipotético, sin ejecutar)
- **Lecturas:** la propia tarea; README.md, para confirmar que existe y contar sus líneas; la estructura del repo, para ubicar el script y la configuración de pytest.
- **Cambios previstos:** crear un script que lea README.md y devuelva su número de líneas; exponerlo como comando; añadir a README.md una mención del comando; añadir tests de pytest.
- **Dependencias:** Python y pytest disponibles (supuesto, no declarado); ruta de README.md resoluble desde el script.
- **Validaciones futuras:** ejecutar pytest; comparar la salida del comando con el recuento real de README.md.

## FUTURO
- Un humano debe fijar nombre del comando, lenguaje, ubicación del script y formato de salida.
- Un humano debe decidir si README.md se modifica y con qué contenido.
- Un humano debe completar Implementation Path, Done When y Rationale.
- Un humano debe definir qué cuenta como línea.
- Otro nodo implementa y ejecuta pytest una vez tomadas estas decisiones.
