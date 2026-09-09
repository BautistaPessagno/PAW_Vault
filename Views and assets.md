---
title: "Views and assets"
categories: ["Web"]
type: "guide"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
sources: ["webapp/src/main/webapp/WEB-INF/views/landing/index.jsp", "webapp/src/main/webapp/WEB-INF/views/post/contact.jsp", "webapp/src/main/webapp/WEB-INF/views/publish/index.jsp", "webapp/src/main/webapp/images/covers/placeholder.svg"]
---

# Views and assets

Only three JSP views remain. The helloworld create/profile views were removed. Product pages load tokens.css, components.css and style.css, declare /WEB-INF/tags and include viewport metadata. There is no JavaScript source asset or frontend build manifest.

| View | Model | Rendering |
|---|---|---|
| landing/index | posts, optional contactSent | Editorial cards, publish/contact buttons, localized empty/success text |
| publish/index | publishForm, BindingResult, optional coverTooLarge | Multipart Spring form, five text/numeric fields and optional file input |
| post/contact | post, contactForm, BindingResult | Compact card and Spring contact form; no deliveryFailed banner |

ui:text-input inherits relative binding paths from form:form and renders all field errors. The cover input uses form:label and form:errors directly, accepts PNG/JPEG/WebP and displays a 5 MB hint. A whole-request overflow displays the coverTooLarge message with a fresh form.

ui:vinyl-card chooses /images/covers/placeholder.svg for a missing coverImageId or /covers/{id} otherwise. It never displays publisherEmail. c:url handles deployment contexts; c:out escapes tag text and URL attributes. Submit and back-to-catalogue buttons remain shared components.

The previous versus.png file is deleted. The placeholder is a local SVG; stored covers are database bytes returned by [[ImageController]]. [[Cover image flow]] explains ownership and caching.

## landing/index.jsp

[webapp/src/main/webapp/WEB-INF/views/landing/index.jsp, lines 1–48](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/landing/index.jsp>)

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<c:url value="/css/tokens.css" var="tokensCss"/>
<c:url value="/css/components.css" var="componentsCss"/>
<c:url value="/css/style.css" var="cssUrl"/>
<spring:message code="landing.heading" var="heading"/>
<spring:message code="landing.publish" var="publishLabel"/>
<spring:message code="post.contact.action" var="contactLabel"/>
<!DOCTYPE html>
<html lang="${pageContext.response.locale}">
<head>
    <meta charset="UTF-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <title><spring:message code="landing.pageTitle"/></title>
    <link rel="stylesheet" href="${tokensCss}"/>
    <link rel="stylesheet" href="${componentsCss}"/>
    <link rel="stylesheet" href="${cssUrl}"/>
</head>
<body>
<main class="page-shell">
    <header class="page-header">
        <ui:h1 text="${heading}" tone="accent"/>
        <ui:button label="${publishLabel}" variant="primary" href="/publish"/>
    </header>
    <c:if test="${contactSent}">
        <p class="notice"><spring:message code="landing.contact.sent"/></p>
    </c:if>
    <c:choose>
        <c:when test="${empty posts}">
            <p class="empty-state"><spring:message code="landing.empty"/></p>
        </c:when>
        <c:otherwise>
            <ul class="post-grid">
                <c:forEach items="${posts}" var="post">
                    <li>
                        <ui:vinyl-card item="${post}" variant="editorial">
                            <ui:button label="${contactLabel}" variant="ghost" size="sm" href="/post/${post.id}/contact"/>
                        </ui:vinyl-card>
                    </li>
                </c:forEach>
            </ul>
        </c:otherwise>
    </c:choose>
</main>
</body>
</html>
```

## post/contact.jsp

[webapp/src/main/webapp/WEB-INF/views/post/contact.jsp, lines 1–41](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/post/contact.jsp>)

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="form" uri="http://www.springframework.org/tags/form" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<c:url value="/post/${post.id}/contact" var="contactUrl"/>
<c:url value="/css/tokens.css" var="tokensCss"/>
<c:url value="/css/components.css" var="componentsCss"/>
<c:url value="/css/style.css" var="cssUrl"/>
<spring:message code="post.contact.heading" var="heading"/>
<spring:message code="post.contact.name.label" var="nameLabel"/>
<spring:message code="post.contact.email.label" var="emailLabel"/>
<spring:message code="post.contact.submit" var="submitLabel"/>
<spring:message code="post.contact.back" var="backLabel"/>
<!DOCTYPE html>
<html lang="${pageContext.response.locale}">
<head>
    <meta charset="UTF-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <title><spring:message code="post.contact.pageTitle"/></title>
    <link rel="stylesheet" href="${tokensCss}"/>
    <link rel="stylesheet" href="${componentsCss}"/>
    <link rel="stylesheet" href="${cssUrl}"/>
</head>
<body>
<main class="page-shell">
    <header class="page-header">
        <ui:h1 text="${heading}"/>
    </header>
    <ui:vinyl-card item="${post}" variant="compact"/>
    <form:form cssClass="surface form-stack" action="${contactUrl}" method="post" modelAttribute="contactForm">
        <ui:text-input path="contactName" label="${nameLabel}" maxLength="100"/>
        <ui:text-input path="contactEmail" label="${emailLabel}" type="email" maxLength="100"/>
        <div class="form-stack__actions">
            <ui:button label="${submitLabel}" type="submit"/>
            <ui:button label="${backLabel}" variant="ghost" href="/"/>
        </div>
    </form:form>
</main>
</body>
</html>
```

