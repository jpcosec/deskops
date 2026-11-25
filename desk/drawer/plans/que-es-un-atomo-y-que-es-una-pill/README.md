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

## Tipos propuestos

Salen de la definición de arriba, no de lo que hay en los desks. Un tipo es una subclase que solo
agrega campos, y sus compuertas son reglas, igual que los tipos de tarea. Todo es propuesta.

### Átomos

Un tipo por cada cosa que el código no puede decir de sí mismo. Todo átomo, del tipo que sea,
lleva al menos un ancla al código del que habla.

| Tipo | Qué guarda | Qué agrega al átomo base | Qué se puede chequear |
|---|---|---|---|
| `atom.adr` | Por qué es así: una decisión | contexto, decisión, consecuencias, quién y cuándo; relación de reemplazo hacia otro ADR | uno aceptado no está reemplazado por otro aceptado; aceptarlo pide recibo del dueño |
| `atom.invariant` | Qué tiene que cumplirse entre varias piezas | las piezas (anclas) y la regla o prueba que lo comprueba | todo invariante tiene una comprobación; la comprobación pasa |
| `atom.intent` | Para quién es y qué necesita poder hacer | el destinatario, la necesidad, y la prueba de aceptación como materialización | toda intención tiene una prueba de aceptación |

Notas:

- `atom.adr` ya tiene tarea en este desk. Una decisión pendiente no es un átomo: es una tarea
  `task.decision`.
- Lo descartado no tiene tipo propio. Si fue parte de una decisión, va en las alternativas del
  ADR. Si alguien podría volver a intentarlo al leer el código, va como comentario en el código.
  Si no es ninguna de las dos, se borra y queda en el historial de git.
- `atom.invariant` guarda el porqué del invariante; la comprobación es una regla de sldb o una
  prueba, no texto. Un invariante que no se puede comprobar es una intención o una decisión.
- `atom.intent` no guarda si se cumple. Eso lo dice su prueba. Por eso se descartó
  `atom.capability` con un campo de estado.
- No hay tipo para definiciones de términos: sldb ya ata un término a su significado y a su
  referente (`AnchorDoc`).
- Descartados en la conversación: `atom.measurement`, `atom.assumption` y `atom.discarded`. Una
  medición es evidencia y vence; un supuesto no está asentado; lo descartado va al ADR, al código
  o se borra.

### Pills

Un tipo por cada clase de contexto que un trabajo puede necesitar. Toda pill, del tipo que sea,
lleva el trabajo al que pertenece y cómo termina: pasa al código, se destila a un átomo, o se
borra. Sin trabajo abierto no hay pill.

| Tipo | Qué entrega a quien ejecuta | Qué agrega a la pill base | Cómo termina |
|---|---|---|---|
| `pill.pointer` | Qué hay que leer y respetar: átomos, anclas, nodos de specIR | la lista de referencias; ningún razonamiento propio | se borra al cerrar el trabajo |
| `pill.question` | Algo sin decidir que afecta al trabajo | la pregunta, las opciones, hacia dónde se inclina y quién decide | se vuelve `task.decision` y después `atom.adr`, o se descarta |
| `pill.constraint` | Qué no se puede romper mientras dure este trabajo | el límite y cómo se comprueba | se borra; si resulta permanente, pasa a `atom.invariant` con su regla |
| `pill.finding` | Algo que se descubrió trabajando y todavía no tiene lugar | lo observado, dónde (ancla) y qué se propone hacer | pasa al código o a su docstring, a un átomo, o a una tarea |

Notas:

- `pill.pointer` es la candidata a no escribirse a mano: specIR sabe a qué afecta un cambio y
  podría armarla.
- `pill.constraint` es un guardrail con fecha de término. Un guardrail permanente y global no es
  una pill: es un `atom.invariant` con su regla.
- `pill.finding` existe para que lo que se aprende en un trabajo no se pierda ni se quede a vivir
  en la pill.

### Cómo se encadenan

```
pill.question ──► task.decision ──► atom.adr
pill.constraint ──(si resulta permanente)──► atom.invariant + regla
pill.finding ──► código / docstring ──o──► átomo ──o──► tarea
pill.pointer ──► se borra
```

### Antes de implementarlos

Conviene aplicar primero las tres preguntas a lo que existe: tipar antes le pondría estructura a
contenido mal ubicado.

## Una pregunta, un tipo de documento

JP (2026-11-25): los tipos de arriba responden un qué. Falta un tipo de documento transversal y
componible que detalle el dónde; el porqué va en el ADR, el cómo en la pill, y el cuándo en los
rituales.

Leído así, cada pregunta tiene su documento, y los documentos se componen en vez de que cada uno
cargue con todas las preguntas:

