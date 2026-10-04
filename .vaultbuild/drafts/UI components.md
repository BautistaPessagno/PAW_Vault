@title: UI components
@categories: Web
@module: webapp
@files: webapp/src/main/webapp/WEB-INF/tags/account-nav.tag, webapp/src/main/webapp/WEB-INF/tags/address-fields.tag, webapp/src/main/webapp/WEB-INF/tags/address.tag, webapp/src/main/webapp/WEB-INF/tags/avatar.tag, webapp/src/main/webapp/WEB-INF/tags/back-link.tag, webapp/src/main/webapp/WEB-INF/tags/brand.tag, webapp/src/main/webapp/WEB-INF/tags/button.tag, webapp/src/main/webapp/WEB-INF/tags/confirm-dialog.tag, webapp/src/main/webapp/WEB-INF/tags/h1.tag, webapp/src/main/webapp/WEB-INF/tags/h3.tag, webapp/src/main/webapp/WEB-INF/tags/head.tag, webapp/src/main/webapp/WEB-INF/tags/icon.tag, webapp/src/main/webapp/WEB-INF/tags/inbox-group-header.tag, webapp/src/main/webapp/WEB-INF/tags/inbox-last-message.tag, webapp/src/main/webapp/WEB-INF/tags/input-control.tag, webapp/src/main/webapp/WEB-INF/tags/inquiry-nav.tag, webapp/src/main/webapp/WEB-INF/tags/inquiry-status.tag, webapp/src/main/webapp/WEB-INF/tags/p.tag, webapp/src/main/webapp/WEB-INF/tags/pagination-link.tag, webapp/src/main/webapp/WEB-INF/tags/pagination.tag, webapp/src/main/webapp/WEB-INF/tags/post-badge.tag, webapp/src/main/webapp/WEB-INF/tags/resend-verification.tag, webapp/src/main/webapp/WEB-INF/tags/segmented-control.tag, webapp/src/main/webapp/WEB-INF/tags/select-control.tag, webapp/src/main/webapp/WEB-INF/tags/select.tag, webapp/src/main/webapp/WEB-INF/tags/site-header.tag, webapp/src/main/webapp/WEB-INF/tags/span.tag, webapp/src/main/webapp/WEB-INF/tags/star-rating-input.tag, webapp/src/main/webapp/WEB-INF/tags/text-input.tag, webapp/src/main/webapp/WEB-INF/tags/textarea.tag, webapp/src/main/webapp/WEB-INF/tags/vinyl-card.tag

> [!summary] En una frase
> Las páginas no repiten HTML: se arman con 31 componentes propios (tag files de JSP) que encapsulan el marcado, el escape de datos, las URL y los textos traducidos.

## Herramientas

| Herramienta | Para qué |
|---|---|
| Tag files (`WEB-INF/tags/*.tag`) | Componentes reutilizables escritos en JSP, sin clases Java |
| `<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>` | Importarlos en una vista: `<ui:button .../>` |
| `<%@ attribute %>` | Declarar los parámetros de un componente, con tipo y obligatoriedad |
| `<jsp:doBody/>` | Insertar el contenido que la vista puso dentro del tag |
| JSTL `c:` | Condicionales, bucles, `c:out` y `c:url` |
| `spring:message` | Textos traducidos |
| `form:` de Spring | Campos ligados al formulario y sus errores |
| `sec:` de Spring Security | Mostrar u ocultar según la sesión y agregar el token CSRF |

## Reglas que cumplen todos

- **Sin scriptlets.** Solo tags y expresiones EL.
- **Todo dato se escapa** con `<c:out>` (o con los tags `form:`, que escapan solos). Es la defensa contra XSS: un nombre o una descripción con HTML se muestra como texto.
- **Toda URL pasa por `<c:url>`**, que antepone el context path. En el servidor de la cátedra la aplicación no cuelga de la raíz.
- **Ningún texto literal**: todo sale de `spring:message`.
- **Accesibilidad**: etiquetas asociadas a sus campos, `aria-describedby` para pistas y errores, `aria-current` en la navegación, iconos decorativos ocultos a lectores de pantalla.

## Catálogo

