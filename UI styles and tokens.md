---
title: "UI styles and tokens"
categories: ["Web"]
type: "guide"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["webapp/src/main/webapp/css/tokens.css", "webapp/src/main/webapp/css/components.css", "webapp/src/main/webapp/css/style.css"]
---

# UI styles and tokens

ui:head loads tokens.css, components.css and style.css in that order. Tokens define palette aliases, system font stacks, radii, shadows, focus and control sizing. Dark mode follows prefers-color-scheme.

components.css styles typography, buttons, bound inputs/selects/textareas, linked vinyl cards and commercial metadata. style.css owns page/form layouts, account navigation, search/filter controls, inquiry lists and error pages. Filters use a responsive grid; account and action rows wrap. Disabled-button styles apply to controls disabled by submit-once.js.

The catalog uses four columns, three below 1024px and two below 600px. Compact cards adapt at the smaller breakpoint. Reduced-motion rules remove button/card transitions. There is no JavaScript theme switch. Browser rendering, contrast and responsive layout were not tested in this documentation refresh.

## tokens.css

[webapp/src/main/webapp/css/tokens.css, lines 1–62](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/css/tokens.css>)

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

[webapp/src/main/webapp/css/components.css, lines 1–359](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/css/components.css>)

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
    font-size: clamp(2.55rem, 7vw, 5.4rem);
    font-weight: 600;
    letter-spacing: -0.035em;
    line-height: 0.98;
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

.button--sm {
    font-size: 0.78rem;
    min-height: 2.25rem;
    padding: 0.55rem 0.9rem;
}

.button--md {
    font-size: 0.9rem;
    padding: 0.7rem 1.15rem;
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

.vinyl-card__price-label {
    color: var(--color-text-muted);
    font-size: 0.72rem;
    font-weight: 650;
    letter-spacing: 0.08em;
    line-height: 1.2;
    text-transform: uppercase;
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

.vinyl-card__actions {
    display: flex;
    flex-wrap: wrap;
    gap: 0.55rem;
    margin-top: 0.5rem;
    position: relative;
    z-index: 2;
}

.vinyl-card--editorial {
    display: grid;
    grid-template-rows: auto 1fr;
    max-width: 22rem;
    width: 100%;
}

.vinyl-card--editorial .vinyl-card__content {
    padding: 1.25rem;
}

.vinyl-card--editorial .vinyl-card__actions .button--ghost {
    border-color: transparent;
    border-radius: 0;
    border-bottom-color: var(--color-border);
    min-height: 2.2rem;
    padding-inline: 0;
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

    .vinyl-card__actions .button {
        flex: 1 1 auto;
    }
}

@media (prefers-reduced-motion: reduce) {
    .button,
    .vinyl-card {
        transition: none;
    }
}
.page-header__actions,
.account-nav {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: var(--space-2);
}

.account-nav__logout {
  margin: 0;
}

.account-nav__identity {
  color: var(--color-text-muted);
  overflow-wrap: anywhere;
}
```

## style.css

[webapp/src/main/webapp/css/style.css, lines 1–311](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/css/style.css>)

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

.page-shell {
    display: grid;
    gap: 2.5rem;
    margin: 0 auto;
    max-width: 78rem;
    padding: 3rem 2rem 6rem;
}

/* El 404 es la unica pantalla sin header ni nada debajo: se centra en la ventana
   entera y con padding vertical simetrico, si no queda cabecera arriba. */
.page-shell--centered {
    align-content: center;
    min-height: 100vh;
    padding-block: clamp(3rem, 8vh, 5rem);
}

.page-header {
    align-items: center;
    display: flex;
    flex-wrap: wrap;
    gap: 1.5rem;
    justify-content: space-between;
}

.page-header__intro {
    display: grid;
    gap: 0.5rem;
}

.surface {
    background: color-mix(in srgb, var(--color-surface) 91%, transparent);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-card);
    padding: clamp(1.25rem, 3vw, 2rem);
}

.search-bar {
    /* Los filtros son mas altos que el buscador: todo se alinea por abajo. */
    align-items: flex-end;
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
}

.search-bar__control {
    flex: 1 1 18rem;
    max-width: 34rem;
}

.filter-grid {
    display: grid;
    flex: 1 0 100%;
    gap: 0.75rem;
    grid-template-columns: repeat(auto-fit, minmax(9rem, 1fr));
}

.filter-field {
    color: var(--color-text-muted);
    display: grid;
    font-size: 0.82rem;
    gap: 0.35rem;
}

/* Los artistas se guardan en minuscula para poder deduplicarlos: el filtro los
   muestra capitalizados sin tocar lo que hay en la base. */
.artist-name {
    text-transform: capitalize;
}

.search-bar__summary {
    color: var(--color-text-muted);
    margin: -1.5rem 0 0;
}

.post-grid {
    display: grid;
    gap: 1.5rem;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    list-style: none;
    margin: 0;
    padding: 0;
}

.post-grid .vinyl-card--editorial {
    max-width: none;
}

.page-shell > .vinyl-card--compact {
    max-width: 40rem;
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

.form-stack__actions {
    align-items: center;
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
}

.inquiry-section {
    display: grid;
    gap: 1rem;
}

.inquiry-list {
    display: grid;
    gap: 1rem;
    list-style: none;
    margin: 0;
    padding: 0;
}

.inquiry-card {
    display: grid;
    gap: 0.75rem;
    max-width: 48rem;
}

.inquiry-card h3,
.inquiry-card p {
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

@media (max-width: 1024px) {
    .post-grid {
        grid-template-columns: repeat(3, minmax(0, 1fr));
    }
}

@media (max-width: 860px) {
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

@media (max-width: 600px) {
    .page-shell {
        gap: 2rem;
        padding: 2rem 0.75rem 4rem;
    }

    .post-grid {
        gap: 1rem;
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .not-found__intro .text-h1 {
        font-size: clamp(1.95rem, 8vw, 2.6rem);
    }
}
```

[[UI components]] · [[Views and assets]]
