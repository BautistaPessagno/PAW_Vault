---
title: "Views and assets"
categories: ["Web"]
type: "guide"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["webapp/src/main/webapp/WEB-INF/views/admin/index.jsp", "webapp/src/main/webapp/WEB-INF/views/artist/suggestions.jsp", "webapp/src/main/webapp/WEB-INF/views/auth/forgot-password.jsp", "webapp/src/main/webapp/WEB-INF/views/auth/login.jsp", "webapp/src/main/webapp/WEB-INF/views/auth/register.jsp", "webapp/src/main/webapp/WEB-INF/views/auth/reset-password.jsp", "webapp/src/main/webapp/WEB-INF/views/auth/verify.jsp", "webapp/src/main/webapp/WEB-INF/views/error/400.jsp", "webapp/src/main/webapp/WEB-INF/views/error/403.jsp", "webapp/src/main/webapp/WEB-INF/views/error/404.jsp", "webapp/src/main/webapp/WEB-INF/views/error/409.jsp", "webapp/src/main/webapp/WEB-INF/views/inquiry/received.jsp", "webapp/src/main/webapp/WEB-INF/views/inquiry/sent.jsp", "webapp/src/main/webapp/WEB-INF/views/landing/index.jsp", "webapp/src/main/webapp/WEB-INF/views/post/contact.jsp", "webapp/src/main/webapp/WEB-INF/views/post/detail.jsp", "webapp/src/main/webapp/WEB-INF/views/profile/index.jsp", "webapp/src/main/webapp/WEB-INF/views/publish/index.jsp", "webapp/src/main/webapp/WEB-INF/views/search/suggestions.jsp", "webapp/src/main/webapp/js/submit-once.js", "webapp/src/main/webapp/js/catalog.js", "webapp/src/main/webapp/js/confirm-action.js", "webapp/src/main/webapp/js/autocomplete.js", "webapp/src/main/webapp/js/account-edit.js", "webapp/src/main/webapp/js/publish-preview.js", "webapp/src/main/webapp/images/covers/placeholder.svg", "webapp/src/main/webapp/images/logo.svg"]
---

# Views and assets

The current source has 19 JSP views, 25 shared tags, six JavaScript assets and two SVG images. Every full page uses ui:head; product pages add ui:site-header, while the auth pages show only the ui:brand logo. Two views are HTML fragments for autocomplete requests rather than pages.

| View | Model and behavior |
|---|---|
| landing/index | query, sort, sorts/genres/conditions, selected filters, posts and postPage; sidebar GET filter form, auto-submitting sort, cards linking to /post/{id}, previous/next pagination |
| post/detail | post and postCreated/postUpdated flashes; state marker, metadata, owner edit link and delete form with confirmation, contact button for others |
| post/contact | PostSummary and optional-message contactForm; compact card, identity notice, data-submit-once, cancel to the detail page |
| publish/index | publishForm, genres, conditions, editing, formAction, cancelHref, existingCoverImageId and coverTooLarge; multipart form with data-submit-once, artist autocomplete, required genre picker and condition segmented control, live preview card |
| profile/index | profileUser, profileForm, changePasswordForm, postPage and open-row flags; inline username/password rows, logout form, own publications with status chips and numbered pagination |
| inquiry/received | receivedPage and both counts; tab navigation, groups with header, accept form with confirmation and reject form with CSRF, status markers, pagination |
| inquiry/sent | sentPage, both counts and inquirySubmitted flash; groups with seller name and status markers |
| auth/login | loginForm; notices for error, logout, verificationSent, verified, passwordChanged, resetLinkSent and passwordReset; links to recovery and registration |
| auth/register | Email-only registerForm |
| auth/verify | Token, username, password and confirmation with validation errors; escaped hidden token |
| auth/forgot-password | Email-only forgotPasswordForm with a uniform confirmation afterwards |
| auth/reset-password | Hidden token written through c:out, password and confirmation, global invalid-link error and a link to request a new one |
| artist/suggestions, search/suggestions | Fragments of escaped li options for autocomplete.js |
| admin/index | Informational page |
| error/400, 403, 404, 409 | Localized status pages; the landing reuses the not-found layout for an empty text search |

ui:head always loads submit-once.js, catalog.js, confirm-action.js and autocomplete.js deferred; a page can add one script through its pageScript attribute (the profile uses account-edit). publish/index includes publish-preview.js directly. Every script is progressive enhancement: forms, links, selects and confirmation-free POSTs still work without JavaScript, and ownership/state rules remain in the services.

The static cover fallback is the SVG placeholder; real image IDs use ImageController. logo.svg is both the favicon and the brand mark. The former inquiry/index.jsp was replaced by the received and sent views. No frontend package manager or build pipeline is present.

## admin/index.jsp

[webapp/src/main/webapp/WEB-INF/views/admin/index.jsp, lines 1–16](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/admin/index.jsp>)

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<spring:message code="auth.admin.heading" var="heading"/>
<!DOCTYPE html>
<html lang="${pageContext.response.locale}">
<ui:head titleCode="auth.admin.pageTitle"/>
<body>
<ui:site-header/>
<main class="page-shell">
    <ui:h1 text="${heading}"/>
    <ui:back-link/>
    <p class="surface"><spring:message code="auth.admin.message"/></p>
</main>
</body>
</html>
```

## artist/suggestions.jsp

[webapp/src/main/webapp/WEB-INF/views/artist/suggestions.jsp, lines 1–10](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/artist/suggestions.jsp>)

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<c:forEach items="${artists}" var="artist" varStatus="status">
    <li class="autocomplete__option"
        id="artist-suggestion-${status.index}"
        role="option"
        data-autocomplete-option
        data-value="<c:out value="${artist.name}"/>"
        aria-selected="false"><c:out value="${artist.name}"/></li>
</c:forEach>
```

## auth/forgot-password.jsp

[webapp/src/main/webapp/WEB-INF/views/auth/forgot-password.jsp, lines 1–34](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/auth/forgot-password.jsp>)

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="form" uri="http://www.springframework.org/tags/form" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<c:url value="/forgot-password" var="forgotPasswordUrl"/>
<c:url value="/login" var="loginUrl"/>
<spring:message code="auth.forgotPassword.heading" var="heading"/>
<spring:message code="auth.email.label" var="emailLabel"/>
<spring:message code="auth.forgotPassword.submit" var="submitLabel"/>
<!DOCTYPE html>
<html lang="${pageContext.response.locale}">
<ui:head titleCode="auth.forgotPassword.pageTitle"/>
<body>
<main class="page-shell auth-shell">
    <header class="auth-shell__header">
        <ui:brand size="lg"/>
    </header>
    <form:form cssClass="surface form-stack" action="${forgotPasswordUrl}" method="post"
               modelAttribute="forgotPasswordForm">
        <h1 class="auth-shell__title"><c:out value="${heading}"/></h1>
        <p class="hint"><spring:message code="auth.forgotPassword.hint"/></p>
        <ui:text-input path="email" label="${emailLabel}" type="email" maxLength="100"/>
        <div class="form-stack__actions">
            <ui:button label="${submitLabel}" type="submit"/>
        </div>
        <p class="auth-shell__switch">
            <spring:message code="auth.register.loginPrompt"/>
            <a href="${loginUrl}"><spring:message code="auth.login.action"/></a>
        </p>
    </form:form>
</main>
</body>
</html>
```

## auth/login.jsp

[webapp/src/main/webapp/WEB-INF/views/auth/login.jsp, lines 1–59](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/auth/login.jsp>)

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="form" uri="http://www.springframework.org/tags/form" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<c:url value="/login" var="loginUrl"/>
<c:url value="/register" var="registerUrl"/>
<c:url value="/forgot-password" var="forgotPasswordUrl"/>
<spring:message code="auth.login.heading" var="heading"/>
<spring:message code="auth.email.label" var="emailLabel"/>
<spring:message code="auth.password.label" var="passwordLabel"/>
<spring:message code="auth.login.submit" var="submitLabel"/>
<!DOCTYPE html>
<html lang="${pageContext.response.locale}">
<ui:head titleCode="auth.login.pageTitle"/>
<body>
<main class="page-shell auth-shell">
    <header class="auth-shell__header">
        <ui:brand size="lg"/>
    </header>
    <form:form cssClass="surface form-stack" action="${loginUrl}" method="post" modelAttribute="loginForm">
        <h1 class="auth-shell__title"><c:out value="${heading}"/></h1>
        <c:if test="${param.error != null}">
            <p class="error"><spring:message code="auth.login.invalid"/></p>
        </c:if>
        <c:if test="${param.logout != null}">
            <p class="notice"><spring:message code="auth.login.loggedOut"/></p>
        </c:if>
        <c:if test="${param.verificationSent != null}">
            <p class="notice"><spring:message code="auth.login.verificationSent"/></p>
        </c:if>
        <c:if test="${param.verified != null}">
            <p class="notice"><spring:message code="auth.login.verified"/></p>
        </c:if>
        <c:if test="${param.passwordChanged != null}">
            <p class="notice"><spring:message code="auth.login.passwordChanged"/></p>
        </c:if>
        <c:if test="${param.resetLinkSent != null}">
            <p class="notice"><spring:message code="auth.login.resetLinkSent"/></p>
        </c:if>
        <c:if test="${param.passwordReset != null}">
            <p class="notice"><spring:message code="auth.login.passwordReset"/></p>
        </c:if>
        <ui:text-input path="email" label="${emailLabel}" type="email" maxLength="100"/>
        <ui:text-input path="password" label="${passwordLabel}" type="password" maxLength="72"/>
        <div class="form-stack__actions">
            <ui:button label="${submitLabel}" type="submit"/>
        </div>
        <p class="auth-shell__switch">
            <a href="${forgotPasswordUrl}"><spring:message code="auth.login.forgotPasswordLink"/></a>
        </p>
        <p class="auth-shell__switch">
            <spring:message code="auth.login.registerPrompt"/>
            <a href="${registerUrl}"><spring:message code="auth.login.registerLink"/></a>
        </p>
    </form:form>
</main>
</body>
</html>
```

