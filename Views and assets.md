---
title: "Views and assets"
categories: ["Web"]
type: "guide"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["webapp/src/main/webapp/WEB-INF/views/admin/index.jsp", "webapp/src/main/webapp/WEB-INF/views/auth/login.jsp", "webapp/src/main/webapp/WEB-INF/views/auth/register.jsp", "webapp/src/main/webapp/WEB-INF/views/auth/verify.jsp", "webapp/src/main/webapp/WEB-INF/views/error/400.jsp", "webapp/src/main/webapp/WEB-INF/views/error/403.jsp", "webapp/src/main/webapp/WEB-INF/views/error/404.jsp", "webapp/src/main/webapp/WEB-INF/views/error/409.jsp", "webapp/src/main/webapp/WEB-INF/views/inquiry/index.jsp", "webapp/src/main/webapp/WEB-INF/views/landing/index.jsp", "webapp/src/main/webapp/WEB-INF/views/post/contact.jsp", "webapp/src/main/webapp/WEB-INF/views/publish/index.jsp", "webapp/src/main/webapp/js/submit-once.js", "webapp/src/main/webapp/images/covers/placeholder.svg"]
---

# Views and assets

The current source has 12 JSP views, eleven shared tags and one JavaScript asset. Product/auth/inquiry/error pages use ui:head and shared styles. The old helloworld views remain removed.

| View | Model and behavior |
|---|---|
| landing/index | Results, parsed filters/options, query, sort and contactSent; GET search form and linked cards |
| publish/index | publishForm, enum options, BindingResult and coverTooLarge; multipart POST with data-submit-once |
| post/contact | PostSummary, optional-message contactForm and errors; authenticated identity and data-submit-once |
| inquiry/index | sentInquiries/receivedInquiries, action flashes; owner accept/reject forms with CSRF |
| auth/login | loginForm; query flags for error/logout/verificationSent/verified |
| auth/register | Email-only registerForm |
| auth/verify | Token, username/password/confirmation, validation errors; escaped hidden token |
| admin/index | Informational page and navigation |
| error/400,403,404,409 | Localized status pages and navigation |

submit-once.js attaches to forms with data-submit-once, disables submit controls and sets aria-busy after the first submit. It prevents a repeated submit event and restores controls on pageshow. It is a browser convenience, not server-side idempotency. The inbox action forms do not opt into this attribute.

Static cover fallback is the SVG placeholder; real image IDs use ImageController. No frontend package manager or build pipeline is present.

## admin/index.jsp

[webapp/src/main/webapp/WEB-INF/views/admin/index.jsp, lines 1–17](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/admin/index.jsp>)

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<spring:message code="auth.admin.heading" var="heading"/>
<!DOCTYPE html>
<html lang="${pageContext.response.locale}">
<ui:head titleCode="auth.admin.pageTitle"/>
<body>
<main class="page-shell">
    <header class="page-header">
        <ui:h1 text="${heading}"/>
        <ui:account-nav/>
    </header>
    <p class="surface"><spring:message code="auth.admin.message"/></p>
</main>
</body>
</html>
```

## auth/login.jsp

[webapp/src/main/webapp/WEB-INF/views/auth/login.jsp, lines 1–43](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/auth/login.jsp>)

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="form" uri="http://www.springframework.org/tags/form" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<c:url value="/login" var="loginUrl"/>
<spring:message code="auth.login.heading" var="heading"/>
<spring:message code="auth.email.label" var="emailLabel"/>
<spring:message code="auth.password.label" var="passwordLabel"/>
<spring:message code="auth.login.submit" var="submitLabel"/>
<spring:message code="auth.register.action" var="registerLabel"/>
<!DOCTYPE html>
<html lang="${pageContext.response.locale}">
<ui:head titleCode="auth.login.pageTitle"/>
<body>
<main class="page-shell auth-shell">
    <header class="page-header">
        <ui:h1 text="${heading}"/>
        <ui:account-nav/>
    </header>
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
    <form:form cssClass="surface form-stack" action="${loginUrl}" method="post" modelAttribute="loginForm">
        <ui:text-input path="email" label="${emailLabel}" type="email" maxLength="100"/>
        <ui:text-input path="password" label="${passwordLabel}" type="password" maxLength="72"/>
        <div class="form-stack__actions">
            <ui:button label="${submitLabel}" type="submit"/>
            <ui:button label="${registerLabel}" variant="ghost" href="/register"/>
        </div>
    </form:form>
</main>
</body>
</html>
```

## auth/register.jsp

