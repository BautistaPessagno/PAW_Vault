---
title: "UI styles and tokens"
categories: ["Web"]
type: "guide"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["webapp/src/main/webapp/css/tokens.css", "webapp/src/main/webapp/css/components.css", "webapp/src/main/webapp/css/style.css"]
---

# UI styles and tokens

ui:head loads tokens.css, components.css and style.css in that order. Tokens now define a small room palette (background, surface, sunk, rule, foreground, dim, two accents, danger) mapped to semantic color aliases, color-mix soft accents, vinyl colors that stay dark in both themes, body/display/mono font stacks, a 90rem page width, radii, shadows and a focus ring. Dark mode still follows prefers-color-scheme by redefining the room palette.

components.css styles typography, buttons (including danger and danger-outline variants), icons, bound and unbound inputs, the segmented control, the JavaScript select picker, autocomplete listboxes, the brand, back link, site header and search, and vinyl cards with state chips. style.css owns page layouts: the catalog grid with its filter sidebar and results bar, the publish workspace and preview, the detail page, profile account rows, the inbox and its tab navigation, pagination, the confirmation dialog, notices and error pages.

The catalog grid shows five columns on wide screens, three below 1100px and two below 600px. Below 1100px the publish preview also stacks under the form; below 900px the filter sidebar stacks above the results and form rows use two columns; at 860px the detail, contact and not-found layouts become single-column; the site header search wraps below 760px; below 700px form rows use one column; below 600px the page gutter shrinks and compact cards simplify. Reduced-motion rules remove button, back-link and card transitions. There is no JavaScript theme switch. Browser rendering, contrast and responsive layout were not tested in this documentation refresh.

## tokens.css

[webapp/src/main/webapp/css/tokens.css, lines 1–64](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/css/tokens.css>)

```css
:root {
    color-scheme: light;

    --room-bg: #e9e6ee;
    --room-surface: #f7f5fa;
    --room-sunk: #dfdbe7;
    --room-rule: #cbc5d6;
    --room-fg: #16141b;
    --room-dim: #5c5669;
    --room-accent: #be3a21;
    --room-accent-2: #166f68;
    --room-on-accent: #fbf8f4;
    --room-danger: #b3261e;

    --color-bg: var(--room-bg);
    --color-surface: var(--room-surface);
    --color-surface-muted: var(--room-sunk);
    --color-border: var(--room-rule);
    --color-text: var(--room-fg);
    --color-text-muted: var(--room-dim);
    --color-accent: var(--room-accent);
    --color-accent-secondary: var(--room-accent-2);
    --color-text-on-accent: var(--room-on-accent);
    --color-danger: var(--room-danger);
    --color-accent-soft: color-mix(in srgb, var(--color-accent) 13%, var(--color-surface));
    --color-secondary-soft: color-mix(in srgb, var(--color-accent-secondary) 14%, var(--color-surface));

    /* Un vinilo es negro en los dos temas, asi que estos no se invierten en dark. */
    --color-vinyl: #17151c;
    --color-vinyl-groove: #262231;
    --color-vinyl-sheen: rgba(255, 255, 255, 0.13);

    --font-body: "Avenir Next", "Segoe UI", Arial, sans-serif;
    --font-display: Georgia, "Times New Roman", serif;
    --font-mono: "SFMono-Regular", Consolas, "Liberation Mono", monospace;

    --page-max-width: 90rem;

    --radius-sm: 0.5rem;
    --radius-md: 1rem;
    --radius-lg: 1.5rem;
    --radius-pill: 999px;
    --shadow-card: 0 8px 20px color-mix(in srgb, var(--color-text) 8%, transparent);
    --shadow-card-hover: 0 14px 28px color-mix(in srgb, var(--color-text) 13%, transparent);
    --focus-ring: 0 0 0 3px color-mix(in srgb, var(--color-accent) 34%, transparent);
}

@media (prefers-color-scheme: dark) {
    :root {
        color-scheme: dark;

        --room-bg: #0e0d11;
        --room-surface: #17151c;
        --room-sunk: #100e14;
        --room-rule: #2a2632;
        --room-fg: #ede6da;
        --room-dim: #9a93a5;
        --room-accent: #e4573d;
        --room-accent-2: #86d9d0;
        --room-on-accent: #1a1114;
        --room-danger: #ef5a48;
    }
}

```

## components.css

[webapp/src/main/webapp/css/components.css, lines 1–771](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/css/components.css>)