## auth/register.jsp

[webapp/src/main/webapp/WEB-INF/views/auth/register.jsp, lines 1–32](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/auth/register.jsp>)

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="form" uri="http://www.springframework.org/tags/form" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<c:url value="/register" var="registerUrl"/>
<c:url value="/login" var="loginUrl"/>
<spring:message code="auth.register.heading" var="heading"/>
<spring:message code="auth.email.label" var="emailLabel"/>
<spring:message code="auth.register.submit" var="submitLabel"/>
<!DOCTYPE html>
<html lang="${pageContext.response.locale}">
<ui:head titleCode="auth.register.pageTitle"/>
<body>
<main class="page-shell auth-shell">
    <header class="auth-shell__header">
        <ui:brand size="lg"/>
    </header>
    <form:form cssClass="surface form-stack" action="${registerUrl}" method="post" modelAttribute="registerForm">
        <h1 class="auth-shell__title"><c:out value="${heading}"/></h1>
        <ui:text-input path="email" label="${emailLabel}" type="email" maxLength="100"/>
        <div class="form-stack__actions">
            <ui:button label="${submitLabel}" type="submit"/>
        </div>
        <p class="auth-shell__switch">
            <spring:message code="auth.register.loginPrompt"/>
            <a href="${loginUrl}"><spring:message code="auth.login.action"/></a>
        </p>
    </form:form>
</main>
</body>
</html>
```

## auth/reset-password.jsp

[webapp/src/main/webapp/WEB-INF/views/auth/reset-password.jsp, lines 1–48](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/auth/reset-password.jsp>)

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="form" uri="http://www.springframework.org/tags/form" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<c:url value="/reset-password" var="resetPasswordUrl"/>
<c:url value="/forgot-password" var="forgotPasswordUrl"/>
<spring:message code="auth.resetPassword.heading" var="heading"/>
<spring:message code="auth.password.label" var="passwordLabel"/>
<spring:message code="auth.passwordConfirmation.label" var="passwordConfirmationLabel"/>
<spring:message code="auth.resetPassword.submit" var="submitLabel"/>
<!DOCTYPE html>
<html lang="${pageContext.response.locale}">
<ui:head titleCode="auth.resetPassword.pageTitle"/>
<body>
<main class="page-shell auth-shell">
    <header class="auth-shell__header">
        <ui:brand size="lg"/>
    </header>
    <form:form cssClass="surface form-stack" action="${resetPasswordUrl}" method="post"
               modelAttribute="resetPasswordForm">
        <h1 class="auth-shell__title"><c:out value="${heading}"/></h1>
        <p class="hint"><spring:message code="auth.resetPassword.hint"/></p>
        <%-- Los errores de cada campo los muestra ui:text-input debajo del campo. Aca van
             solo los que no tienen un campo visible: el enlace vencido y el token faltante. --%>
        <form:errors cssClass="input-field__error" element="p"/>
        <form:errors path="token" cssClass="input-field__error" element="p"/>
        <%-- El token viene del query string. form:hidden lo escribiria sin escapar
             (defaultHtmlEscape no esta activado), asi que se emite como el resto de
             los campos: el valor pasa por c:out. --%>
        <spring:bind path="token">
            <input type="hidden" name="<c:out value="${status.expression}"/>"
                   value="<c:out value="${status.value}"/>"/>
        </spring:bind>
        <ui:text-input path="password" label="${passwordLabel}" type="password" maxLength="72"/>
        <ui:text-input path="passwordConfirmation" label="${passwordConfirmationLabel}" type="password" maxLength="72"/>
        <p class="hint"><spring:message code="auth.password.hint"/></p>
        <div class="form-stack__actions">
            <ui:button label="${submitLabel}" type="submit"/>
        </div>
        <p class="auth-shell__switch">
            <spring:message code="auth.resetPassword.expiredPrompt"/>
            <a href="${forgotPasswordUrl}"><spring:message code="auth.resetPassword.expiredLink"/></a>
        </p>
    </form:form>
</main>
</body>
</html>
```

## auth/verify.jsp

[webapp/src/main/webapp/WEB-INF/views/auth/verify.jsp, lines 1–49](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/auth/verify.jsp>)

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="form" uri="http://www.springframework.org/tags/form" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<c:url value="/verify" var="verifyUrl"/>
<c:url value="/login" var="loginUrl"/>
<spring:message code="auth.verify.heading" var="heading"/>
<spring:message code="auth.password.label" var="passwordLabel"/>
<spring:message code="auth.username.label" var="usernameLabel"/>
<spring:message code="auth.passwordConfirmation.label" var="passwordConfirmationLabel"/>
<spring:message code="auth.verify.submit" var="submitLabel"/>
<!DOCTYPE html>
<html lang="${pageContext.response.locale}">
<ui:head titleCode="auth.verify.pageTitle"/>
<body>
<main class="page-shell auth-shell">
    <header class="auth-shell__header">
        <ui:brand size="lg"/>
    </header>
    <form:form cssClass="surface form-stack" action="${verifyUrl}" method="post" modelAttribute="verifyEmailForm">
        <h1 class="auth-shell__title"><c:out value="${heading}"/></h1>
        <p class="hint"><spring:message code="auth.verify.hint"/></p>
        <%-- Los errores de cada campo los muestra ui:text-input debajo del campo. Aca van
             solo los que no tienen un campo visible: el enlace vencido y el token faltante. --%>
        <form:errors cssClass="input-field__error" element="p"/>
        <form:errors path="token" cssClass="input-field__error" element="p"/>
        <%-- El token viene del query string. form:hidden lo escribiria sin escapar
             (defaultHtmlEscape no esta activado), asi que se emite como el resto de
             los campos: el valor pasa por c:out. --%>
        <spring:bind path="token">
            <input type="hidden" name="<c:out value="${status.expression}"/>"
                   value="<c:out value="${status.value}"/>"/>
        </spring:bind>
        <ui:text-input path="username" label="${usernameLabel}" maxLength="100"/>
        <ui:text-input path="password" label="${passwordLabel}" type="password" maxLength="72"/>
        <ui:text-input path="passwordConfirmation" label="${passwordConfirmationLabel}" type="password" maxLength="72"/>
        <p class="hint"><spring:message code="auth.password.hint"/></p>
        <div class="form-stack__actions">
            <ui:button label="${submitLabel}" type="submit"/>
        </div>
        <p class="auth-shell__switch">
            <spring:message code="auth.register.loginPrompt"/>
            <a href="${loginUrl}"><spring:message code="auth.login.action"/></a>
        </p>
    </form:form>
</main>
</body>
</html>
```

## error/400.jsp

[webapp/src/main/webapp/WEB-INF/views/error/400.jsp, lines 1–28](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/error/400.jsp>)

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<spring:message code="error.badRequest.code" var="codeLabel"/>
<spring:message code="error.badRequest.heading" var="heading"/>
<spring:message code="error.badRequest.message" var="message"/>
<spring:message code="nav.back" var="backLabel"/>
<!DOCTYPE html>
<html lang="${pageContext.response.locale}">
<ui:head titleCode="error.badRequest.pageTitle"/>
<body>
<main class="page-shell page-shell--centered">
    <section class="not-found">
        <div class="not-found__record">
            <p class="not-found__code"><span class="not-found__digits"><c:out value="${codeLabel}"/></span></p>
        </div>
        <div class="not-found__intro">
            <ui:h1 text="${heading}" tone="accent"/>
            <ui:p text="${message}" variant="lead"/>
            <div class="not-found__actions">
                <ui:button label="${backLabel}" href="/"/>
            </div>
        </div>
    </section>
</main>
</body>
</html>
```

## error/403.jsp

[webapp/src/main/webapp/WEB-INF/views/error/403.jsp, lines 1–18](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/error/403.jsp>)

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<spring:message code="error.forbidden.heading" var="heading"/>
<spring:message code="error.forbidden.message" var="message"/>
<spring:message code="nav.back" var="backLabel"/>
<!DOCTYPE html>
<html lang="${pageContext.response.locale}">
<ui:head titleCode="error.forbidden.pageTitle"/>
<body>
<main class="page-shell error-page">
    <p class="error-page__code"><spring:message code="error.forbidden.code"/></p>
    <ui:h1 text="${heading}"/>
    <ui:p text="${message}"/>
    <div class="form-stack__actions"><ui:button label="${backLabel}" href="/"/></div>
</main>
</body>
</html>
```

## error/404.jsp

[webapp/src/main/webapp/WEB-INF/views/error/404.jsp, lines 1–30](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/error/404.jsp>)

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<spring:message code="error.notFound.code" var="codeLabel"/>
<spring:message code="error.notFound.heading" var="heading"/>
<spring:message code="error.notFound.message" var="message"/>
<spring:message code="error.notFound.publish" var="publishLabel"/>
<spring:message code="nav.back" var="backLabel"/>
<!DOCTYPE html>
<html lang="${pageContext.response.locale}">
<ui:head titleCode="error.notFound.pageTitle"/>
<body>
<main class="page-shell page-shell--centered">
    <section class="not-found">
        <div class="not-found__record">
            <p class="not-found__code"><span class="not-found__digits"><c:out value="${codeLabel}"/></span></p>
        </div>
        <div class="not-found__intro">
            <ui:h1 text="${heading}" tone="accent"/>
            <ui:p text="${message}" variant="lead"/>
            <div class="not-found__actions">
                <ui:button label="${backLabel}" href="/"/>
                <ui:button label="${publishLabel}" variant="ghost" href="/publish"/>
            </div>
        </div>
    </section>
</main>
</body>
</html>
```

## error/409.jsp

