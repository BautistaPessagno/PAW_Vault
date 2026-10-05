---
title: "UI components"
categories: ["Web"]
type: "guide"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["webapp/src/main/webapp/WEB-INF/tags/account-nav.tag", "webapp/src/main/webapp/WEB-INF/tags/address-fields.tag", "webapp/src/main/webapp/WEB-INF/tags/address.tag", "webapp/src/main/webapp/WEB-INF/tags/avatar.tag", "webapp/src/main/webapp/WEB-INF/tags/back-link.tag", "webapp/src/main/webapp/WEB-INF/tags/brand.tag", "webapp/src/main/webapp/WEB-INF/tags/button.tag", "webapp/src/main/webapp/WEB-INF/tags/confirm-dialog.tag", "webapp/src/main/webapp/WEB-INF/tags/filter-chips.tag", "webapp/src/main/webapp/WEB-INF/tags/h1.tag", "webapp/src/main/webapp/WEB-INF/tags/h3.tag", "webapp/src/main/webapp/WEB-INF/tags/head.tag", "webapp/src/main/webapp/WEB-INF/tags/icon.tag", "webapp/src/main/webapp/WEB-INF/tags/inbox-group-header.tag", "webapp/src/main/webapp/WEB-INF/tags/inbox-last-message.tag", "webapp/src/main/webapp/WEB-INF/tags/input-control.tag", "webapp/src/main/webapp/WEB-INF/tags/inquiry-nav.tag", "webapp/src/main/webapp/WEB-INF/tags/inquiry-status.tag", "webapp/src/main/webapp/WEB-INF/tags/p.tag", "webapp/src/main/webapp/WEB-INF/tags/pagination-link.tag", "webapp/src/main/webapp/WEB-INF/tags/pagination.tag", "webapp/src/main/webapp/WEB-INF/tags/post-badge.tag", "webapp/src/main/webapp/WEB-INF/tags/rating.tag", "webapp/src/main/webapp/WEB-INF/tags/resend-verification.tag", "webapp/src/main/webapp/WEB-INF/tags/review-content.tag", "webapp/src/main/webapp/WEB-INF/tags/segmented-control.tag", "webapp/src/main/webapp/WEB-INF/tags/select-control.tag", "webapp/src/main/webapp/WEB-INF/tags/select.tag", "webapp/src/main/webapp/WEB-INF/tags/site-header.tag", "webapp/src/main/webapp/WEB-INF/tags/span.tag", "webapp/src/main/webapp/WEB-INF/tags/star-rating-input.tag", "webapp/src/main/webapp/WEB-INF/tags/text-input.tag", "webapp/src/main/webapp/WEB-INF/tags/textarea.tag", "webapp/src/main/webapp/WEB-INF/tags/user-byline.tag", "webapp/src/main/webapp/WEB-INF/tags/vinyl-card.tag"]
---

# UI components

> [!summary] En una frase
> Las páginas no repiten HTML: se arman con 35 componentes propios (tag files de JSP) que encapsulan el marcado, el escape de datos, las URL y los textos traducidos.

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
| `avatar` | Foto o inicial | `imageId`, `userId`, `name`, `size`, `alt`, `preview` | user-byline, profile/index, profile/public |
| `back-link` | Enlace de volver | `href`, `label`, `page`, `postStatus`, `fragment` | inquiry/detail, post/detail |
| `brand` | Marca | `size` | site-header, auth/forgot-password, auth/login, auth/register, auth/reset-password, auth/verify-required y 1 más |
| `button` | Botón o enlace con variantes | `label`, `variant`, `size`, `type`, `href`, `url`, `id`, `icon`, `data`, `name`, `value` | account-nav, confirm-dialog, resend-verification, site-header, auth/forgot-password, auth/login y 18 más |
| `confirm-dialog` | Diálogo de confirmación | `title`, `confirmLabel`, `confirmVariant` | inquiry/detail, post/detail, profile/index |
| `filter-chips` | Chips de filtro con su cantidad; el chip activo lleva a la URL sin filtro | `baseUrl`, `paramName`, `values`, `active`, `counts`, `messagePrefix`, `label`, `fragment` | inquiry/received, inquiry/sent, profile/index |
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
| `pagination-link` | Un enlace de página | `baseUrl`, `extraParams`, `page`, `pageParam`, `fragment`, `label`, `rel` | pagination |
| `pagination` | Flechas que conservan parámetros y ancla | `currentPage`, `hasPrevious`, `hasNext`, `baseUrl`, `pageParam`, `extraParams`, `fragment`, `ariaLabel` | inquiry/received, inquiry/sent, landing/index, profile/index, profile/public |
| `post-badge` | Estado de una publicación | `deleted`, `status`, `showAvailable`, `variant` | inbox-group-header, vinyl-card, post/detail |
| `rating` | Estrellas de solo lectura con relleno parcial para promedios | `value`, `maxRating`, `label` | review-content, profile/public |
| `resend-verification` | Botón de reenvío: POST con CSRF | `variant` | site-header, auth/verify-required, auth/verify |
| `review-content` | Puntaje, comentario y, opcional, autor de una reseña | `review`, `maxRating`, `showAuthor` | inquiry/detail, profile/public |
| `segmented-control` | Grupo de radios | `name`, `legend`, `hideLegend`, `items`, `messagePrefix`, `selectedValue`, `emptyLabel`, `hasError`, `errorId`, `required` | landing/index, profile/public, publish/index |
| `select-control` | Select sin ligar | `id`, `name`, `items`, `messagePrefix`, `selectedValue`, `emptyLabel`, `labelledBy`, `describedBy`, `cssClass`, `hasError`, `placeholderOnly` | select, landing/index |
| `select` | Select ligado | `path`, `label`, `items`, `messagePrefix`, `emptyLabel`, `placeholderOnly` | address-fields, landing/index, publish/index |
| `site-header` | Barra superior: marca, buscador, acciones, aviso de verificación | `query`, `formId` | cart/index, inquiry/detail, inquiry/received, inquiry/sent, landing/index, post/contact y 4 más |
| `span` | Texto en línea | `text`, `variant` | vinyl-card, post/detail |
| `star-rating-input` | Estrellas como radios accesibles | `path`, `legend`, `max`, `valueCode` | inquiry/detail |
| `text-input` | Campo ligado a un form con etiqueta, pista y error | `path`, `label`, `type`, `maxLength`, `min`, `max`, `suggestionsId`, `sourceUrl`, `hint`, `autofocus`, `placeholder`, `hideLabel`, `describedBy`, `externalErrorsId` | address-fields, auth/forgot-password, auth/login, auth/register, auth/reset-password, landing/index y 2 más |
| `textarea` | Área de texto ligada | `path`, `label`, `maxLength`, `id`, `rows`, `hideLabel` | inquiry/detail, post/contact, publish/index |
| `user-byline` | Foto y nombre de una Cuenta con enlace a su perfil público | `userId`, `username`, `imageId` | review-content, inquiry/detail, post/detail |
| `vinyl-card` | La tarjeta de un vinilo; el componente más reutilizado | `item`, `variant`, `href`, `hrefParams`, `title`, `artistName`, `price`, `coverUrl`, `preview`, `showStatus` | landing/index, post/contact, profile/index, profile/public, publish/index |

"Lo usan" se calculó buscando `<ui:nombre` en las vistas y en los demás tags de `c3e2a4c`.

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

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/tags/account-nav.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/account-nav.tag>), líneas 1–30.

```jsp
<%@ tag body-content="empty" pageEncoding="UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="sec" uri="http://www.springframework.org/security/tags" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<spring:message code="auth.navigation.label" var="navigationLabel"/>
<spring:message code="auth.login.action" var="loginLabel"/>
<spring:message code="auth.register.action" var="registerLabel"/>
<spring:message code="inquiry.navigation" var="inquiryLabel"/>
<c:url value="/profile" var="profileUrl"/>
<nav class="account-nav" aria-label="${navigationLabel}">
    <sec:authorize access="isAnonymous()">
        <ui:button label="${loginLabel}" variant="ghost" size="sm" href="/login"/>
        <ui:button label="${registerLabel}" variant="primary" size="sm" href="/register"/>
    </sec:authorize>
    <sec:authorize access="isAuthenticated()">
        <%-- getUsername() del UserDetails es el email (con el que se inicia sesion). En la
             cabecera va el nombre que la persona eligio al verificar la cuenta. --%>
        <sec:authentication property="principal.displayName" var="displayName" scope="page"/>
        <ui:button label="${inquiryLabel}" variant="ghost" size="sm" href="/inquiries" icon="inbox"/>
        <%-- El carrito es de cuentas verificadas: cartCount lo deja CartCountAdvice solo para ellas. --%>
        <sec:authorize access="principal.verified">
            <spring:message code="cart.navigation" var="cartLabel" arguments="${empty cartCount ? 0 : cartCount.value}"/>
            <ui:button label="${cartLabel}" variant="ghost" size="sm" href="/cart" icon="cart"/>
        </sec:authorize>
        <%-- La identidad va al final: es el ancla de la cuenta y lleva al perfil. --%>
        <a class="button button--ghost button--sm account-nav__identity" href="<c:out value="${profileUrl}"/>"
           title="<c:out value="${displayName}"/>"><ui:icon name="user"/><span class="account-nav__name"><c:out value="${displayName}"/></span></a>
    </sec:authorize>
</nav>
```

### address-fields

Campos de una dirección.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/tags/address-fields.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/address-fields.tag>), líneas 1–24.

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>

<%-- Los campos de una direccion, para usar dentro de un form:form cuyo modelo tenga street,
     streetNumber, apartment, city, province, postalCode y notes. Necesita ${provinces}. --%>