```css
/* Box model: la biblioteca asume border-box aunque se use sin demo.css. */
*,
*::before,
*::after {
    box-sizing: border-box;
}

/* Typography */
.text {
    color: var(--color-text);
    font-family: var(--font-body);
    margin-block: 0;
}

.text-h1 {
    font-family: var(--font-display);
    font-size: clamp(1.6rem, 2.4vw, 2.1rem);
    font-weight: 600;
    letter-spacing: -0.02em;
    line-height: 1.1;
}

.text-h3 {
    font-size: clamp(1.35rem, 2.5vw, 1.75rem);
    font-weight: 650;
    letter-spacing: -0.025em;
    line-height: 1.2;
}

.text-body {
    font-size: 1rem;
    line-height: 1.7;
}

.text-lead {
    color: var(--color-text-muted);
    font-size: 1.12rem;
    line-height: 1.55;
}

.text-inline {
    display: inline-block;
    font-size: 0.9rem;
    font-weight: 600;
    line-height: 1.35;
}

.text--accent {
    color: var(--color-accent);
}

.text--muted {
    color: var(--color-text-muted);
}

/* Buttons */
.button {
    align-items: center;
    border: 1px solid transparent;
    border-radius: var(--radius-pill);
    cursor: pointer;
    display: inline-flex;
    font-family: var(--font-body);
    font-weight: 650;
    gap: 0.45rem;
    justify-content: center;
    line-height: 1;
    min-height: 2.75rem;
    text-decoration: none;
    transition: background-color 190ms ease, border-color 190ms ease, color 190ms ease, transform 190ms ease;
}

.button:hover {
    transform: translateY(-1px);
}

.button:active {
    transform: scale(0.98);
}

.button:focus-visible {
    box-shadow: var(--focus-ring);
    outline: 0;
}

.button:disabled {
    cursor: progress;
    opacity: 0.6;
    pointer-events: none;
    transform: none;
}

.button--primary {
    background: var(--color-accent);
    color: var(--color-text-on-accent);
}

.button--primary:hover {
    background: color-mix(in srgb, var(--color-accent) 86%, var(--color-text));
}

.button--ghost {
    background: transparent;
    border-color: var(--color-border);
    color: var(--color-text);
}

.button--ghost:hover {
    border-color: var(--color-accent);
    color: var(--color-accent);
}

.button--danger {
    background: var(--color-danger);
    color: var(--color-text-on-accent);
}

.button--danger:hover {
    background: color-mix(in srgb, var(--color-danger) 86%, var(--color-text));
}

.button--sm {
    font-size: 0.78rem;
    min-height: 2.25rem;
    padding: 0.55rem 0.9rem;
}

.button--md {
    font-size: 0.9rem;
    padding: 0.7rem 1.15rem;
}

/* Icono de trazo dentro de texto o boton: hereda color y se alinea con la caja del texto. */
.icon {
    flex: none;
    height: 1em;
    width: 1em;
}

.button .icon {
    margin-inline-start: -0.15rem;
}

/* Accion destructiva secundaria: vacio con borde y texto de peligro; al pasar se tiñe suave. */
.button--danger-outline {
    background: transparent;
    border-color: color-mix(in srgb, var(--color-danger) 55%, var(--color-border));
    color: var(--color-danger);
}

.button--danger-outline:hover {
    background: color-mix(in srgb, var(--color-danger) 12%, var(--color-surface));
    border-color: var(--color-danger);
}

/* Text input */
.input-field {
    display: grid;
    gap: 0.5rem;
}

.input-field__label {
    color: var(--color-text);
    font-size: 0.86rem;
    font-weight: 650;
}

/* Etiqueta solo para lectores de pantalla: la fila en linea del perfil la muestra como placeholder. */
.visually-hidden {
    clip: rect(0 0 0 0);
    height: 1px;
    overflow: hidden;
    position: absolute;
    white-space: nowrap;
    width: 1px;
}

.input-field__control {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    color: var(--color-text);
    font: inherit;
    min-height: 3rem;
    padding: 0.72rem 0.95rem;
    transition: border-color 190ms ease, box-shadow 190ms ease;
    width: 100%;
}

.input-field__control-wrap {
    min-width: 0;
    position: relative;
}

select.input-field__control,
.select-picker__trigger {
    appearance: none;
    background-image:
            linear-gradient(45deg, transparent 50%, var(--color-text-muted) 50%),
            linear-gradient(135deg, var(--color-text-muted) 50%, transparent 50%);
    background-position:
            calc(100% - 1.15rem) 50%,
            calc(100% - 0.82rem) 50%;
    background-repeat: no-repeat;
    background-size: 0.34rem 0.34rem;
    padding-inline-end: 2.75rem;
}

.select-picker {
    min-width: 0;
    position: relative;
    width: 100%;
}

.select-picker__trigger {
    cursor: pointer;
    text-align: start;
}

.select-picker__trigger[aria-expanded="true"] {
    border-color: var(--color-accent);
    box-shadow: var(--focus-ring);
}

.select-picker .autocomplete__list {
    max-height: min(20rem, 50vh);
    overflow-y: auto;
}

.select-picker .autocomplete__option {
    align-items: center;
    display: flex;
    gap: 1rem;
    justify-content: space-between;
}

.select-picker .autocomplete__option[aria-selected="true"]::after {
    border-color: var(--color-accent);
    border-style: solid;
    border-width: 0 0.14rem 0.14rem 0;
    content: "";
    height: 0.65rem;
    margin-inline: 0.2rem;
    transform: rotate(45deg);
    width: 0.34rem;
}

input[type="number"].input-field__control {
    -moz-appearance: textfield;
    appearance: textfield;
}

input[type="number"].input-field__control::-webkit-inner-spin-button,
input[type="number"].input-field__control::-webkit-outer-spin-button {
    -webkit-appearance: none;
    margin: 0;
}

.input-field__control:focus {
    border-color: var(--color-accent);
    box-shadow: var(--focus-ring);
    outline: 0;
}

textarea.input-field__control {
    min-height: 7rem;
    resize: vertical;
}

.input-field--error .input-field__control {
    border-color: var(--color-danger);
}

.input-field__error {
    color: var(--color-danger);
    font-size: 0.82rem;
    margin: 0;
}

/* Radio group shared by catalog filters and forms. */
.segmented-control {
    align-items: stretch;
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    display: grid;
    gap: 0.2rem;
    grid-auto-columns: minmax(0, 1fr);
    grid-auto-flow: column;
    min-height: 3rem;
    padding: 0.2rem;
}

.segmented-control__option {
    cursor: pointer;
    display: grid;
    min-width: 0;
    position: relative;
}

.segmented-control__input {
    height: 1px;
    opacity: 0;
    position: absolute;
    width: 1px;
}

.segmented-control__label {
    border-radius: calc(var(--radius-md) - 0.25rem);
    color: var(--color-text-muted);
    display: grid;
    font-size: 0.75rem;
    font-weight: 650;
    line-height: 1;
    overflow: hidden;
    padding: 0.5rem 0.35rem;
    place-content: center;
    text-align: center;
    text-overflow: ellipsis;
    transition: background-color 190ms ease, color 190ms ease, box-shadow 190ms ease;
    white-space: nowrap;
}

.segmented-control__input:checked + .segmented-control__label {
    background: var(--color-accent);
    color: var(--color-text-on-accent);
}

.segmented-control__input:focus-visible + .segmented-control__label {
    box-shadow: var(--focus-ring);
}

.segmented-control__option:hover .segmented-control__label {
    color: var(--color-text);
}

.segmented-control__input:checked + .segmented-control__label,
.segmented-control__option:hover .segmented-control__input:checked + .segmented-control__label {
    color: var(--color-text-on-accent);
}

/* Autocomplete */
.autocomplete__list {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-card-hover);
    inset-inline: 0;
    list-style: none;
    margin: 0.35rem 0 0;
    max-width: 100%;
    overflow: hidden;
    padding: 0.35rem;
    position: absolute;
    top: 100%;
    z-index: 20;
}

.autocomplete__option {
    border-radius: calc(var(--radius-md) - 0.35rem);
    color: var(--color-text);
    cursor: pointer;
    padding: 0.7rem 0.75rem;
}

.autocomplete__option[hidden] {
    display: none;
}

.autocomplete__option:hover,
.autocomplete__option--active {
    background: var(--color-accent-soft);
}

.autocomplete__option--rich {
    align-items: center;
    display: flex;
    gap: 0.75rem;
    justify-content: space-between;
}

.autocomplete__option-main {
    display: grid;
    gap: 0.12rem;
    min-width: 0;
}

.autocomplete__option-value,
.autocomplete__option-detail {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.autocomplete__option-detail,
.autocomplete__option-type {
    color: var(--color-text-muted);
    font-size: 0.75rem;
}

.autocomplete__option-type {
    flex: none;
    font-weight: 650;
}

/* Vinyl card */
.vinyl-card {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-card);
    color: var(--color-text);
    overflow: hidden;
    position: relative;
    transition: border-color 190ms ease, box-shadow 190ms ease, transform 190ms ease;
}

.vinyl-card:hover {
    border-color: color-mix(in srgb, var(--color-accent) 45%, var(--color-border));
    box-shadow: var(--shadow-card-hover);
    transform: translateY(-2px);
}

.vinyl-card--linked {
    cursor: pointer;
}

.vinyl-card__link {
    inset: 0;
    position: absolute;
    z-index: 1;
}

.vinyl-card__link:focus-visible {
    border-radius: var(--radius-lg);
    outline: 2px solid var(--color-accent);
    outline-offset: 2px;
}

.vinyl-card__cover {
    aspect-ratio: 1;
    background: var(--color-surface-muted);
    overflow: hidden;
    position: relative;
}

/* El estado flota en la esquina de la portada, por encima del link que cubre la card. */
.vinyl-card__cover .state-marker--chip {
    pointer-events: none;
    position: absolute;
    right: 0.6rem;
    top: 0.6rem;
    z-index: 2;
}

.vinyl-card__image {
    display: block;
    height: 100%;
    object-fit: cover;
    width: 100%;
}

.vinyl-card__content {
    display: flex;
    flex-direction: column;
    gap: 0.7rem;
    min-width: 0;
    padding: 1.4rem;
}

.vinyl-card__price {
    display: grid;
    gap: 0.15rem;
    margin-block: 0.15rem 0.1rem;
}

.vinyl-card__price-value {
    color: var(--color-accent);
    font-size: clamp(1.65rem, 3vw, 2rem);
    font-variant-numeric: tabular-nums;
    font-weight: 700;
    letter-spacing: -0.025em;
    line-height: 1.1;
}

.vinyl-card__metadata {
    display: grid;
    gap: 0.7rem;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    margin: 0.45rem 0 0;
}

.vinyl-card__datum {
    display: grid;
    gap: 0.25rem;
}

.vinyl-card__datum dd {
    margin: 0;
}

.vinyl-card__description {
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 3;
    display: -webkit-box;
    line-clamp: 3;
    overflow: hidden;
    overflow-wrap: anywhere;
}

.vinyl-card--editorial {
    display: grid;
    grid-template-rows: auto 1fr;
    max-width: 15rem;
    width: 100%;
}

.vinyl-card--editorial .vinyl-card__content {
    gap: 0.3rem;
    height: 100%;
    padding: 0.85rem 0.95rem 1rem;
}

/* En el grid el titulo y el artista se recortan para que las cards de una misma
   fila queden alineadas; el titulo completo se ve en el tooltip y en el detalle. */
.vinyl-card--editorial .text-h3 {
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2;
    display: -webkit-box;
    font-size: 1rem;
    line-clamp: 2;
    line-height: 1.25;
    overflow: hidden;
    overflow-wrap: anywhere;
}

.vinyl-card--editorial .text-lead {
    font-size: 0.85rem;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.vinyl-card--editorial .vinyl-card__price {
    margin-top: auto;
    padding-top: 0.35rem;
}

.vinyl-card--editorial .vinyl-card__price-value {
    font-size: 1.2rem;
}

.vinyl-card--compact {
    align-items: stretch;
    display: grid;
    grid-template-columns: minmax(8.5rem, 0.42fr) minmax(0, 1fr);
}

.vinyl-card--compact .vinyl-card__cover {
    aspect-ratio: auto;
    min-height: 100%;
}

.vinyl-card--compact .vinyl-card__content {
    padding: 1.25rem;
}

.vinyl-card--compact .vinyl-card__metadata {
    border-top: 1px solid var(--color-border);
    padding-top: 0.75rem;
}

/* Cabecera global: barra pegada arriba con marca, buscador y acciones. El fondo
   translucido con blur deja leer las tarjetas que pasan por debajo al scrollear. */
.site-header {
    backdrop-filter: blur(8px);
    background: color-mix(in srgb, var(--color-surface) 92%, transparent);
    border-bottom: 1px solid var(--color-border);
    position: sticky;
    top: 0;
    z-index: 10;
}

.site-header__inner {
    align-items: center;
    display: flex;
    gap: 1.25rem;
    margin: 0 auto;
    max-width: var(--page-max-width);
    min-height: 4rem;
    padding: 0.65rem 2rem;
}

/* Marca: isotipo + nombre. La usan el header y, mas grande, las pantallas de auth. */
.brand {
    align-items: center;
    color: var(--color-accent);
    display: inline-flex;
    font-family: var(--font-display);
    font-size: 1.5rem;
    font-weight: 600;
    gap: 0.5rem;
    letter-spacing: -0.03em;
    text-decoration: none;
    white-space: nowrap;
}

.brand--lg {
    font-size: 1.9rem;
}

/* El disco se mide en em para acompanar el tamano del nombre. */
.brand__mark {
    flex: none;
    height: 1.3em;
    width: 1.3em;
}

.brand:focus-visible {
    border-radius: var(--radius-sm);
    box-shadow: var(--focus-ring);
    outline: 0;
}

.site-search {
    display: flex;
    flex: 1 1 18rem;
    gap: 0.5rem;
    margin: 0;
    max-width: 38rem;
}

.site-search__field {
    flex: 1 1 auto;
    min-width: 0;
}

.site-search__field .autocomplete__list {
    max-height: min(22rem, 60vh);
    overflow-y: auto;
}

/* El control por defecto mide 3rem de alto: demasiado para una barra de cabecera. */
.site-search__field .input-field__control {
    min-height: 2.5rem;
    padding-block: 0.45rem;
}

/* Boton cuadrado a la altura del campo; el icono hereda el color del texto del boton. */
.site-search__submit {
    flex: none;
    min-height: 2.5rem;
    padding: 0;
    width: 2.5rem;
}

.site-search__icon {
    display: block;
    height: 1.1rem;
    width: 1.1rem;
}

.site-header__actions {
    align-items: center;
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    justify-content: flex-end;
    margin-left: auto;
}

/* Las pildoras de la cabecera no parten su texto aunque la fila se reordene. */
.site-header__actions .button {
    white-space: nowrap;
}

.account-nav {
    align-items: center;
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}

.account-nav__logout {
    margin: 0;
}

/* El enlace reutiliza el boton ghost sm. Solo agrega el limite propio del navbar;
   el title conserva el nombre completo cuando hace falta truncarlo. */
.account-nav__identity {
    max-width: 12rem;
    min-width: 0;
}

/* text-overflow no aplica a un contenedor flex: el recorte con puntos suspensivos
   tiene que vivir en el span que envuelve el nombre. */
.account-nav__name {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

/* page-shell es un grid: sin esto el link de volver se estira a todo el ancho. */
.back-link {
    justify-self: start;
}

.back-link__anchor {
    align-items: center;
    color: var(--color-text-muted);
    display: inline-flex;
    font-size: 0.9rem;
    font-weight: 650;
    gap: 0.4rem;
    text-decoration: none;
}

.back-link__anchor:hover {
    color: var(--color-accent);
}

.back-link__anchor:hover .back-link__arrow {
    transform: translateX(-2px);
}

.back-link__anchor:focus-visible {
    border-radius: var(--radius-sm);
    box-shadow: var(--focus-ring);
    outline: 0;
}

.back-link__arrow {
    transition: transform 190ms ease;
}

/* En pantallas angostas la marca y las acciones comparten la primera fila y el
   buscador baja a la segunda. */
@media (max-width: 760px) {
    .site-header__inner {
        flex-wrap: wrap;
        padding-inline: 0.75rem;
    }

    .site-search {
        flex-basis: 100%;
        max-width: none;
        order: 3;
    }
}

@media (max-width: 600px) {
    .vinyl-card--compact {
        grid-template-columns: 1fr;
    }

    .vinyl-card--compact .vinyl-card__cover {
        aspect-ratio: 16 / 10;
    }

    .vinyl-card__metadata {
        grid-template-columns: 1fr;
    }
}

@media (prefers-reduced-motion: reduce) {
    .button,
    .back-link__arrow,
    .vinyl-card {
        transition: none;
    }
}
```

