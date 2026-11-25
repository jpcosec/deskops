# Propuesta: qué debería ser un átomo y qué una pill

Escrita el 2026-11-25, de una conversación con JP. Es una propuesta para discutir, no una
decisión, y no trae tareas: JP pidió dejarla aquí y no resolverla todavía.

## Lo que fijó JP

1. Se propone desde lo que debería ser, no desde lo que hay en los desks.
2. specIR ya existe para algunas cosas; no se duplica.
3. sldb puede apuntar al código y a su docstring. El código es siempre la primera fuente de
   verdad; la idea es que esté bien hecho y que haga lo que dice que hace.
4. Hay muchas pills mal hechas, y muchos átomos también. La definición no está en duda.

## Quién dice qué

Cada cosa se dice en un solo lugar, y se parte por el que está más cerca del código.

| Qué se quiere saber | Dónde vive | Quién lo escribe |
|---|---|---|
| Qué es una pieza y cómo funciona | El código y su docstring | quien escribe el código |
| Cómo se relacionan las piezas entre capas: entidades, operaciones, controles, a qué afecta un cambio | specIR | nadie: se extrae del código |
| Que una afirmación habla de este trozo de código, y si ese trozo cambió | Un ancla de sldb | quien hace la afirmación |
| Lo que el código no puede decir de sí mismo | Un átomo | quien lo sabe |
| Lo que hace falta saber para hacer bien un trabajo | Una pill | quien prepara el trabajo |

## Átomo

Un átomo guarda solo lo que no se puede leer ni extraer del código:

- **por qué** es así: la decisión y su contexto;
- **qué se descartó** y por qué no;
- **qué tiene que cumplirse** entre varias piezas, que ninguna de ellas puede afirmar sola;
- **para quién** es.

Y apunta, con un ancla, al código del que habla. Así, cuando el código cambia, se sabe qué
átomos hay que volver a mirar.

Lo que no es un átomo:

- Cómo funciona una función o qué formato tiene una respuesta. Si hace falta escribirlo, falta
  en el docstring, y se arregla ahí.
- Qué piezas existen y cómo se conectan. Eso lo extrae specIR.
- Un estado, una medición o un supuesto sin verificar. No son conocimiento estable.

## Pill

Una pill es el contexto que necesita un trabajo concreto y que todavía no está en ningún otro
lugar: un razonamiento a medio asentar, o punteros a átomos, anclas y nodos de specIR.

Nace con el trabajo y termina con él, de una de tres maneras:

- lo que decía pasó al código o a su docstring;
- lo que decía era durable y se destiló a un átomo;
- ya no hace falta, y se borra.

Una pill que sigue viva sin trabajo abierto está mal hecha.

## Tres preguntas, en orden

Para cualquier cosa que alguien quiera anotar:

1. ¿Se puede leer del código o de su docstring? Entonces se mejora el código, no se anota.
2. ¿Lo puede extraer specIR? Entonces no se escribe a mano.
3. ¿Seguiría valiendo si el trabajo en curso desapareciera? Si sí, es un átomo; si no, una pill.

## Tipos

Con esta definición, el único tipo de átomo que se justifica de inmediato es la decisión
(`atom.adr`, que ya tiene tarea en este desk). Una decisión pendiente ya tiene artefacto, la tarea
`task.decision`; la aceptada es el átomo.

Otros tipos, de átomo o de pill, conviene verlos después de aplicar las tres preguntas a lo que
existe: tipar antes le pondría estructura a contenido mal ubicado. En la conversación se
propusieron y se descartaron `atom.capability`, `atom.measurement` y `atom.assumption`, porque
guardaban estado, evidencia o cosas sin asentar.

## Sin resolver

- Dónde viven las capacidades (lo que un producto tiene que poder hacer) y su prueba: ¿átomo con
  su prueba como materialización, o algo que specIR ya modela?
- Si "qué tiene que cumplirse entre varias piezas" es un átomo o una regla de sldb (`RuleDoc`).
  Si se puede comprobar, debería ser la regla.
- Qué partes del contexto que hoy va en pills puede entregar specIR directamente a quien ejecuta.
- Cómo se revisa lo que ya existe sin hacerlo a mano.

## Lo que hay hoy, solo como referencia

Contado el 2026-11-25 en los desks de johanes; no es la base de la propuesta.

- 647 átomos: graph_ui 265, deskops 237, sldb 107, IR 38. Por pregunta: cómo 237, qué 167, cómo
  no 60, por qué 57, dónde 46, cuándo 45, para quién 34. Los de "cómo", "qué" y "dónde" son los
  candidatos a estar repitiendo el código o lo que specIR extrae.
- 59 pills: deskops 29, sldb 24, IR 4, graph_ui 2. Varias son permanentes y globales, lo que por
  definición no es una pill.
- Una pill del desk de sldb (`pill-context-pills-carry-reasoning-not-a-copy-of-code-or-docs`) ya
  dice "el código es la verdad, la documentación es el índice y el contexto es razonamiento", y
  trae una clasificación de pills en prosa (tipo, alcance, ciclo de vida, dueño, disparador de
  revisión) que nada modela.