| Componente | Qué es | Atributos | Lo usan |
|---|---|---|---|
| `account-nav` | Menú de la cuenta en la cabecera | — | site-header |
| `address-fields` | Campos de una dirección | — | cart/index, post/contact, profile/index |
| `address` | Muestra una dirección, completa o recortada | `address` | cart/index, inquiry/detail, inquiry/received, post/contact, profile/index |
| `avatar` | Foto o inicial | `imageId`, `userId`, `name`, `size`, `alt`, `preview` | post/detail, profile/index, profile/public |
| `back-link` | Enlace de volver | `href`, `label`, `page`, `fragment` | inquiry/detail, post/detail |
| `brand` | Marca | `size` | site-header, auth/forgot-password, auth/login, auth/register, auth/reset-password, auth/verify-required y 1 más |
| `button` | Botón o enlace con variantes | `label`, `variant`, `size`, `type`, `href`, `url`, `id`, `icon`, `data`, `name`, `value` | account-nav, confirm-dialog, resend-verification, site-header, auth/forgot-password, auth/login y 18 más |
| `confirm-dialog` | Diálogo de confirmación | `title`, `confirmLabel`, `confirmVariant` | inquiry/detail, post/detail, profile/index |
| `h1` | Título | `text`, `tone` | cart/index, error/400, error/403, error/404, error/409, inquiry/detail y 8 más |
| `h3` | Subtítulo con nivel configurable | `text`, `level` | inbox-group-header, vinyl-card, cart/index |
| `head` | Cabecera HTML común: estilos y scripts | `titleCode`, `pageScript` | auth/forgot-password, auth/login, auth/register, auth/reset-password, auth/verify-required, auth/verify y 14 más |
| `icon` | Iconos SVG de una lista cerrada | `name` | account-nav, button, inquiry-status, pagination, post-badge, cart/index y 1 más |
| `inbox-group-header` | Cabecera de un grupo de la bandeja: miniatura, título y estado. Elige la URL de la tapa según exista o no el post | `group` | inquiry/detail, inquiry/received, inquiry/sent |
| `inbox-last-message` | Último mensaje de la conversación | `inquiry`, `viewerId` | inquiry/received, inquiry/sent |
| `input-control` | Input sin ligar, con soporte de sugerencias | `id`, `name`, `type`, `value`, `maxLength`, `min`, `max`, `placeholder`, `ariaLabel`, `describedBy`, `suggestionsId`, `sourceUrl`, `submitOnSelect`, `accept`, `multiple`, `form`, `cssClass`, `hasError`, `autofocus` | site-header, text-input, inquiry/detail, profile/index, publish/index |
| `inquiry-nav` | Pestañas recibidas y enviadas | `active`, `receivedCount`, `sentCount` | inquiry/received, inquiry/sent |
| `inquiry-status` | Estado de la consulta como texto | `status` | inquiry/detail, inquiry/received, inquiry/sent |
| `p` | Párrafo | `text`, `variant` | inbox-group-header, vinyl-card, auth/verify-required, cart/index, error/400, error/403 y 4 más |
| `pagination-link` | Un enlace de página | `baseUrl`, `extraParams`, `page`, `fragment`, `label`, `rel` | pagination |
| `pagination` | Flechas que conservan parámetros y ancla | `currentPage`, `hasPrevious`, `hasNext`, `baseUrl`, `extraParams`, `fragment`, `ariaLabel` | inquiry/received, inquiry/sent, landing/index, profile/index, profile/public |
| `post-badge` | Estado de una publicación | `deleted`, `status`, `showAvailable`, `variant` | inbox-group-header, vinyl-card, post/detail |
| `resend-verification` | Botón de reenvío: POST con CSRF | `variant` | site-header, auth/verify-required, auth/verify |
| `segmented-control` | Grupo de radios | `name`, `legend`, `items`, `messagePrefix`, `selectedValue`, `emptyLabel`, `hasError`, `errorId`, `required` | landing/index, publish/index |
| `select-control` | Select sin ligar | `id`, `name`, `items`, `messagePrefix`, `selectedValue`, `emptyLabel`, `labelledBy`, `describedBy`, `cssClass`, `hasError`, `placeholderOnly` | select, landing/index |
| `select` | Select ligado | `path`, `label`, `items`, `messagePrefix`, `emptyLabel`, `placeholderOnly` | address-fields, landing/index, publish/index |
| `site-header` | Barra superior: marca, buscador, acciones, aviso de verificación | `query`, `formId` | cart/index, inquiry/detail, inquiry/received, inquiry/sent, landing/index, post/contact y 4 más |
| `span` | Texto en línea | `text`, `variant` | vinyl-card, post/detail |
| `star-rating-input` | Estrellas como radios accesibles | `path`, `legend`, `max`, `valueCode` | inquiry/detail |
| `text-input` | Campo ligado a un form con etiqueta, pista y error | `path`, `label`, `type`, `maxLength`, `min`, `max`, `suggestionsId`, `sourceUrl`, `hint`, `autofocus`, `placeholder`, `hideLabel`, `describedBy`, `externalErrorsId` | address-fields, auth/forgot-password, auth/login, auth/register, auth/reset-password, landing/index y 2 más |
| `textarea` | Área de texto ligada | `path`, `label`, `maxLength`, `id` | inquiry/detail, post/contact, publish/index |
| `vinyl-card` | La tarjeta de un vinilo; el componente más reutilizado | `item`, `variant`, `href`, `hrefParams`, `title`, `artistName`, `price`, `coverUrl`, `preview`, `showStatus` | landing/index, post/contact, profile/index, profile/public, publish/index |