<spring:message code="address.street.label" var="streetLabel"/>
<spring:message code="address.streetNumber.label" var="streetNumberLabel"/>
<spring:message code="address.apartment.label" var="apartmentLabel"/>
<spring:message code="address.city.label" var="cityLabel"/>
<spring:message code="address.province.label" var="provinceLabel"/>
<spring:message code="address.province.placeholder" var="provincePlaceholder"/>
<spring:message code="address.postalCode.label" var="postalCodeLabel"/>
<spring:message code="address.notes.label" var="notesLabel"/>
<div class="address-fields">
    <ui:text-input path="street" label="${streetLabel}" maxLength="100"/>
    <ui:text-input path="streetNumber" label="${streetNumberLabel}" maxLength="10"/>
    <ui:text-input path="apartment" label="${apartmentLabel}" maxLength="20"/>
    <ui:text-input path="city" label="${cityLabel}" maxLength="100"/>
    <ui:select path="province" label="${provinceLabel}" items="${provinces}" messagePrefix="province"
               emptyLabel="${provincePlaceholder}" placeholderOnly="${true}"/>
    <ui:text-input path="postalCode" label="${postalCodeLabel}" maxLength="10"/>
    <ui:text-input path="notes" label="${notesLabel}" maxLength="200"/>
</div>
```

### address

Muestra una dirección, completa o recortada.

Atributos: `address` (obligatorio).

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/tags/address.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/address.tag>), líneas 1–20.

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%@ attribute name="address" required="true" type="ar.edu.itba.paw.models.Address" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>

<%-- Una direccion de envio: calle y altura con piso, y debajo ciudad, CP y provincia. Si el
     service la recorto a ciudad y provincia, se muestra solo eso. --%>
<spring:message code="province.${address.province}" var="provinceName"/>
<span class="address">
    <c:choose>
        <c:when test="${address.cityAndProvinceOnly}">
            <span class="address__line"><c:out value="${address.city}"/>, <c:out value="${provinceName}"/></span>
        </c:when>
        <c:otherwise>
            <span class="address__line"><c:out value="${address.street}"/> <c:out value="${address.streetNumber}"/><c:if test="${not empty address.apartment}">, <c:out value="${address.apartment}"/></c:if></span>
            <span class="address__line address__line--muted"><c:out value="${address.city}"/> (<c:out value="${address.postalCode}"/>), <c:out value="${provinceName}"/></span>
            <c:if test="${not empty address.notes}"><span class="address__line address__line--muted"><c:out value="${address.notes}"/></span></c:if>
        </c:otherwise>
    </c:choose>
</span>
```

### avatar

Foto o inicial.

Atributos: `imageId`, `userId` (obligatorio), `name` (obligatorio), `size`, `alt`, `preview`.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/tags/avatar.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/avatar.tag>), líneas 1–32.

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%@ attribute name="imageId" required="false" type="java.lang.Long" %>
<%@ attribute name="userId" required="true" type="java.lang.Long" %>
<%-- name: el nombre de la Cuenta; sin foto se muestra su inicial. --%>
<%@ attribute name="name" required="true" %>
<%@ attribute name="size" required="false" %>
<%-- alt vacio cuando el nombre ya se lee al lado: la foto es decorativa. --%>
<%@ attribute name="alt" required="false" %>
<%-- preview: emite la imagen y la inicial a la vez (una oculta), con los data-* que usa
     account-edit.js para mostrar la foto elegida antes de guardarla. --%>
<%@ attribute name="preview" required="false" type="java.lang.Boolean" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions" %>
<c:set var="safeSize" value="${size eq 'sm' or size eq 'lg' or size eq 'xl' ? size : 'md'}" />
<%-- Primer code point, no primer char: un username que arranca con un emoji (fuera del BMP)
     no puede quedar partido en medio surrogate. --%>
<c:set var="initial" value="${empty name ? '' : fn:toUpperCase(name.substring(0, name.offsetByCodePoints(0, 1)))}" />
<span class="avatar avatar--${safeSize}">
    <c:choose>
        <c:when test="${preview}">
            <c:if test="${not empty imageId}"><c:url value="/users/${userId}/avatar/${imageId}" var="avatarSrc" /></c:if>
            <img class="avatar__image"<c:if test="${not empty imageId}"> src="<c:out value="${avatarSrc}" />"</c:if> alt="<c:out value="${alt}" />"
                 data-avatar-preview<c:if test="${empty imageId}"> hidden</c:if> />
            <span class="avatar__initial" aria-hidden="true" data-avatar-placeholder<c:if test="${not empty imageId}"> hidden</c:if>><c:out value="${initial}" /></span>
        </c:when>
        <c:when test="${not empty imageId}">
            <c:url value="/users/${userId}/avatar/${imageId}" var="avatarSrc" />
            <img class="avatar__image" src="<c:out value="${avatarSrc}" />" alt="<c:out value="${alt}" />" />
        </c:when>
        <c:otherwise><span class="avatar__initial" aria-hidden="true"><c:out value="${initial}" /></span></c:otherwise>
    </c:choose>
</span>
```

### back-link

Enlace de volver.

Atributos: `href`, `label`, `page`, `postStatus`, `fragment`.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/tags/back-link.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/back-link.tag>), líneas 1–24.

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%@ attribute name="href" required="false" %>
<%@ attribute name="label" required="false" %>
<%@ attribute name="page" required="false" type="java.lang.Integer" %>
<%@ attribute name="postStatus" required="false" type="java.lang.Object" %>
<%@ attribute name="fragment" required="false" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>

<spring:message code="nav.back" var="defaultLabel" />
<c:set var="backLabel" value="${empty label ? defaultLabel : label}" />
<c:url value="${empty href ? '/' : href}" var="backHref">
    <c:if test="${not empty postStatus}"><c:param name="postStatus" value="${postStatus}" /></c:if>
    <c:if test="${not empty page}"><c:param name="page" value="${page}" /></c:if>
</c:url>

<%-- El link va envuelto: page-shell es un grid y un ancla suelta se estira a todo el ancho. --%>
<div class="back-link">
    <%-- La flecha es decorativa: el texto visible ya dice a donde vuelve el link. --%>
    <a class="back-link__anchor" href="<c:out value="${backHref}${empty fragment ? '' : '#'.concat(fragment)}" />">
        <span class="back-link__arrow" aria-hidden="true">&#8592;</span>
        <c:out value="${backLabel}" />
    </a>
</div>
```

### brand

Marca.

Atributos: `size`.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/tags/brand.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/brand.tag>), líneas 1–14.

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%@ attribute name="size" required="false" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>

<spring:message code="landing.heading" var="brandLabel" />
<c:url value="/" var="homeUrl" />
<c:url value="/images/logo.svg" var="logoUrl" />

<%-- El disco es decorativo: el texto ya nombra el link al catalogo. --%>
<a class="brand ${size eq 'lg' ? 'brand--lg' : ''}" href="<c:out value="${homeUrl}" />">
    <img class="brand__mark" src="<c:out value="${logoUrl}" />" alt="" />
    <c:out value="${brandLabel}" />
</a>
```

### button

Botón o enlace con variantes.

Atributos: `label` (obligatorio), `variant`, `size`, `type`, `href`, `url`, `id`, `icon`, `data`, `name`, `value`.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/tags/button.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/button.tag>), líneas 1–33.

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%@ attribute name="label" required="true" %>
<%@ attribute name="variant" required="false" %>
<%@ attribute name="size" required="false" %>
<%@ attribute name="type" required="false" %>
<%-- href: ruta sin context path, el tag la pasa por c:url. url: URL ya resuelta con c:url
     (para sumarle c:param o un fragmento); se usa tal cual. --%>
<%@ attribute name="href" required="false" %>
<%@ attribute name="url" required="false" %>
<%@ attribute name="id" required="false" %>
<%@ attribute name="icon" required="false" %>
<%-- Atributo de datos para el JS de la pagina, sin valor: data="cancel-edit" emite data-cancel-edit. --%>
<%@ attribute name="data" required="false" %>
<%-- name y value: para que un form con varios submit sepa cual se apreto. Solo en <button>. --%>
<%@ attribute name="name" required="false" %>
<%@ attribute name="value" required="false" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>

<c:set var="classes" value="button button--${empty variant ? 'primary' : variant} button--${empty size ? 'md' : size}" />

<c:choose>
    <c:when test="${not empty href or not empty url}">
        <c:choose>
            <c:when test="${not empty url}"><c:set var="buttonHref" value="${url}" /></c:when>
            <c:otherwise><c:url value="${href}" var="buttonHref" /></c:otherwise>
        </c:choose>
        <a class="${classes}" href="<c:out value="${buttonHref}" />"<c:if test="${not empty id}"> id="<c:out value="${id}" />"</c:if><c:if test="${not empty data}"> data-<c:out value="${data}" /></c:if>><c:if test="${not empty icon}"><ui:icon name="${icon}"/></c:if><c:out value="${label}" /></a>
    </c:when>
    <c:otherwise>
        <button class="${classes}" type="${type eq 'submit' ? 'submit' : 'button'}"<c:if test="${not empty name}"> name="<c:out value="${name}" />" value="<c:out value="${value}" />"</c:if><c:if test="${not empty id}"> id="<c:out value="${id}" />"</c:if><c:if test="${not empty data}"> data-<c:out value="${data}" /></c:if>><c:if test="${not empty icon}"><ui:icon name="${icon}"/></c:if><c:out value="${label}" /></button>
    </c:otherwise>
</c:choose>
```

### confirm-dialog

Diálogo de confirmación.

Atributos: `title` (obligatorio), `confirmLabel` (obligatorio), `confirmVariant`.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/tags/confirm-dialog.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/confirm-dialog.tag>), líneas 1–23.

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%@ attribute name="title" required="true" %>
<%@ attribute name="confirmLabel" required="true" %>
<%@ attribute name="confirmVariant" required="false" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>

