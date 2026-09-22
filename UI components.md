---
title: "UI components"
categories: ["Web"]
type: "guide"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["webapp/src/main/webapp/WEB-INF/tags/account-nav.tag", "webapp/src/main/webapp/WEB-INF/tags/back-link.tag", "webapp/src/main/webapp/WEB-INF/tags/brand.tag", "webapp/src/main/webapp/WEB-INF/tags/button.tag", "webapp/src/main/webapp/WEB-INF/tags/confirm-dialog.tag", "webapp/src/main/webapp/WEB-INF/tags/h1.tag", "webapp/src/main/webapp/WEB-INF/tags/h3.tag", "webapp/src/main/webapp/WEB-INF/tags/head.tag", "webapp/src/main/webapp/WEB-INF/tags/icon.tag", "webapp/src/main/webapp/WEB-INF/tags/inbox-group-header.tag", "webapp/src/main/webapp/WEB-INF/tags/input-control.tag", "webapp/src/main/webapp/WEB-INF/tags/inquiry-nav.tag", "webapp/src/main/webapp/WEB-INF/tags/inquiry-status.tag", "webapp/src/main/webapp/WEB-INF/tags/p.tag", "webapp/src/main/webapp/WEB-INF/tags/pagination.tag", "webapp/src/main/webapp/WEB-INF/tags/pagination-link.tag", "webapp/src/main/webapp/WEB-INF/tags/post-badge.tag", "webapp/src/main/webapp/WEB-INF/tags/segmented-control.tag", "webapp/src/main/webapp/WEB-INF/tags/select.tag", "webapp/src/main/webapp/WEB-INF/tags/select-control.tag", "webapp/src/main/webapp/WEB-INF/tags/site-header.tag", "webapp/src/main/webapp/WEB-INF/tags/span.tag", "webapp/src/main/webapp/WEB-INF/tags/text-input.tag", "webapp/src/main/webapp/WEB-INF/tags/textarea.tag", "webapp/src/main/webapp/WEB-INF/tags/vinyl-card.tag"]
---

# UI components

There are 25 shared JSP tags under webapp/src/main/webapp/WEB-INF/tags, fourteen more than at `40328f0`. Pages declare the ui tag directory. head, site-header and account-nav centralize page resources, navigation and account actions. Bound form tags (text-input, select, textarea) wrap spring:bind, while unbound controls (input-control, select-control, segmented-control) serve GET filters and are reused internally.

Spring form:form provides the binding context and integrates CSRF with Spring Security. Plain POST forms for logout, inquiry actions and deletion emit sec:csrfInput explicitly. User values use escaped outputs, and password and file inputs never repopulate values. State is always shown with an icon plus text (post-badge, inquiry-status), not by color alone.

## account-nav

Anonymous visitors see login and register buttons. Authenticated users see an inbox link, an admin link for ADMIN, and, last, an identity link with the user icon and escaped display name that leads to /profile. Logout moved to the profile page.

[webapp/src/main/webapp/WEB-INF/tags/account-nav.tag, lines 1–29](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/account-nav.tag>)

```jsp
<%@ tag body-content="empty" pageEncoding="UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="sec" uri="http://www.springframework.org/security/tags" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<spring:message code="auth.navigation.label" var="navigationLabel"/>
<spring:message code="auth.login.action" var="loginLabel"/>
<spring:message code="auth.register.action" var="registerLabel"/>
<spring:message code="auth.admin.action" var="adminLabel"/>
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
        <sec:authorize access="hasRole('ADMIN')">
            <ui:button label="${adminLabel}" variant="ghost" size="sm" href="/admin" icon="shield"/>
        </sec:authorize>
        <%-- La identidad va al final: es el ancla de la cuenta y lleva al perfil. --%>
        <a class="button button--ghost button--sm account-nav__identity" href="<c:out value="${profileUrl}"/>"
           title="<c:out value="${displayName}"/>"><ui:icon name="user"/><span class="account-nav__name"><c:out value="${displayName}"/></span></a>
    </sec:authorize>
</nav>
```

## back-link

Text link with a decorative left arrow, defaulting to the nav.back label and the catalog. Wrapped in a div so the page grid does not stretch it.

[webapp/src/main/webapp/WEB-INF/tags/back-link.tag, lines 1–18](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/back-link.tag>)

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%@ attribute name="href" required="false" %>
<%@ attribute name="label" required="false" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>