[webapp/src/main/webapp/WEB-INF/views/auth/register.jsp, lines 1–31](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/auth/register.jsp>)

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="form" uri="http://www.springframework.org/tags/form" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<c:url value="/register" var="registerUrl"/>
<spring:message code="auth.register.heading" var="heading"/>
<spring:message code="auth.email.label" var="emailLabel"/>
<spring:message code="auth.register.submit" var="submitLabel"/>
<spring:message code="auth.login.action" var="loginLabel"/>
<!DOCTYPE html>
<html lang="${pageContext.response.locale}">
<ui:head titleCode="auth.register.pageTitle"/>
<body>
<main class="page-shell auth-shell">
    <header class="page-header">
        <ui:h1 text="${heading}"/>
        <ui:account-nav/>
    </header>
    <form:form cssClass="surface form-stack" action="${registerUrl}" method="post" modelAttribute="registerForm">
        <form:errors path="*" cssClass="input-field__error" element="p"/>
        <ui:text-input path="email" label="${emailLabel}" type="email" maxLength="100"/>
        <p class="hint"><spring:message code="auth.register.verification.hint"/></p>
        <div class="form-stack__actions">
            <ui:button label="${submitLabel}" type="submit"/>
            <ui:button label="${loginLabel}" variant="ghost" href="/login"/>
        </div>
    </form:form>
</main>
</body>
</html>
```

## auth/verify.jsp

[webapp/src/main/webapp/WEB-INF/views/auth/verify.jsp, lines 1–43](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/auth/verify.jsp>)

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="form" uri="http://www.springframework.org/tags/form" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<c:url value="/verify" var="verifyUrl"/>
<spring:message code="auth.verify.heading" var="heading"/>
<spring:message code="auth.password.label" var="passwordLabel"/>
<spring:message code="auth.username.label" var="usernameLabel"/>
<spring:message code="auth.passwordConfirmation.label" var="passwordConfirmationLabel"/>
<spring:message code="auth.verify.submit" var="submitLabel"/>
<spring:message code="auth.login.action" var="loginLabel"/>
<!DOCTYPE html>
<html lang="${pageContext.response.locale}">
<ui:head titleCode="auth.verify.pageTitle"/>
<body>
<main class="page-shell auth-shell">
    <header class="page-header">
        <ui:h1 text="${heading}"/>
        <ui:account-nav/>
    </header>
    <p class="hint"><spring:message code="auth.verify.hint"/></p>
    <form:form cssClass="surface form-stack" action="${verifyUrl}" method="post" modelAttribute="verifyEmailForm">
        <form:errors path="*" cssClass="input-field__error" element="p"/>
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
        <p class="hint"><spring:message code="auth.register.password.hint"/></p>
        <div class="form-stack__actions">
            <ui:button label="${submitLabel}" type="submit"/>
            <ui:button label="${loginLabel}" variant="ghost" href="/login"/>
        </div>
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
<spring:message code="error.badRequest.back" var="backLabel"/>
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
<spring:message code="error.forbidden.back" var="backLabel"/>
<!DOCTYPE html>
<html lang="${pageContext.response.locale}">
<ui:head titleCode="error.forbidden.pageTitle"/>
<body>
<main class="page-shell error-page">
    <p class="error-page__code"><spring:message code="error.forbidden.code"/></p>
    <ui:h1 text="${heading}"/>
    <ui:p text="${message}"/>
    <ui:button label="${backLabel}" href="/"/>
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
<spring:message code="error.notFound.back" var="backLabel"/>
<spring:message code="error.notFound.publish" var="publishLabel"/>
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
<spring:message code="error.conflict.back" var="backLabel"/>
<!DOCTYPE html>
<html lang="${pageContext.response.locale}">
<ui:head titleCode="error.conflict.pageTitle"/>
<body>
<main class="page-shell error-page">
    <p class="error-page__code"><spring:message code="error.conflict.code"/></p>
    <ui:h1 text="${heading}"/>
    <ui:p text="${message}"/>
    <ui:button label="${backLabel}" href="/"/>
</main>
</body>
</html>
```

## inquiry/index.jsp