<%-- Dialogo que abre confirm-action.js para todo form con data-confirm-message. Los ids son
     los que busca el script: uno solo por pagina. --%>
<spring:message code="form.cancel" var="cancelLabel"/>
<dialog class="confirm-dialog" id="confirm-action-dialog" aria-labelledby="confirm-action-dialog-title" aria-describedby="confirm-action-dialog-message">
    <div class="confirm-dialog__content">
        <h2 class="confirm-dialog__title" id="confirm-action-dialog-title"><c:out value="${title}"/></h2>
        <p class="confirm-dialog__message" id="confirm-action-dialog-message"></p>
        <div class="confirm-dialog__actions">
            <form method="dialog">
                <ui:button label="${cancelLabel}" variant="ghost" type="submit"/>
            </form>
            <ui:button label="${confirmLabel}" variant="${confirmVariant}" id="confirm-action-dialog-confirm"/>
        </div>
    </div>
</dialog>
```

### filter-chips

Chips de filtro con su cantidad; el chip activo lleva a la URL sin filtro.

Atributos: `baseUrl` (obligatorio), `paramName` (obligatorio), `values` (obligatorio), `active`, `counts` (obligatorio), `messagePrefix` (obligatorio), `label` (obligatorio), `fragment`.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/tags/filter-chips.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/filter-chips.tag>), líneas 1–39.

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%-- Ruta del listado sin context path, ej. /inquiries. --%>
<%@ attribute name="baseUrl" required="true" %>
<%-- Query param del filtro. No puede llamarse param: en EL ese nombre es el de los parametros del request. --%>
<%@ attribute name="paramName" required="true" %>
<%@ attribute name="values" required="true" type="java.lang.Object[]" %>
<%@ attribute name="active" required="false" type="java.lang.Object" %>
<%-- Valor -> cantidad. Un valor que no esta en el mapa se muestra como 0. --%>
<%@ attribute name="counts" required="true" type="java.util.Map" %>
<%-- Usa <prefix>.<VALOR> para el texto de cada chip. --%>
<%@ attribute name="messagePrefix" required="true" %>
<%@ attribute name="label" required="true" %>
<%@ attribute name="fragment" required="false" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>

<%-- Sin filtro se ve todo: no hay chip "Todas". El chip activo lleva a la URL sin filtro, asi
     tocarlo de nuevo lo quita. Cambiar de filtro vuelve a la pagina 1: los links no llevan page. --%>
<c:set var="anchor" value="${empty fragment ? '' : '#'.concat(fragment)}"/>
<c:url value="${baseUrl}" var="clearUrl"/>
<spring:message code="filterChips.clear" var="clearLabel"/>
<nav class="filter-chips" aria-label="<c:out value="${label}"/>">
    <c:forEach items="${values}" var="value">
        <c:set var="valueName">${value}</c:set>
        <c:set var="selected" value="${not empty active and active eq value}"/>
        <c:url value="${baseUrl}" var="valueUrl">
            <c:param name="${paramName}" value="${valueName}"/>
        </c:url>
        <a class="filter-chips__chip${selected ? ' filter-chips__chip--active' : ''}"
           href="<c:out value="${selected ? clearUrl : valueUrl}${anchor}"/>"
           <c:if test="${selected}">aria-current="true"</c:if>>
            <spring:message code="${messagePrefix}.${valueName}"/>
            <span class="filter-chips__count"><c:out value="${counts[value]}" default="0"/></span>
            <c:if test="${selected}">
                <span class="visually-hidden"><c:out value="${clearLabel}"/></span>
            </c:if>
        </a>
    </c:forEach>
</nav>
```

### h1

Título.

Atributos: `text` (obligatorio), `tone`.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/tags/h1.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/h1.tag>), líneas 1–6.

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%@ attribute name="text" required="true" %>
<%@ attribute name="tone" required="false" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>

<h1 class="text text-h1 ${tone eq 'accent' ? 'text--accent' : ''}"><c:out value="${text}" /></h1>
```

### h3

Subtítulo con nivel configurable.

Atributos: `text` (obligatorio), `level`.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/tags/h3.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/h3.tag>), líneas 1–12.

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="scriptless" %>
<%@ attribute name="text" required="true" %>
<%-- level="2" para las secciones que encabezan su propia region: el estilo es el mismo,
     lo que cambia es el nivel del esquema del documento. El cuerpo, opcional, va detras
     del texto: sirve para colgarle una insignia al titulo. --%>
<%@ attribute name="level" required="false" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>

<c:choose>
    <c:when test="${level eq '2'}"><h2 class="text text-h3"><c:out value="${text}" /><jsp:doBody /></h2></c:when>
    <c:otherwise><h3 class="text text-h3"><c:out value="${text}" /><jsp:doBody /></h3></c:otherwise>
</c:choose>
```

### head

Cabecera HTML común: estilos y scripts.

Atributos: `titleCode` (obligatorio), `pageScript`.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/tags/head.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/head.tag>), líneas 1–31.

```jsp
<%@ tag body-content="empty" pageEncoding="UTF-8" %>
<%@ attribute name="titleCode" required="true" rtexprvalue="true" type="java.lang.String" %>
<%-- Script propio de una pagina (nombre sin .js): se carga solo donde se usa. --%>
<%@ attribute name="pageScript" required="false" type="java.lang.String" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<c:url value="/images/logo.svg" var="faviconUrl"/>
<c:url value="/css/tokens.css" var="tokensCss"/>
<c:url value="/css/components.css" var="componentsCss"/>
<c:url value="/css/style.css" var="cssUrl"/>
<c:url value="/js/submit-once.js" var="submitOnceJs"/>
<c:url value="/js/catalog.js" var="catalogJs"/>
<c:url value="/js/confirm-action.js" var="confirmActionJs"/>
<c:url value="/js/autocomplete.js" var="autocompleteJs"/>
<head>
    <meta charset="UTF-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <title><spring:message code="${titleCode}"/></title>
    <link rel="icon" type="image/svg+xml" href="${faviconUrl}"/>
    <link rel="stylesheet" href="${tokensCss}"/>
    <link rel="stylesheet" href="${componentsCss}"/>
    <link rel="stylesheet" href="${cssUrl}"/>
    <script src="${submitOnceJs}" defer></script>
    <script src="${catalogJs}" defer></script>
    <script src="${confirmActionJs}" defer></script>
    <script src="${autocompleteJs}" defer></script>
    <c:if test="${not empty pageScript}">
        <c:url value="/js/${pageScript}.js" var="pageScriptJs"/>
        <script src="${pageScriptJs}" defer></script>
    </c:if>
</head>
```

### icon

Iconos SVG de una lista cerrada.

Atributos: `name` (obligatorio).

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/tags/icon.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/icon.tag>), líneas 1–34.

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%@ attribute name="name" required="true" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions" %>

<%-- Iconos de trazo (16px, currentColor). Decorativos: el texto que acompanan ya dice
     que hacen. Lista cerrada: un nombre desconocido no dibuja nada. --%>
<c:set var="path">
    <c:choose>
        <c:when test="${name eq 'plus'}">M12 5v14M5 12h14</c:when>
        <c:when test="${name eq 'cart'}">M8 21a1 1 0 1 0 0-2 1 1 0 0 0 0 2zM19 21a1 1 0 1 0 0-2 1 1 0 0 0 0 2zM2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12</c:when>
        <c:when test="${name eq 'inbox'}">M22 12h-6l-2 3h-4l-2-3H2M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z</c:when>
        <c:when test="${name eq 'user'}">M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2M16 7a4 4 0 1 1-8 0 4 4 0 0 1 8 0z</c:when>
        <c:when test="${name eq 'shield'}">M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z</c:when>
        <c:when test="${name eq 'log-out'}">M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9</c:when>
        <c:when test="${name eq 'pencil'}">M17 3a2.83 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z</c:when>
        <c:when test="${name eq 'trash'}">M3 6h18M8 6V4h8v2M19 6l-1 14H6L5 6M10 11v6M14 11v6</c:when>
        <c:when test="${name eq 'mail'}">M4 4h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2zM22 6l-10 7L2 6</c:when>
        <c:when test="${name eq 'check'}">M20 6 9 17l-5-5</c:when>
        <c:when test="${name eq 'x'}">M18 6 6 18M6 6l12 12</c:when>
        <c:when test="${name eq 'arrow-up-right'}">M7 17 17 7M7 7h10v10</c:when>
        <c:when test="${name eq 'clock'}">M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0zM12 7v5l3 2</c:when>
        <c:when test="${name eq 'tag'}">M20.6 13.4 13.4 20.6a2 2 0 0 1-2.8 0L3 13V3h10l7.6 7.6a2 2 0 0 1 0 2.8ZM7.5 7.5h.01</c:when>
        <c:when test="${name eq 'chevron-left'}">m15 18-6-6 6-6</c:when>
        <c:when test="${name eq 'chevron-right'}">m9 18 6-6-6-6</c:when>
    </c:choose>
</c:set>
<%-- Un nombre fuera de la lista no matchea ningun c:when y deja el valor en blanco: el
     trim lo normaliza a vacio para que el c:if no dibuje un svg sin trazo. --%>
<c:set var="d" value="${fn:trim(path)}"/>
<c:if test="${not empty d}">
<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.25"
     stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="<c:out value="${d}"/>"/></svg>