## publish/index.jsp

[webapp/src/main/webapp/WEB-INF/views/publish/index.jsp, lines 1–55](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/publish/index.jsp>)

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="form" uri="http://www.springframework.org/tags/form" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<c:url value="/publish" var="publishUrl"/>
<c:url value="/css/tokens.css" var="tokensCss"/>
<c:url value="/css/components.css" var="componentsCss"/>
<c:url value="/css/style.css" var="cssUrl"/>
<spring:message code="publish.heading" var="heading"/>
<spring:message code="publish.username.label" var="usernameLabel"/>
<spring:message code="publish.publisherEmail.label" var="publisherEmailLabel"/>
<spring:message code="publish.title.label" var="titleLabel"/>
<spring:message code="publish.artistName.label" var="artistNameLabel"/>
<spring:message code="publish.releaseYear.label" var="releaseYearLabel"/>
<spring:message code="publish.submit" var="submitLabel"/>
<spring:message code="publish.back" var="backLabel"/>
<!DOCTYPE html>
<html lang="${pageContext.response.locale}">
<head>
    <meta charset="UTF-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <title><spring:message code="publish.pageTitle"/></title>
    <link rel="stylesheet" href="${tokensCss}"/>
    <link rel="stylesheet" href="${componentsCss}"/>
    <link rel="stylesheet" href="${cssUrl}"/>
</head>
<body>
<main class="page-shell">
    <header class="page-header">
        <ui:h1 text="${heading}"/>
    </header>
    <c:if test="${coverTooLarge}">
        <p class="error"><spring:message code="publish.cover.tooLarge"/></p>
    </c:if>
    <form:form cssClass="surface form-stack" action="${publishUrl}" method="post" modelAttribute="publishForm" enctype="multipart/form-data">
        <ui:text-input path="username" label="${usernameLabel}" maxLength="100"/>
        <ui:text-input path="publisherEmail" label="${publisherEmailLabel}" type="email" maxLength="100"/>
        <ui:text-input path="title" label="${titleLabel}" maxLength="255"/>
        <ui:text-input path="artistName" label="${artistNameLabel}" maxLength="255"/>
        <ui:text-input path="releaseYear" label="${releaseYearLabel}" type="number" min="1000" max="9999"/>
        <div class="input-field">
            <form:label path="cover" cssClass="input-field__label"><spring:message code="publish.cover.label"/></form:label>
            <input id="cover" name="cover" type="file" class="input-field__control" accept="image/png,image/jpeg,image/webp"/>
            <p class="hint"><spring:message code="publish.cover.hint"/></p>
            <form:errors path="cover" cssClass="input-field__error" element="p"/>
        </div>
        <div class="form-stack__actions">
            <ui:button label="${submitLabel}" type="submit"/>
            <ui:button label="${backLabel}" variant="ghost" href="/"/>
        </div>
    </form:form>
</main>
</body>
</html>
```


## Placeholder source

[webapp/src/main/webapp/images/covers/placeholder.svg, lines 1–9](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/images/covers/placeholder.svg>)

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" role="img" aria-hidden="true">
  <rect width="600" height="600" fill="#e8e8e8"/>
  <circle cx="300" cy="300" r="230" fill="#2b2b2b"/>
  <circle cx="300" cy="300" r="190" fill="none" stroke="#3a3a3a" stroke-width="2"/>
  <circle cx="300" cy="300" r="150" fill="none" stroke="#3a3a3a" stroke-width="2"/>
  <circle cx="300" cy="300" r="110" fill="none" stroke="#3a3a3a" stroke-width="2"/>
  <circle cx="300" cy="300" r="70" fill="#bdbdbd"/>
  <circle cx="300" cy="300" r="8" fill="#e8e8e8"/>
</svg>
```

[[UI components]] · [[UI styles and tokens]] · [[Publish flow]] · [[Contact flow]]