<spring:message code="nav.back" var="defaultLabel" />
<c:set var="backLabel" value="${empty label ? defaultLabel : label}" />
<c:url value="${empty href ? '/' : href}" var="backHref" />

<%-- El link va envuelto: page-shell es un grid y un ancla suelta se estira a todo el ancho. --%>
<div class="back-link">
    <%-- La flecha es decorativa: el texto visible ya dice a donde vuelve el link. --%>
    <a class="back-link__anchor" href="<c:out value="${backHref}" />">
        <span class="back-link__arrow" aria-hidden="true">&#8592;</span>
        <c:out value="${backLabel}" />
    </a>
</div>
```

## brand

Logo mark plus the application name linking home. The lg size is used on auth pages.

[webapp/src/main/webapp/WEB-INF/tags/brand.tag, lines 1–14](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/brand.tag>)

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

## button

Renders an anchor for href (passed through c:url) or url (already resolved), or a button otherwise. Variants primary, ghost, danger and danger-outline; sizes sm and md; submit must be explicit. Optional icon and a valueless data-* attribute. Escapes labels.

[webapp/src/main/webapp/WEB-INF/tags/button.tag, lines 1–30](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/button.tag>)

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
        <button class="${classes}" type="${type eq 'submit' ? 'submit' : 'button'}"<c:if test="${not empty id}"> id="<c:out value="${id}" />"</c:if><c:if test="${not empty data}"> data-<c:out value="${data}" /></c:if>><c:if test="${not empty icon}"><ui:icon name="${icon}"/></c:if><c:out value="${label}" /></button>
    </c:otherwise>
</c:choose>
```

## confirm-dialog

Native dialog opened by confirm-action.js for forms with data-confirm-message. It fixes the element IDs the script looks for, so one dialog is allowed per page. Cancel closes through a method=dialog form.

[webapp/src/main/webapp/WEB-INF/tags/confirm-dialog.tag, lines 1–23](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/confirm-dialog.tag>)

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

## h1

Escaped heading with optional accent tone.

[webapp/src/main/webapp/WEB-INF/tags/h1.tag, lines 1–6](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/h1.tag>)

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%@ attribute name="text" required="true" %>
<%@ attribute name="tone" required="false" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>

<h1 class="text text-h1 ${tone eq 'accent' ? 'text--accent' : ''}"><c:out value="${text}" /></h1>
```

## h3

Escaped card heading. level=2 renders an h2 with the same style, and an optional body follows the text, used to attach a state marker.

[webapp/src/main/webapp/WEB-INF/tags/h3.tag, lines 1–12](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/h3.tag>)

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

## head

Emits charset, viewport, localized title, logo favicon, tokens/components/style CSS and the four shared deferred scripts. The optional pageScript attribute adds one page-specific script.

[webapp/src/main/webapp/WEB-INF/tags/head.tag, lines 1–31](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/head.tag>)

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

## icon

Closed set of fourteen 24-unit stroke icons drawn with currentColor and hidden from assistive technology. An unknown name renders nothing.

[webapp/src/main/webapp/WEB-INF/tags/icon.tag, lines 1–32](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/icon.tag>)

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
        <c:when test="${name eq 'inbox'}">M22 12h-6l-2 3h-4l-2-3H2M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z</c:when>
        <c:when test="${name eq 'user'}">M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2M16 7a4 4 0 1 1-8 0 4 4 0 0 1 8 0z</c:when>
        <c:when test="${name eq 'shield'}">M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z</c:when>
        <c:when test="${name eq 'log-out'}">M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9</c:when>
        <c:when test="${name eq 'pencil'}">M17 3a2.83 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z</c:when>
        <c:when test="${name eq 'trash'}">M3 6h18M8 6V4h8v2M19 6l-1 14H6L5 6M10 11v6M14 11v6</c:when>
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

## inbox-group-header

Header of an inbox group: cover or placeholder, title with ui:post-badge and artist. A stretched link opens the detail page unless the publication was deleted.

[webapp/src/main/webapp/WEB-INF/tags/inbox-group-header.tag, lines 1–26](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/inbox-group-header.tag>)

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%@ attribute name="group" required="true" type="ar.edu.itba.paw.models.InquiryGroup" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>

<%-- Cabecera de un grupo de la bandeja (recibidas y enviadas): miniatura, titulo con el
     estado de la publicacion y artista. La cabecera entera lleva a la ficha con un enlace
     estirado, como la card; una publicacion eliminada no tiene adonde ir y no lo dibuja. --%>
<c:choose>
    <c:when test="${empty group.coverImageId}"><c:url value="/images/covers/placeholder.svg" var="coverUrl"/></c:when>
    <c:otherwise><c:url value="/covers/${group.coverImageId}" var="coverUrl"/></c:otherwise>
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

## input-control

Unbound input used for filters, search and file upload, and internally by text-input. Whitelists the type, omits values for password and file, and adds combobox attributes when a suggestion source is given. The body holds the listbox.

[webapp/src/main/webapp/WEB-INF/tags/input-control.tag, lines 1–45](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/input-control.tag>)

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
           <c:if test="${not empty describedBy}">aria-describedby="<c:out value="${describedBy}" />"</c:if>
           <c:if test="${not empty suggestionsId or not empty sourceUrl}">autocomplete="off" role="combobox" aria-autocomplete="list" aria-haspopup="listbox" aria-controls="<c:out value="${suggestionsId}" />" aria-expanded="false"</c:if>
           <c:if test="${not empty accept}">accept="<c:out value="${accept}" />"</c:if>
           <c:if test="${hasError}">aria-invalid="true"</c:if>
           <c:if test="${autofocus}">autofocus</c:if> />
    <jsp:doBody />
</div>
```