</c:if>
```

### inbox-group-header

Cabecera de un grupo de la bandeja: miniatura, título y estado. Elige la URL de la tapa según exista o no el post.

Atributos: `group` (obligatorio).

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/tags/inbox-group-header.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/inbox-group-header.tag>), líneas 1–31.

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%-- Un InquiryGroup de la bandeja o el InquirySummary de la Venta: los dos exponen coverImageId,
     postId, albumId, postDeleted, title, postStatus y artistName. --%>
<%@ attribute name="group" required="true" type="java.lang.Object" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>

<%-- Cabecera de un grupo de la bandeja (recibidas y enviadas): miniatura, titulo con el
     estado de la publicacion y artista. La cabecera entera lleva a la ficha con un enlace
     estirado, como la card; una publicacion eliminada no tiene adonde ir y no lo dibuja. --%>
<c:choose>
    <c:when test="${empty group.coverImageId}"><c:url value="/images/covers/placeholder.svg" var="coverUrl"/></c:when>
    <c:when test="${group.postDeleted}">
        <c:url value="/albums/${group.albumId}/cover/${group.coverImageId}" var="coverUrl"/>
    </c:when>
    <c:otherwise><c:url value="/post/${group.postId}/images/${group.coverImageId}" var="coverUrl"/></c:otherwise>
</c:choose>
<spring:message code="vinylCard.cover.alt" var="coverAlt"><spring:argument value="${group.title}"/></spring:message>
<div class="inbox-group__post${group.postDeleted ? '' : ' inbox-group__post--linked'}">
    <c:if test="${not group.postDeleted}">
        <c:url value="/post/${group.postId}" var="postUrl"/>
        <spring:message code="vinylCard.open" var="openLabel"><spring:argument value="${group.title}"/></spring:message>
        <a class="inbox-group__anchor" href="<c:out value="${postUrl}"/>" aria-label="<c:out value="${openLabel}"/>"></a>
    </c:if>
    <div class="inbox-group__cover"><img src="<c:out value="${coverUrl}"/>" alt="<c:out value="${coverAlt}"/>"/></div>
    <div class="inbox-group__title">
        <ui:h3 text="${group.title}" level="2"><ui:post-badge deleted="${group.postDeleted}" status="${group.postStatus}"/></ui:h3>
        <ui:p text="${group.artistName}" variant="lead"/>
    </div>
</div>
```

### inbox-last-message

Último mensaje de la conversación.

Atributos: `inquiry` (obligatorio), `viewerId` (obligatorio).

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/tags/inbox-last-message.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/inbox-last-message.tag>), líneas 1–25.

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%@ attribute name="inquiry" required="true" type="ar.edu.itba.paw.models.InquirySummary" %>
<%@ attribute name="viewerId" required="true" type="java.lang.Long" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>

<%-- Ultimo Mensaje de la Conversacion en una fila de la bandeja, recortado a dos lineas y con
     su autor: "Vos" si lo escribio quien mira, o el nombre de la otra parte. --%>
<c:set var="lastMessage" value="${inquiry.lastMessage}"/>
<c:choose>
    <c:when test="${empty lastMessage}">
        <p class="inbox-row__msg inbox-row__msg--empty"><spring:message code="inquiry.conversation.empty.short"/></p>
    </c:when>
    <c:otherwise>
        <c:choose>
            <c:when test="${lastMessage.senderId eq viewerId}"><spring:message code="inquiry.conversation.you" var="author"/></c:when>
            <c:when test="${lastMessage.senderId eq inquiry.buyerId}"><c:set var="author" value="${inquiry.buyerUsername}"/></c:when>
            <c:otherwise><c:set var="author" value="${inquiry.sellerUsername}"/></c:otherwise>
        </c:choose>
        <spring:message code="inquiry.conversation.authorPrefix" var="authorPrefix">
            <spring:argument value="${author}"/>
        </spring:message>
        <p class="inbox-row__msg inbox-row__msg--clamp"><span class="inbox-row__author"><c:out value="${authorPrefix}"/></span> <c:out value="${lastMessage.body}"/></p>
    </c:otherwise>
</c:choose>
```

### input-control

Input sin ligar, con soporte de sugerencias.

Atributos: `id` (obligatorio), `name` (obligatorio), `type`, `value`, `maxLength`, `min`, `max`, `placeholder`, `ariaLabel`, `describedBy`, `suggestionsId`, `sourceUrl`, `submitOnSelect`, `accept`, `multiple`, `form`, `cssClass`, `hasError`, `autofocus`.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/tags/input-control.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/input-control.tag>), líneas 1–49.

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="scriptless" %>
<%@ attribute name="id" required="true" %>
<%@ attribute name="name" required="true" %>
<%@ attribute name="type" required="false" %>
<%@ attribute name="value" required="false" %>
<%@ attribute name="maxLength" required="false" type="java.lang.Integer" %>
<%@ attribute name="min" required="false" type="java.lang.Integer" %>
<%@ attribute name="max" required="false" type="java.lang.Integer" %>
<%@ attribute name="placeholder" required="false" %>
<%@ attribute name="ariaLabel" required="false" %>
<%@ attribute name="describedBy" required="false" %>
<%@ attribute name="suggestionsId" required="false" %>
<%@ attribute name="sourceUrl" required="false" %>
<%@ attribute name="submitOnSelect" required="false" type="java.lang.Boolean" %>
<%@ attribute name="accept" required="false" %>
<%@ attribute name="multiple" required="false" type="java.lang.Boolean" %>
<%@ attribute name="form" required="false" %>
<%@ attribute name="cssClass" required="false" %>
<%@ attribute name="hasError" required="false" type="java.lang.Boolean" %>
<%@ attribute name="autofocus" required="false" type="java.lang.Boolean" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>

<c:set var="safeType" value="text" />
<c:if test="${type eq 'search' or type eq 'email' or type eq 'number' or type eq 'password' or type eq 'file'}">
    <c:set var="safeType" value="${type}" />
</c:if>
<div class="input-field__control-wrap${empty cssClass ? '' : ' '}${cssClass}"
     <c:if test="${not empty suggestionsId or not empty sourceUrl}">data-autocomplete</c:if>
     <c:if test="${not empty sourceUrl}">data-autocomplete-source="<c:out value="${sourceUrl}" />"</c:if>
     <c:if test="${submitOnSelect}">data-autocomplete-submit="true"</c:if>>
    <input class="input-field__control"
           id="<c:out value="${id}" />"
           name="<c:out value="${name}" />"
           type="${safeType}"
           <c:if test="${safeType ne 'password' and safeType ne 'file'}">value="<c:out value="${value}" />"</c:if>
           <c:if test="${maxLength ne null}">maxlength="${maxLength}"</c:if>
           <c:if test="${min ne null}">min="${min}"</c:if>
           <c:if test="${max ne null}">max="${max}"</c:if>
           <c:if test="${not empty placeholder}">placeholder="<c:out value="${placeholder}" />"</c:if>
           <c:if test="${not empty ariaLabel}">aria-label="<c:out value="${ariaLabel}" />"</c:if>
           <c:if test="${not empty form}">form="<c:out value="${form}" />"</c:if>
           <c:if test="${not empty describedBy}">aria-describedby="<c:out value="${describedBy}" />"</c:if>
           <c:if test="${not empty suggestionsId or not empty sourceUrl}">autocomplete="off" role="combobox" aria-autocomplete="list" aria-haspopup="listbox" aria-controls="<c:out value="${suggestionsId}" />" aria-expanded="false"</c:if>
           <c:if test="${not empty accept}">accept="<c:out value="${accept}" />"</c:if>
           <c:if test="${multiple}">multiple</c:if>
           <c:if test="${hasError}">aria-invalid="true"</c:if>
           <c:if test="${autofocus}">autofocus</c:if> />
    <jsp:doBody />
</div>
```

### inquiry-nav

Pestañas recibidas y enviadas.

Atributos: `active` (obligatorio), `receivedCount` (obligatorio), `sentCount` (obligatorio).

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/tags/inquiry-nav.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/inquiry-nav.tag>), líneas 1–32.

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%@ attribute name="active" required="true" %>
<%@ attribute name="receivedCount" required="true" type="java.lang.Integer" %>
<%@ attribute name="sentCount" required="true" type="java.lang.Integer" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>

<spring:message code="inquiry.nav.label" var="navLabel"/>
<spring:message code="inquiry.nav.count" var="receivedCountLabel">
    <spring:argument value="${receivedCount}"/>
</spring:message>
<spring:message code="inquiry.nav.count" var="sentCountLabel">
    <spring:argument value="${sentCount}"/>
</spring:message>
<c:url value="/inquiries" var="receivedUrl"/>
<c:url value="/inquiries/sent" var="sentUrl"/>

<nav class="inquiry-nav" aria-label="<c:out value="${navLabel}"/>">
    <%-- aria-current marca la vista abierta: el color por si solo no alcanza. --%>
    <a class="inquiry-nav__tab${active eq 'received' ? ' inquiry-nav__tab--active' : ''}"
       href="<c:out value="${receivedUrl}"/>"
       <c:if test="${active eq 'received'}">aria-current="page"</c:if>>
        <spring:message code="inquiry.received.heading"/>
        <span class="inquiry-nav__count"><c:out value="${receivedCountLabel}"/></span>
    </a>
    <a class="inquiry-nav__tab${active eq 'sent' ? ' inquiry-nav__tab--active' : ''}"
       href="<c:out value="${sentUrl}"/>"
       <c:if test="${active eq 'sent'}">aria-current="page"</c:if>>
        <spring:message code="inquiry.sent.heading"/>
        <span class="inquiry-nav__count"><c:out value="${sentCountLabel}"/></span>
    </a>