[webapp/src/main/webapp/WEB-INF/views/error/409.jsp, lines 1–18](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/error/409.jsp>)

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<spring:message code="error.conflict.heading" var="heading"/>
<spring:message code="error.conflict.message" var="message"/>
<spring:message code="nav.back" var="backLabel"/>
<!DOCTYPE html>
<html lang="${pageContext.response.locale}">
<ui:head titleCode="error.conflict.pageTitle"/>
<body>
<main class="page-shell error-page">
    <p class="error-page__code"><spring:message code="error.conflict.code"/></p>
    <ui:h1 text="${heading}"/>
    <ui:p text="${message}"/>
    <div class="form-stack__actions"><ui:button label="${backLabel}" href="/"/></div>
</main>
</body>
</html>
```

## inquiry/received.jsp

[webapp/src/main/webapp/WEB-INF/views/inquiry/received.jsp, lines 1–81](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/inquiry/received.jsp>)

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="sec" uri="http://www.springframework.org/security/tags" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<spring:message code="inquiry.heading" var="heading"/>
<spring:message code="inquiry.accept" var="acceptLabel"/>
<spring:message code="inquiry.reject" var="rejectLabel"/>
<spring:message code="inquiry.accept.dialog.title" var="acceptDialogTitle"/>
<spring:message code="inquiry.message.empty" var="emptyMessageLabel"/>
<spring:message code="inquiry.pagination" var="paginationLabel"/>
<!DOCTYPE html>
<html lang="${pageContext.response.locale}">
<ui:head titleCode="inquiry.received.pageTitle"/>
<body>
<ui:site-header/>
<main class="page-shell">
    <ui:h1 text="${heading}"/>
    <ui:inquiry-nav active="received" receivedCount="${receivedCount}" sentCount="${sentCount}"/>
    <c:if test="${inquiryAccepted}"><p class="notice"><spring:message code="inquiry.accepted"/></p></c:if>
    <c:if test="${inquiryRejected}"><p class="notice"><spring:message code="inquiry.rejected"/></p></c:if>

    <section class="inbox" id="inquiries">
        <c:choose>
            <c:when test="${empty receivedPage.groups}">
                <p class="empty-state"><spring:message code="inquiry.received.empty"/></p>
            </c:when>
            <c:otherwise>
                <c:forEach items="${receivedPage.groups}" var="group">
                    <section class="inbox-group">
                        <ui:inbox-group-header group="${group}"/>
                        <ul class="inbox-list">
                            <c:forEach items="${group.inquiries}" var="inquiry">
                                <li class="inbox-row">
                                    <span class="inbox-row__who"><c:out value="${inquiry.buyerUsername}"/></span>
                                    <c:choose>
                                        <c:when test="${empty inquiry.message}"><p class="inbox-row__msg inbox-row__msg--empty"><c:out value="${emptyMessageLabel}"/></p></c:when>
                                        <c:otherwise><p class="inbox-row__msg"><c:out value="${inquiry.message}"/></p></c:otherwise>
                                    </c:choose>
                                    <div class="inbox-row__end">
                                        <c:choose>
                                            <c:when test="${inquiry.pending and inquiry.postAvailable}">
                                                <spring:message code="inquiry.accept.confirmation" var="acceptConfirmation">
                                                    <spring:argument value="${group.title}"/>
                                                    <spring:argument value="${group.artistName}"/>
                                                </spring:message>
                                                <c:url value="/inquiries/${inquiry.id}/accept" var="acceptUrl"/>
                                                <form action="${acceptUrl}" method="post" data-confirm-message="<c:out value="${acceptConfirmation}"/>">
                                                    <sec:csrfInput/>
                                                    <ui:button label="${acceptLabel}" size="sm" type="submit" icon="check"/>
                                                </form>
                                                <c:url value="/inquiries/${inquiry.id}/reject" var="rejectUrl"/>
                                                <form action="${rejectUrl}" method="post">
                                                    <sec:csrfInput/>
                                                    <ui:button label="${rejectLabel}" variant="danger-outline" size="sm" type="submit" icon="x"/>
                                                </form>
                                            </c:when>
                                            <c:otherwise>
                                                <ui:inquiry-status status="${inquiry.status}"/>
                                            </c:otherwise>
                                        </c:choose>
                                    </div>
                                </li>
                            </c:forEach>
                        </ul>
                    </section>
                </c:forEach>
                <ui:pagination currentPage="${receivedPage.pageNumber}"
                               hasPrevious="${receivedPage.hasPrevious}"
                               hasNext="${receivedPage.hasNext}"
                               totalPages="${receivedPage.totalPages}"
                               baseUrl="/inquiries"
                               fragment="inquiries"
                               ariaLabel="${paginationLabel}"/>
            </c:otherwise>
        </c:choose>
    </section>
</main>
<ui:confirm-dialog title="${acceptDialogTitle}" confirmLabel="${acceptLabel}"/>
</body>
</html>
```

## inquiry/sent.jsp

[webapp/src/main/webapp/WEB-INF/views/inquiry/sent.jsp, lines 1–55](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/inquiry/sent.jsp>)

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<spring:message code="inquiry.heading" var="heading"/>
<spring:message code="inquiry.message.empty" var="emptyMessageLabel"/>
<spring:message code="inquiry.pagination" var="paginationLabel"/>
<!DOCTYPE html>
<html lang="${pageContext.response.locale}">
<ui:head titleCode="inquiry.sent.pageTitle"/>
<body>
<ui:site-header/>
<main class="page-shell">
    <ui:h1 text="${heading}"/>
    <ui:inquiry-nav active="sent" receivedCount="${receivedCount}" sentCount="${sentCount}"/>
    <c:if test="${inquirySubmitted}"><p class="notice"><spring:message code="inquiry.submitted"/></p></c:if>

    <section class="inbox" id="inquiries">
        <c:choose>
            <c:when test="${empty sentPage.groups}">
                <p class="empty-state"><spring:message code="inquiry.sent.empty"/></p>
            </c:when>
            <c:otherwise>
                <c:forEach items="${sentPage.groups}" var="group">
                    <section class="inbox-group">
                        <ui:inbox-group-header group="${group}"/>
                        <ul class="inbox-list">
                            <c:forEach items="${group.inquiries}" var="inquiry">
                                <li class="inbox-row">
                                    <span class="inbox-row__who"><c:out value="${group.sellerUsername}"/></span>
                                    <c:choose>
                                        <c:when test="${empty inquiry.message}"><p class="inbox-row__msg inbox-row__msg--empty"><c:out value="${emptyMessageLabel}"/></p></c:when>
                                        <c:otherwise><p class="inbox-row__msg"><c:out value="${inquiry.message}"/></p></c:otherwise>
                                    </c:choose>
                                    <div class="inbox-row__end">
                                        <ui:inquiry-status status="${inquiry.status}"/>
                                    </div>
                                </li>
                            </c:forEach>
                        </ul>
                    </section>
                </c:forEach>
                <ui:pagination currentPage="${sentPage.pageNumber}"
                               hasPrevious="${sentPage.hasPrevious}"
                               hasNext="${sentPage.hasNext}"
                               totalPages="${sentPage.totalPages}"
                               baseUrl="/inquiries/sent"
                               fragment="inquiries"
                               ariaLabel="${paginationLabel}"/>
            </c:otherwise>
        </c:choose>
    </section>
