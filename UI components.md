---
title: "UI components"
categories: ["Web"]
type: "guide"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["webapp/src/main/webapp/WEB-INF/tags/account-nav.tag", "webapp/src/main/webapp/WEB-INF/tags/button.tag", "webapp/src/main/webapp/WEB-INF/tags/h1.tag", "webapp/src/main/webapp/WEB-INF/tags/h3.tag", "webapp/src/main/webapp/WEB-INF/tags/head.tag", "webapp/src/main/webapp/WEB-INF/tags/p.tag", "webapp/src/main/webapp/WEB-INF/tags/select.tag", "webapp/src/main/webapp/WEB-INF/tags/span.tag", "webapp/src/main/webapp/WEB-INF/tags/text-input.tag", "webapp/src/main/webapp/WEB-INF/tags/textarea.tag", "webapp/src/main/webapp/WEB-INF/tags/vinyl-card.tag"]
---

# UI components

There are 11 shared JSP tags under webapp/src/main/webapp/WEB-INF/tags. Pages declare the ui tag directory. head and account-nav centralize shared page resources and account actions; select and textarea extend the bound form controls.

Spring form:form provides the binding context and integrates CSRF with Spring Security. Plain logout/inquiry POST forms explicitly emit sec:csrfInput. User values use escaped outputs; password inputs omit retained values. File input remains directly in the publish JSP.

## account-nav

Shows login/register for anonymous users and escaped display name, inquiry link and POST logout with CSRF for authenticated users. ADMIN also sees its section link.

[webapp/src/main/webapp/WEB-INF/tags/account-nav.tag, lines 1–32](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/account-nav.tag>)

```jsp
<%@ tag body-content="empty" pageEncoding="UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="sec" uri="http://www.springframework.org/security/tags" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<spring:message code="auth.navigation.label" var="navigationLabel"/>
<spring:message code="auth.login.action" var="loginLabel"/>
<spring:message code="auth.register.action" var="registerLabel"/>
<spring:message code="auth.logout.action" var="logoutLabel"/>
<spring:message code="auth.admin.action" var="adminLabel"/>
<spring:message code="inquiry.navigation" var="inquiryLabel"/>
<c:url value="/logout" var="logoutUrl"/>
<nav class="account-nav" aria-label="${navigationLabel}">
    <sec:authorize access="isAnonymous()">
        <ui:button label="${loginLabel}" variant="ghost" size="sm" href="/login"/>
        <ui:button label="${registerLabel}" variant="primary" size="sm" href="/register"/>
    </sec:authorize>
    <sec:authorize access="isAuthenticated()">
        <%-- getUsername() del UserDetails es el email (con el que se inicia sesion). En la
             cabecera va el nombre que la persona eligio al verificar la cuenta. --%>
        <sec:authentication property="principal.displayName" var="displayName" scope="page"/>
        <span class="account-nav__identity"><c:out value="${displayName}"/></span>
        <ui:button label="${inquiryLabel}" variant="ghost" size="sm" href="/inquiries"/>
        <sec:authorize access="hasRole('ADMIN')">
            <ui:button label="${adminLabel}" variant="ghost" size="sm" href="/admin"/>
        </sec:authorize>
        <form class="account-nav__logout" action="${logoutUrl}" method="post">
            <sec:csrfInput/>
            <ui:button label="${logoutLabel}" variant="ghost" size="sm" type="submit"/>
        </form>
    </sec:authorize>
</nav>
```

## button

Renders a context-aware anchor for href or a button otherwise. Supports primary/ghost and sm/md; submit must be explicit. Escapes labels.

[webapp/src/main/webapp/WEB-INF/tags/button.tag, lines 1–19](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/button.tag>)

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%@ attribute name="label" required="true" %>
<%@ attribute name="variant" required="false" %>
<%@ attribute name="size" required="false" %>
<%@ attribute name="type" required="false" %>
<%@ attribute name="href" required="false" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>

<c:set var="classes" value="button button--${empty variant ? 'primary' : variant} button--${empty size ? 'md' : size}" />