</nav>
```

### inquiry-status

Estado de la consulta como texto.

Atributos: `status` (obligatorio).

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/tags/inquiry-status.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/inquiry-status.tag>), líneas 1–18.

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%@ attribute name="status" required="true" type="java.lang.Object" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>

<%-- Estado de una consulta como texto con icono: sin modificador de color por diseño, el
     estado es texto plano. statusCode fija el valor del code de i18n en vez del crudo. --%>
<c:set var="statusName">${status}</c:set>
<c:choose>
    <c:when test="${statusName eq 'ACCEPTED'}"><c:set var="statusCode" value="ACCEPTED"/><c:set var="icon" value="check"/></c:when>
    <c:when test="${statusName eq 'REJECTED'}"><c:set var="statusCode" value="REJECTED"/><c:set var="icon" value="x"/></c:when>
    <c:when test="${statusName eq 'AWAITING_PAYMENT'}"><c:set var="statusCode" value="AWAITING_PAYMENT"/><c:set var="icon" value="clock"/></c:when>
    <c:when test="${statusName eq 'PAYMENT_SUBMITTED'}"><c:set var="statusCode" value="PAYMENT_SUBMITTED"/><c:set var="icon" value="inbox"/></c:when>
    <c:when test="${statusName eq 'CANCELLED'}"><c:set var="statusCode" value="CANCELLED"/><c:set var="icon" value="x"/></c:when>
    <c:otherwise><c:set var="statusCode" value="PENDING"/><c:set var="icon" value="clock"/></c:otherwise>
</c:choose>
<span class="inquiry-status"><ui:icon name="${icon}"/><spring:message code="inquiry.status.${statusCode}"/></span>
```

### p

Párrafo.

Atributos: `text` (obligatorio), `variant`.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/tags/p.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/p.tag>), líneas 1–6.

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%@ attribute name="text" required="true" %>
<%@ attribute name="variant" required="false" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>

<p class="text text-${empty variant ? 'body' : variant}"><c:out value="${text}" /></p>
```

### pagination-link

Un enlace de página.

Atributos: `baseUrl` (obligatorio), `extraParams`, `page` (obligatorio), `pageParam`, `fragment`, `label` (obligatorio), `rel`.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/tags/pagination-link.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/pagination-link.tag>), líneas 1–22.

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="scriptless" %>
<%@ attribute name="baseUrl" required="true" type="java.lang.String" %>
<%@ attribute name="extraParams" required="false" type="java.util.Map" %>
<%@ attribute name="page" required="true" type="java.lang.Integer" %>
<%@ attribute name="pageParam" required="false" type="java.lang.String" %>
<%@ attribute name="fragment" required="false" type="java.lang.String" %>
<%-- Texto accesible del enlace: nombre accesible y tooltip. --%>
<%@ attribute name="label" required="true" type="java.lang.String" %>
<%@ attribute name="rel" required="false" type="java.lang.String" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>

<%-- Unico armado de URL de la paginacion: los parametros vigentes de la vista, la pagina
     destino y el ancla de la seccion. Lo usan ambas flechas. --%>
<c:url value="${baseUrl}" var="pageUrl">
    <c:forEach items="${extraParams}" var="parameter">
        <c:if test="${not empty parameter.value}"><c:param name="${parameter.key}" value="${parameter.value}"/></c:if>
    </c:forEach>
    <c:param name="${empty pageParam ? 'page' : pageParam}" value="${page}"/>
</c:url>
<a class="pagination__link"
   href="<c:out value="${pageUrl}${empty fragment ? '' : '#'.concat(fragment)}"/>"<c:if test="${not empty rel}"> rel="<c:out value="${rel}"/>"</c:if>
   aria-label="<c:out value="${label}"/>" title="<c:out value="${label}"/>"><jsp:doBody/></a>
```

### pagination

Flechas que conservan parámetros y ancla.

Atributos: `currentPage` (obligatorio), `hasPrevious` (obligatorio), `hasNext` (obligatorio), `baseUrl` (obligatorio), `pageParam`, `extraParams`, `fragment`, `ariaLabel` (obligatorio).

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/tags/pagination.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/pagination.tag>), líneas 1–53.

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%@ attribute name="currentPage" required="true" type="java.lang.Integer" %>
<%@ attribute name="hasPrevious" required="true" type="java.lang.Boolean" %>
<%@ attribute name="hasNext" required="true" type="java.lang.Boolean" %>
<%@ attribute name="baseUrl" required="true" type="java.lang.String" %>
<%@ attribute name="pageParam" required="false" type="java.lang.String" %>
<%@ attribute name="extraParams" required="false" type="java.util.Map" %>
<%@ attribute name="fragment" required="false" type="java.lang.String" %>
<%@ attribute name="ariaLabel" required="true" type="java.lang.String" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>

<%-- Solo se muestra la pagina actual; las flechas conservan los parametros y el ancla. --%>
<c:if test="${hasPrevious or hasNext}">
    <spring:message code="pagination.previous" var="previousLabel"/>
    <spring:message code="pagination.next" var="nextLabel"/>
    <nav class="pagination" aria-label="<c:out value="${ariaLabel}"/>">
        <ul class="pagination__list">
            <li>
                <c:choose>
                    <c:when test="${hasPrevious}">
                        <ui:pagination-link baseUrl="${baseUrl}" extraParams="${extraParams}" fragment="${fragment}"
                                            page="${currentPage - 1}" pageParam="${pageParam}" label="${previousLabel}" rel="prev"><ui:icon name="chevron-left"/></ui:pagination-link>
                    </c:when>
                    <c:otherwise>
                        <span class="pagination__link pagination__link--disabled" aria-disabled="true">
                            <span class="visually-hidden"><c:out value="${previousLabel}"/></span><ui:icon name="chevron-left"/>
                        </span>
                    </c:otherwise>
                </c:choose>
            </li>
            <spring:message code="pagination.page" var="pageLabel"><spring:argument value="${currentPage}"/></spring:message>
            <li>
                <span class="pagination__link pagination__link--current" aria-current="page"
                      aria-label="<c:out value="${pageLabel}"/>"><c:out value="${currentPage}"/></span>
            </li>
            <li>
                <c:choose>
                    <c:when test="${hasNext}">
                        <ui:pagination-link baseUrl="${baseUrl}" extraParams="${extraParams}" fragment="${fragment}"
                                            page="${currentPage + 1}" pageParam="${pageParam}" label="${nextLabel}" rel="next"><ui:icon name="chevron-right"/></ui:pagination-link>
                    </c:when>
                    <c:otherwise>
                        <span class="pagination__link pagination__link--disabled" aria-disabled="true">
                            <span class="visually-hidden"><c:out value="${nextLabel}"/></span><ui:icon name="chevron-right"/>
                        </span>
                    </c:otherwise>
                </c:choose>
            </li>
        </ul>
    </nav>
</c:if>
```

### post-badge

Estado de una publicación.

Atributos: `deleted`, `status`, `showAvailable`, `variant`.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/tags/post-badge.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/post-badge.tag>), líneas 1–21.

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%@ attribute name="deleted" required="false" type="java.lang.Boolean" %>
<%@ attribute name="status" required="false" type="java.lang.Object" %>
<%@ attribute name="showAvailable" required="false" type="java.lang.Boolean" %>
<%@ attribute name="variant" required="false" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>

<%-- Estado de una publicacion, siempre con el mismo marcador. Eliminada pesa mas que vendida o reservada.
     Disponible solo se marca donde el listado lo pide (perfil): en el resto se sobreentiende.
     inline: texto atenuado junto al titulo. chip: pastilla sobre la portada de la card. --%>
<c:choose>
    <c:when test="${deleted}"><c:set var="stateCode" value="post.detail.deleted"/><c:set var="icon" value="x"/><c:set var="tone" value="muted"/></c:when>
    <c:when test="${status eq 'SOLD'}"><c:set var="stateCode" value="post.detail.sold"/><c:set var="icon" value="tag"/><c:set var="tone" value="muted"/></c:when>
    <c:when test="${status eq 'RESERVED'}"><c:set var="stateCode" value="post.detail.reserved"/><c:set var="icon" value="clock"/><c:set var="tone" value="muted"/></c:when>
    <c:when test="${showAvailable}"><c:set var="stateCode" value="profile.post.available"/><c:set var="icon" value="check"/><c:set var="tone" value="available"/></c:when>
</c:choose>
<c:if test="${not empty stateCode}">
    <span class="state-marker state-marker--${tone}${variant eq 'chip' ? ' state-marker--chip' : ''}"><ui:icon name="${icon}"/><spring:message code="${stateCode}"/></span>
</c:if>
```

### rating

Estrellas de solo lectura con relleno parcial para promedios.

Atributos: `value` (obligatorio), `maxRating` (obligatorio), `label` (obligatorio).

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/tags/rating.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/rating.tag>), líneas 1–12.

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%@ attribute name="value" required="true" type="java.lang.Double" %>
<%@ attribute name="maxRating" required="true" type="java.lang.Integer" %>
<%@ attribute name="label" required="true" type="java.lang.String" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<span class="rating" role="img" aria-label="<c:out value="${label}"/>">
    <c:forEach begin="1" end="${maxRating}" var="star">
        <c:set var="fill" value="${value ge star ? 100 : (value le star - 1 ? 0 : (value - star + 1) * 100)}"/>
        <%-- Porcentaje numerico derivado de la puntuacion; los estilos viven en components.css. --%>
        <span class="rating__star" aria-hidden="true">&#9733;<span class="rating__fill" style="width: <c:out value="${fill}"/>%">&#9733;</span></span>
    </c:forEach>
</span>
```

### resend-verification

Botón de reenvío: POST con CSRF.

Atributos: `variant`.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/tags/resend-verification.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/resend-verification.tag>), líneas 1–13.

```jsp
<%@ tag body-content="empty" pageEncoding="UTF-8" %>
<%@ attribute name="variant" required="false" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="sec" uri="http://www.springframework.org/security/tags" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<%-- Pide un enlace de verificacion nuevo. Es un POST con CSRF: invalida los enlaces anteriores. --%>
<c:url value="/verify/resend" var="resendUrl"/>
<spring:message code="auth.verification.resend" var="resendLabel"/>
<form class="resend-verification" action="<c:out value="${resendUrl}"/>" method="post">
    <sec:csrfInput/>
    <ui:button label="${resendLabel}" variant="${empty variant ? 'primary' : variant}" size="sm" type="submit" icon="mail"/>