[webapp/src/main/webapp/WEB-INF/views/inquiry/index.jsp, lines 1–94](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/inquiry/index.jsp>)

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="sec" uri="http://www.springframework.org/security/tags" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<spring:message code="inquiry.heading" var="heading"/>
<spring:message code="inquiry.accept" var="acceptLabel"/>
<spring:message code="inquiry.reject" var="rejectLabel"/>
<!DOCTYPE html>
<html lang="${pageContext.response.locale}">
<ui:head titleCode="inquiry.pageTitle"/>
<body>
<main class="page-shell">
    <header class="page-header">
        <ui:h1 text="${heading}"/>
        <ui:account-nav/>
    </header>
    <c:if test="${inquiryAccepted}"><p class="notice"><spring:message code="inquiry.accepted"/></p></c:if>
    <c:if test="${inquiryRejected}"><p class="notice"><spring:message code="inquiry.rejected"/></p></c:if>

    <section class="inquiry-section">
        <h2><spring:message code="inquiry.received.heading"/></h2>
        <c:choose>
            <c:when test="${empty receivedInquiries}">
                <p class="empty-state"><spring:message code="inquiry.received.empty"/></p>
            </c:when>
            <c:otherwise>
                <ul class="inquiry-list">
                    <c:forEach items="${receivedInquiries}" var="inquiry">
                        <li class="surface inquiry-card">
                            <spring:message code="inquiry.item.title" var="itemTitle">
                                <spring:argument value="${inquiry.title}"/>
                                <spring:argument value="${inquiry.artistName}"/>
                            </spring:message>
                            <spring:message code="inquiry.from" var="buyerText">
                                <spring:argument value="${inquiry.buyerUsername}"/>
                            </spring:message>
                            <spring:message code="inquiry.status.${inquiry.status}" var="statusLabel"/>
                            <ui:h3 text="${itemTitle}"/>
                            <ui:p text="${buyerText}"/>
                            <c:if test="${not empty inquiry.message}"><ui:p text="${inquiry.message}"/></c:if>
                            <ui:p text="${statusLabel}" variant="muted"/>
                            <c:if test="${inquiry.pending and inquiry.postAvailable}">
                                <div class="form-stack__actions">
                                    <c:url value="/inquiries/${inquiry.id}/accept" var="acceptUrl"/>
                                    <form action="${acceptUrl}" method="post">
                                        <sec:csrfInput/>
                                        <ui:button label="${acceptLabel}" type="submit"/>
                                    </form>
                                    <c:url value="/inquiries/${inquiry.id}/reject" var="rejectUrl"/>
                                    <form action="${rejectUrl}" method="post">
                                        <sec:csrfInput/>
                                        <ui:button label="${rejectLabel}" variant="ghost" type="submit"/>
                                    </form>
                                </div>
                            </c:if>
                        </li>
                    </c:forEach>
                </ul>
            </c:otherwise>
        </c:choose>
    </section>

    <section class="inquiry-section">
        <h2><spring:message code="inquiry.sent.heading"/></h2>
        <c:choose>
            <c:when test="${empty sentInquiries}">
                <p class="empty-state"><spring:message code="inquiry.sent.empty"/></p>
            </c:when>
            <c:otherwise>
                <ul class="inquiry-list">
                    <c:forEach items="${sentInquiries}" var="inquiry">
                        <li class="surface inquiry-card">
                            <spring:message code="inquiry.item.title" var="itemTitle">
                                <spring:argument value="${inquiry.title}"/>
                                <spring:argument value="${inquiry.artistName}"/>
                            </spring:message>
                            <spring:message code="inquiry.to" var="sellerText">
                                <spring:argument value="${inquiry.sellerUsername}"/>
                            </spring:message>
                            <spring:message code="inquiry.status.${inquiry.status}" var="statusLabel"/>
                            <ui:h3 text="${itemTitle}"/>
                            <ui:p text="${sellerText}"/>
                            <c:if test="${not empty inquiry.message}"><ui:p text="${inquiry.message}"/></c:if>
                            <ui:p text="${statusLabel}" variant="muted"/>
                        </li>
                    </c:forEach>
                </ul>
            </c:otherwise>
        </c:choose>
    </section>