## inquiry-nav

Two tabs for received and sent inquiries with their counts; aria-current marks the open view.

[webapp/src/main/webapp/WEB-INF/tags/inquiry-nav.tag, lines 1–32](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/inquiry-nav.tag>)

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

## inquiry-status

Inquiry state as icon plus localized text: clock for PENDING, check for ACCEPTED, x for REJECTED. No color modifier.

[webapp/src/main/webapp/WEB-INF/tags/inquiry-status.tag, lines 1–15](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/inquiry-status.tag>)

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
    <c:otherwise><c:set var="statusCode" value="PENDING"/><c:set var="icon" value="clock"/></c:otherwise>
</c:choose>
<span class="inquiry-status"><ui:icon name="${icon}"/><spring:message code="inquiry.status.${statusCode}"/></span>
```

## p

Escaped paragraph; variant selects the text class suffix.

[webapp/src/main/webapp/WEB-INF/tags/p.tag, lines 1–6](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/p.tag>)

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%@ attribute name="text" required="true" %>
<%@ attribute name="variant" required="false" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>

<p class="text text-${empty variant ? 'body' : variant}"><c:out value="${text}" /></p>
```

## pagination

Draws nothing without a previous or next page. With a known total it renders chevrons and numbered links with ellipses around a five-page window; otherwise only chevrons. See [[Paginated listings]].

[webapp/src/main/webapp/WEB-INF/tags/pagination.tag, lines 1–123](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/pagination.tag>)

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%@ attribute name="currentPage" required="true" type="java.lang.Integer" %>
<%@ attribute name="hasPrevious" required="true" type="java.lang.Boolean" %>
<%@ attribute name="hasNext" required="true" type="java.lang.Boolean" %>
<%@ attribute name="totalPages" required="false" type="java.lang.Integer" %>
<%@ attribute name="baseUrl" required="true" type="java.lang.String" %>
<%@ attribute name="extraParams" required="false" type="java.util.Map" %>
<%@ attribute name="fragment" required="false" type="java.lang.String" %>
<%@ attribute name="ariaLabel" required="true" type="java.lang.String" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>

<%-- Con total conocido dibuja numeros y flechas; sin total, anterior/siguiente. Hasta
     siete paginas se listan todas; con mas, la primera, la ultima, la actual y dos a cada
     lado, con puntos suspensivos en los huecos. El recorrido es solo de la ventana: no
     itera las paginas que no dibuja. --%>