"Lo usan" se calculó buscando `<ui:nombre` en las vistas y en los demás tags de `8929aea`.

## Decisiones y por qué

| Decisión | Motivo | Fuente |
|---|---|---|
| Tag files en vez de `include` | Parámetros con nombre y tipo; el componente no depende de variables sueltas de la página | Estructura del código; inferencia |
| El escape vive dentro del componente | Una vista no puede olvidarse del `c:out` si usa el tag | `CLAUDE.md` del repo |
| `button` acepta `href` (ruta) o `url` (ya resuelta) | Poder agregar parámetros o un ancla con `c:url` antes de pasarla | Comentario en `button.tag` |
| Lista cerrada de iconos | Un nombre desconocido no dibuja nada en vez de romper la página | Comentario en `icon.tag` |
| Controles ligados (`text-input`, `select`, `textarea`) y sin ligar (`input-control`, `select-control`) | Los ligados usan `form:` y muestran errores; los otros sirven fuera de un `form:form`, como el buscador | Atributos de cada tag |
| El estado se muestra con texto, no solo con color | Accesibilidad | Comentarios en `inquiry-status.tag` e `inquiry-nav.tag` |

## Preguntas de defensa

**¿Cómo evitan XSS en las vistas?**
Todo dato que viene de la base o de quien usa el sitio se imprime con `c:out` o con los tags `form:`, que escapan HTML. Los componentes lo hacen adentro.

**¿Por qué usan `c:url`?**
Porque antepone el context path. Con una URL escrita a mano la aplicación funcionaría en local y fallaría en el servidor.

**¿Qué es un tag file?**
Un fragmento JSP con atributos declarados que se usa como una etiqueta propia. Es la forma de tener componentes sin scriptlets ni clases Java.

**¿Dónde va el token CSRF?**
`form:form` lo agrega solo. Los formularios escritos con `<form>` lo agregan con `sec:csrfInput`.

## Código de cada componente

### account-nav

Menú de la cuenta en la cabecera.

{{file:webapp/src/main/webapp/WEB-INF/tags/account-nav.tag}}

### address-fields

Campos de una dirección.

{{file:webapp/src/main/webapp/WEB-INF/tags/address-fields.tag}}

### address

Muestra una dirección, completa o recortada.

Atributos: `address` (obligatorio).

{{file:webapp/src/main/webapp/WEB-INF/tags/address.tag}}

### avatar

Foto o inicial.

Atributos: `imageId`, `userId` (obligatorio), `name` (obligatorio), `size`, `alt`, `preview`.

{{file:webapp/src/main/webapp/WEB-INF/tags/avatar.tag}}

### back-link

Enlace de volver.

Atributos: `href`, `label`, `page`, `fragment`.

{{file:webapp/src/main/webapp/WEB-INF/tags/back-link.tag}}

### brand

Marca.

Atributos: `size`.

{{file:webapp/src/main/webapp/WEB-INF/tags/brand.tag}}

### button

Botón o enlace con variantes.

Atributos: `label` (obligatorio), `variant`, `size`, `type`, `href`, `url`, `id`, `icon`, `data`, `name`, `value`.

{{file:webapp/src/main/webapp/WEB-INF/tags/button.tag}}

### confirm-dialog

Diálogo de confirmación.

Atributos: `title` (obligatorio), `confirmLabel` (obligatorio), `confirmVariant`.

{{file:webapp/src/main/webapp/WEB-INF/tags/confirm-dialog.tag}}

### h1

Título.

Atributos: `text` (obligatorio), `tone`.

{{file:webapp/src/main/webapp/WEB-INF/tags/h1.tag}}

### h3

Subtítulo con nivel configurable.

Atributos: `text` (obligatorio), `level`.

{{file:webapp/src/main/webapp/WEB-INF/tags/h3.tag}}

### head

Cabecera HTML común: estilos y scripts.

Atributos: `titleCode` (obligatorio), `pageScript`.

{{file:webapp/src/main/webapp/WEB-INF/tags/head.tag}}

### icon

Iconos SVG de una lista cerrada.

Atributos: `name` (obligatorio).

{{file:webapp/src/main/webapp/WEB-INF/tags/icon.tag}}

### inbox-group-header

Cabecera de un grupo de la bandeja: miniatura, título y estado. Elige la URL de la tapa según exista o no el post.

Atributos: `group` (obligatorio).

{{file:webapp/src/main/webapp/WEB-INF/tags/inbox-group-header.tag}}

### inbox-last-message

Último mensaje de la conversación.

Atributos: `inquiry` (obligatorio), `viewerId` (obligatorio).

{{file:webapp/src/main/webapp/WEB-INF/tags/inbox-last-message.tag}}