<c:choose>
    <c:when test="${not empty href}">
        <c:url value="${href}" var="buttonHref" />
        <a class="${classes}" href="<c:out value="${buttonHref}" />"><c:out value="${label}" /></a>
    </c:when>
    <c:otherwise>
        <button class="${classes}" type="${type eq 'submit' ? 'submit' : 'button'}"><c:out value="${label}" /></button>
    </c:otherwise>
</c:choose>
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

Escaped card heading.

[webapp/src/main/webapp/WEB-INF/tags/h3.tag, lines 1–5](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/h3.tag>)

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%@ attribute name="text" required="true" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>

<h3 class="text text-h3"><c:out value="${text}" /></h3>
```

## head

Emits charset, viewport, localized title, SVG favicon, tokens/components/style CSS and deferred submit-once.js.

[webapp/src/main/webapp/WEB-INF/tags/head.tag, lines 1–19](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/head.tag>)

```jsp
<%@ tag body-content="empty" pageEncoding="UTF-8" %>
<%@ attribute name="titleCode" required="true" rtexprvalue="true" type="java.lang.String" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<c:url value="/images/covers/placeholder.svg" var="faviconUrl"/>
<c:url value="/css/tokens.css" var="tokensCss"/>
<c:url value="/css/components.css" var="componentsCss"/>
<c:url value="/css/style.css" var="cssUrl"/>
<c:url value="/js/submit-once.js" var="submitOnceJs"/>
<head>
    <meta charset="UTF-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <title><spring:message code="${titleCode}"/></title>
    <link rel="icon" type="image/svg+xml" href="${faviconUrl}"/>
    <link rel="stylesheet" href="${tokensCss}"/>
    <link rel="stylesheet" href="${componentsCss}"/>
    <link rel="stylesheet" href="${cssUrl}"/>
    <script src="${submitOnceJs}" defer></script>
</head>
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

## select

Binds enum options from an Object[] with localized labels and an empty choice, retaining selection and rendering errors.

[webapp/src/main/webapp/WEB-INF/tags/select.tag, lines 1–36](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/select.tag>)

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%@ attribute name="path" required="true" %>
<%@ attribute name="label" required="true" %>
<%@ attribute name="items" required="true" type="java.lang.Object[]" %>
<%@ attribute name="messagePrefix" required="true" %>
<%@ attribute name="emptyLabel" required="true" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>

<spring:bind path="${path}">
    <c:set var="fieldName" value="${status.expression}" />
    <c:set var="hasError" value="${status.error}" />
    <c:set var="errorId" value="${fieldName}-error" />

    <div class="input-field ${hasError ? 'input-field--error' : ''}">
        <label class="input-field__label" for="<c:out value="${fieldName}" />"><c:out value="${label}" /></label>
        <select class="input-field__control"
                id="<c:out value="${fieldName}" />"
                name="<c:out value="${fieldName}" />"
                <c:if test="${hasError}">aria-invalid="true" aria-describedby="<c:out value="${errorId}" />"</c:if>>
            <option value=""><c:out value="${emptyLabel}" /></option>
            <c:forEach items="${items}" var="item">
                <c:set var="itemName">${item}</c:set>
                <spring:message code="${messagePrefix}.${itemName}" var="itemLabel" />
                <option value="<c:out value="${itemName}" />" ${status.value eq itemName ? 'selected' : ''}><c:out value="${itemLabel}" /></option>
            </c:forEach>
        </select>
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

Uses spring:bind for field value/errors and accessibility attributes. Supports text/search/email/number/password. Password values are omitted on redisplay. Numeric bounds and maxLength are optional.

[webapp/src/main/webapp/WEB-INF/tags/text-input.tag, lines 1–40](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/text-input.tag>)

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%@ attribute name="path" required="true" %>
<%@ attribute name="label" required="true" %>
<%@ attribute name="type" required="false" %>
<%@ attribute name="maxLength" required="false" type="java.lang.Integer" %>
<%@ attribute name="min" required="false" type="java.lang.Integer" %>
<%@ attribute name="max" required="false" type="java.lang.Integer" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>

<c:set var="safeType" value="text" />
<c:if test="${type eq 'search' or type eq 'email' or type eq 'number' or type eq 'password'}">
    <c:set var="safeType" value="${type}" />
</c:if>