</main>
</body>
</html>
```

## landing/index.jsp

[webapp/src/main/webapp/WEB-INF/views/landing/index.jsp, lines 1–135](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/landing/index.jsp>)

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<spring:message code="landing.heading" var="heading"/>
<spring:message code="landing.publish" var="publishLabel"/>
<spring:message code="post.contact.action" var="contactLabel"/>
<spring:message code="landing.search.label" var="searchLabel"/>
<spring:message code="landing.search.placeholder" var="searchPlaceholder"/>
<spring:message code="landing.search.submit" var="searchSubmitLabel"/>
<spring:message code="landing.search.clear" var="searchClearLabel"/>
<spring:message code="landing.sort.label" var="sortLabel"/>
<spring:message code="landing.filter.genre" var="genreLabel"/>
<spring:message code="landing.filter.condition" var="conditionLabel"/>
<spring:message code="landing.filter.artist" var="artistLabel"/>
<spring:message code="landing.filter.year" var="yearLabel"/>
<spring:message code="landing.filter.minPrice" var="minPriceLabel"/>
<spring:message code="landing.filter.maxPrice" var="maxPriceLabel"/>
<spring:message code="landing.filter.any" var="anyLabel"/>
<c:url value="/" var="searchUrl"/>
<c:choose>
    <c:when test="${sort eq 'NEWEST'}"><c:set var="clearHref" value="/"/></c:when>
    <c:otherwise><c:set var="clearHref" value="/?sort=${sort}"/></c:otherwise>
</c:choose>
<%-- El orden siempre tiene valor, asi que no cuenta como filtro: solo decide como se
     ordena lo que se ve. "Ver todos" y el estado vacio miran los demas controles. --%>
<c:set var="hasFilters" value="${not empty query or not empty selectedGenre
        or not empty selectedCondition or not empty selectedArtistId
        or not empty selectedYear or not empty minPrice or not empty maxPrice}"/>
<!DOCTYPE html>
<html lang="${pageContext.response.locale}">
<ui:head titleCode="landing.pageTitle"/>
<body>
<main class="page-shell">
    <header class="page-header">
        <ui:h1 text="${heading}" tone="accent"/>
        <div class="page-header__actions">
            <ui:button label="${publishLabel}" variant="primary" href="/publish"/>
            <ui:account-nav/>
        </div>
    </header>
    <c:if test="${contactSent}">
        <p class="notice"><spring:message code="landing.contact.sent"/></p>
    </c:if>
    <form class="search-bar" action="${searchUrl}" method="get" role="search">
        <input class="input-field__control search-bar__control" id="q" name="q" type="search"
               aria-label="<c:out value="${searchLabel}"/>"
               value="<c:out value="${query}"/>" placeholder="<c:out value="${searchPlaceholder}"/>"
               maxlength="255" autocomplete="off"/>
        <div class="filter-grid">
            <label class="filter-field" for="genre"><c:out value="${genreLabel}"/>
                <select class="input-field__control" id="genre" name="genre">
                    <option value=""><c:out value="${anyLabel}"/></option>
                    <c:forEach items="${genres}" var="option">
                        <spring:message code="genre.${option}" var="optionLabel"/>
                        <option value="<c:out value="${option}"/>" <c:if test="${selectedGenre eq option}">selected</c:if>><c:out value="${optionLabel}"/></option>
                    </c:forEach>
                </select>
            </label>
            <label class="filter-field" for="condition"><c:out value="${conditionLabel}"/>
                <select class="input-field__control" id="condition" name="condition">
                    <option value=""><c:out value="${anyLabel}"/></option>
                    <c:forEach items="${conditions}" var="option">
                        <spring:message code="condition.${option}" var="optionLabel"/>
                        <option value="<c:out value="${option}"/>" <c:if test="${selectedCondition eq option}">selected</c:if>><c:out value="${optionLabel}"/></option>
                    </c:forEach>
                </select>
            </label>
            <label class="filter-field" for="artistId"><c:out value="${artistLabel}"/>
                <select class="input-field__control artist-name" id="artistId" name="artistId">
                    <option value=""><c:out value="${anyLabel}"/></option>
                    <c:forEach items="${artists}" var="artist">
                        <option value="<c:out value="${artist.id}"/>" <c:if test="${selectedArtistId eq artist.id}">selected</c:if>><c:out value="${artist.name}"/></option>
                    </c:forEach>
                </select>
            </label>
            <label class="filter-field" for="year"><c:out value="${yearLabel}"/>
                <input class="input-field__control" id="year" name="year" type="number" value="<c:out value="${selectedYear}"/>"/>
            </label>
            <label class="filter-field" for="minPrice"><c:out value="${minPriceLabel}"/>
                <input class="input-field__control" id="minPrice" name="minPrice" type="number" value="<c:out value="${minPrice}"/>"/>
            </label>
            <label class="filter-field" for="maxPrice"><c:out value="${maxPriceLabel}"/>
                <input class="input-field__control" id="maxPrice" name="maxPrice" type="number" value="<c:out value="${maxPrice}"/>"/>
            </label>
            <label class="filter-field" for="sort"><c:out value="${sortLabel}"/>
                <select class="input-field__control" id="sort" name="sort">
                    <c:forEach items="${sorts}" var="option">
                        <spring:message code="landing.sort.${option}" var="optionLabel"/>
                        <option value="<c:out value="${option}"/>" <c:if test="${sort eq option}">selected</c:if>><c:out value="${optionLabel}"/></option>
                    </c:forEach>
                </select>
            </label>
        </div>
        <ui:button label="${searchSubmitLabel}" type="submit"/>
        <c:if test="${hasFilters}">
            <ui:button label="${searchClearLabel}" variant="ghost" href="${clearHref}"/>
        </c:if>
    </form>
    <c:if test="${not empty query and not empty posts}">
        <p class="search-bar__summary">
            <spring:message code="landing.search.results" htmlEscape="true">
                <spring:argument value="${query}"/>
            </spring:message>
        </p>
    </c:if>
    <c:choose>
        <c:when test="${empty posts and not empty query}">
            <p class="empty-state">
                <spring:message code="landing.search.empty" htmlEscape="true">
                    <spring:argument value="${query}"/>
                </spring:message>
            </p>
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
                        <ui:vinyl-card item="${post}" variant="editorial" href="/post/${post.id}/contact">
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
<spring:message code="post.contact.back" var="backLabel"/>
<!DOCTYPE html>
<html lang="${pageContext.response.locale}">
<ui:head titleCode="post.contact.pageTitle"/>
<body>
<main class="page-shell">
    <header class="page-header">
        <ui:h1 text="${heading}"/>
        <ui:account-nav/>
    </header>
    <ui:vinyl-card item="${post}" variant="compact"/>
    <form:form cssClass="surface form-stack" action="${contactUrl}" method="post" modelAttribute="contactForm" data-submit-once="true">
        <p><spring:message code="post.contact.identity"/></p>
        <ui:textarea path="contactMessage" label="${messageLabel}" maxLength="500"/>
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

[webapp/src/main/webapp/WEB-INF/views/publish/index.jsp, lines 1–57](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/publish/index.jsp>)

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="form" uri="http://www.springframework.org/tags/form" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<c:url value="/publish" var="publishUrl"/>
<spring:message code="publish.heading" var="heading"/>
<spring:message code="publish.title.label" var="titleLabel"/>
<spring:message code="publish.artistName.label" var="artistNameLabel"/>
<spring:message code="publish.releaseYear.label" var="releaseYearLabel"/>
<spring:message code="publish.genre.label" var="genreLabel"/>
<spring:message code="publish.genre.empty" var="genreEmptyLabel"/>
<spring:message code="publish.price.label" var="priceLabel"/>
<spring:message code="publish.condition.label" var="conditionLabel"/>
<spring:message code="publish.condition.empty" var="conditionEmptyLabel"/>
<spring:message code="publish.zone.label" var="zoneLabel"/>
<spring:message code="publish.pressingYear.label" var="pressingYearLabel"/>
<spring:message code="publish.description.label" var="descriptionLabel"/>
<spring:message code="publish.submit" var="submitLabel"/>
<spring:message code="publish.back" var="backLabel"/>
<!DOCTYPE html>
<html lang="${pageContext.response.locale}">
<ui:head titleCode="publish.pageTitle"/>
<body>
<main class="page-shell">
    <header class="page-header">
        <ui:h1 text="${heading}"/>
        <ui:account-nav/>
    </header>
    <c:if test="${coverTooLarge}">
        <p class="error"><spring:message code="publish.cover.tooLarge"/></p>
    </c:if>
    <form:form cssClass="surface form-stack" action="${publishUrl}" method="post" modelAttribute="publishForm" enctype="multipart/form-data" data-submit-once="true">
        <form:errors cssClass="input-field__error" element="p"/>
        <ui:text-input path="title" label="${titleLabel}" maxLength="255"/>
        <ui:text-input path="artistName" label="${artistNameLabel}" maxLength="255"/>
        <ui:text-input path="releaseYear" label="${releaseYearLabel}" type="number" min="1000" max="9999"/>
        <ui:select path="genre" label="${genreLabel}" items="${genres}" messagePrefix="genre" emptyLabel="${genreEmptyLabel}"/>
        <ui:text-input path="price" label="${priceLabel}" type="number" min="1" max="99999999"/>
        <ui:select path="condition" label="${conditionLabel}" items="${conditions}" messagePrefix="condition" emptyLabel="${conditionEmptyLabel}"/>
        <ui:text-input path="zone" label="${zoneLabel}" maxLength="100"/>
        <ui:text-input path="pressingYear" label="${pressingYearLabel}" type="number" min="1000" max="9999"/>
        <ui:textarea path="description" label="${descriptionLabel}" maxLength="1000"/>
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

## Submit prevention

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

[[UI components]] · [[Landing flow]] · [[Inquiry and sale flow]]