<c:if test="${hasPrevious or hasNext}">
    <spring:message code="pagination.previous" var="previousLabel"/>
    <spring:message code="pagination.next" var="nextLabel"/>
    <nav class="pagination" aria-label="<c:out value="${ariaLabel}"/>">
        <ul class="pagination__list">
            <li>
                <c:choose>
                    <c:when test="${hasPrevious}">
                        <ui:pagination-link baseUrl="${baseUrl}" extraParams="${extraParams}" fragment="${fragment}"
                                            page="${currentPage - 1}" label="${previousLabel}" rel="prev"><ui:icon name="chevron-left"/></ui:pagination-link>
                    </c:when>
                    <c:otherwise>
                        <span class="pagination__link pagination__link--disabled" aria-disabled="true"><ui:icon name="chevron-left"/></span>
                    </c:otherwise>
                </c:choose>
            </li>
            <c:if test="${not empty totalPages and totalPages gt 0}">
                <%-- La ventana son las paginas intermedias que se dibujan; la primera y la
                     ultima van siempre aparte. Con siete o menos la ventana es todo el rango. --%>
                <c:set var="windowStart" value="${totalPages le 7 or currentPage - 2 lt 2 ? 2 : currentPage - 2}"/>
                <c:set var="windowEnd" value="${totalPages le 7 or currentPage + 2 gt totalPages - 1 ? totalPages - 1 : currentPage + 2}"/>
                <spring:message code="pagination.page" var="firstLabel"><spring:argument value="1"/></spring:message>
                <li>
                    <c:choose>
                        <c:when test="${currentPage eq 1}">
                            <span class="pagination__link pagination__link--current" aria-current="page" aria-label="<c:out value="${firstLabel}"/>">1</span>
                        </c:when>
                        <c:otherwise>
                            <ui:pagination-link baseUrl="${baseUrl}" extraParams="${extraParams}" fragment="${fragment}"
                                                page="${1}" label="${firstLabel}">1</ui:pagination-link>
                        </c:otherwise>
                    </c:choose>
                </li>
                <%-- Un hueco de una sola pagina se dibuja entero: los puntos suspensivos
                     ocuparian el mismo lugar que el numero que esconden. --%>
                <c:if test="${windowStart gt 2}">
                    <c:choose>
                        <c:when test="${windowStart eq 3}">
                            <spring:message code="pagination.page" var="secondLabel"><spring:argument value="2"/></spring:message>
                            <li>
                                <ui:pagination-link baseUrl="${baseUrl}" extraParams="${extraParams}" fragment="${fragment}"
                                                    page="${2}" label="${secondLabel}">2</ui:pagination-link>
                            </li>
                        </c:when>
                        <c:otherwise>
                            <li aria-hidden="true"><span class="pagination__ellipsis">&#8230;</span></li>
                        </c:otherwise>
                    </c:choose>
                </c:if>
                <c:forEach begin="${windowStart}" end="${windowEnd}" var="page">
                    <spring:message code="pagination.page" var="pageLabel"><spring:argument value="${page}"/></spring:message>
                    <li>
                        <c:choose>
                            <c:when test="${page eq currentPage}">
                                <span class="pagination__link pagination__link--current" aria-current="page" aria-label="<c:out value="${pageLabel}"/>"><c:out value="${page}"/></span>
                            </c:when>
                            <c:otherwise>
                                <ui:pagination-link baseUrl="${baseUrl}" extraParams="${extraParams}" fragment="${fragment}"
                                                    page="${page}" label="${pageLabel}"><c:out value="${page}"/></ui:pagination-link>
                            </c:otherwise>
                        </c:choose>
                    </li>
                </c:forEach>
                <c:if test="${windowEnd lt totalPages - 1}">
                    <c:choose>
                        <c:when test="${windowEnd eq totalPages - 2}">
                            <spring:message code="pagination.page" var="secondLastLabel"><spring:argument value="${totalPages - 1}"/></spring:message>
                            <li>
                                <ui:pagination-link baseUrl="${baseUrl}" extraParams="${extraParams}" fragment="${fragment}"
                                                    page="${totalPages - 1}" label="${secondLastLabel}"><c:out value="${totalPages - 1}"/></ui:pagination-link>
                            </li>
                        </c:when>
                        <c:otherwise>
                            <li aria-hidden="true"><span class="pagination__ellipsis">&#8230;</span></li>
                        </c:otherwise>
                    </c:choose>
                </c:if>
                <c:if test="${totalPages gt 1}">
                    <spring:message code="pagination.page" var="lastLabel"><spring:argument value="${totalPages}"/></spring:message>
                    <li>
                        <c:choose>
                            <c:when test="${currentPage eq totalPages}">
                                <span class="pagination__link pagination__link--current" aria-current="page" aria-label="<c:out value="${lastLabel}"/>"><c:out value="${totalPages}"/></span>
                            </c:when>
                            <c:otherwise>
                                <ui:pagination-link baseUrl="${baseUrl}" extraParams="${extraParams}" fragment="${fragment}"
                                                    page="${totalPages}" label="${lastLabel}"><c:out value="${totalPages}"/></ui:pagination-link>
                            </c:otherwise>
                        </c:choose>
                    </li>
                </c:if>
            </c:if>
            <li>
                <c:choose>
                    <c:when test="${hasNext}">
                        <ui:pagination-link baseUrl="${baseUrl}" extraParams="${extraParams}" fragment="${fragment}"
                                            page="${currentPage + 1}" label="${nextLabel}" rel="next"><ui:icon name="chevron-right"/></ui:pagination-link>
                    </c:when>
                    <c:otherwise>
                        <span class="pagination__link pagination__link--disabled" aria-disabled="true"><ui:icon name="chevron-right"/></span>
                    </c:otherwise>
                </c:choose>
            </li>
        </ul>
    </nav>