### input-control

Input sin ligar, con soporte de sugerencias.

Atributos: `id` (obligatorio), `name` (obligatorio), `type`, `value`, `maxLength`, `min`, `max`, `placeholder`, `ariaLabel`, `describedBy`, `suggestionsId`, `sourceUrl`, `submitOnSelect`, `accept`, `multiple`, `form`, `cssClass`, `hasError`, `autofocus`.

{{file:webapp/src/main/webapp/WEB-INF/tags/input-control.tag}}

### inquiry-nav

Pestañas recibidas y enviadas.

Atributos: `active` (obligatorio), `receivedCount` (obligatorio), `sentCount` (obligatorio).

{{file:webapp/src/main/webapp/WEB-INF/tags/inquiry-nav.tag}}

### inquiry-status

Estado de la consulta como texto.

Atributos: `status` (obligatorio).

{{file:webapp/src/main/webapp/WEB-INF/tags/inquiry-status.tag}}

### p

Párrafo.

Atributos: `text` (obligatorio), `variant`.

{{file:webapp/src/main/webapp/WEB-INF/tags/p.tag}}

### pagination-link

Un enlace de página.

Atributos: `baseUrl` (obligatorio), `extraParams`, `page` (obligatorio), `fragment`, `label` (obligatorio), `rel`.

{{file:webapp/src/main/webapp/WEB-INF/tags/pagination-link.tag}}

### pagination

Flechas que conservan parámetros y ancla.

Atributos: `currentPage` (obligatorio), `hasPrevious` (obligatorio), `hasNext` (obligatorio), `baseUrl` (obligatorio), `extraParams`, `fragment`, `ariaLabel` (obligatorio).

{{file:webapp/src/main/webapp/WEB-INF/tags/pagination.tag}}

### post-badge

Estado de una publicación.

Atributos: `deleted`, `status`, `showAvailable`, `variant`.

{{file:webapp/src/main/webapp/WEB-INF/tags/post-badge.tag}}

### resend-verification

Botón de reenvío: POST con CSRF.

Atributos: `variant`.

{{file:webapp/src/main/webapp/WEB-INF/tags/resend-verification.tag}}

### segmented-control

Grupo de radios.

Atributos: `name` (obligatorio), `legend` (obligatorio), `items` (obligatorio), `messagePrefix` (obligatorio), `selectedValue`, `emptyLabel`, `hasError`, `errorId`, `required`.

{{file:webapp/src/main/webapp/WEB-INF/tags/segmented-control.tag}}

### select-control

Select sin ligar.

Atributos: `id` (obligatorio), `name` (obligatorio), `items` (obligatorio), `messagePrefix` (obligatorio), `selectedValue`, `emptyLabel`, `labelledBy`, `describedBy`, `cssClass`, `hasError`, `placeholderOnly`.

{{file:webapp/src/main/webapp/WEB-INF/tags/select-control.tag}}

### select

Select ligado.

Atributos: `path` (obligatorio), `label` (obligatorio), `items` (obligatorio), `messagePrefix` (obligatorio), `emptyLabel` (obligatorio), `placeholderOnly`.

{{file:webapp/src/main/webapp/WEB-INF/tags/select.tag}}

### site-header

Barra superior: marca, buscador, acciones, aviso de verificación.

Atributos: `query`, `formId`.

{{file:webapp/src/main/webapp/WEB-INF/tags/site-header.tag}}

### span

Texto en línea.

Atributos: `text` (obligatorio), `variant`.

{{file:webapp/src/main/webapp/WEB-INF/tags/span.tag}}

### star-rating-input

Estrellas como radios accesibles.

Atributos: `path` (obligatorio), `legend` (obligatorio), `max` (obligatorio), `valueCode` (obligatorio).

{{file:webapp/src/main/webapp/WEB-INF/tags/star-rating-input.tag}}

### text-input

Campo ligado a un form con etiqueta, pista y error.

Atributos: `path` (obligatorio), `label` (obligatorio), `type`, `maxLength`, `min`, `max`, `suggestionsId`, `sourceUrl`, `hint`, `autofocus`, `placeholder`, `hideLabel`, `describedBy`, `externalErrorsId`.

{{file:webapp/src/main/webapp/WEB-INF/tags/text-input.tag}}

### textarea

Área de texto ligada.

Atributos: `path` (obligatorio), `label` (obligatorio), `maxLength`, `id`.

{{file:webapp/src/main/webapp/WEB-INF/tags/textarea.tag}}

### vinyl-card

La tarjeta de un vinilo; el componente más reutilizado.

Atributos: `item`, `variant`, `href`, `hrefParams`, `title`, `artistName`, `price`, `coverUrl`, `preview`, `showStatus`.

{{file:webapp/src/main/webapp/WEB-INF/tags/vinyl-card.tag}}