</main>
</body>
</html>
```

## landing/index.jsp

[webapp/src/main/webapp/WEB-INF/views/landing/index.jsp, lines 1–174](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/landing/index.jsp>)

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<spring:message code="landing.search.clear" var="searchClearLabel"/>
<spring:message code="landing.search.empty.heading" var="searchEmptyHeading"/>
<spring:message code="nav.back" var="backLabel"/>
<spring:message code="landing.results.count" var="countText">
    <spring:argument value="${fn:length(posts)}"/>
</spring:message>
<spring:message code="landing.sort.label" var="sortLabel"/>
<spring:message code="landing.sort.submit" var="sortSubmitLabel"/>
<spring:message code="landing.filters.apply" var="applyLabel"/>
<spring:message code="landing.filter.genre" var="genreLabel"/>
<spring:message code="landing.filter.condition" var="conditionLabel"/>
<spring:message code="landing.filter.year" var="yearLabel"/>
<spring:message code="landing.filter.price" var="priceLabel"/>
<spring:message code="landing.filter.priceMin" var="priceMinLabel"/>
<spring:message code="landing.filter.priceMax" var="priceMaxLabel"/>
<spring:message code="landing.filter.any" var="anyLabel"/>
<spring:message code="landing.pagination" var="paginationLabel"/>
<c:url value="/" var="searchUrl"/>
<%-- "Quitar filtros" limpia solo la barra lateral: la busqueda del header y el orden
     se conservan, porque no son filtros sino formas de recorrer el catalogo. --%>
<c:url value="/" var="clearHref">
    <c:if test="${not empty query}"><c:param name="q" value="${query}"/></c:if>
    <c:if test="${sort ne 'NEWEST'}"><c:param name="sort" value="${sort}"/></c:if>
</c:url>
<c:set var="hasFilters" value="${not empty selectedGenre
        or not empty selectedCondition or not empty selectedArtistId
        or not empty selectedYear or not empty minPrice or not empty maxPrice}"/>
<c:set var="searchIsEmpty" value="${empty posts and not empty query}"/>
<jsp:useBean id="paginationParams" class="java.util.LinkedHashMap" scope="page"/>
<c:if test="${not empty query}"><c:set target="${paginationParams}" property="q" value="${query}"/></c:if>
<c:if test="${sort ne 'NEWEST'}"><c:set target="${paginationParams}" property="sort" value="${sort}"/></c:if>
<c:if test="${not empty selectedGenre}"><c:set target="${paginationParams}" property="genre" value="${selectedGenre}"/></c:if>
<c:if test="${not empty selectedCondition}"><c:set target="${paginationParams}" property="condition" value="${selectedCondition}"/></c:if>
<c:if test="${not empty selectedArtistId}"><c:set target="${paginationParams}" property="artistId" value="${selectedArtistId}"/></c:if>
<c:if test="${not empty selectedYear}"><c:set target="${paginationParams}" property="year" value="${selectedYear}"/></c:if>
<c:if test="${not empty minPrice}"><c:set target="${paginationParams}" property="minPrice" value="${minPrice}"/></c:if>
<c:if test="${not empty maxPrice}"><c:set target="${paginationParams}" property="maxPrice" value="${maxPrice}"/></c:if>
<!DOCTYPE html>
<html lang="${pageContext.response.locale}">
<ui:head titleCode="landing.pageTitle"/>
<body class="${searchIsEmpty ? 'catalog-empty-page' : ''}">
<ui:site-header query="${query}"/>
<main class="page-shell">
    <div class="catalog">
    <aside class="catalog__filters">
        <details class="filters" open>
            <summary class="filters__summary"><spring:message code="landing.filters.heading"/></summary>
            <h2 class="filters__heading"><spring:message code="landing.filters.heading"/></h2>
            <form class="filters__form" action="${searchUrl}" method="get">
                <c:if test="${not empty query}">
                    <input type="hidden" name="q" value="<c:out value="${query}"/>"/>
                </c:if>
                <c:if test="${sort ne 'NEWEST'}">
                    <input type="hidden" name="sort" value="<c:out value="${sort}"/>"/>
                </c:if>
                <c:if test="${not empty selectedArtistId}">
                    <input type="hidden" name="artistId" value="<c:out value="${selectedArtistId}"/>"/>
                </c:if>
                <div class="filter-field">
                    <label id="genre-label" for="genre"><c:out value="${genreLabel}"/></label>
                    <ui:select-control id="genre" name="genre" items="${genres}" messagePrefix="genre"
                                       selectedValue="${selectedGenre}" emptyLabel="${anyLabel}"
                                       labelledBy="genre-label" />
                </div>
                <ui:segmented-control name="condition" legend="${conditionLabel}" items="${conditions}"
                                      messagePrefix="condition" selectedValue="${selectedCondition}"
                                      emptyLabel="${anyLabel}" />
                <div class="filter-field">
                    <label for="year"><c:out value="${yearLabel}"/></label>
                    <ui:input-control id="year" name="year" type="number" value="${selectedYear}" />
                </div>
                <fieldset class="filter-group">
                    <legend class="filter-group__legend"><c:out value="${priceLabel}"/></legend>
                    <div class="filter-group__range">
                        <div class="filter-field">
                            <label for="minPrice"><c:out value="${priceMinLabel}"/></label>
                            <ui:input-control id="minPrice" name="minPrice" type="number" value="${minPrice}" />
                        </div>
                        <div class="filter-field">
                            <label for="maxPrice"><c:out value="${priceMaxLabel}"/></label>
                            <ui:input-control id="maxPrice" name="maxPrice" type="number" value="${maxPrice}" />
                        </div>
                    </div>
                </fieldset>
                <ui:button label="${applyLabel}" type="submit" size="sm"/>
            </form>
        </details>
    </aside>
    <section class="catalog__results">
        <c:if test="${not searchIsEmpty}">
            <div class="results-bar">
                <div class="results-bar__summary">
                    <ui:h1 text="${countText}"/>
                    <c:if test="${not empty query}">
                        <p class="results-bar__query">
                            <spring:message code="landing.search.results" htmlEscape="true">
                                <spring:argument value="${query}"/>
                            </spring:message>
                        </p>
                    </c:if>
                    <c:if test="${hasFilters}">
                        <%-- clearHref ya viene de c:url: pasarlo por ui:button duplicaria el context path. --%>
                        <a class="button button--ghost button--sm" href="<c:out value="${clearHref}"/>"><c:out value="${searchClearLabel}"/></a>
                    </c:if>
                </div>
                <c:if test="${not empty posts}">
                    <form class="sort-form" action="${searchUrl}" method="get" data-auto-submit="true">
                        <c:if test="${not empty query}"><input type="hidden" name="q" value="<c:out value="${query}"/>"/></c:if>
                        <c:if test="${not empty selectedGenre}"><input type="hidden" name="genre" value="<c:out value="${selectedGenre}"/>"/></c:if>
                        <c:if test="${not empty selectedCondition}"><input type="hidden" name="condition" value="<c:out value="${selectedCondition}"/>"/></c:if>
                        <c:if test="${not empty selectedArtistId}"><input type="hidden" name="artistId" value="<c:out value="${selectedArtistId}"/>"/></c:if>
                        <c:if test="${not empty selectedYear}"><input type="hidden" name="year" value="<c:out value="${selectedYear}"/>"/></c:if>
                        <c:if test="${not empty minPrice}"><input type="hidden" name="minPrice" value="<c:out value="${minPrice}"/>"/></c:if>
                        <c:if test="${not empty maxPrice}"><input type="hidden" name="maxPrice" value="<c:out value="${maxPrice}"/>"/></c:if>
                        <label class="sort-form__label" id="sort-label" for="sort"><c:out value="${sortLabel}"/></label>
                        <ui:select-control id="sort" name="sort" items="${sorts}"
                                           messagePrefix="landing.sort" selectedValue="${sort}"
                                           labelledBy="sort-label" cssClass="sort-form__control" />
                        <ui:button label="${sortSubmitLabel}" variant="ghost" size="sm" type="submit"/>
                    </form>
                </c:if>
            </div>
        </c:if>
        <c:choose>
            <c:when test="${searchIsEmpty}">
                <spring:message code="landing.search.empty" var="searchEmptyMessage">
                    <spring:argument value="${query}"/>
                </spring:message>
                <section class="not-found not-found--catalog">
                    <a class="not-found__record" href="<c:out value="${searchUrl}"/>"
                       aria-label="<c:out value="${backLabel}"/>">
                        <span class="not-found__code" aria-hidden="true"></span>
                    </a>
                    <div class="not-found__intro">
                        <ui:h1 text="${searchEmptyHeading}" tone="accent"/>
                        <ui:p text="${searchEmptyMessage}" variant="lead"/>
                        <div class="not-found__actions">
                            <ui:button label="${backLabel}" href="/"/>
                        </div>
                    </div>
                </section>
            </c:when>
            <c:when test="${empty posts and hasFilters}">
                <p class="empty-state"><spring:message code="landing.filter.empty"/></p>
            </c:when>
            <c:when test="${empty posts}">
                <p class="empty-state"><spring:message code="landing.empty"/></p>
            </c:when>
            <c:otherwise>
                <ul class="post-grid">
                    <c:forEach items="${posts}" var="post">
                        <li>
                            <ui:vinyl-card item="${post}" variant="editorial" href="/post/${post.id}"/>
                        </li>
                    </c:forEach>
                </ul>
            </c:otherwise>
        </c:choose>
        <ui:pagination currentPage="${postPage.pageNumber}"
                       hasPrevious="${postPage.hasPrevious}"
                       hasNext="${postPage.hasNext}"
                       baseUrl="/"
                       extraParams="${paginationParams}"
                       ariaLabel="${paginationLabel}"/>
    </section>
    </div>
</main>
</body>
</html>
```

## post/contact.jsp

[webapp/src/main/webapp/WEB-INF/views/post/contact.jsp, lines 1–31](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/post/contact.jsp>)

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="form" uri="http://www.springframework.org/tags/form" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<c:url value="/post/${post.id}/contact" var="contactUrl"/>
<spring:message code="post.contact.heading" var="heading"/>
<spring:message code="post.contact.message.label" var="messageLabel"/>
<spring:message code="post.contact.submit" var="submitLabel"/>
<spring:message code="form.cancel" var="cancelLabel"/>
<!DOCTYPE html>
<html lang="${pageContext.response.locale}">
<ui:head titleCode="post.contact.pageTitle"/>
<body>
<ui:site-header/>
<main class="page-shell">
    <ui:h1 text="${heading}"/>
    <div class="contact-layout">
        <ui:vinyl-card item="${post}" variant="compact"/>
        <form:form cssClass="surface form-stack" action="${contactUrl}" method="post" modelAttribute="contactForm" data-submit-once="true">
            <p><spring:message code="post.contact.identity"/></p>
            <ui:textarea path="contactMessage" label="${messageLabel}" maxLength="500"/>
            <div class="form-stack__actions">
                <ui:button label="${submitLabel}" type="submit"/>
                <ui:button label="${cancelLabel}" variant="ghost" href="/post/${post.id}"/>
            </div>
        </form:form>
    </div>