</form>
```

### review-content

Puntaje, comentario y, opcional, autor de una reseña.

Atributos: `review` (obligatorio), `maxRating` (obligatorio), `showAuthor`.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/tags/review-content.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/review-content.tag>), líneas 1–15.

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%@ attribute name="review" required="true" type="ar.edu.itba.paw.models.Review" %>
<%@ attribute name="maxRating" required="true" type="java.lang.Integer" %>
<%@ attribute name="showAuthor" required="false" type="java.lang.Boolean" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<div class="review-content">
    <spring:message code="review.rating.value" var="ratingLabel"><spring:argument value="${review.rating}"/></spring:message>
    <ui:rating value="${review.rating}" maxRating="${maxRating}" label="${ratingLabel}"/>
    <c:if test="${not empty review.body}"><p class="profile-reviews__body"><c:out value="${review.body}"/></p></c:if>
    <c:if test="${showAuthor}">
        <ui:user-byline userId="${review.authorId}" username="${review.authorUsername}" imageId="${review.authorAvatarImageId}"/>
    </c:if>
</div>
```

### segmented-control

Grupo de radios.

Atributos: `name` (obligatorio), `legend` (obligatorio), `hideLegend`, `items` (obligatorio), `messagePrefix` (obligatorio), `selectedValue`, `emptyLabel`, `hasError`, `errorId`, `required`.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/tags/segmented-control.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/segmented-control.tag>), líneas 1–38.

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%@ attribute name="name" required="true" %>
<%@ attribute name="legend" required="true" %>
<%@ attribute name="hideLegend" required="false" type="java.lang.Boolean" %>
<%@ attribute name="items" required="true" type="java.lang.Object[]" %>
<%@ attribute name="messagePrefix" required="true" %>
<%@ attribute name="selectedValue" required="false" %>
<%@ attribute name="emptyLabel" required="false" %>
<%@ attribute name="hasError" required="false" type="java.lang.Boolean" %>
<%@ attribute name="errorId" required="false" %>
<%@ attribute name="required" required="false" type="java.lang.Boolean" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>

<fieldset class="filter-group input-field${hasError ? ' input-field--error' : ''}"
          <c:if test="${required}">aria-required="true"</c:if>
          <c:if test="${hasError}">aria-invalid="true" aria-describedby="<c:out value="${errorId}" />"</c:if>>
    <legend class="${hideLegend ? 'visually-hidden' : 'filter-group__legend'}"><c:out value="${legend}" /></legend>
    <div class="segmented-control">
        <c:if test="${not empty emptyLabel}">
            <label class="segmented-control__option segmented-control__option--empty">
                <input class="segmented-control__input" type="radio" name="<c:out value="${name}" />" value=""
                       <c:if test="${empty selectedValue}">checked</c:if> />
                <span class="segmented-control__label"><c:out value="${emptyLabel}" /></span>
            </label>
        </c:if>
        <c:forEach items="${items}" var="item">
            <c:set var="itemName">${item}</c:set>
            <spring:message code="${messagePrefix}.${itemName}" var="itemLabel" />
            <label class="segmented-control__option">
                <input class="segmented-control__input" type="radio" name="<c:out value="${name}" />"
                       value="<c:out value="${itemName}" />"
                       <c:if test="${selectedValue eq itemName}">checked</c:if> />
                <span class="segmented-control__label"><c:out value="${itemLabel}" /></span>
            </label>
        </c:forEach>
    </div>
</fieldset>
```

### select-control

Select sin ligar.

Atributos: `id` (obligatorio), `name` (obligatorio), `items` (obligatorio), `messagePrefix` (obligatorio), `selectedValue`, `emptyLabel`, `labelledBy`, `describedBy`, `cssClass`, `hasError`, `placeholderOnly`.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/tags/select-control.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/select-control.tag>), líneas 1–33.

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%@ attribute name="id" required="true" %>
<%@ attribute name="name" required="true" %>
<%@ attribute name="items" required="true" type="java.lang.Object[]" %>
<%@ attribute name="messagePrefix" required="true" %>
<%@ attribute name="selectedValue" required="false" %>
<%@ attribute name="emptyLabel" required="false" %>
<%@ attribute name="labelledBy" required="false" %>
<%@ attribute name="describedBy" required="false" %>
<%@ attribute name="cssClass" required="false" %>
<%@ attribute name="hasError" required="false" type="java.lang.Boolean" %>
<%@ attribute name="placeholderOnly" required="false" type="java.lang.Boolean" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>

<select class="input-field__control${empty cssClass ? '' : ' '}${cssClass}"
        id="<c:out value="${id}" />"
        name="<c:out value="${name}" />"
        data-select-picker
        <c:if test="${not empty labelledBy}">aria-labelledby="<c:out value="${labelledBy}" />"</c:if>
        <c:if test="${not empty describedBy}">aria-describedby="<c:out value="${describedBy}" />"</c:if>
        <c:if test="${placeholderOnly}">aria-required="true"</c:if>
        <c:if test="${hasError}">aria-invalid="true"</c:if>>
    <c:if test="${not empty emptyLabel}">
        <option value="" <c:if test="${empty selectedValue}">selected</c:if>
                <c:if test="${placeholderOnly}">disabled hidden</c:if>><c:out value="${emptyLabel}" /></option>
    </c:if>
    <c:forEach items="${items}" var="item">
        <c:set var="itemName">${item}</c:set>
        <spring:message code="${messagePrefix}.${itemName}" var="itemLabel" />
        <option value="<c:out value="${itemName}" />" <c:if test="${selectedValue eq itemName}">selected</c:if>><c:out value="${itemLabel}" /></option>
    </c:forEach>
</select>
```

### select

Select ligado.

Atributos: `path` (obligatorio), `label` (obligatorio), `items` (obligatorio), `messagePrefix` (obligatorio), `emptyLabel` (obligatorio), `placeholderOnly`.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/tags/select.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/select.tag>), líneas 1–35.

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%@ attribute name="path" required="true" %>
<%@ attribute name="label" required="true" %>
<%@ attribute name="items" required="true" type="java.lang.Object[]" %>
<%@ attribute name="messagePrefix" required="true" %>
<%@ attribute name="emptyLabel" required="true" %>
<%@ attribute name="placeholderOnly" required="false" type="java.lang.Boolean" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>

<spring:bind path="${path}">
    <c:set var="fieldName" value="${status.expression}" />
    <c:set var="hasError" value="${status.error}" />
    <c:set var="errorId" value="${fieldName}-error" />
    <c:set var="labelId" value="${fieldName}-label" />

    <div class="input-field ${hasError ? 'input-field--error' : ''}">
        <label class="input-field__label" id="<c:out value="${labelId}" />"
               for="<c:out value="${fieldName}" />"><c:out value="${label}" /></label>
        <ui:select-control id="${fieldName}" name="${fieldName}" items="${items}"
                           messagePrefix="${messagePrefix}" selectedValue="${status.value}"
                           emptyLabel="${emptyLabel}" hasError="${hasError}"
                           placeholderOnly="${placeholderOnly}"
                           labelledBy="${labelId}"
                           describedBy="${hasError ? errorId : ''}" />
        <c:if test="${hasError}">
            <div class="input-field__errors" id="<c:out value="${errorId}" />" role="alert">
                <c:forEach items="${status.errorMessages}" var="errorMessage">
                    <p class="input-field__error"><c:out value="${errorMessage}" /></p>
                </c:forEach>
            </div>
        </c:if>
    </div>
</spring:bind>
```

### site-header

Barra superior: marca, buscador, acciones, aviso de verificación.

Atributos: `query`, `formId`.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/tags/site-header.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/site-header.tag>), líneas 1–56.

```jsp
<%@ tag body-content="empty" pageEncoding="UTF-8" %>
<%@ attribute name="query" required="false" %>
<%-- En el catalogo, el campo y la lupa pertenecen al formulario de filtros: buscar manda
     los filtros tal como estan en pantalla, aunque se hayan editado sin aplicar. --%>
<%@ attribute name="formId" required="false" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="sec" uri="http://www.springframework.org/security/tags" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<spring:message code="landing.search.label" var="searchLabel"/>
<spring:message code="landing.search.placeholder" var="searchPlaceholder"/>
<spring:message code="landing.search.submit" var="searchSubmitLabel"/>
<spring:message code="landing.publish" var="publishLabel"/>
<c:url value="/" var="homeUrl"/>
<c:url value="/search/suggestions" var="searchSuggestionsUrl"/>
<header class="site-header">
    <div class="site-header__inner">
        <ui:brand/>
        <form class="site-search" action="${homeUrl}" method="get" role="search">
            <ui:input-control id="q" name="q" type="search" value="${query}"
                              ariaLabel="${searchLabel}" placeholder="${searchPlaceholder}" maxLength="255"
                              suggestionsId="site-search-suggestions" sourceUrl="${searchSuggestionsUrl}"
                              submitOnSelect="${true}" form="${formId}" cssClass="site-search__field">
                <ul class="autocomplete__list" id="site-search-suggestions" role="listbox" hidden></ul>
            </ui:input-control>
            <%-- Boton solo icono: el texto de landing.search.submit queda como aria-label y tooltip. --%>
            <button class="button button--primary button--sm site-search__submit" type="submit"<c:if test="${not empty formId}"> form="<c:out value="${formId}"/>"</c:if>
                    aria-label="<c:out value="${searchSubmitLabel}"/>" title="<c:out value="${searchSubmitLabel}"/>">
                <svg class="site-search__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                     stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">
                    <circle cx="11" cy="11" r="7"/>
                    <line x1="20" y1="20" x2="16" y2="16"/>
                </svg>
            </button>
        </form>
        <div class="site-header__actions">
            <ui:button label="${publishLabel}" variant="primary" size="sm" href="/publish" icon="plus"/>
            <ui:account-nav/>
        </div>
    </div>
    <%-- Mientras la cuenta no abra el enlace, cada pagina le recuerda que le falta verificar. --%>
    <sec:authorize access="isAuthenticated() and !principal.verified">
        <div class="verification-banner" role="status">
            <div class="verification-banner__inner">
                <p class="verification-banner__text">
                    <c:choose>
                        <c:when test="${verificationResent}"><spring:message code="auth.verification.resent"/></c:when>
                        <c:when test="${verificationThrottled}"><spring:message code="auth.verification.throttled"/></c:when>
                        <c:otherwise><spring:message code="auth.verification.banner"/></c:otherwise>
                    </c:choose>
                </p>
                <ui:resend-verification variant="ghost"/>
            </div>
        </div>
    </sec:authorize>