## style.css

[webapp/src/main/webapp/css/style.css, lines 1–1219](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/css/style.css>)

```css
html {
    background: var(--color-bg);
    font-family: var(--font-body);
}

body {
    background:
        radial-gradient(circle at 8% 4%, var(--color-secondary-soft), transparent 24rem),
        radial-gradient(circle at 90% 26%, var(--color-accent-soft), transparent 28rem),
        var(--color-bg);
    color: var(--color-text);
    margin: 0;
    min-height: 100vh;
}

.catalog-empty-page {
    display: grid;
    grid-template-rows: auto minmax(0, 1fr);
    height: 100dvh;
    min-height: 0;
    overflow: hidden;
}

.catalog-empty-page .page-shell {
    height: 100%;
    min-height: 0;
    padding-block: 1rem;
    width: 100%;
}

.catalog-empty-page .catalog,
.catalog-empty-page .catalog__results {
    height: 100%;
    min-height: 0;
}

.page-shell {
    display: grid;
    gap: 2rem;
    margin: 0 auto;
    max-width: var(--page-max-width);
    padding: 1.75rem 2rem 5rem;
}

/* El 404 es la unica pantalla sin header ni nada debajo: se centra en la ventana
   entera y con padding vertical simetrico, si no queda cabecera arriba. */
.page-shell--centered {
    align-content: center;
    min-height: 100vh;
    padding-block: clamp(3rem, 8vh, 5rem);
}

.surface {
    background: color-mix(in srgb, var(--color-surface) 91%, transparent);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-card);
    padding: clamp(1.25rem, 3vw, 2rem);
}

/* Catalogo: filtros a la izquierda, resultados a la derecha. La barra lateral se
   pega debajo del header sticky mientras dura la columna. */
.catalog {
    align-items: start;
    display: grid;
    gap: 1.5rem;
    grid-template-columns: 13rem minmax(0, 1fr);
}

.catalog__notice {
    grid-column: 1 / -1;
}

.catalog__filters {
    position: sticky;
    top: 5.25rem;
}

/* Misma superficie que .surface con menos aire: la columna es angosta. */
.filters {
    background: color-mix(in srgb, var(--color-surface) 91%, transparent);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-card);
    padding: 1.25rem;
}

.filters__summary {
    cursor: pointer;
    font-weight: 650;
    list-style: none;
}

.filters__summary::-webkit-details-marker {
    display: none;
}

/* En escritorio el details siempre esta abierto y el titulo lo da el h2;
   en mobile el h2 sobra porque el summary ya rotula la seccion. */
.filters__heading {
    font-size: 1rem;
    font-weight: 650;
    margin: 0 0 0.9rem;
}

.filters__form {
    --filter-label-gap: 0.35rem;
    display: grid;
    gap: 0.9rem;
}

.filter-group {
    border: 0;
    display: grid;
    gap: 0;
    margin: 0;
    padding: 0;
}

.filter-group__legend {
    color: var(--color-text-muted);
    display: block;
    font-size: 0.82rem;
    margin: 0 0 var(--filter-label-gap);
    padding: 0;
    width: 100%;
}

.filter-group__range {
    display: grid;
    gap: 0.5rem;
    grid-template-columns: repeat(2, minmax(0, 1fr));
}

.filters .input-field__control {
    min-height: 2.5rem;
    padding-block: 0.45rem;
}

.filters .segmented-control {
    min-height: 2.5rem;
}

@media (min-width: 901px) {
    .filters__summary {
        display: none;
    }

    /* Con la barra lateral en 13rem, tres opciones en fila dejan menos de 3rem de texto por
       celda y las etiquetas largas ("Cualquiera", "Occasion") se recortan por los dos lados.
       La opcion vacia se lleva la primera fila entera y las concretas comparten la de abajo.
       Debajo de 901px los filtros ocupan todo el ancho y las tres entran en una fila. */
    .filters .segmented-control {
        grid-auto-flow: row;
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .filters .segmented-control__option--empty {
        grid-column: 1 / -1;
    }
}

.results-bar {
    align-items: center;
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    justify-content: space-between;
}

.results-bar__summary {
    align-items: center;
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem 1rem;
}

.results-bar__query {
    color: var(--color-text-muted);
    margin: 0;
}

.sort-form {
    align-items: center;
    display: flex;
    gap: 0.5rem;
    margin: 0;
}

.sort-form__label {
    color: var(--color-text-muted);
    font-size: 0.82rem;
    white-space: nowrap;
}

.sort-form__control {
    min-height: 2.5rem;
    padding-block: 0.45rem;
    width: auto;
}

.sort-form .select-picker {
    max-width: min(22rem, calc(100vw - 2rem));
    width: auto;
}

.sort-form .select-picker__trigger {
    min-width: 12rem;
}

.sort-form .autocomplete__list {
    inset-inline: auto 0;
    max-width: min(22rem, calc(100vw - 2rem));
    min-width: 100%;
    width: max-content;
}

/* Con JS el select submitea solo: el boton queda de mas. */
.sort-form.is-enhanced .button {
    display: none;
}

.catalog__results {
    display: grid;
    gap: 1.5rem;
}

.filter-field {
    color: var(--color-text-muted);
    display: grid;
    font-size: 0.82rem;
    gap: var(--filter-label-gap);
}

.post-grid {
    display: grid;
    gap: 0.85rem;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    list-style: none;
    margin: 0;
    padding: 0;
}

.post-grid .vinyl-card--editorial {
    height: 100%;
    max-width: none;
}

.pagination {
    display: flex;
    justify-content: flex-end;
    width: 100%;
}

.pagination__list {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    list-style: none;
    margin: 0;
    padding: 0;
}

.pagination__link {
    align-items: center;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-pill);
    color: var(--color-text-muted);
    display: inline-flex;
    font-size: 0.86rem;
    font-weight: 650;
    height: 2.25rem;
    justify-content: center;
    min-width: 2.25rem;
    padding: 0 0.6rem;
    text-decoration: none;
    transition: border-color 190ms ease, color 190ms ease;
}

a.pagination__link:hover {
    border-color: var(--color-accent);
    color: var(--color-accent);
}

.pagination__link:focus-visible {
    box-shadow: var(--focus-ring);
    outline: 0;
}

.pagination__link--current {
    background: var(--color-accent-soft);
    border-color: color-mix(in srgb, var(--color-accent) 38%, var(--color-border));
    color: var(--color-accent);
}

.pagination__link--disabled {
    opacity: 0.5;
    pointer-events: none;
    user-select: none;
}

.pagination__ellipsis {
    align-items: center;
    color: var(--color-text-muted);
    display: inline-flex;
    height: 2.25rem;
    padding: 0 0.25rem;
}

.hint {
    color: var(--color-text-muted);
    font-size: 0.82rem;
    margin: 0;
}

.form-stack {
    display: grid;
    gap: 1.25rem;
    max-width: 34rem;
}

.form-stack--wide {
    max-width: none;
    width: 100%;
}

/* Los formularios largos usan dos columnas; los bloques anchos cruzan las dos. */
.form-grid {
    display: grid;
    gap: 1.25rem;
    grid-template-columns: repeat(2, minmax(0, 1fr));
}

.form-grid__full {
    grid-column: 1 / -1;
}

.publish-workspace {
    align-items: start;
    display: grid;
    gap: 1.5rem;
    grid-template-columns: minmax(0, 46rem) 15rem;
    justify-content: center;
}

.publish-form {
    max-width: none;
}

.form-layout {
    display: grid;
    gap: 1.25rem;
}

.form-layout__row {
    align-items: start;
    display: grid;
    gap: 1.25rem;
}

.form-layout__row--equal {
    grid-template-columns: repeat(2, minmax(0, 1fr));
}

.form-layout__row--catalog {
    grid-template-columns: 8rem minmax(12rem, 1fr) minmax(18rem, auto);
}

.form-layout__row--commerce {
    grid-template-columns: 10rem minmax(10rem, 1fr) 14.5rem;
}

.form-layout__row--commerce .input-field__label {
    white-space: nowrap;
}

.form-layout__row--content {
    grid-template-columns: minmax(0, 1fr);
}

.form-layout .filter-group__legend {
    color: var(--color-text);
    font-size: 0.86rem;
    font-weight: 650;
    margin-bottom: 0.5rem;
}

.publish-preview {
    display: grid;
    gap: 1rem;
    width: 15rem;
    position: sticky;
    top: 5.5rem;
}

.publish-preview > h2 {
    margin: 0;
}

/* Los formularios chicos (auth) quedan en una columna angosta y centrada. */
.auth-shell {
    max-width: 34rem;
}

.auth-shell .form-stack {
    max-width: none;
}

/* Login, registro y verificacion no tienen header: la marca de arriba es la salida al
   catalogo. */
.auth-shell__header {
    display: grid;
    justify-items: center;
    padding-top: clamp(1.5rem, 6vh, 3.5rem);
}

/* El titulo va dentro de la tarjeta y en la fuente de texto: la serif queda para la
   marca, asi las dos no se confunden. */
.auth-shell__title {
    color: var(--color-text);
    font-family: var(--font-body);
    font-size: 1.35rem;
    font-weight: 700;
    letter-spacing: -0.01em;
    line-height: 1.2;
    margin: 0;
}

.auth-shell__switch a:focus-visible {
    border-radius: var(--radius-sm);
    box-shadow: var(--focus-ring);
    outline: 0;
}

.auth-shell__switch {
    color: var(--color-text-muted);
    font-size: 0.9rem;
    margin: 0;
}

.auth-shell__switch a {
    color: var(--color-accent);
    font-weight: 650;
    text-decoration: none;
}

.auth-shell__switch a:hover {
    text-decoration: underline;
}

.contact-layout {
    align-items: start;
    display: grid;
    gap: 2rem;
    grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
}

.contact-layout .form-stack {
    max-width: none;
}

/* Recibidas y enviadas son dos vistas: la sub-nav es lo que dice en cual estas y
   cuanto hay del otro lado. */
.inquiry-nav {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}

.inquiry-nav__tab {
    border: 1px solid var(--color-border);
    border-radius: var(--radius-pill);
    color: var(--color-text-muted);
    font-weight: 650;
    padding: 0.5rem 1.1rem;
    text-decoration: none;
    transition: background 190ms ease, border-color 190ms ease, color 190ms ease;
}

.inquiry-nav__tab:hover {
    border-color: color-mix(in srgb, var(--color-accent) 38%, var(--color-border));
    color: var(--color-text);
}

.inquiry-nav__tab:focus-visible {
    box-shadow: var(--focus-ring);
    outline: 0;
}

.inquiry-nav__tab--active {
    background: var(--color-accent-soft);
    border-color: color-mix(in srgb, var(--color-accent) 38%, var(--color-border));
    color: var(--color-accent);
}

.inquiry-nav__count {
    font-weight: 600;
    opacity: 0.7;
}

.form-stack__actions {
    align-items: center;
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
}

/* Bandeja: lista plana por publicacion. Cabecera con miniatura y titulo (toda un enlace),
   y una fila por consulta separada por lineas finas. La columna derecha tiene ancho fijo
   para que botones y estados queden alineados de arriba a abajo. */
.inbox {
    display: grid;
    gap: 2rem;
}

.inbox-group__post {
    align-items: center;
    display: grid;
    gap: 0 1rem;
    grid-template-columns: 3.5rem minmax(0, 1fr);
    padding-bottom: 0.75rem;
    position: relative;
}

/* Enlace estirado sobre la cabecera: mismo patron que vinyl-card__link. */
.inbox-group__anchor {
    border-radius: var(--radius-md);
    inset: 0;
    position: absolute;
    z-index: 1;
}

.inbox-group__anchor:focus-visible {
    box-shadow: var(--focus-ring);
    outline: 0;
}

.inbox-group__cover {
    aspect-ratio: 1;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    overflow: hidden;
    transition: border-color 190ms ease;
}

.inbox-group__cover img {
    display: block;
    height: 100%;
    object-fit: cover;
    width: 100%;
}

.inbox-group__title {
    display: grid;
    gap: 0.1rem;
    min-width: 0;
    overflow-wrap: anywhere;
}

.inbox-group__title .text-h3 {
    align-items: center;
    display: flex;
    flex-wrap: wrap;
    font-size: 1.15rem;
    gap: 0.6rem;
    transition: color 190ms ease;
}

.inbox-group__title .text-lead {
    font-size: 0.95rem;
}

.inbox-group__post--linked:hover .text-h3 {
    color: var(--color-accent);
}

.inbox-group__post--linked:hover .inbox-group__cover {
    border-color: var(--color-accent);
}

.inbox-list {
    border-top: 1px solid var(--color-border);
    display: grid;
    list-style: none;
    margin: 0;
    padding: 0;
}

.inbox-row {
    align-items: center;
    border-bottom: 1px solid var(--color-border);
    display: grid;
    gap: 0.25rem 1.5rem;
    grid-template-columns: 10rem minmax(0, 1fr) auto;
    padding: 0.9rem 0 0.9rem 4.5rem;
}

.inbox-row__who {
    font-weight: 650;
    overflow-wrap: anywhere;
}

.inbox-row__msg {
    line-height: 1.55;
    margin: 0;
    overflow-wrap: anywhere;
}

.inbox-row__msg--empty {
    color: var(--color-text-muted);
    font-style: italic;
}

.inbox-row__end {
    display: flex;
    gap: 0.5rem;
    justify-content: flex-end;
    min-width: 12rem;
}

.inbox-row__end form {
    margin: 0;
}

/* Estado de una consulta: texto normal con icono atenuado. Sin pastilla, para que la
   columna derecha de la bandeja solo tenga botones o texto. */
.inquiry-status {
    align-items: center;
    color: var(--color-text);
    display: inline-flex;
    font-size: 0.86rem;
    font-weight: 650;
    gap: 0.35rem;
    white-space: nowrap;
}

.inquiry-status .icon {
    color: var(--color-text-muted);
}

/* Estado de una publicacion. En linea va junto al titulo; como chip flota sobre la portada. */
.state-marker {
    align-items: center;
    display: inline-flex;
    font-size: 0.78rem;
    font-weight: 650;
    gap: 0.35rem;
    white-space: nowrap;
}

.state-marker--muted {
    color: var(--color-text-muted);
}

.state-marker--available {
    color: var(--color-accent-secondary);
}

.state-marker--chip {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-pill);
    box-shadow: var(--shadow-card);
    padding: 0.3rem 0.75rem;
}

.state-marker--chip.state-marker--available {
    background: var(--color-secondary-soft);
    border-color: color-mix(in srgb, var(--color-accent-secondary) 38%, var(--color-border));
}

.confirm-dialog {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-card-hover);
    color: var(--color-text);
    max-width: 34rem;
    padding: 0;
    width: calc(100% - 2rem);
}

.confirm-dialog::backdrop {
    backdrop-filter: blur(3px);
    background: color-mix(in srgb, var(--color-text) 58%, transparent);
}

.confirm-dialog__content {
    display: grid;
    gap: 1.25rem;
    padding: clamp(1.25rem, 3vw, 2rem);
}

.confirm-dialog__title,
.confirm-dialog__message {
    margin: 0;
}

.confirm-dialog__title {
    font-family: var(--font-display);
    font-size: clamp(1.35rem, 2.5vw, 1.75rem);
    font-weight: 600;
    letter-spacing: -0.02em;
    line-height: 1.2;
}

.confirm-dialog__message {
    color: var(--color-text-muted);
    line-height: 1.6;
}

.confirm-dialog__actions {
    align-items: center;
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    justify-content: flex-end;
}

.confirm-dialog__actions form {
    margin: 0;
}

.notice,
.error,
.empty-state {
    border-left: 3px solid currentColor;
    margin: 0;
    padding: 0.75rem 1rem;
}

.notice {
    color: var(--color-accent-secondary);
    background: var(--color-secondary-soft);
}

.error {
    color: var(--color-danger);
}

.empty-state {
    color: var(--color-text-muted);
    background: var(--color-surface-muted);
}

/* Ficha de la publicacion: portada grande a la izquierda, datos a la derecha. */
.detail {
    align-items: start;
    display: grid;
    gap: 2.5rem;
    grid-template-columns: minmax(0, 26rem) minmax(0, 1fr);
}

.detail__cover {
    aspect-ratio: 1;
    background: var(--color-surface-muted);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-card);
    overflow: hidden;
}

.detail__image {
    display: block;
    height: 100%;
    object-fit: cover;
    width: 100%;
}

.detail__body {
    display: grid;
    gap: 1rem;
}

.detail__heading {
    align-items: start;
    display: flex;
    gap: 1rem;
    justify-content: space-between;
}

.detail__title {
    align-items: center;
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    min-width: 0;
}

.detail__heading .button {
    flex: none;
}

.detail__owner-actions {
    display: flex;
    flex: none;
    gap: 0.5rem;
}

.detail__metadata {
    display: grid;
    gap: 0.7rem;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    margin: 0;
}

.detail__datum {
    display: grid;
    gap: 0.25rem;
}

.detail__datum dd {
    margin: 0;
}

.detail__description {
    overflow-wrap: anywhere;
    white-space: pre-line;
}

.detail__actions {
    display: grid;
    gap: 0.5rem;
    justify-items: start;
}

/* Perfil: una columna. La tarjeta de la cuenta tiene filas con el mismo ritmo (1rem a cada
   lado de cada linea); el padding del surface manda arriba y abajo. */
.profile-account {
    display: grid;
    gap: 0;
}

.profile-account > h2,
.profile-posts h2 {
    margin: 0;
}

.profile-account > h2 {
    padding-bottom: 1rem;
}

.account-rows {
    display: grid;
}

/* details como grid: el summary y el form son items de la misma grilla. Cerrada, el summary
   ocupa las dos columnas; abierta, el summary se queda con la etiqueta y el form con el
   resto de la fila. summary con min-height igual al control: la fila no cambia de alto. */
.account-row {
    align-content: center;
    align-items: center;
    border-top: 1px solid var(--color-border);
    column-gap: 1rem;
    display: grid;
    grid-template-columns: 11rem minmax(0, 1fr);
    padding: 1rem 0;
}

.account-row__summary {
    align-items: center;
    cursor: pointer;
    display: grid;
    gap: 0.75rem;
    grid-column: 1 / -1;
    grid-template-columns: 11rem minmax(0, max-content) max-content;
    list-style: none;
    min-height: 2.75rem;
}

.account-row__summary::-webkit-details-marker {
    display: none;
}

.account-row__summary:focus-visible {
    border-radius: var(--radius-sm);
    box-shadow: var(--focus-ring);
    outline: 0;
}

.account-row--static .account-row__summary {
    cursor: default;
    grid-template-columns: 11rem minmax(0, max-content);
}

.account-row__label {
    color: var(--color-text-muted);
    font-size: 0.86rem;
}

.account-row__value {
    overflow-wrap: anywhere;
}

.account-row__edit {
    align-items: center;
    border: 1px solid transparent;
    border-radius: var(--radius-pill);
    color: var(--color-text-muted);
    display: inline-flex;
    height: 1.9rem;
    justify-content: center;
    transition: border-color 190ms ease, color 190ms ease;
    width: 1.9rem;
}

.account-row__edit .icon {
    height: 0.95rem;
    width: 0.95rem;
}

.account-row__summary:hover .account-row__edit {
    border-color: var(--color-accent);
    color: var(--color-accent);
}

.account-row[open] .account-row__summary {
    grid-column: 1;
    grid-template-columns: 1fr;
}

.account-row[open] .account-row__value,
.account-row[open] .account-row__edit {
    display: none;
}

.account-row__form {
    align-items: center;
    display: flex;
    flex-wrap: wrap;
    gap: 0.6rem;
    /* Con ::details-content (Chrome 131+) el form queda envuelto y esta declaracion es inerte: el auto-placement lo deja en la misma celda; se conserva para los motores anteriores. */
    grid-column: 2;
    margin: 0;
}

.account-row__form .input-field {
    flex: 1 1 12rem;
    max-width: 20rem;
}

.account-row__form .input-field__control {
    min-height: 2.75rem;
    padding-block: 0.5rem;
}

.account-row__actions {
    display: flex;
    gap: 0.5rem;
}

/* La ayuda de la politica va en una linea propia debajo de los campos. */
.account-row__hint {
    flex-basis: 100%;
    margin: 0;
}

.profile-account__footer {
    border-top: 1px solid var(--color-border);
    padding-top: 1rem;
}

.profile-account__footer form {
    margin: 0;
}

.profile-posts {
    display: grid;
    gap: 1rem;
}

/* 404 */
.not-found {
    align-items: center;
    display: grid;
    gap: clamp(3rem, 7vw, 7rem);
    /* Columnas acotadas + justify-content: el bloque se centra en el shell en vez de
       estirarse hasta los 78rem y quedar pegado a los bordes. */
    grid-template-columns: minmax(0, 24rem) minmax(0, 34rem);
    justify-content: center;
}

.not-found__record {
    aspect-ratio: 1;
    background: repeating-radial-gradient(circle at 50% 50%,
        var(--color-vinyl) 0 3px,
        var(--color-vinyl-groove) 3px 5px);
    border-radius: 50%;
    box-shadow: var(--shadow-card-hover);
    display: grid;
    margin-inline: auto;
    place-items: center;
    position: relative;
    width: min(100%, 24rem);
}

/* Brillo diagonal: sin esto el disco se lee plano contra el fondo. */
.not-found__record::before {
    background: linear-gradient(118deg, transparent 32%, var(--color-vinyl-sheen) 47%, transparent 60%);
    border-radius: inherit;
    content: "";
    inset: 0;
    position: absolute;
}

.not-found__code {
    align-content: center;
    background: var(--color-accent);
    border-radius: 50%;
    color: var(--color-text-on-accent);
    display: grid;
    gap: 0.45rem;
    height: 42%;
    justify-items: center;
    margin: 0;
    position: relative;
    width: 42%;
}

.not-found__digits {
    font-family: var(--font-display);
    font-size: clamp(1.5rem, 3.6vw, 2.35rem);
    font-weight: 600;
    letter-spacing: -0.02em;
    line-height: 1;
}

/* El agujero del centro del disco. */
.not-found__code::after {
    background: var(--color-vinyl);
    border-radius: 50%;
    content: "";
    height: 0.7rem;
    width: 0.7rem;
}

.not-found__intro {
    display: grid;
    gap: clamp(1.5rem, 2.6vw, 2.25rem);
    justify-items: start;
}

.not-found__intro .text-h1 {
    font-size: clamp(2.4rem, 4.6vw, 3.6rem);
}

/* Corta el parrafo antes del borde de la columna: dos renglones parejos leen mejor
   que uno largo y otro de tres palabras. */
.not-found__intro .text-lead {
    max-width: 30rem;
}

.not-found__actions {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    padding-block-start: 0.5rem;
}

.not-found--catalog {
    align-content: center;
    gap: clamp(0.75rem, 2vh, 1.5rem);
    grid-template-columns: minmax(0, 30rem);
    height: 100%;
    min-height: 0;
    text-align: center;
    width: min(100%, calc(100vw - 1.5rem));
}

.catalog-empty-page .not-found--catalog {
    margin-inline: 0;
}

.not-found--catalog .not-found__record {
    color: inherit;
    text-decoration: none;
    width: min(100%, clamp(9rem, 27vh, 17rem));
}

.not-found--catalog .not-found__record:focus-visible {
    box-shadow: var(--shadow-card-hover), var(--focus-ring);
    outline: none;
}

.not-found--catalog .not-found__intro {
    gap: clamp(0.75rem, 2vh, 1.5rem);
    justify-items: stretch;
    min-width: 0;
}

.not-found--catalog .not-found__actions {
    justify-content: center;
}

@media (max-width: 1100px) {
    .post-grid {
        grid-template-columns: repeat(3, minmax(0, 1fr));
    }

    .publish-workspace {
        grid-template-columns: minmax(0, 1fr);
    }

    .publish-preview {
        justify-self: center;
        max-width: 15rem;
        position: static;
        width: 100%;
    }
}

@media (max-width: 900px) {
    .form-layout__row {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .form-layout__row > :last-child:nth-child(3) {
        grid-column: 1 / -1;
    }

    .catalog {
        grid-template-columns: minmax(0, 1fr);
    }

    .catalog-empty-page .catalog {
        grid-template-rows: auto minmax(0, 1fr);
    }

    .catalog__filters {
        position: static;
    }

    .filters__heading {
        display: none;
    }

    .filters__summary {
        margin-bottom: 0;
    }

    .filters[open] .filters__summary {
        margin-bottom: 0.9rem;
    }
}

@media (max-width: 860px) {
    .detail {
        grid-template-columns: minmax(0, 1fr);
    }

    .contact-layout {
        grid-template-columns: minmax(0, 1fr);
    }

    /* 1fr + max-width y no una columna de ancho fijo: con minmax(0, 32rem) la
       columna se planta en 32rem y desborda apenas la ventana es mas angosta. */
    .not-found {
        gap: clamp(2.5rem, 6vw, 3.5rem);
        grid-template-columns: minmax(0, 1fr);
        margin-inline: auto;
        max-width: 32rem;
        text-align: center;
    }

    .not-found__record {
        width: min(100%, 18rem);
    }

    /* stretch y no center: con justify-items centrado el h1 se mide por su max-content
       y se desborda a lo ancho en pantallas angostas. */
    .not-found__intro {
        justify-items: stretch;
    }

    .not-found__intro .text-lead {
        margin-inline: auto;
    }

    .not-found__actions {
        justify-content: center;
    }
}

@media (max-width: 700px) {
    .form-grid,
    .form-layout__row {
        grid-template-columns: minmax(0, 1fr);
    }

    .form-layout__row > :last-child:nth-child(3) {
        grid-column: 1 / -1;
    }
}

@media (max-width: 600px) {
    .page-shell {
        gap: 2rem;
        padding: 2rem 0.75rem 4rem;
    }

    .post-grid {
        gap: 0.75rem;
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .not-found__intro .text-h1 {
        font-size: clamp(1.95rem, 8vw, 2.6rem);
    }
}

@media (max-width: 600px) and (max-height: 700px) {
    .catalog-empty-page .catalog {
        grid-template-rows: minmax(0, 1fr);
    }

    .catalog-empty-page .catalog__filters,
    .catalog-empty-page .not-found--catalog .text-lead {
        display: none;
    }
}
```

[[UI components]] · [[Views and assets]]
