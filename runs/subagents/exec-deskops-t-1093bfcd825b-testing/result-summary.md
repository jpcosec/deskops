# Resultado del tester (lo escribe el coordinador): sin veredicto propio

El tester pi deskops-t-1093bfcd825b llegó al límite de 2 h (LIMITS_EXCEEDED) con la suite completa de deskops corriendo en un solo proceso dentro del contenedor, al 88 % (full-suite.log), y no escribió informe. Su log muestra 2 F al principio y un worker caído ("node down"). La suite completa del integrador en copia limpia, con el mismo cambio (80264d68), dio 1232 passed y 0 failed, así que esas F son del entorno del contenedor (su python no coincide con el .venv; hay tarea abierta).

Aprendizaje para el despacho automático: el encargo del tester pi debe pedir solo los tests de los archivos tocados. La suite completa la corre integrate en el host.