</main>
</body>
</html>
```

## post/detail.jsp

[webapp/src/main/webapp/WEB-INF/views/post/detail.jsp, lines 1–131](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/post/detail.jsp>)

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="sec" uri="http://www.springframework.org/security/tags" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<c:choose>
    <c:when test="${empty post.coverImageId}">
        <c:url value="/images/covers/placeholder.svg" var="coverUrl"/>
    </c:when>
    <c:otherwise>
        <c:url value="/covers/${post.coverImageId}" var="coverUrl"/>
    </c:otherwise>
</c:choose>
<spring:message code="vinylCard.cover.alt" var="coverAlt">
    <spring:argument value="${post.title}"/>
</spring:message>
<spring:message code="vinylCard.year" var="yearLabel"/>
<spring:message code="vinylCard.condition" var="conditionLabel"/>
<spring:message code="vinylCard.zone" var="zoneLabel"/>
<spring:message code="vinylCard.genre" var="genreLabel"/>
<spring:message code="vinylCard.pressingYear" var="pressingYearLabel"/>
<spring:message code="post.contact.action" var="contactLabel"/>
<spring:message code="post.edit.action" var="editLabel"/>
<spring:message code="post.delete.action" var="deleteLabel"/>
<spring:message code="post.delete.dialog.title" var="deleteDialogTitle"/>
<spring:message code="post.delete.confirmation" var="deleteConfirmation">
    <spring:argument value="${post.title}"/>
    <spring:argument value="${post.artistName}"/>
</spring:message>
<!DOCTYPE html>
<html lang="${pageContext.response.locale}">
<ui:head titleCode="post.detail.pageTitle"/>
<body>
<ui:site-header/>
<main class="page-shell">
    <ui:back-link/>
    <c:if test="${postCreated}"><p class="notice"><spring:message code="post.created"/></p></c:if>
    <c:if test="${postUpdated}"><p class="notice"><spring:message code="post.updated"/></p></c:if>
    <sec:authorize access="isAuthenticated()">
        <sec:authentication property="principal.id" var="currentUserId" scope="page"/>
    </sec:authorize>
    <c:set var="ownsAvailablePost" value="${not empty currentUserId and currentUserId eq post.userId and post.status eq 'AVAILABLE'}"/>
    <article class="detail">
        <div class="detail__cover">
            <img class="detail__image" src="<c:out value="${coverUrl}"/>" alt="<c:out value="${coverAlt}"/>"/>
        </div>
        <div class="detail__body">
            <div class="detail__heading">
                <div class="detail__title">
                    <ui:h1 text="${post.title}"/>
                    <ui:post-badge status="${post.status}"/>
                </div>
                <c:if test="${ownsAvailablePost}">
                    <div class="detail__owner-actions">
                        <ui:button label="${editLabel}" variant="ghost" size="sm" href="/post/${post.id}/edit" icon="pencil"/>
                        <c:url value="/post/${post.id}/delete" var="deleteUrl"/>
                        <form action="${deleteUrl}" method="post" data-confirm-message="<c:out value="${deleteConfirmation}"/>">
                            <sec:csrfInput/>
                            <ui:button label="${deleteLabel}" variant="danger" size="sm" type="submit" icon="trash"/>
                        </form>
                    </div>
                </c:if>
            </div>
            <ui:p text="${post.artistName}" variant="lead"/>
            <spring:message code="vinylCard.price.format" var="priceValue">
                <spring:argument value="${post.price}"/>
            </spring:message>
            <div class="vinyl-card__price">
                <span class="vinyl-card__price-value"><c:out value="${priceValue}"/></span>
            </div>
            <dl class="detail__metadata">
                <div class="detail__datum">
                    <dt><ui:span text="${yearLabel}" variant="muted"/></dt>
                    <dd><ui:span text="${post.releaseYear}"/></dd>
                </div>
                <c:if test="${not empty post.condition}">
                    <spring:message code="condition.${post.condition}" var="conditionValue"/>
                    <div class="detail__datum">
                        <dt><ui:span text="${conditionLabel}" variant="muted"/></dt>
                        <dd><ui:span text="${conditionValue}"/></dd>
                    </div>
                </c:if>
                <c:if test="${not empty post.zone}">
                    <div class="detail__datum">
                        <dt><ui:span text="${zoneLabel}" variant="muted"/></dt>
                        <dd><ui:span text="${post.zone}"/></dd>
                    </div>
                </c:if>
                <c:if test="${not empty post.genre}">
                    <spring:message code="genre.${post.genre}" var="genreValue"/>
                    <div class="detail__datum">
                        <dt><ui:span text="${genreLabel}" variant="muted"/></dt>
                        <dd><ui:span text="${genreValue}"/></dd>
                    </div>
                </c:if>
                <c:if test="${not empty post.pressingYear}">
                    <div class="detail__datum">
                        <dt><ui:span text="${pressingYearLabel}" variant="muted"/></dt>
                        <dd><ui:span text="${post.pressingYear}"/></dd>
                    </div>
                </c:if>
            </dl>
            <c:if test="${not empty post.description}">
                <h2 class="text text-h3"><spring:message code="post.detail.description"/></h2>
                <p class="text text-body detail__description"><c:out value="${post.description}"/></p>
            </c:if>
            <div class="detail__actions">
                <c:if test="${post.status eq 'AVAILABLE'}">
                    <sec:authorize access="isAnonymous()">
                        <ui:button label="${contactLabel}" href="/post/${post.id}/contact"/>
                    </sec:authorize>
                    <sec:authorize access="isAuthenticated()">
                        <c:choose>
                            <c:when test="${currentUserId eq post.userId}">
                                <p class="hint"><spring:message code="post.detail.own"/></p>
                            </c:when>
                            <c:otherwise>
                                <ui:button label="${contactLabel}" href="/post/${post.id}/contact"/>
                            </c:otherwise>
                        </c:choose>
                    </sec:authorize>
                </c:if>
            </div>
        </div>
    </article>
</main>
<c:if test="${ownsAvailablePost}">
<ui:confirm-dialog title="${deleteDialogTitle}" confirmLabel="${deleteLabel}" confirmVariant="danger"/>
</c:if>
</body>
</html>
```

## profile/index.jsp

[webapp/src/main/webapp/WEB-INF/views/profile/index.jsp, lines 1–122](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/profile/index.jsp>)

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="form" uri="http://www.springframework.org/tags/form" %>
<%@ taglib prefix="sec" uri="http://www.springframework.org/security/tags" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<c:url value="/profile" var="profileUrl" />
<%-- Cancelar sin JavaScript vuelve al perfil en la misma pagina del listado. --%>
<c:url value="/profile" var="cancelUrl"><c:param name="page" value="${postPage.pageNumber}"/></c:url>
<c:url value="/profile/password" var="profilePasswordUrl" />
<c:url value="/logout" var="logoutUrl" />
<spring:message code="profile.heading" var="heading" />
<spring:message code="profile.username.label" var="usernameLabel" />
<spring:message code="profile.username.edit" var="usernameEditLabel" />
<spring:message code="profile.password.label" var="passwordLabel" />
<spring:message code="profile.password.edit" var="passwordEditLabel" />
<spring:message code="profile.password.masked" var="passwordMasked" />
<spring:message code="profile.edit.save" var="saveLabel" />
<spring:message code="profile.edit.cancel" var="cancelLabel" />
<spring:message code="profile.password.current.label" var="currentPasswordLabel" />
<spring:message code="profile.password.new.label" var="newPasswordLabel" />
<spring:message code="auth.passwordConfirmation.label" var="passwordConfirmationLabel" />
<spring:message code="auth.password.hint" var="passwordHint" />
<spring:message code="profile.posts.pagination" var="paginationLabel" />
<spring:message code="auth.logout.action" var="logoutLabel" />
<!DOCTYPE html>
<html lang="${pageContext.response.locale}">
<ui:head titleCode="profile.pageTitle" pageScript="account-edit" />
<body>
<ui:site-header />
<main class="page-shell">
    <ui:h1 text="${heading}" />
    <c:if test="${profileUpdated}">
        <p class="notice"><spring:message code="profile.updated" /></p>
    </c:if>
    <section class="surface profile-account" id="account">
        <h2><spring:message code="profile.account.heading" /></h2>
        <div class="account-rows">
            <%-- details como grid: el summary (etiqueta, valor y lapiz) y el formulario
                 comparten la fila. Abierta, el valor y el lapiz se ocultan y el formulario
                 ocupa la columna del valor. --%>
            <details class="account-row" <c:if test="${profileEditOpen}">open</c:if>>
                <summary class="account-row__summary">
                    <span class="account-row__label"><c:out value="${usernameLabel}" /></span>
                    <span class="account-row__value"><c:out value="${profileUser.username}" /></span>
                    <span class="account-row__edit" role="img" aria-label="<c:out value="${usernameEditLabel}" />"><ui:icon name="pencil"/></span>
                </summary>
                <form:form cssClass="account-row__form" action="${profileUrl}" method="post" modelAttribute="profileForm">
                    <ui:text-input path="username" label="${usernameLabel}" maxLength="100" hideLabel="${true}" placeholder="${usernameLabel}" autofocus="${profileEditOpen}" />
                    <div class="account-row__actions">
                        <ui:button label="${saveLabel}" type="submit" />
                        <ui:button label="${cancelLabel}" variant="ghost" url="${cancelUrl}#account" data="cancel-edit" />
                    </div>
                    <%-- La pagina del listado viaja con el POST: un error de validacion vuelve a la
                         misma. Va al final para no ser el primer input de la fila: el foco al abrir
                         busca el primer campo visible. --%>
                    <input type="hidden" name="page" value="<c:out value="${postPage.pageNumber}" />" />
                </form:form>
            </details>
            <div class="account-row account-row--static">
                <div class="account-row__summary">
                    <span class="account-row__label"><spring:message code="profile.email.label" /></span>
                    <span class="account-row__value"><c:out value="${profileUser.email}" /></span>
                </div>
            </div>
            <details class="account-row" <c:if test="${passwordEditOpen}">open</c:if>>
                <summary class="account-row__summary">
                    <span class="account-row__label"><c:out value="${passwordLabel}" /></span>
                    <span class="account-row__value" aria-hidden="true"><c:out value="${passwordMasked}" /></span>
                    <span class="account-row__edit" role="img" aria-label="<c:out value="${passwordEditLabel}" />"><ui:icon name="pencil"/></span>
                </summary>
                <form:form cssClass="account-row__form" action="${profilePasswordUrl}#account" method="post" modelAttribute="changePasswordForm">
                    <ui:text-input path="currentPassword" label="${currentPasswordLabel}" type="password" maxLength="72" hideLabel="${true}" placeholder="${currentPasswordLabel}" autofocus="${passwordEditOpen}" />
                    <ui:text-input path="password" label="${newPasswordLabel}" type="password" maxLength="72" hideLabel="${true}" placeholder="${newPasswordLabel}" describedBy="password-hint" />
                    <ui:text-input path="passwordConfirmation" label="${passwordConfirmationLabel}" type="password" maxLength="72" hideLabel="${true}" placeholder="${passwordConfirmationLabel}" />
                    <div class="account-row__actions">
                        <ui:button label="${saveLabel}" type="submit" />
                        <ui:button label="${cancelLabel}" variant="ghost" url="${cancelUrl}#account" data="cancel-edit" />
                    </div>
                    <p class="hint account-row__hint" id="password-hint"><c:out value="${passwordHint}" /></p>
                    <input type="hidden" name="page" value="<c:out value="${postPage.pageNumber}" />" />
                </form:form>
            </details>
        </div>
        <div class="profile-account__footer">
            <form action="${logoutUrl}" method="post">
                <sec:csrfInput />
                <ui:button label="${logoutLabel}" variant="danger-outline" size="sm" type="submit" icon="log-out" />
            </form>
        </div>
    </section>

    <section class="profile-posts" id="posts">
        <h2><spring:message code="profile.posts.heading" /></h2>
        <c:if test="${postDeleted}">
            <p class="notice"><spring:message code="post.deleted" /></p>
        </c:if>
        <c:choose>
            <c:when test="${empty postPage.posts}">
                <p class="empty-state"><spring:message code="profile.posts.empty" /></p>
            </c:when>
            <c:otherwise>
                <ul class="post-grid profile-posts__grid">
                    <c:forEach items="${postPage.posts}" var="post">
                        <li>
                            <ui:vinyl-card item="${post}" variant="editorial" href="/post/${post.id}" showStatus="${true}"/>
                        </li>
                    </c:forEach>
                </ul>
                <ui:pagination currentPage="${postPage.pageNumber}"
                               hasPrevious="${postPage.hasPrevious}"
                               hasNext="${postPage.hasNext}"
                               totalPages="${postPage.totalKnown ? postPage.totalPages : null}"
                               baseUrl="/profile"
                               fragment="posts"
                               ariaLabel="${paginationLabel}"/>
            </c:otherwise>
        </c:choose>
    </section>