<spring:bind path="${path}">
    <c:set var="fieldName" value="${status.expression}" />
    <c:set var="hasError" value="${status.error}" />
    <c:set var="errorId" value="${fieldName}-error" />

    <div class="input-field ${hasError ? 'input-field--error' : ''}">
        <label class="input-field__label" for="<c:out value="${fieldName}" />"><c:out value="${label}" /></label>
        <input class="input-field__control"
               id="<c:out value="${fieldName}" />"
               name="<c:out value="${fieldName}" />"
               type="${safeType}"
               <c:if test="${safeType ne 'password'}">value="<c:out value="${status.value}" />"</c:if>
               <c:if test="${maxLength ne null}">maxlength="${maxLength}"</c:if>
               <c:if test="${min ne null}">min="${min}"</c:if>
               <c:if test="${max ne null}">max="${max}"</c:if>
               <c:if test="${hasError}">aria-invalid="true" aria-describedby="<c:out value="${errorId}" />"</c:if> />
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

Renders PostSummary cover/placeholder, price or unavailable copy, album year and optional genre, condition, zone, pressing year and description. Optional href makes the card linked; jsp:doBody supplies actions. Does not show seller email.

[webapp/src/main/webapp/WEB-INF/tags/vinyl-card.tag, lines 1–101](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/vinyl-card.tag>)

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="scriptless" %>
<%@ attribute name="item" required="true" type="ar.edu.itba.paw.models.PostSummary" %>
<%@ attribute name="variant" required="false" %>
<%@ attribute name="href" required="false" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>

<c:choose>
    <c:when test="${empty item.coverImageId}">
        <c:url value="/images/covers/placeholder.svg" var="coverUrl" />
    </c:when>
    <c:otherwise>
        <c:url value="/covers/${item.coverImageId}" var="coverUrl" />
    </c:otherwise>
</c:choose>
<spring:message code="vinylCard.cover.alt" var="coverAlt">
    <spring:argument value="${item.title}" />
</spring:message>
<spring:message code="vinylCard.year" var="yearLabel" />
<spring:message code="vinylCard.price" var="priceLabel" />
<spring:message code="vinylCard.condition" var="conditionLabel" />
<spring:message code="vinylCard.zone" var="zoneLabel" />
<spring:message code="vinylCard.genre" var="genreLabel" />
<spring:message code="vinylCard.pressingYear" var="pressingYearLabel" />
<c:if test="${not empty href}">
    <c:url value="${href}" var="cardHref" />
    <spring:message code="vinylCard.open" var="openLabel">
        <spring:argument value="${item.title}" />
    </spring:message>
</c:if>

<article class="vinyl-card vinyl-card--${empty variant ? 'editorial' : variant}${empty href ? '' : ' vinyl-card--linked'}">
    <c:if test="${not empty href}">
        <a class="vinyl-card__link" href="<c:out value="${cardHref}" />" aria-label="<c:out value="${openLabel}" />"></a>
    </c:if>
    <div class="vinyl-card__cover">
        <img src="<c:out value="${coverUrl}" />"
             alt="<c:out value="${coverAlt}" />"
             class="vinyl-card__image" />
    </div>
    <div class="vinyl-card__content">
        <ui:h3 text="${item.title}" />
        <ui:p text="${item.artistName}" variant="lead" />

        <c:choose>
            <c:when test="${not empty item.price}">
                <spring:message code="vinylCard.price.format" var="priceValue">
                    <spring:argument value="${item.price}" />
                </spring:message>
            </c:when>
            <c:otherwise>
                <spring:message code="vinylCard.price.unavailable" var="priceValue" />
            </c:otherwise>
        </c:choose>
        <div class="vinyl-card__price">
            <span class="vinyl-card__price-label"><c:out value="${priceLabel}" /></span>
            <span class="vinyl-card__price-value"><c:out value="${priceValue}" /></span>
        </div>

        <dl class="vinyl-card__metadata">
            <div class="vinyl-card__datum">
                <dt><ui:span text="${yearLabel}" variant="muted" /></dt>
                <dd><ui:span text="${item.releaseYear}" /></dd>
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

        <div class="vinyl-card__actions">
            <jsp:doBody />
        </div>
    </div>
</article>
```

[[Views and assets]] · [[UI styles and tokens]] · [[Authentication flow]]