</c:if>
```

## pagination-link

Builds one pagination URL from the base path, current parameters, target page and optional fragment, with accessible label and rel.

[webapp/src/main/webapp/WEB-INF/tags/pagination-link.tag, lines 1–21](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/pagination-link.tag>)

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="scriptless" %>
<%@ attribute name="baseUrl" required="true" type="java.lang.String" %>
<%@ attribute name="extraParams" required="false" type="java.util.Map" %>
<%@ attribute name="page" required="true" type="java.lang.Integer" %>
<%@ attribute name="fragment" required="false" type="java.lang.String" %>
<%-- Texto accesible del enlace: nombre accesible y tooltip. --%>
<%@ attribute name="label" required="true" type="java.lang.String" %>
<%@ attribute name="rel" required="false" type="java.lang.String" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>

<%-- Unico armado de URL de la paginacion: los parametros vigentes de la vista, la pagina
     destino y el ancla de la seccion. Lo usan las flechas y cada numero. --%>
<c:url value="${baseUrl}" var="pageUrl">
    <c:forEach items="${extraParams}" var="parameter">
        <c:if test="${not empty parameter.value}"><c:param name="${parameter.key}" value="${parameter.value}"/></c:if>
    </c:forEach>
    <c:param name="page" value="${page}"/>
</c:url>
<a class="pagination__link"
   href="<c:out value="${pageUrl}${empty fragment ? '' : '#'.concat(fragment)}"/>"<c:if test="${not empty rel}"> rel="<c:out value="${rel}"/>"</c:if>
   aria-label="<c:out value="${label}"/>" title="<c:out value="${label}"/>"><jsp:doBody/></a>
```

## post-badge

Publication state marker: deleted outranks sold; available appears only when requested (profile). inline or chip variant.

[webapp/src/main/webapp/WEB-INF/tags/post-badge.tag, lines 1–20](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/post-badge.tag>)

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%@ attribute name="deleted" required="false" type="java.lang.Boolean" %>
<%@ attribute name="status" required="false" type="java.lang.Object" %>
<%@ attribute name="showAvailable" required="false" type="java.lang.Boolean" %>
<%@ attribute name="variant" required="false" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>

<%-- Estado de una publicacion, siempre con el mismo marcador. Eliminada pesa mas que vendida.
     Disponible solo se marca donde el listado lo pide (perfil): en el resto se sobreentiende.
     inline: texto atenuado junto al titulo. chip: pastilla sobre la portada de la card. --%>
<c:choose>
    <c:when test="${deleted}"><c:set var="stateCode" value="post.detail.deleted"/><c:set var="icon" value="x"/><c:set var="tone" value="muted"/></c:when>
    <c:when test="${status eq 'SOLD'}"><c:set var="stateCode" value="post.detail.sold"/><c:set var="icon" value="tag"/><c:set var="tone" value="muted"/></c:when>
    <c:when test="${showAvailable}"><c:set var="stateCode" value="profile.post.available"/><c:set var="icon" value="check"/><c:set var="tone" value="available"/></c:when>
</c:choose>
<c:if test="${not empty stateCode}">
    <span class="state-marker state-marker--${tone}${variant eq 'chip' ? ' state-marker--chip' : ''}"><ui:icon name="${icon}"/><spring:message code="${stateCode}"/></span>