</header>
```

### span

Texto en línea.

Atributos: `text` (obligatorio), `variant`.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/tags/span.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/span.tag>), líneas 1–6.

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%@ attribute name="text" required="true" %>
<%@ attribute name="variant" required="false" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>

<span class="text text-inline ${variant eq 'muted' ? 'text--muted' : ''}"><c:out value="${text}" /></span>
```

### star-rating-input

Estrellas como radios accesibles.

Atributos: `path` (obligatorio), `legend` (obligatorio), `max` (obligatorio), `valueCode` (obligatorio).

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/tags/star-rating-input.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/star-rating-input.tag>), líneas 1–37.

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%@ attribute name="path" required="true" %>
<%@ attribute name="legend" required="true" %>
<%@ attribute name="max" required="true" type="java.lang.Integer" %>
<%@ attribute name="valueCode" required="true" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>

<spring:bind path="${path}">
    <c:set var="fieldName" value="${status.expression}" />
    <c:set var="currentValue">${status.value}</c:set>
    <c:set var="errorId" value="${fieldName}-error" />
    <fieldset class="star-rating input-field${status.error ? ' input-field--error' : ''}"
              <c:if test="${status.error}">aria-invalid="true" aria-describedby="<c:out value="${errorId}" />"</c:if>>
        <legend class="visually-hidden"><c:out value="${legend}" /></legend>
        <div class="star-rating__stars">
            <c:forEach begin="1" end="${max}" var="star">
                <c:set var="starValue">${star}</c:set>
                <spring:message code="${valueCode}" var="starLabel"><spring:argument value="${star}" /></spring:message>
                <input class="star-rating__input visually-hidden" type="radio" id="<c:out value="${fieldName}-${star}" />"
                       name="<c:out value="${fieldName}" />" value="<c:out value="${starValue}" />"
                       <c:if test="${currentValue eq starValue}">checked</c:if> />
                <label class="star-rating__star" for="<c:out value="${fieldName}-${star}" />">
                    <span aria-hidden="true">&#9733;</span>
                    <span class="visually-hidden"><c:out value="${starLabel}" /></span>
                </label>
            </c:forEach>
        </div>
        <c:if test="${status.error}">
            <div class="input-field__errors" id="<c:out value="${errorId}" />" role="alert">
                <c:forEach items="${status.errorMessages}" var="errorMessage">
                    <p class="input-field__error"><c:out value="${errorMessage}" /></p>
                </c:forEach>
            </div>
        </c:if>
    </fieldset>
</spring:bind>
```

### text-input

Campo ligado a un form con etiqueta, pista y error.

Atributos: `path` (obligatorio), `label` (obligatorio), `type`, `maxLength`, `min`, `max`, `suggestionsId`, `sourceUrl`, `hint`, `autofocus`, `placeholder`, `hideLabel`, `describedBy`, `externalErrorsId`.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/tags/text-input.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/text-input.tag>), líneas 1–51.

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="scriptless" %>
<%@ attribute name="path" required="true" %>
<%@ attribute name="label" required="true" %>
<%@ attribute name="type" required="false" %>
<%@ attribute name="maxLength" required="false" type="java.lang.Integer" %>
<%@ attribute name="min" required="false" type="java.lang.Integer" %>
<%@ attribute name="max" required="false" type="java.lang.Integer" %>
<%@ attribute name="suggestionsId" required="false" %>
<%@ attribute name="sourceUrl" required="false" %>
<%@ attribute name="hint" required="false" %>
<%@ attribute name="autofocus" required="false" type="java.lang.Boolean" %>
<%@ attribute name="placeholder" required="false" %>
<%@ attribute name="hideLabel" required="false" type="java.lang.Boolean" %>
<%-- Ids extra para aria-describedby: se suman a la pista y al error que calcula el tag. --%>
<%@ attribute name="describedBy" required="false" %>
<%-- Cuando el error se muestra fuera del campo, conserva su referencia accesible. --%>
<%@ attribute name="externalErrorsId" required="false" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>

<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>

<spring:bind path="${path}">
    <c:set var="fieldName" value="${status.expression}" />
    <c:set var="hasError" value="${status.error}" />
    <c:set var="errorId" value="${fieldName}-error" />
    <c:if test="${not empty externalErrorsId}"><c:set var="errorId" value="${externalErrorsId}" /></c:if>
    <c:set var="hintId" value="${fieldName}-hint" />

    <div class="input-field ${hasError ? 'input-field--error' : ''}">
        <label class="input-field__label${hideLabel ? ' visually-hidden' : ''}" for="<c:out value="${fieldName}" />"><c:out value="${label}" /></label>
        <c:set var="describedByIds"><c:if test="${not empty hint}"><c:out value="${hintId}" /></c:if><c:if test="${hasError and not empty hint}"> </c:if><c:if test="${hasError}"><c:out value="${errorId}" /></c:if><c:if test="${not empty describedBy}"><c:if test="${not empty hint or hasError}"> </c:if><c:out value="${describedBy}" /></c:if></c:set>
        <ui:input-control id="${fieldName}" name="${fieldName}" type="${type}" value="${status.value}"
                          maxLength="${maxLength}" min="${min}" max="${max}"
                          suggestionsId="${suggestionsId}" sourceUrl="${sourceUrl}" hasError="${hasError}" autofocus="${autofocus}"
                          placeholder="${placeholder}"
                          describedBy="${describedByIds}">
            <jsp:doBody/>
        </ui:input-control>
        <c:if test="${not empty hint}">
            <p class="hint" id="<c:out value="${hintId}" />"><c:out value="${hint}" /></p>
        </c:if>
        <c:if test="${hasError and empty externalErrorsId}">
            <div class="input-field__errors" id="<c:out value="${errorId}" />" role="alert">
                <c:forEach items="${status.errorMessages}" var="errorMessage">
                    <p class="input-field__error"><c:out value="${errorMessage}" /></p>
                </c:forEach>
            </div>
        </c:if>
    </div>
</spring:bind>
```

### textarea

Área de texto ligada.

Atributos: `path` (obligatorio), `label` (obligatorio), `maxLength`, `id`, `rows`, `hideLabel`.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/tags/textarea.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/textarea.tag>), líneas 1–35.

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%@ attribute name="path" required="true" %>
<%@ attribute name="label" required="true" %>
<%@ attribute name="maxLength" required="false" type="java.lang.Integer" %>
<%-- Id del textarea, para cuando dos formularios de la misma pagina ligan un campo con el mismo nombre.
     Sin id, se usa el nombre del campo. --%>
<%@ attribute name="id" required="false" %>
<%@ attribute name="rows" required="false" type="java.lang.Integer" %>
<%@ attribute name="hideLabel" required="false" type="java.lang.Boolean" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>

<spring:bind path="${path}">
    <c:set var="fieldName" value="${status.expression}" />
    <c:set var="controlId" value="${empty id ? fieldName : id}" />
    <c:set var="hasError" value="${status.error}" />
    <c:set var="errorId" value="${controlId}-error" />

    <div class="input-field ${hasError ? 'input-field--error' : ''}">
        <label class="input-field__label${hideLabel ? ' visually-hidden' : ''}" for="<c:out value="${controlId}" />"><c:out value="${label}" /></label>
        <textarea class="input-field__control"
                  id="<c:out value="${controlId}" />"
                  name="<c:out value="${fieldName}" />"
                  rows="${empty rows ? 4 : rows}"
                  <c:if test="${maxLength ne null}">maxlength="${maxLength}"</c:if>
                  <c:if test="${hasError}">aria-invalid="true" aria-describedby="<c:out value="${errorId}" />"</c:if>><c:out value="${status.value}" /></textarea>
        <c:if test="${hasError}">
            <div class="input-field__errors" id="<c:out value="${errorId}" />" role="alert">
                <c:forEach items="${status.errorMessages}" var="errorMessage">
                    <p class="input-field__error"><c:out value="${errorMessage}" /></p>
                </c:forEach>
            </div>
        </c:if>
    </div>
</spring:bind>
```

### user-byline

Foto y nombre de una Cuenta con enlace a su perfil público.

Atributos: `userId` (obligatorio), `username` (obligatorio), `imageId`.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/tags/user-byline.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/user-byline.tag>), líneas 1–13.

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%@ attribute name="userId" required="true" type="java.lang.Long" %>
<%@ attribute name="username" required="true" %>
<%@ attribute name="imageId" required="false" type="java.lang.Long" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<c:url value="/users/${userId}" var="profileUrl" />
<spring:message code="userByline.open" var="openLabel"><spring:argument value="${username}" /></spring:message>
<a class="user-byline" href="<c:out value="${profileUrl}" />" aria-label="<c:out value="${openLabel}" />">
    <ui:avatar userId="${userId}" imageId="${imageId}" name="${username}" size="sm" alt="" />
    <span class="user-byline__name"><c:out value="${username}" /></span>
</a>
```

### vinyl-card

La tarjeta de un vinilo; el componente más reutilizado.