</main>
</body>
</html>
```

## publish/index.jsp

[webapp/src/main/webapp/WEB-INF/views/publish/index.jsp, lines 1–116](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/publish/index.jsp>)

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="form" uri="http://www.springframework.org/tags/form" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<c:url value="${formAction}" var="publishUrl"/>
<c:url value="/js/publish-preview.js" var="previewScriptUrl"/>
<c:url value="/artists/suggestions" var="artistSuggestionsUrl"/>
<c:set var="headingCode" value="${editing ? 'publish.edit.heading' : 'publish.heading'}"/>
<c:set var="pageTitleCode" value="${editing ? 'publish.edit.pageTitle' : 'publish.pageTitle'}"/>
<c:set var="submitCode" value="${editing ? 'publish.edit.submit' : 'publish.submit'}"/>
<spring:message code="${headingCode}" var="heading"/>
<spring:message code="publish.title.label" var="titleLabel"/>
<spring:message code="publish.artistName.label" var="artistNameLabel"/>
<spring:message code="publish.releaseYear.label" var="releaseYearLabel"/>
<spring:message code="publish.genre.label" var="genreLabel"/>
<spring:message code="publish.genre.placeholder" var="genrePlaceholder"/>
<spring:message code="publish.price.label" var="priceLabel"/>
<spring:message code="publish.condition.label" var="conditionLabel"/>
<spring:message code="publish.zone.label" var="zoneLabel"/>
<spring:message code="publish.pressingYear.label" var="pressingYearLabel"/>
<spring:message code="publish.description.label" var="descriptionLabel"/>
<spring:message code="${submitCode}" var="submitLabel"/>
<spring:message code="publish.preview.heading" var="previewHeading"/>
<spring:message code="publish.preview.titlePlaceholder" var="previewTitle"/>
<spring:message code="publish.preview.artistPlaceholder" var="previewArtist"/>
<spring:message code="publish.preview.pricePlaceholder" var="previewPrice"/>
<spring:message code="form.cancel" var="cancelLabel"/>
<c:choose>
    <c:when test="${not empty existingCoverImageId}">
        <c:url value="/covers/${existingCoverImageId}" var="previewCoverUrl"/>
    </c:when>
    <c:otherwise>
        <c:url value="/images/covers/placeholder.svg" var="previewCoverUrl"/>
    </c:otherwise>
</c:choose>
<!DOCTYPE html>
<html lang="${pageContext.response.locale}">
<ui:head titleCode="${pageTitleCode}"/>
<body>
<ui:site-header/>
<main class="page-shell">
    <ui:h1 text="${heading}"/>
    <c:if test="${coverTooLarge}">
        <p class="error"><spring:message code="publish.cover.tooLarge"/></p>
    </c:if>
    <div class="publish-workspace">
        <form:form cssClass="surface form-stack publish-form" action="${publishUrl}" method="post"
                   modelAttribute="publishForm" enctype="multipart/form-data" data-submit-once="true"
                   data-publish-form="true">
            <form:errors cssClass="input-field__error" element="p"/>
            <div class="form-layout">
                <div class="form-layout__row form-layout__row--equal">
                    <ui:text-input path="title" label="${titleLabel}" maxLength="255"/>
                    <ui:text-input path="artistName" label="${artistNameLabel}" type="search" maxLength="255"
                           suggestionsId="artist-suggestions" sourceUrl="${artistSuggestionsUrl}">
                        <ul class="autocomplete__list" id="artist-suggestions" role="listbox" hidden></ul>
                    </ui:text-input>
                </div>
                <div class="form-layout__row form-layout__row--catalog">
                    <ui:text-input path="releaseYear" label="${releaseYearLabel}" type="number" min="1000" max="9999"/>
                    <ui:select path="genre" label="${genreLabel}" items="${genres}" messagePrefix="genre"
                               emptyLabel="${genrePlaceholder}" placeholderOnly="${true}"/>
                    <div>
                        <spring:bind path="condition">
                            <c:set var="conditionErrorId" value="condition-error" />
                            <ui:segmented-control name="condition" legend="${conditionLabel}" items="${conditions}"
                                                  messagePrefix="condition" selectedValue="${status.value}"
                                                  required="${true}" hasError="${status.error}"
                                                  errorId="${conditionErrorId}" />
                            <c:if test="${status.error}">
                                <div class="input-field__errors" id="${conditionErrorId}" role="alert">
                                    <c:forEach items="${status.errorMessages}" var="errorMessage">
                                        <p class="input-field__error"><c:out value="${errorMessage}" /></p>
                                    </c:forEach>
                                </div>
                            </c:if>
                        </spring:bind>
                    </div>
                </div>
                <div class="form-layout__row form-layout__row--commerce">
                    <ui:text-input path="price" label="${priceLabel}" type="number" min="1" max="99999999"/>
                    <ui:text-input path="zone" label="${zoneLabel}" maxLength="100"/>
                    <ui:text-input path="pressingYear" label="${pressingYearLabel}" type="number" min="1000" max="9999"/>
                </div>
                <div class="form-layout__row form-layout__row--content">
                    <ui:textarea path="description" label="${descriptionLabel}" maxLength="1000"/>
                    <div class="input-field">
                        <form:label path="cover" cssClass="input-field__label"><spring:message code="publish.cover.label"/></form:label>
                        <ui:input-control id="cover" name="cover" type="file" accept="image/png,image/jpeg,image/webp" />
                        <p class="hint"><spring:message code="publish.cover.hint"/></p>
                        <form:errors path="cover" cssClass="input-field__error" element="p"/>
                    </div>
                </div>
                <div class="form-stack__actions">
                    <ui:button label="${submitLabel}" type="submit"/>
                    <ui:button label="${cancelLabel}" variant="ghost" href="${cancelHref}"/>
                </div>
            </div>
        </form:form>
        <aside class="publish-preview" aria-labelledby="publish-preview-heading"
               data-price-placeholder="<c:out value="${previewPrice}"/>"
               data-price-locale="<c:out value="${pageContext.response.locale}"/>"
               data-price-currency="ARS">
            <h2 id="publish-preview-heading" class="text text-h3"><c:out value="${previewHeading}"/></h2>
            <ui:vinyl-card variant="editorial" preview="${true}"
                           title="${empty publishForm.title ? previewTitle : publishForm.title}"
                           artistName="${empty publishForm.artistName ? previewArtist : publishForm.artistName}"
                           price="${publishForm.price}"
                           coverUrl="${previewCoverUrl}" />
        </aside>
    </div>
</main>
<script src="<c:out value="${previewScriptUrl}"/>"></script>
</body>
</html>
```

## search/suggestions.jsp

[webapp/src/main/webapp/WEB-INF/views/search/suggestions.jsp, lines 1–20](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/search/suggestions.jsp>)

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<c:forEach items="${suggestions}" var="suggestion" varStatus="status">
    <spring:message code="search.suggestion.${suggestion.type}" var="typeLabel"/>
    <li class="autocomplete__option autocomplete__option--rich"
        id="site-search-suggestion-${status.index}"
        role="option"
        data-autocomplete-option
        data-value="<c:out value="${suggestion.value}"/>"
        aria-selected="false">
        <span class="autocomplete__option-main">
            <span class="autocomplete__option-value"><c:out value="${suggestion.value}"/></span>
            <c:if test="${suggestion.type eq 'ALBUM'}">
                <span class="autocomplete__option-detail"><c:out value="${suggestion.artistName}"/></span>
            </c:if>
        </span>
        <span class="autocomplete__option-type"><c:out value="${typeLabel}"/></span>
    </li>