</c:if>
```

## segmented-control

Radio-group fieldset built from enum values with localized labels, an optional empty choice, and required/error ARIA attributes. Used for condition in filters and in the publish form.

[webapp/src/main/webapp/WEB-INF/tags/segmented-control.tag, lines 1–37](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/segmented-control.tag>)

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%@ attribute name="name" required="true" %>
<%@ attribute name="legend" required="true" %>
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
    <legend class="filter-group__legend"><c:out value="${legend}" /></legend>
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

## select

Bound select for form fields: label, ui:select-control with the bound value, placeholder-only empty option and field errors.

[webapp/src/main/webapp/WEB-INF/tags/select.tag, lines 1–35](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/select.tag>)

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

## select-control

Unbound select with localized enum options, optional empty or placeholder-only option and ARIA wiring. Marked data-select-picker for the JavaScript picker.

[webapp/src/main/webapp/WEB-INF/tags/select-control.tag, lines 1–33](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/select-control.tag>)

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

## site-header

Compact header with ui:brand, the global search form with autocomplete that submits on selection, an icon-only submit button, the publish button and ui:account-nav.

[webapp/src/main/webapp/WEB-INF/tags/site-header.tag, lines 1–37](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/site-header.tag>)

```jsp
<%@ tag body-content="empty" pageEncoding="UTF-8" %>
<%@ attribute name="query" required="false" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
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
                              submitOnSelect="${true}" cssClass="site-search__field">
                <ul class="autocomplete__list" id="site-search-suggestions" role="listbox" hidden></ul>
            </ui:input-control>
            <%-- Boton solo icono: el texto de landing.search.submit queda como aria-label y tooltip. --%>
            <button class="button button--primary button--sm site-search__submit" type="submit"
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
</header>
```

## span

Escaped inline text; muted variant selects the muted class.

[webapp/src/main/webapp/WEB-INF/tags/span.tag, lines 1–6](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/span.tag>)

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%@ attribute name="text" required="true" %>
<%@ attribute name="variant" required="false" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>

<span class="text text-inline ${variant eq 'muted' ? 'text--muted' : ''}"><c:out value="${text}" /></span>
```

## text-input

Uses spring:bind for value, errors and accessibility attributes, then delegates to ui:input-control. Adds hint, placeholder, hidden label, autofocus, extra describedBy IDs and an autocomplete source. Password values are omitted on redisplay.

[webapp/src/main/webapp/WEB-INF/tags/text-input.tag, lines 1–48](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/text-input.tag>)

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
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>

<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>

<spring:bind path="${path}">
    <c:set var="fieldName" value="${status.expression}" />
    <c:set var="hasError" value="${status.error}" />
    <c:set var="errorId" value="${fieldName}-error" />
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

## textarea

Binds escaped multiline text, optional maxlength and field errors; used for publication descriptions and inquiry messages.

[webapp/src/main/webapp/WEB-INF/tags/textarea.tag, lines 1–29](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/textarea.tag>)

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%@ attribute name="path" required="true" %>
<%@ attribute name="label" required="true" %>
<%@ attribute name="maxLength" required="false" type="java.lang.Integer" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>

<spring:bind path="${path}">
    <c:set var="fieldName" value="${status.expression}" />
    <c:set var="hasError" value="${status.error}" />
    <c:set var="errorId" value="${fieldName}-error" />

    <div class="input-field ${hasError ? 'input-field--error' : ''}">
        <label class="input-field__label" for="<c:out value="${fieldName}" />"><c:out value="${label}" /></label>
        <textarea class="input-field__control"
                  id="<c:out value="${fieldName}" />"
                  name="<c:out value="${fieldName}" />"
                  rows="4"
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

## vinyl-card

Card for a PostSummary or explicit preview values. The editorial variant shows cover, title, artist and price; compact adds year, condition, zone, genre, pressing year and description. Optional stretched link, status chip and preview data attributes. It no longer accepts a body and never shows seller identity.

[webapp/src/main/webapp/WEB-INF/tags/vinyl-card.tag, lines 1–113](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/vinyl-card.tag>)

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%@ attribute name="item" required="false" type="ar.edu.itba.paw.models.PostSummary" %>
<%@ attribute name="variant" required="false" %>
<%@ attribute name="href" required="false" %>
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
        <c:url value="/covers/${item.coverImageId}" var="coverUrl" />
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
    <c:url value="${href}" var="cardHref" />
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

[[Views and assets]] · [[UI styles and tokens]] · [[Authentication flow]]