Atributos: `item`, `variant`, `href`, `hrefParams`, `title`, `artistName`, `price`, `coverUrl`, `preview`, `showStatus`.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/tags/vinyl-card.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/vinyl-card.tag>), líneas 1–118.

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%@ attribute name="item" required="false" type="ar.edu.itba.paw.models.PostSummary" %>
<%@ attribute name="variant" required="false" %>
<%@ attribute name="href" required="false" %>
<%@ attribute name="hrefParams" required="false" type="java.util.Map" %>
<%@ attribute name="title" required="false" %>
<%@ attribute name="artistName" required="false" %>
<%@ attribute name="price" required="false" type="java.lang.Integer" %>
<%@ attribute name="coverUrl" required="false" %>
<%@ attribute name="preview" required="false" type="java.lang.Boolean" %>
<%@ attribute name="showStatus" required="false" type="java.lang.Boolean" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>

<c:set var="resolvedTitle" value="${not empty item ? item.title : title}" />
<c:set var="resolvedArtistName" value="${not empty item ? item.artistName : artistName}" />
<c:set var="resolvedPrice" value="${not empty item ? item.price : price}" />
<c:choose>
    <c:when test="${not empty coverUrl}">
        <c:set var="resolvedCoverUrl" value="${coverUrl}" />
    </c:when>
    <c:when test="${empty item.coverImageId}">
        <c:url value="/images/covers/placeholder.svg" var="coverUrl" />
        <c:set var="resolvedCoverUrl" value="${coverUrl}" />
    </c:when>
    <c:otherwise>
        <c:url value="/post/${item.id}/images/${item.coverImageId}" var="coverUrl" />
        <c:set var="resolvedCoverUrl" value="${coverUrl}" />
    </c:otherwise>
</c:choose>
<spring:message code="vinylCard.cover.alt" var="coverAlt">
    <spring:argument value="${resolvedTitle}" />
</spring:message>
<spring:message code="vinylCard.year" var="yearLabel" />
<spring:message code="vinylCard.condition" var="conditionLabel" />
<spring:message code="vinylCard.zone" var="zoneLabel" />
<spring:message code="vinylCard.genre" var="genreLabel" />
<spring:message code="vinylCard.pressingYear" var="pressingYearLabel" />
<c:set var="resolvedVariant" value="${empty variant ? 'editorial' : variant}" />
<c:if test="${not empty href}">
    <c:url value="${href}" var="cardHref">
        <c:forEach items="${hrefParams}" var="parameter">
            <c:param name="${parameter.key}" value="${parameter.value}" />
        </c:forEach>
    </c:url>
    <spring:message code="vinylCard.open" var="openLabel">
        <spring:argument value="${resolvedTitle}" />
    </spring:message>
</c:if>

<article class="vinyl-card vinyl-card--${resolvedVariant}${empty href ? '' : ' vinyl-card--linked'}">
    <c:if test="${not empty href}">
        <a class="vinyl-card__link" href="<c:out value="${cardHref}" />" aria-label="<c:out value="${openLabel}" />" title="<c:out value="${resolvedTitle}" />"></a>
    </c:if>
    <div class="vinyl-card__cover">
        <c:if test="${showStatus and not empty item}">
            <ui:post-badge status="${item.status}" showAvailable="${true}" variant="chip"/>
        </c:if>
        <img src="<c:out value="${resolvedCoverUrl}" />"
             alt="<c:out value="${coverAlt}" />"
             class="vinyl-card__image"<c:if test="${preview}"> data-preview-cover</c:if> />
    </div>
    <div class="vinyl-card__content">
        <div<c:if test="${preview}"> data-preview-value="title"</c:if>><ui:h3 text="${resolvedTitle}" /></div>
        <div<c:if test="${preview}"> data-preview-value="artistName"</c:if>><ui:p text="${resolvedArtistName}" variant="lead" /></div>

        <c:choose>
            <c:when test="${not empty resolvedPrice}">
                <spring:message code="vinylCard.price.format" var="priceValue">
                    <spring:argument value="${resolvedPrice}" />
                </spring:message>
            </c:when>
            <c:otherwise><spring:message code="publish.preview.pricePlaceholder" var="priceValue" /></c:otherwise>
        </c:choose>
        <div class="vinyl-card__price">
            <span class="vinyl-card__price-value"<c:if test="${preview}"> data-preview-value="price"</c:if>><c:out value="${priceValue}" /></span>
        </div>

        <c:if test="${resolvedVariant eq 'compact'}">
            <dl class="vinyl-card__metadata">
                <div class="vinyl-card__datum">
                    <dt><ui:span text="${yearLabel}" variant="muted" /></dt>
                    <dd><ui:span text="${empty item.releaseYear ? '—' : item.releaseYear}" /></dd>
                </div>
                <c:if test="${not empty item.condition}">
                    <spring:message code="condition.${item.condition}" var="conditionValue" />
                    <div class="vinyl-card__datum">
                        <dt><ui:span text="${conditionLabel}" variant="muted" /></dt>
                        <dd><ui:span text="${conditionValue}" /></dd>
                    </div>
                </c:if>
                <c:if test="${not empty item.zone}">
                    <div class="vinyl-card__datum">
                        <dt><ui:span text="${zoneLabel}" variant="muted" /></dt>
                        <dd><ui:span text="${item.zone}" /></dd>
                    </div>
                </c:if>
                <c:if test="${not empty item.genre}">
                    <spring:message code="genre.${item.genre}" var="genreValue" />
                    <div class="vinyl-card__datum">
                        <dt><ui:span text="${genreLabel}" variant="muted" /></dt>
                        <dd><ui:span text="${genreValue}" /></dd>
                    </div>
                </c:if>
                <c:if test="${not empty item.pressingYear}">
                    <div class="vinyl-card__datum">
                        <dt><ui:span text="${pressingYearLabel}" variant="muted" /></dt>
                        <dd><ui:span text="${item.pressingYear}" /></dd>
                    </div>
                </c:if>
            </dl>
            <c:if test="${not empty item.description}">
                <p class="text text-body vinyl-card__description"><c:out value="${item.description}" /></p>
            </c:if>
        </c:if>
    </div>
</article>
```

## Archivos para seguir el flujo

- [webapp/src/main/webapp/WEB-INF/tags/account-nav.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/account-nav.tag>)
- [webapp/src/main/webapp/WEB-INF/tags/address-fields.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/address-fields.tag>)
- [webapp/src/main/webapp/WEB-INF/tags/address.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/address.tag>)
- [webapp/src/main/webapp/WEB-INF/tags/avatar.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/avatar.tag>)
- [webapp/src/main/webapp/WEB-INF/tags/back-link.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/back-link.tag>)
- [webapp/src/main/webapp/WEB-INF/tags/brand.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/brand.tag>)
- [webapp/src/main/webapp/WEB-INF/tags/button.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/button.tag>)
- [webapp/src/main/webapp/WEB-INF/tags/confirm-dialog.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/confirm-dialog.tag>)
- [webapp/src/main/webapp/WEB-INF/tags/filter-chips.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/filter-chips.tag>)
- [webapp/src/main/webapp/WEB-INF/tags/h1.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/h1.tag>)
- [webapp/src/main/webapp/WEB-INF/tags/h3.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/h3.tag>)
- [webapp/src/main/webapp/WEB-INF/tags/head.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/head.tag>)
- [webapp/src/main/webapp/WEB-INF/tags/icon.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/icon.tag>)
- [webapp/src/main/webapp/WEB-INF/tags/inbox-group-header.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/inbox-group-header.tag>)
- [webapp/src/main/webapp/WEB-INF/tags/inbox-last-message.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/inbox-last-message.tag>)
- [webapp/src/main/webapp/WEB-INF/tags/input-control.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/input-control.tag>)
- [webapp/src/main/webapp/WEB-INF/tags/inquiry-nav.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/inquiry-nav.tag>)
- [webapp/src/main/webapp/WEB-INF/tags/inquiry-status.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/inquiry-status.tag>)
- [webapp/src/main/webapp/WEB-INF/tags/p.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/p.tag>)
- [webapp/src/main/webapp/WEB-INF/tags/pagination-link.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/pagination-link.tag>)
- [webapp/src/main/webapp/WEB-INF/tags/pagination.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/pagination.tag>)
- [webapp/src/main/webapp/WEB-INF/tags/post-badge.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/post-badge.tag>)
- [webapp/src/main/webapp/WEB-INF/tags/rating.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/rating.tag>)
- [webapp/src/main/webapp/WEB-INF/tags/resend-verification.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/resend-verification.tag>)
- [webapp/src/main/webapp/WEB-INF/tags/review-content.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/review-content.tag>)
- [webapp/src/main/webapp/WEB-INF/tags/segmented-control.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/segmented-control.tag>)
- [webapp/src/main/webapp/WEB-INF/tags/select-control.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/select-control.tag>)
- [webapp/src/main/webapp/WEB-INF/tags/select.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/select.tag>)
- [webapp/src/main/webapp/WEB-INF/tags/site-header.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/site-header.tag>)
- [webapp/src/main/webapp/WEB-INF/tags/span.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/span.tag>)
- [webapp/src/main/webapp/WEB-INF/tags/star-rating-input.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/star-rating-input.tag>)
- [webapp/src/main/webapp/WEB-INF/tags/text-input.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/text-input.tag>)
- [webapp/src/main/webapp/WEB-INF/tags/textarea.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/textarea.tag>)
- [webapp/src/main/webapp/WEB-INF/tags/user-byline.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/user-byline.tag>)
- [webapp/src/main/webapp/WEB-INF/tags/vinyl-card.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/vinyl-card.tag>)

Fuente inspeccionada: `c3e2a4c`, 2026-10-05. Es evidencia estática; no implica ejecución de la aplicación. [[Source inventory]] · [[Roadmap de lectura]]
