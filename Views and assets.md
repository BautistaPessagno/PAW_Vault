---
title: "Views and assets"
categories: ["Web"]
type: "guide"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "041ce34404963b689d05443ca00abb7e75aa7f15"
status: "documented"
sources: ["webapp/src/main/webapp/WEB-INF/views/helloworld/create.jsp", "webapp/src/main/webapp/WEB-INF/views/helloworld/index.jsp", "webapp/src/main/webapp/WEB-INF/views/landing/index.jsp", "webapp/src/main/webapp/WEB-INF/views/post/contact.jsp", "webapp/src/main/webapp/WEB-INF/views/publish/index.jsp", "webapp/src/main/webapp/images/covers/versus.png"]
---

# Views and assets

This note reflects the committed UI merge at `041ce34404963b689d05443ca00abb7e75aa7f15`. Controllers, services and DAO behavior remain as documented; the view layer now composes reusable JSP tags.

The view resolver prefixes logical names with /WEB-INF/views/ and appends .jsp. Product views load tokens.css, components.css and style.css, declare the ui tag directory, and include a viewport meta tag. No JavaScript source asset or frontend package manifest is present.

| View | Model | Current rendering |
|---|---|---|
| landing/index | posts and optional contactSent | Page header, publish button, empty state or editorial vinyl cards; each body contains a contact button |
| publish/index | publishForm and BindingResult | Spring form:form with relative ui:text-input paths, submit and back-to-catalogue buttons |
| post/contact | post, contactForm, optional deliveryFailed | Compact vinyl card, retained input/error components, submit and back buttons |
| helloworld/create | form | Legacy Spring form tags with literal English labels |
| helloworld/index | user | Escaped username in a literal English greeting |

[[UI components]] explains the complete tag contracts and exact markup. ui:vinyl-card requires [[PostSummary]], renders no publisher email, and uses jsp:doBody for page-supplied actions. ui:text-input uses spring:bind to retrieve field values and validation errors from the existing model. Page labels are resolved through spring:message before passing them into tags. c:out handles text and attribute escaping inside components. Publish and contact use form:form modelAttribute to establish the binding context; text-input renders all field error messages.

c:url in pages/tags handles deployment context paths. Shared buttons receive /publish or /post/{id}/contact and turn them into appropriate links. Publish and contact both pass / to their back buttons. No wishlist tag, CSS, route or storage is present in the committed implementation.

## helloworld/create.jsp

[webapp/src/main/webapp/WEB-INF/views/helloworld/create.jsp, lines 1–27](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/helloworld/create.jsp>)

```jsp
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="form" uri="http://www.springframework.org/tags/form" %>
<c:url value="/create" var="createUrl" />
<html>
<head>
    <link rel="stylesheet" href="<c:url value='/css/style.css'/>"/>
</head>
<body>
<form:form action="${createUrl}" method="post" modelAttribute="form">
    <div>
        <form:label path="username">Username:</form:label>
        <form:input type="text" path="username"/>
        <form:errors path="username" cssClass="error" element="p"/>
    </div>

    <div>
        <form:label path="email">Email:</form:label>
        <form:input type="text" path="email"/>
        <form:errors path="email" cssClass="error" element="p"/>
    </div>

    <div>
        <input type="submit" value="Register!"/>
    </div>
</form:form>
</body>
</html>
```

## helloworld/index.jsp

[webapp/src/main/webapp/WEB-INF/views/helloworld/index.jsp, lines 1–6](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/helloworld/index.jsp>)

```jsp
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<html>
<body>
<h2>Hello <c:out value="${user.username}"/>!</h2>
</body>
</html>
```

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

[webapp/src/main/webapp/WEB-INF/views/post/contact.jsp, lines 1–44](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/post/contact.jsp>)

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
    <c:if test="${deliveryFailed}">
        <p class="error"><spring:message code="post.contact.deliveryFailed"/></p>
    </c:if>
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

[webapp/src/main/webapp/WEB-INF/views/publish/index.jsp, lines 1–46](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/publish/index.jsp>)

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
    <form:form cssClass="surface form-stack" action="${publishUrl}" method="post" modelAttribute="publishForm">
        <ui:text-input path="username" label="${usernameLabel}" maxLength="100"/>
        <ui:text-input path="publisherEmail" label="${publisherEmailLabel}" type="email" maxLength="100"/>
        <ui:text-input path="title" label="${titleLabel}" maxLength="255"/>
        <ui:text-input path="artistName" label="${artistNameLabel}" maxLength="255"/>
        <ui:text-input path="releaseYear" label="${releaseYearLabel}" type="number" min="1000" max="9999"/>
        <div class="form-stack__actions">
            <ui:button label="${submitLabel}" type="submit"/>
            <ui:button label="${backLabel}" variant="ghost" href="/"/>
        </div>
    </form:form>
</main>
</body>
</html>
```

## Styles and image

[[UI styles and tokens]] explains all three CSS files, their load order and responsive/dark-mode rules. The single local cover remains images/covers/versus.png and new albums still use it. [[AlbumServiceImpl]] owns that choice.

[[Landing flow]] · [[Publish flow]] · [[Contact flow]] · [[Legacy user flow]]
