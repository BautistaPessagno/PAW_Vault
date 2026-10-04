@title: UI styles and tokens
@categories: Web
@module: webapp
@files: webapp/src/main/webapp/css/tokens.css, webapp/src/main/webapp/css/components.css, webapp/src/main/webapp/css/style.css, webapp/src/main/webapp/WEB-INF/tags/head.tag

> [!summary] En una frase
> Tres hojas de estilo CSS sin framework ni preprocesador: una define variables (colores, tipografías, radios, sombras), otra los componentes y otra el diseño de cada página; el modo oscuro sale de redefinir diez variables.

## Herramientas

| Herramienta | Para qué |
|---|---|
| Propiedades personalizadas de CSS (`--nombre`) | Definir cada valor de diseño una sola vez |
| `@media (prefers-color-scheme: dark)` | Modo oscuro según el sistema operativo |
| `color-mix()` | Derivar tonos suaves, sombras y el anillo de foco a partir de los colores base |
| Grid y Flexbox | Disposición de páginas y componentes |
| `@media` por ancho | Adaptar a pantallas angostas |
| `@media (prefers-reduced-motion)` | Quitar transiciones a quien las desactivó |

No hay Bootstrap, Tailwind ni Sass. Los archivos se sirven tal cual, como recursos estáticos de `/css/**` ([[Startup and dependency injection]]).

## Los tres archivos

| Archivo | Líneas | Qué contiene | Orden de carga |
|---|---|---|---|
| `tokens.css` | 64 | Variables: paleta, colores semánticos, tipografías, ancho máximo, radios, sombras, anillo de foco. Redefinición para modo oscuro | 1 |
| `components.css` | 846 | Estilos de los componentes de [[UI components]]: texto, botones, campos, radios, autocompletado, tarjeta de vinilo, cabecera, marca | 2 |
| `style.css` | 1985 | Diseño por página: catálogo, formularios, auth, carrito, bandejas, venta, conversación, ficha, avatar, perfil público y privado, diálogo de foto | 3 |

`head.tag` los enlaza en ese orden en todas las páginas. El orden importa: a igual especificidad gana la regla que se declara después, así que una página puede ajustar un componente.

## Cómo funcionan los tokens

Hay dos niveles de variables:

1. **Paleta** (`--room-*`): diez colores concretos. Es lo único que cambia entre tema claro y oscuro.
2. **Semánticos** (`--color-*`): nombres por función (`--color-bg`, `--color-surface`, `--color-text`, `--color-accent`, `--color-danger`) que apuntan a la paleta. Los componentes usan solo estos.

Como los componentes nunca nombran un color concreto, el modo oscuro es redefinir la paleta dentro de un `@media`; nada más cambia. Los tonos derivados (`--color-accent-soft`, sombras, foco) se calculan con `color-mix()` y se adaptan solos.

Dos colores quedan fuera a propósito: `--color-vinyl` y `--color-vinyl-groove`. Un disco es negro en los dos temas.

Tipografías: una de texto (`--font-body`), una serif para títulos (`--font-display`) y una monoespaciada (`--font-mono`), todas con fuentes del sistema; no se descarga ninguna.

## Convención de nombres

Las clases siguen el patrón bloque, elemento y modificador: `vinyl-card`, `vinyl-card__link`, `button--primary`, `text--muted`. Un componente es un bloque; sus partes llevan `__`; sus variantes, `--`. Así una clase dice a qué componente pertenece y no pisa a otra.

## Decisiones y por qué

| Decisión | Motivo | Fuente |
|---|---|---|
| CSS propio, sin framework | Control del diseño y cero dependencias de front | Estructura del código; inferencia |
| Tokens separados de los componentes | Cambiar el tema sin tocar componentes | Estructura de `tokens.css` |
| El disco no invierte color en modo oscuro | Un vinilo es negro en los dos temas | Comentario en `tokens.css` |
| El estado no depende solo del color | Accesibilidad | Comentarios en `style.css` y en los tags de estado |
| Componentes con `border-box` declarado | Que funcionen aunque se usen sin el resto de los estilos | Primer comentario de `components.css` |
| El diálogo de la foto usa un velo liso, sin desenfoque | El velo toma el color del vinilo, que es negro en los dos temas | Comentario en `style.css` |

## Límites conocidos

- `style.css` tiene casi dos mil líneas en un solo archivo; las secciones se ubican por sus comentarios.
- `color-mix()` y `100dvh` necesitan navegadores recientes.
- No hay minificación ni versionado de los archivos: el navegador los cachea según las cabeceras por defecto del contenedor.

## Preguntas de defensa

**¿Usan algún framework de CSS?**
No. Son tres hojas propias con variables de CSS.

**¿Cómo hicieron el modo oscuro?**
Los componentes usan variables semánticas; un `@media (prefers-color-scheme: dark)` redefine la paleta y todo lo demás se adapta.

**¿Cómo se sirven los CSS?**
Como recursos estáticos mapeados en `WebConfig`, enlazados desde `head.tag` con `c:url`.

## Código

### tokens.css

{{file:webapp/src/main/webapp/css/tokens.css}}

### components.css

{{file:webapp/src/main/webapp/css/components.css}}

### style.css

{{file:webapp/src/main/webapp/css/style.css}}
