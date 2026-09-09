---
title: "UI components"
categories: ["Web"]
type: "guide"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "041ce34404963b689d05443ca00abb7e75aa7f15"
status: "documented"
sources: ["webapp/src/main/webapp/WEB-INF/tags/button.tag", "webapp/src/main/webapp/WEB-INF/tags/h1.tag", "webapp/src/main/webapp/WEB-INF/tags/h3.tag", "webapp/src/main/webapp/WEB-INF/tags/p.tag", "webapp/src/main/webapp/WEB-INF/tags/span.tag", "webapp/src/main/webapp/WEB-INF/tags/text-input.tag", "webapp/src/main/webapp/WEB-INF/tags/vinyl-card.tag"]
---

# UI components

Seven JSP tags are committed in the UI merge at `041ce34404963b689d05443ca00abb7e75aa7f15`. Pages declare `<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>`. [[Views and assets]] shows their callers and [[UI styles and tokens]] explains their CSS. Controller routes and backend behavior did not change.

Publish and contact retain Spring form:form with modelAttribute. ui:text-input wraps spring:bind inside that form context, preserving values and displaying all field errors.

## button

Required label; optional variant, size, type and href. Defaults to primary and md. A nonempty href becomes a context-aware anchor; otherwise type is submit only when explicitly requested, or button. Labels and URLs use c:out. Variant and size are inserted into CSS class names without a whitelist; current callers supply fixed values. CSS defines primary/ghost and sm/md. There is no disabled attribute or reset type.

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

Required text and optional tone. Renders h1 directly, escapes text with c:out, and adds text--accent only for tone=accent.

[webapp/src/main/webapp/WEB-INF/tags/h1.tag, lines 1–6](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/h1.tag>)

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%@ attribute name="text" required="true" %>
<%@ attribute name="tone" required="false" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>

<h1 class="text text-h1 ${tone eq 'accent' ? 'text--accent' : ''}"><c:out value="${text}" /></h1>
```

## h3

Required text. Renders h3 directly with text text-h3 classes and escapes its content. Used by vinyl-card.

[webapp/src/main/webapp/WEB-INF/tags/h3.tag, lines 1–5](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/h3.tag>)

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%@ attribute name="text" required="true" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>

<h3 class="text text-h3"><c:out value="${text}" /></h3>
```

## p

Required text and optional variant. Escapes text and defaults to text-body; variant is inserted into the class suffix. CSS defines body and lead; cards use lead for artist names.

[webapp/src/main/webapp/WEB-INF/tags/p.tag, lines 1–6](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/p.tag>)

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%@ attribute name="text" required="true" %>
<%@ attribute name="variant" required="false" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>

<p class="text text-${empty variant ? 'body' : variant}"><c:out value="${text}" /></p>
```

## span

Required text and optional variant. Escapes text, always uses text-inline, and adds text--muted only for variant=muted. Cards use it for year labels and values.

[webapp/src/main/webapp/WEB-INF/tags/span.tag, lines 1–6](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/span.tag>)

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="empty" %>
<%@ attribute name="text" required="true" %>
<%@ attribute name="variant" required="false" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>

<span class="text text-inline ${variant eq 'muted' ? 'text--muted' : ''}"><c:out value="${text}" /></span>
```

## text-input

Required path and localized label; optional type, maxLength, min and max. Used inside Spring form:form, with relative paths such as contactEmail or title. spring:bind inherits the form model path and exposes status.expression as name/id and status.value as retained input. Types are limited to text/search/email/number. c:out escapes field names, values and errors. The tag renders every status.errorMessages entry in a role=alert container and connects invalid inputs through aria-invalid and aria-describedby. It has no required, placeholder or minLength attribute; server Bean Validation supplies required-field rules. See [[Validation and errors]], [[PublishForm]] and [[ContactForm]].

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
<c:if test="${type eq 'search' or type eq 'email' or type eq 'number'}">
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
               value="<c:out value="${status.value}" />"
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

## vinyl-card

Required item is typed as [[PostSummary]]; variant defaults to editorial and is inserted into the CSS class suffix. Current callers use editorial on landing and compact on contact. c:url resolves the cover path; vinylCard.cover.alt localizes alt text and vinylCard.year labels the year. c:out escapes image attributes. h3, p and span render title, artist and year. jsp:doBody renders the page-supplied contact button. The card does not display publisher email.

[webapp/src/main/webapp/WEB-INF/tags/vinyl-card.tag, lines 1–35](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/vinyl-card.tag>)

```jsp
<%@ tag language="java" pageEncoding="UTF-8" body-content="scriptless" %>
<%@ attribute name="item" required="true" type="ar.edu.itba.paw.models.PostSummary" %>
<%@ attribute name="variant" required="false" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>

<c:url value="${item.coverPath}" var="coverUrl" />
<spring:message code="vinylCard.cover.alt" var="coverAlt">
    <spring:argument value="${item.title}" />
</spring:message>
<spring:message code="vinylCard.year" var="yearLabel" />

<article class="vinyl-card vinyl-card--${empty variant ? 'editorial' : variant}">
    <div class="vinyl-card__cover">
        <img src="<c:out value="${coverUrl}" />"
             alt="<c:out value="${coverAlt}" />"
             class="vinyl-card__image" />
    </div>
    <div class="vinyl-card__content">
        <ui:h3 text="${item.title}" />
        <ui:p text="${item.artistName}" variant="lead" />

        <dl class="vinyl-card__metadata">
            <div class="vinyl-card__datum">
                <dt><ui:span text="${yearLabel}" variant="muted" /></dt>
                <dd><ui:span text="${item.releaseYear}" /></dd>
            </div>
        </dl>

        <div class="vinyl-card__actions">
            <jsp:doBody />
        </div>
    </div>
</article>
```

The earlier working-tree snapshot contained h2, h4, heading and wishlist-button. These files are absent from the committed version. See [[Known gaps and document drift]].

[[Landing flow]] · [[Publish flow]] · [[Contact flow]]