| Pregunta | Documento | Estado |
|---|---|---|
| Qué | Átomo (`atom.intent`, `atom.invariant`) | propuesto arriba |
| Por qué | ADR (`atom.adr`) | con tarea en este desk |
| Cómo | Pill: cómo hacer este trabajo | propuesto arriba |
| Dónde | Punteros a un lugar del código o a una categoría | **falta** como campo común |
| Cuándo | Ritual | existe en deskops |
| Para quién | sin asignar; puede ser el rol, que deskops ya modela, o quedar dentro de `atom.intent` | abierto |
| Cómo no | sin asignar; hoy cae en `pill.constraint` o en `atom.invariant` | abierto |

### El dónde

JP: el dónde tiene que apuntar al código, pero también a categorías como "aplica a toda la UI".

Entonces el dónde es una lista de punteros, y cada puntero es de una de dos clases:

| Clase | Qué nombra | Ejemplo | Con qué pieza que ya existe |
|---|---|---|---|
| Un lugar del código | un archivo, una clase, una función | `notation-view.js`, la función `resolve_view` | el ancla de código de sldb (`code:<ruta>::<nombre>`), que además sabe si el código cambió |
| Una categoría | todo lo que cae bajo un nombre | "toda la UI", "el backend", "graph_ui" | un tag del árbol semántico de sldb (`layer:interface`, `system:graph_ui`), que tiene padres e hijos |

Una categoría se resuelve a código sin escribirlo a mano: los tipos que specIR extrae ya declaran
su capa (un control de interfaz es `layer: interface`), así que "toda la UI" son los nodos de esa
capa, y cada nodo sabe de qué código salió.

Hoy el dónde es texto libre en la pill (`where`) y una lista de rutas en la tarea (`files`). Las
categorías existen como tags en los átomos, pero nada las usa para decir a qué código aplica algo.

Sin verificar: que el árbol semántico tenga hoy las categorías que hacen falta, y cómo se pregunta
"qué documentos aplican a este archivo" cuando el puntero es una categoría.

### Lo que esto cambia en los modelos de hoy

- La pill carga hoy las seis preguntas como secciones (qué, por qué, cuándo, dónde, cómo, cómo
  no). Pasaría a llevar el cómo, con el dónde como punteros y una referencia al porqué.
- El átomo elige hoy su pregunta con un campo. Con un tipo por pregunta, ese campo sobra.
- La tarea dejaría su lista de rutas por esos mismos punteros.

## Lo que choca con una tarea ya escrita

La tarea de `atom.adr` de este desk
(`task-deskops-add-adr-crea-un-registro-de-decision-con-estado-contexto-decision-consecuencias-y-a-cual-ree`,
prioridad alta) se escribió antes de esta conversación y dice tres cosas que aquí cambiaron:

| La tarea dice | Esta propuesta dice |
|---|---|
| Cuatro estados: propuesto, aceptado, reemplazado, rechazado | Una decisión pendiente es una tarea `task.decision`; el átomo existe solo una vez aceptada, y después puede quedar reemplazado |
| Su pregunta queda fija en "qué" | El ADR responde el porqué |
| Los repos afectados van como tags `repo:<nombre>` | El dónde son punteros a un lugar del código o a una categoría |

Si se ejecuta tal cual, construye la forma anterior. No se modificó ni se frenó: JP pidió dejar
esto escrito y no resolverlo. Decidir qué pasa con la tarea es parte de cerrar esta propuesta.

## Piezas que son de otros repos

La propuesta vive en el desk de deskops, pero se apoya en piezas ajenas. Lo que quedó sin
verificar hay que mirarlo en su repo:

| Pieza | Repo |
|---|---|
| El ancla de código y su estado | sldb |
| El árbol semántico de tags, con padres e hijos | sldb |
| La composición de un documento dentro de otro | sldb |
| Las reglas (`RuleDoc`) | sldb |
| Las capas de cada tipo extraído del código, y a qué afecta un cambio | specIR |
| Átomos, pills, tareas, rituales y roles | deskops |

## Sin resolver

- Dónde viven las capacidades (lo que un producto tiene que poder hacer) y su prueba: ¿átomo con
  su prueba como materialización, o algo que specIR ya modela?
- Si "qué tiene que cumplirse entre varias piezas" es un átomo o una regla de sldb (`RuleDoc`).
  Si se puede comprobar, debería ser la regla.
- Qué partes del contexto que hoy va en pills puede entregar specIR directamente a quien ejecuta.
- Cómo se revisa lo que ya existe sin hacerlo a mano.
- Si los punteros del dónde son un campo común a átomo, pill y tarea, o relaciones del store.
- Qué documento responde para quién y cuál cómo no.

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
