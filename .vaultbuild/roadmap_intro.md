> [!summary] En una frase
> Un orden para leer los {{FILES}} archivos versionados del proyecto ({{JAVA}} clases Java, {{LINES}} líneas en total) sin perderse: primero el contexto, después un flujo simple de punta a punta, y luego cada funcionalidad en el orden en que se apoyan unas en otras.

Cada archivo aparece **una sola vez**, con una casilla para marcar. La lista se generó a partir de `git ls-tree` en `c3e2a4c` y el generador falla si un archivo queda sin asignar o aparece dos veces, así que la cobertura es completa.

## Cómo usarlo

1. Abrí la etapa y leé **primero las notas del vault** que indica. Te dan el recorrido, las decisiones y las preguntas de defensa antes de ver el código.
2. Recorré los archivos en el orden de la lista. Dentro de cada etapa el orden sigue al request: web, service, persistencia, vista, tests.
3. Marcá la casilla cuando puedas explicar el archivo sin mirarlo.
4. Cerrá la etapa contestando en voz alta las preguntas del final. Si alguna no sale, volvé a la nota de flujo.

Los enlaces `[[Clase]]` abren la nota de esa clase en el vault, con su resumen, sus métodos, quién la usa y el código completo. Los enlaces con ruta abren el archivo en el repositorio.

## Cómo leer una clase

| Tipo | Qué mirar primero | Qué preguntarte |
|---|---|---|
| Modelo | Campos y constructor | ¿Es una fila de una tabla o una proyección de lectura? ¿Qué reglas lleva adentro? |
| Interfaz de DAO o service | Firmas | ¿Qué recibe y qué devuelve? ¿Qué excepciones declara en los comentarios? |
| DAO JDBC | El SQL y el `RowMapper` | ¿Qué tablas une? ¿Los parámetros están ligados con `?`? ¿Devuelve filas afectadas? |
| Service | Métodos `@Transactional` | ¿Qué valida? ¿Qué bloquea? ¿Qué pasa después del commit? ¿Qué excepción lanza cada rechazo? |
| Controller | `@RequestMapping` y `@PreAuthorize` | ¿Qué ruta, qué método HTTP, quién puede entrar? ¿Queda algo de lógica que debería estar en el service? |
| Formulario y validador | Anotaciones | ¿Qué regla está en el campo y cuál cruza campos? |
| JSP y tag | `<c:out>`, `<c:url>`, `<spring:message>` | ¿Hay algún dato sin escapar o alguna URL armada a mano? |
| Test | Nombre del método | ¿Qué caso cubre? ¿Qué caso falta? |

## Dos formas de recorrerlo

**Completo.** Las 17 etapas en orden. Una etapa por sesión de estudio es un ritmo razonable; las etapas 5 y 9 son las más densas y conviene partirlas en dos.

**Corto, para una defensa.** Si hay poco tiempo, este orden cubre lo que más se pregunta:

1. Etapa 0 (solo `CONTEXT.md` y `CLAUDE.md`) y [[Architecture]].
2. Etapa 5 completa: cuenta, tokens y seguridad.
3. Etapa 6: correo.
4. Etapa 9: consulta y venta, al menos [[InquiryServiceImpl]] con [[Inquiry and sale flow]] al lado.
5. [[Transactions and concurrency]], [[Validation and errors]] y [[Database schema]].
6. [[Defense guide]] para practicar las preguntas.

## Las etapas

| Etapa | Tema | Archivos | Líneas |
|---|---|---|---|
{{TABLE}}

Las líneas son el total de cada archivo en `c3e2a4c`, incluidos comentarios y líneas en blanco. Sirven para estimar el esfuerzo relativo de cada etapa, no como medida de complejidad.

## Qué conviene saltear en una primera lectura

- Los procedimientos para agentes de la etapa 15 (`.claude/skills`, `.agents/skills`, `.codex/prompts`): son tres copias del mismo contenido y no forman parte de la aplicación.
- Los planes largos de la etapa 16 (`venta-con-comprobante.md` y `perfil-consultas-ui.md` suman más de cinco mil líneas): sirven como consulta puntual.
- `style.css` línea por línea: alcanza con ubicar las secciones.
- Los tres bundles de mensajes completos.