</c:forEach>
```

## Submit prevention

Attaches to forms with data-submit-once, disables submit controls and sets aria-busy after the first submit. It prevents a repeated submit event and restores controls on pageshow. It is a browser convenience, not server-side idempotency.

[webapp/src/main/webapp/js/submit-once.js, lines 1–37](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/js/submit-once.js>)

```javascript
// Evita el doble envio: al submitear un form[data-submit-once] se deshabilitan
// sus botones de submit. Si el navegador restaura la pagina desde bfcache
// (volver atras), se vuelven a habilitar.
(function () {
    'use strict';

    function submitButtons(form) {
        return form.querySelectorAll('button[type="submit"], input[type="submit"]');
    }

    function setSubmitting(form, submitting) {
        form.classList.toggle('is-submitting', submitting);
        form.setAttribute('aria-busy', submitting ? 'true' : 'false');
        submitButtons(form).forEach(function (button) {
            button.disabled = submitting;
        });
    }

    document.addEventListener('DOMContentLoaded', function () {
        var forms = document.querySelectorAll('form[data-submit-once]');
        forms.forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (form.classList.contains('is-submitting')) {
                    event.preventDefault();
                    return;
                }
                setSubmitting(form, true);
            });
        });

        window.addEventListener('pageshow', function () {
            forms.forEach(function (form) {
                setSubmitting(form, false);
            });
        });
    });
})();
```

## Catalog enhancements

Submits the sort form as soon as its select changes, keeping the explicit button as the no-JavaScript fallback, and collapses the filter sidebar on screens up to 900px wide.

[webapp/src/main/webapp/js/catalog.js, lines 1–29](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/js/catalog.js>)

```javascript
// El orden del catalogo se submitea solo al cambiar el select: sin JS queda el
// boton "Ordenar" como fallback. En pantallas angostas los filtros arrancan
// plegados para no tapar los resultados.
(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        var forms = document.querySelectorAll('form[data-auto-submit]');
        forms.forEach(function (form) {
            form.classList.add('is-enhanced');
            form.querySelectorAll('select').forEach(function (select) {
                select.addEventListener('change', function () {
                    if (form.requestSubmit) {
                        form.requestSubmit();
                    } else {
                        form.submit();
                    }
                });
            });
        });

        if (window.matchMedia('(max-width: 900px)').matches) {
            var filters = document.querySelector('details.filters');
            if (filters) {
                filters.removeAttribute('open');
            }
        }
    });
})();
```

## Confirmation dialog

Intercepts, in the capture phase, submits of any form with data-confirm-message, shows ui:confirm-dialog with that message and resubmits only after confirmation. Running in capture keeps submit-once from disabling the button while the dialog is open. Focus returns to the triggering control.

[webapp/src/main/webapp/js/confirm-action.js, lines 1–63](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/js/confirm-action.js>)

```javascript
// La confirmacion corre en captura para que, mientras el dialogo esta abierto,
// submit-once no alcance a deshabilitar el boton del formulario. Sin JavaScript el
// POST conserva sus controles de estado y propiedad en el service.
(function () {
    'use strict';

    var dialog = document.getElementById('confirm-action-dialog');
    // El boton se busca por id y no por posicion: con un selector estructural, envolver o
    // reordenar los botones del dialogo hace que confirmar quede enganchado en el equivocado.
    var confirmButton = document.getElementById('confirm-action-dialog-confirm');
    if (!dialog || !confirmButton || typeof dialog.showModal !== 'function') {
        return;
    }

    var messageElement = document.getElementById('confirm-action-dialog-message');
    var pendingForm = null;
    var confirmedForm = null;
    var trigger = null;

    function restoreFocus() {
        if (trigger && typeof trigger.focus === 'function') {
            trigger.focus();
        }
        trigger = null;
    }

    document.addEventListener('submit', function (event) {
        var form = event.target;
        if (form === confirmedForm) {
            confirmedForm = null;
            return;
        }

        var message = form.getAttribute('data-confirm-message');
        if (!message) {
            return;
        }

        event.preventDefault();
        event.stopImmediatePropagation();
        pendingForm = form;
        trigger = document.activeElement;
        messageElement.textContent = message;
        dialog.showModal();
    }, true);

    confirmButton.addEventListener('click', function () {
        var form = pendingForm;
        dialog.close();
        if (!form) {
            return;
        }

        confirmedForm = form;
        form.requestSubmit();
    });

    dialog.addEventListener('close', function () {
        pendingForm = null;
        messageElement.textContent = '';
        restoreFocus();
    });
})();
```

## Autocomplete and select picker

Enhances each data-autocomplete wrapper into an ARIA combobox that fetches server-rendered option fragments with a 150 ms debounce, ignores stale responses and optionally submits on selection. It also replaces every select[data-select-picker] with a button-driven listbox picker while keeping the native select for submission. See [[Search suggestions flow]].

[webapp/src/main/webapp/js/autocomplete.js, lines 1–337](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/js/autocomplete.js>)

```javascript
(function () {
    'use strict';

    var ACTIVE_CLASS = 'autocomplete__option--active';
    var SEARCH_DELAY_MS = 150;

    function initialize(root) {
        var input = root.querySelector('[role="combobox"]');
        var list = root.querySelector('[role="listbox"]');
        var source = root.getAttribute('data-autocomplete-source');
        var submitOnSelect = root.getAttribute('data-autocomplete-submit') === 'true';

        if (!input || !list || !source) {
            return;
        }

        var visibleOptions = [];
        var activeIndex = -1;
        var requestSequence = 0;
        var searchTimer = null;

        function setActive(index) {
            if (activeIndex >= 0 && visibleOptions[activeIndex]) {
                visibleOptions[activeIndex].classList.remove(ACTIVE_CLASS);
                visibleOptions[activeIndex].setAttribute('aria-selected', 'false');
            }

            activeIndex = index;
            if (activeIndex >= 0 && visibleOptions[activeIndex]) {
                var activeOption = visibleOptions[activeIndex];
                activeOption.classList.add(ACTIVE_CLASS);
                activeOption.setAttribute('aria-selected', 'true');
                input.setAttribute('aria-activedescendant', activeOption.id);
            } else {
                input.removeAttribute('aria-activedescendant');
            }
        }

        function close() {
            setActive(-1);
            visibleOptions = [];
            list.hidden = true;
            input.setAttribute('aria-expanded', 'false');
        }

        function cancelSearch() {
            requestSequence += 1;
            window.clearTimeout(searchTimer);
            close();
        }

        function show(markup) {
            list.innerHTML = markup;
            visibleOptions = Array.prototype.slice.call(
                list.querySelectorAll('[data-autocomplete-option]')
            );
            if (visibleOptions.length === 0) {
                close();
                return;
            }
            list.hidden = false;
            input.setAttribute('aria-expanded', 'true');
        }

        function requestOptions(sequence, query) {
            var separator = source.indexOf('?') >= 0 ? '&' : '?';
            window.fetch(source + separator + 'q=' + encodeURIComponent(query), {
                headers: {'X-Requested-With': 'XMLHttpRequest'}
            }).then(function (response) {
                if (!response.ok) {
                    throw new Error('Could not load search suggestions');
                }
                return response.text();
            }).then(function (markup) {
                if (sequence === requestSequence) {
                    show(markup);
                }
            }).catch(function () {
                if (sequence === requestSequence) {
                    close();
                }
            });
        }

        function scheduleSearch() {
            var query = input.value.trim();
            requestSequence += 1;
            window.clearTimeout(searchTimer);
            if (!query) {
                close();
                return;
            }
            close();
            var sequence = requestSequence;
            searchTimer = window.setTimeout(function () {
                requestOptions(sequence, query);
            }, SEARCH_DELAY_MS);
        }

        function select(option) {
            input.value = option.getAttribute('data-value') || '';
            input.dispatchEvent(new Event('change', {bubbles: true}));
            cancelSearch();
            if (submitOnSelect && input.form) {
                if (typeof input.form.requestSubmit === 'function') {
                    input.form.requestSubmit();
                } else {
                    input.form.submit();
                }
                return;
            }
            input.focus();
        }

        input.addEventListener('input', scheduleSearch);
        input.addEventListener('search', scheduleSearch);
        input.addEventListener('keydown', function (event) {
            if (event.key === 'Escape') {
                cancelSearch();
                return;
            }

            if (event.key === 'Tab') {
                cancelSearch();
                return;
            }

            if (event.key === 'Enter' && activeIndex >= 0) {
                event.preventDefault();
                select(visibleOptions[activeIndex]);
                return;
            }

            if (event.key !== 'ArrowDown' && event.key !== 'ArrowUp') {
                return;
            }

            if (visibleOptions.length === 0) {
                return;
            }

            event.preventDefault();
            var direction = event.key === 'ArrowDown' ? 1 : -1;
            var nextIndex = activeIndex + direction;
            if (nextIndex < 0) {
                nextIndex = visibleOptions.length - 1;
            } else if (nextIndex >= visibleOptions.length) {
                nextIndex = 0;
            }
            setActive(nextIndex);
        });

        list.addEventListener('mousedown', function (event) {
            var option = event.target.closest('[data-autocomplete-option]');
            if (!option || option.hidden) {
                return;
            }
            event.preventDefault();
            select(option);
        });

        input.addEventListener('blur', function () {
            window.setTimeout(cancelSearch, 0);
        });
    }

    function initializeSelect(select, pickerIndex) {
        var parent = select.parentNode;
        var wrapper = document.createElement('div');
        var trigger = document.createElement('button');
        var list = document.createElement('ul');
        var optionElements = [];
        var activeIndex = -1;
        var listId = select.id + '-picker-options-' + pickerIndex;
        var triggerId = select.id + '-picker-trigger-' + pickerIndex;

        wrapper.className = 'select-picker';
        parent.insertBefore(wrapper, select);
        wrapper.appendChild(select);

        trigger.className = select.className + ' select-picker__trigger';
        trigger.id = triggerId;
        trigger.type = 'button';
        trigger.setAttribute('role', 'combobox');
        trigger.setAttribute('aria-autocomplete', 'none');
        trigger.setAttribute('aria-controls', listId);
        trigger.setAttribute('aria-expanded', 'false');
        trigger.setAttribute('aria-haspopup', 'listbox');
        ['aria-labelledby', 'aria-describedby', 'aria-invalid', 'aria-required'].forEach(function (attribute) {
            if (select.hasAttribute(attribute)) {
                trigger.setAttribute(attribute, select.getAttribute(attribute));
            }
        });
        if (select.hasAttribute('aria-labelledby')) {
            var labelId = select.getAttribute('aria-labelledby');
            var label = document.getElementById(labelId);
            if (label && label.tagName === 'LABEL') {
                label.htmlFor = triggerId;
            }
        }

        list.className = 'autocomplete__list';
        list.id = listId;
        list.setAttribute('role', 'listbox');
        list.hidden = true;

        Array.prototype.slice.call(select.options).forEach(function (option, optionIndex) {
            if (option.disabled || option.hidden) {
                return;
            }
            var item = document.createElement('li');
            item.className = 'autocomplete__option';
            item.id = listId + '-' + optionIndex;
            item.setAttribute('role', 'option');
            item.setAttribute('aria-selected', option.selected ? 'true' : 'false');
            item.setAttribute('data-option-index', String(optionIndex));
            item.textContent = option.textContent;
            list.appendChild(item);
            optionElements.push(item);
        });

        wrapper.appendChild(trigger);
        wrapper.appendChild(list);
        select.hidden = true;

        function selectedOptionPosition() {
            for (var index = 0; index < optionElements.length; index += 1) {
                if (Number(optionElements[index].getAttribute('data-option-index')) === select.selectedIndex) {
                    return index;
                }
            }
            return optionElements.length > 0 ? 0 : -1;
        }

        function updateTrigger() {
            var selected = select.options[select.selectedIndex];
            trigger.textContent = selected ? selected.textContent : '';
            optionElements.forEach(function (item) {
                var optionIndex = Number(item.getAttribute('data-option-index'));
                item.setAttribute('aria-selected', optionIndex === select.selectedIndex ? 'true' : 'false');
            });
        }

        function setActive(index) {
            if (activeIndex >= 0 && optionElements[activeIndex]) {
                optionElements[activeIndex].classList.remove(ACTIVE_CLASS);
            }
            activeIndex = index;
            if (activeIndex >= 0 && optionElements[activeIndex]) {
                var activeOption = optionElements[activeIndex];
                activeOption.classList.add(ACTIVE_CLASS);
                trigger.setAttribute('aria-activedescendant', activeOption.id);
                activeOption.scrollIntoView({block: 'nearest'});
            } else {
                trigger.removeAttribute('aria-activedescendant');
            }
        }

        function open() {
            list.hidden = false;
            trigger.setAttribute('aria-expanded', 'true');
            setActive(selectedOptionPosition());
        }

        function close() {
            list.hidden = true;
            trigger.setAttribute('aria-expanded', 'false');
            setActive(-1);
        }

        function choose(index) {
            select.selectedIndex = index;
            updateTrigger();
            close();
            select.dispatchEvent(new Event('change', {bubbles: true}));
            trigger.focus();
        }

        function move(direction) {
            if (list.hidden) {
                open();
                return;
            }
            var nextIndex = activeIndex + direction;
            if (nextIndex < 0) {
                nextIndex = optionElements.length - 1;
            } else if (nextIndex >= optionElements.length) {
                nextIndex = 0;
            }
            setActive(nextIndex);
        }

        trigger.addEventListener('click', function () {
            if (list.hidden) {
                open();
            } else {
                close();
            }
        });

        trigger.addEventListener('keydown', function (event) {
            if (event.key === 'Escape' || event.key === 'Tab') {
                close();
                return;
            }
            if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
                event.preventDefault();
                move(event.key === 'ArrowDown' ? 1 : -1);
                return;
            }
            if ((event.key === 'Enter' || event.key === ' ') && !list.hidden && activeIndex >= 0) {
                event.preventDefault();
                choose(Number(optionElements[activeIndex].getAttribute('data-option-index')));
            }
        });

        list.addEventListener('mousedown', function (event) {
            var option = event.target.closest('[data-option-index]');
            if (!option) {
                return;
            }
            event.preventDefault();
            choose(Number(option.getAttribute('data-option-index')));
        });

        trigger.addEventListener('blur', function () {
            window.setTimeout(close, 0);
        });

        updateTrigger();
    }

    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('[data-autocomplete]').forEach(initialize);
        document.querySelectorAll('select[data-select-picker]').forEach(initializeSelect);
    });
}());
```

## Profile row editing

Loaded only by the profile page through ui:head pageScript. Focuses the first field when an account row opens and makes Cancel reset and close the row without reloading.

[webapp/src/main/webapp/js/account-edit.js, lines 1–50](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/js/account-edit.js>)

```javascript
// Filas de edicion del perfil. Al abrir una fila el foco va al primer campo con el cursor
// al final; Cancelar resetea el formulario y cierra la fila sin recargar. Sin JavaScript,
// Cancelar es un enlace al perfil y el foco lo pone el autofocus que el servidor deja cuando
// reabre por error.
(function () {
    'use strict';

    function focusFirstField(row) {
        var field = row.querySelector('input:not([type="hidden"])');
        if (!field) {
            return;
        }
        field.focus();
        if (typeof field.setSelectionRange === 'function' && field.type !== 'number') {
            var end = field.value.length;
            field.setSelectionRange(end, end);
        }
    }

    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('details.account-row').forEach(function (row) {
            row.addEventListener('toggle', function () {
                if (row.open) {
                    focusFirstField(row);
                }
            });
        });
    });

    document.addEventListener('click', function (event) {
        var cancel = event.target.closest('[data-cancel-edit]');
        if (!cancel) {
            return;
        }
        var row = cancel.closest('details.account-row');
        if (!row) {
            return;
        }
        event.preventDefault();
        var form = row.querySelector('form');
        if (form) {
            form.reset();
        }
        row.removeAttribute('open');
        var summary = row.querySelector('summary');
        if (summary) {
            summary.focus();
        }
    });
})();
```

## Publish preview

Mirrors title, artist, formatted ARS price and a locally selected cover into the preview card. It uses object URLs that are revoked on change and pagehide; nothing is uploaded before submit.

[webapp/src/main/webapp/js/publish-preview.js, lines 1–88](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/js/publish-preview.js>)

```javascript
(function () {
    'use strict';

    function textTarget(root, fieldName) {
        return root.querySelector('[data-preview-value="' + fieldName + '"]');
    }

    function replaceText(target, value, fallback) {
        if (!target) {
            return;
        }
        var text = value && value.trim() ? value.trim() : fallback;
        var nestedText = target.querySelector('.text');
        (nestedText || target).textContent = text;
    }

    function initialize(form) {
        var workspace = form.closest('.publish-workspace');
        var preview = workspace && workspace.querySelector('.publish-preview');
        if (!preview) {
            return;
        }

        var titleInput = form.elements.title;
        var artistInput = form.elements.artistName;
        var priceInput = form.elements.price;
        var coverInput = form.elements.cover;
        var titleTarget = textTarget(preview, 'title');
        var artistTarget = textTarget(preview, 'artistName');
        var priceTarget = textTarget(preview, 'price');
        var coverTarget = preview.querySelector('[data-preview-cover]');
        var titleFallback = titleTarget ? titleTarget.textContent.trim() : '';
        var artistFallback = artistTarget ? artistTarget.textContent.trim() : '';
        var pricePlaceholder = preview.getAttribute('data-price-placeholder') || '';
        var priceLocale = (preview.getAttribute('data-price-locale') || document.documentElement.lang).replace(/_/g, '-');
        var priceCurrency = preview.getAttribute('data-price-currency');
        var priceFormatter = new Intl.NumberFormat(priceLocale, {
            style: 'currency',
            currency: priceCurrency,
            currencyDisplay: 'narrowSymbol',
            maximumFractionDigits: 0
        });
        var coverObjectUrl = null;
        var originalCoverUrl = coverTarget ? coverTarget.src : '';

        function updateText() {
            replaceText(titleTarget, titleInput.value, titleFallback);
            replaceText(artistTarget, artistInput.value, artistFallback);

            var price = Number(priceInput.value);
            priceTarget.textContent = Number.isFinite(price) && price > 0
                ? priceFormatter.format(price)
                : pricePlaceholder;
        }

        function updateCover() {
            if (!coverTarget || !coverInput.files) {
                return;
            }
            if (coverObjectUrl) {
                window.URL.revokeObjectURL(coverObjectUrl);
                coverObjectUrl = null;
            }
            if (coverInput.files.length === 0) {
                coverTarget.src = originalCoverUrl;
                return;
            }
            coverObjectUrl = window.URL.createObjectURL(coverInput.files[0]);
            coverTarget.src = coverObjectUrl;
        }

        [titleInput, artistInput, priceInput].forEach(function (input) {
            input.addEventListener('input', updateText);
            input.addEventListener('change', updateText);
        });
        coverInput.addEventListener('change', updateCover);
        window.addEventListener('pagehide', function () {
            if (coverObjectUrl) {
                window.URL.revokeObjectURL(coverObjectUrl);
            }
        });
        updateText();
    }

    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('[data-publish-form]').forEach(initialize);
    });
}());
```

## Placeholder

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

## Logo

The disc mark used by ui:brand and as the SVG favicon.

[webapp/src/main/webapp/images/logo.svg, lines 1–29](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/images/logo.svg>)

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
    <!-- Isotipo de quieroVinilos: un vinilo con el label en el color de acento. Es el favicon
         y el disco de la marca. Un SVG cargado como imagen no ve los tokens de la app, asi que
         los colores repiten los de tokens.css (el color del vinilo y el acento de cada tema). -->
    <style>
        .disc, .hole { fill: #17151c; }
        .groove { fill: none; stroke: #36313f; stroke-width: 1.6; }
        .rim { fill: none; stroke: #4a4456; stroke-width: 1.5; }
        .label { fill: #be3a21; }
        @media (prefers-color-scheme: dark) {
            .label { fill: #e4573d; }
        }
    </style>
    <defs>
        <linearGradient id="sheen" x1="0" y1="0.15" x2="1" y2="0.85">
            <stop offset="0.32" stop-color="#fff" stop-opacity="0"/>
            <stop offset="0.47" stop-color="#fff" stop-opacity="0.14"/>
            <stop offset="0.6" stop-color="#fff" stop-opacity="0"/>
        </linearGradient>
    </defs>
    <circle class="disc" cx="50" cy="50" r="48"/>
    <circle class="groove" cx="50" cy="50" r="25.68"/>
    <circle class="groove" cx="50" cy="50" r="33.12"/>
    <circle class="groove" cx="50" cy="50" r="40.56"/>
    <circle cx="50" cy="50" r="48" fill="url(#sheen)"/>
    <circle class="rim" cx="50" cy="50" r="47.25"/>
    <circle class="label" cx="50" cy="50" r="18.24"/>
    <circle class="hole" cx="50" cy="50" r="3.2"/>
</svg>
```

[[UI components]] · [[Landing flow]] · [[Post detail flow]] · [[Inquiry and sale flow]] · [[Profile flow]]
