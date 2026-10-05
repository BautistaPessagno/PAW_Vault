---
title: "Views and assets"
categories: ["Web"]
type: "guide"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["webapp/src/main/webapp/WEB-INF/views/auth/forgot-password.jsp", "webapp/src/main/webapp/WEB-INF/views/auth/login.jsp", "webapp/src/main/webapp/WEB-INF/views/auth/register.jsp", "webapp/src/main/webapp/WEB-INF/views/auth/reset-password.jsp", "webapp/src/main/webapp/WEB-INF/views/auth/verify-required.jsp", "webapp/src/main/webapp/WEB-INF/views/auth/verify.jsp", "webapp/src/main/webapp/WEB-INF/views/cart/index.jsp", "webapp/src/main/webapp/WEB-INF/views/error/400.jsp", "webapp/src/main/webapp/WEB-INF/views/error/403.jsp", "webapp/src/main/webapp/WEB-INF/views/error/404.jsp", "webapp/src/main/webapp/WEB-INF/views/error/409.jsp", "webapp/src/main/webapp/WEB-INF/views/inquiry/detail.jsp", "webapp/src/main/webapp/WEB-INF/views/inquiry/received.jsp", "webapp/src/main/webapp/WEB-INF/views/inquiry/sent.jsp", "webapp/src/main/webapp/WEB-INF/views/landing/index.jsp", "webapp/src/main/webapp/WEB-INF/views/post/contact.jsp", "webapp/src/main/webapp/WEB-INF/views/post/detail.jsp", "webapp/src/main/webapp/WEB-INF/views/profile/index.jsp", "webapp/src/main/webapp/WEB-INF/views/profile/public.jsp", "webapp/src/main/webapp/WEB-INF/views/publish/index.jsp", "webapp/src/main/webapp/js/account-edit.js", "webapp/src/main/webapp/js/autocomplete.js", "webapp/src/main/webapp/js/catalog.js", "webapp/src/main/webapp/js/confirm-action.js", "webapp/src/main/webapp/js/post-gallery.js", "webapp/src/main/webapp/js/publish-preview.js", "webapp/src/main/webapp/js/sale-detail.js", "webapp/src/main/webapp/js/submit-once.js", "webapp/src/main/webapp/images/covers/placeholder.svg", "webapp/src/main/webapp/images/logo.svg"]
---

# Views and assets

> [!summary] En una frase
> 20 vistas JSP, 8 scripts y 2 imágenes: las vistas solo componen componentes y muestran lo que el controller dejó en el modelo, y cada script mejora algo que ya funciona sin JavaScript.

Los componentes compartidos están en [[UI components]] y los estilos en [[UI styles and tokens]].

## Cómo llega una vista al navegador

1. El controller devuelve un `ModelAndView` con un nombre lógico, por ejemplo `post/detail`.
2. El `viewResolver` lo convierte en `/WEB-INF/views/post/detail.jsp`. Al estar bajo `WEB-INF`, la JSP no se puede pedir directamente por URL.
3. La JSP lee el modelo con EL (`${post.title}` llama a `getTitle()`), compone tags `ui:` y escribe HTML.
4. `head.tag` enlaza los tres CSS y los scripts comunes con `defer`.

## Vistas

| Vista | Qué muestra | Controller | Flujo | Líneas |
|---|---|---|---|---|
| `auth/forgot-password` | Pedido de recuperación | [[AuthenticationController]] | [[Password recovery flow]] | 34 |
| `auth/login` | Login: mirá los nombres de los campos y el token CSRF | [[AuthenticationController]] | [[Authentication flow]] | 56 |
| `auth/register` | Formulario de registro | [[AuthenticationController]] | [[Authentication flow]] | 46 |
| `auth/reset-password` | Nueva contraseña con el token en un campo oculto | [[AuthenticationController]] | [[Password recovery flow]] | 48 |
| `auth/verify-required` | Pantalla para la cuenta sin verificar | [[AuthenticationController]] | [[Authentication flow]] | 32 |
| `auth/verify` | Resultado de abrir el enlace de verificación | [[AuthenticationController]] | [[Authentication flow]] | 44 |
| `cart/index` | Carrito agrupado por publicante. Mirá la URL de la tapa (línea 53) | [[CartController]] | [[Cart flow]] | 128 |
| `error/400` | Pedido inválido | [[ErrorResponseAdvice]], [[LandingController]] | [[Validation and errors]] | 28 |
| `error/403` | Sin permiso | [[ErrorController]], [[ErrorResponseAdvice]] | [[Validation and errors]] | 18 |
| `error/404` | No encontrado | [[ErrorController]], [[ErrorResponseAdvice]] | [[Validation and errors]] | 30 |
| `error/409` | Conflicto: el estado cambió | [[InquiryController]], [[PostContactController]], [[PublishController]] | [[Validation and errors]] | 18 |
| `inquiry/detail` | La página de la venta: acciones según estado y rol, conversación, reseña | [[InquiryController]] | [[Inquiry and sale flow]] | 287 |
| `inquiry/received` | Bandeja del vendedor, agrupada por publicación | [[InquiryController]] | [[Inquiry and sale flow]] | 81 |
| `inquiry/sent` | Bandeja del comprador | [[InquiryController]] | [[Inquiry and sale flow]] | 79 |
| `landing/index` | Filtros, orden, grilla, estado vacío y paginación | [[LandingController]] | [[Landing flow]] | 223 |
| `post/contact` | Mensaje y elección de dirección | [[PostContactController]] | [[Contact flow]] | 68 |
| `post/detail` | Ficha: galería, vendedor, acciones según quién mira | [[PostController]] | [[Post detail flow]] | 183 |
| `profile/index` | Perfil privado: cuenta, contraseña, cobro, direcciones, publicaciones | [[ProfileController]] | [[Profile flow]] | 341 |
| `profile/public` | Perfil público: reputación, publicaciones, reseñas | [[PublicProfileController]] | [[Public profile flow]] | 108 |
| `publish/index` | Publicar y editar comparten vista | [[PublishController]] | [[Publish flow]] | 155 |

"Controller" se calculó buscando el nombre lógico de la vista en las clases de `webapp`.

## Scripts

| Script | Qué hace | Dónde corre |
|---|---|---|
| `account-edit.js` | Filas editables del perfil y diálogo de la foto | Perfil privado (`pageScript`) |
| `autocomplete.js` | Sugerencias: espera, número de secuencia, JSON y nodos armados con textContent | Todas las páginas; actúa en el buscador y en el campo de artista |
| `catalog.js` | Envía el orden al cambiar el select; pliega filtros en pantallas angostas | Todas las páginas; actúa en los formularios `data-auto-submit` (orden del catálogo y rol de las reseñas del perfil público) |
| `confirm-action.js` | Abre el diálogo antes de enviar un formulario destructivo | Todas las páginas; actúa donde hay `data-confirm-message` |
| `post-gallery.js` | Cambia la foto principal al tocar una miniatura | Ficha (`pageScript`) |
| `publish-preview.js` | Vista previa de la tarjeta mientras se completa el formulario | Publicar y editar (lo carga la propia vista) |
| `sale-detail.js` | Página de la venta: alto de la conversación, scroll al último mensaje, Enter para enviar y cancelar la edición de la reseña | Página de la venta (`pageScript`) |
| `submit-once.js` | Evita el doble envío | Todas las páginas (lo carga `head.tag`) |

Todos son JavaScript sin dependencias ni framework, cargados con `defer`.

### Mejora progresiva

Cada script agrega comodidad sobre algo que ya anda con HTML y un POST:

| Sin JavaScript | Con JavaScript |
|---|---|
| El orden del catálogo se aplica con un botón | Se aplica al cambiar el select |
| El buscador envía el formulario | Ofrece sugerencias mientras se escribe |
| Un formulario destructivo se envía directo; el service valida estado y propiedad igual | Pide confirmación en un diálogo |
| Un doble clic podría enviar dos veces; el service lo resuelve con sus guardas | Los botones se deshabilitan al enviar |
| El perfil edita con enlaces y recargas | Las filas se abren y cierran en el lugar |
| En la ficha, cada miniatura es un enlace que abre esa foto | Las miniaturas cambian la foto principal sin salir de la página |

La seguridad nunca depende del script: confirmaciones y bloqueos de doble envío son comodidad; la regla está en el service.

## Imágenes

| Archivo | Uso |
|---|---|
| `images/logo.svg` | Isotipo y favicon |
| `images/covers/placeholder.svg` | Tapa cuando la publicación no tiene foto |

Las fotos subidas no son archivos: se guardan en la base y las sirve [[ImageController]] ([[Cover image flow]]).

## Preguntas de defensa

**¿Por qué las JSP están bajo `WEB-INF`?**
Para que solo se llegue a ellas a través de un controller, que arma el modelo y aplica la seguridad.

**¿Hay lógica en las vistas?**
Solo de presentación: condicionales y bucles de JSTL sobre datos ya resueltos. No hay scriptlets ni llamadas a services.

**¿Qué pasa si el navegador no tiene JavaScript?**
Todo funciona con formularios y enlaces. Los scripts solo mejoran la experiencia.

**¿Cómo evitan XSS en el JavaScript?**
Las sugerencias llegan como JSON y los nodos se arman con `textContent`, nunca con `innerHTML`.

## Código de las vistas

### auth/forgot-password

Pedido de recuperación.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/views/auth/forgot-password.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/auth/forgot-password.jsp>), líneas 1–34.

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
               modelAttribute="forgotPasswordForm" novalidate="novalidate">
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

### auth/login

Login: mirá los nombres de los campos y el token CSRF.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/views/auth/login.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/auth/login.jsp>), líneas 1–56.

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
    <form:form cssClass="surface form-stack" action="${loginUrl}" method="post" modelAttribute="loginForm" novalidate="novalidate">
        <h1 class="auth-shell__title"><c:out value="${heading}"/></h1>
        <c:if test="${param.error != null}">
            <p class="error"><spring:message code="auth.login.invalid"/></p>
        </c:if>
        <c:if test="${param.logout != null}">
            <p class="notice"><spring:message code="auth.login.loggedOut"/></p>
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
        <c:if test="${param.sessionExpired != null}">
            <p class="notice"><spring:message code="auth.login.sessionExpired"/></p>
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

### auth/register

Formulario de registro.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/views/auth/register.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/auth/register.jsp>), líneas 1–46.

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="form" uri="http://www.springframework.org/tags/form" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<c:url value="/register" var="registerUrl"/>
<c:url value="/login" var="loginUrl"/>
<c:url value="/forgot-password" var="forgotPasswordUrl"/>
<spring:message code="auth.register.heading" var="heading"/>
<spring:message code="auth.email.label" var="emailLabel"/>
<spring:message code="auth.username.label" var="usernameLabel"/>
<spring:message code="auth.password.label" var="passwordLabel"/>
<spring:message code="auth.passwordConfirmation.label" var="passwordConfirmationLabel"/>
<spring:message code="auth.register.submit" var="submitLabel"/>
<!DOCTYPE html>
<html lang="${pageContext.response.locale}">
<ui:head titleCode="auth.register.pageTitle"/>
<body>
<main class="page-shell auth-shell">
    <header class="auth-shell__header">
        <ui:brand size="lg"/>
    </header>
    <form:form cssClass="surface form-stack" action="${registerUrl}" method="post" modelAttribute="registerForm" novalidate="novalidate">
        <h1 class="auth-shell__title"><c:out value="${heading}"/></h1>
        <ui:text-input path="email" label="${emailLabel}" type="email" maxLength="100"/>
        <c:if test="${duplicateEmail}">
            <p class="auth-shell__switch">
                <spring:message code="auth.register.email.recoverPrompt"/>
                <a href="<c:out value="${forgotPasswordUrl}"/>"><spring:message code="auth.register.email.recoverLink"/></a>
            </p>
        </c:if>
        <ui:text-input path="username" label="${usernameLabel}" maxLength="100"/>
        <ui:text-input path="password" label="${passwordLabel}" type="password" maxLength="72"/>
        <ui:text-input path="passwordConfirmation" label="${passwordConfirmationLabel}" type="password" maxLength="72"/>
        <p class="hint"><spring:message code="auth.password.hint"/></p>
        <div class="form-stack__actions">
            <ui:button label="${submitLabel}" type="submit"/>
        </div>
        <p class="auth-shell__switch">
            <spring:message code="auth.register.loginPrompt"/>
            <a href="<c:out value="${loginUrl}"/>"><spring:message code="auth.login.action"/></a>
        </p>
    </form:form>
</main>
</body>
</html>
```

### auth/reset-password

Nueva contraseña con el token en un campo oculto.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/views/auth/reset-password.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/auth/reset-password.jsp>), líneas 1–48.

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

### auth/verify-required

Pantalla para la cuenta sin verificar.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/views/auth/verify-required.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/auth/verify-required.jsp>), líneas 1–32.

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<spring:message code="auth.verifyRequired.heading" var="heading"/>
<spring:message code="auth.verifyRequired.message" var="message"/>
<spring:message code="nav.back" var="backLabel"/>
<!DOCTYPE html>
<html lang="${pageContext.response.locale}">
<ui:head titleCode="auth.verifyRequired.pageTitle"/>
<body>
<main class="page-shell auth-shell">
    <header class="auth-shell__header">
        <ui:brand size="lg"/>
    </header>
    <section class="surface form-stack">
        <h1 class="auth-shell__title"><c:out value="${heading}"/></h1>
        <ui:p text="${message}"/>
        <c:if test="${verificationResent}">
            <p class="notice"><spring:message code="auth.verification.resent"/></p>
        </c:if>
        <c:if test="${verificationThrottled}">
            <p class="notice"><spring:message code="auth.verification.throttled"/></p>
        </c:if>
        <div class="form-stack__actions">
            <ui:resend-verification/>
            <ui:button label="${backLabel}" variant="ghost" href="/"/>
        </div>
    </section>
</main>
</body>
</html>
```

### auth/verify

Resultado de abrir el enlace de verificación.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/views/auth/verify.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/auth/verify.jsp>), líneas 1–44.

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="sec" uri="http://www.springframework.org/security/tags" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<spring:message code="auth.login.action" var="loginLabel"/>
<spring:message code="nav.back" var="backLabel"/>
<!DOCTYPE html>
<html lang="${pageContext.response.locale}">
<ui:head titleCode="auth.verify.pageTitle"/>
<body>
<main class="page-shell auth-shell">
    <header class="auth-shell__header">
        <ui:brand size="lg"/>
    </header>
    <section class="surface form-stack">
        <c:choose>
            <c:when test="${verified}">
                <h1 class="auth-shell__title"><spring:message code="auth.verify.success.heading"/></h1>
                <p class="notice"><spring:message code="auth.verify.success.message"/></p>
            </c:when>
            <c:otherwise>
                <h1 class="auth-shell__title"><spring:message code="auth.verify.invalid.heading"/></h1>
                <p class="error"><spring:message code="auth.verify.invalid"/></p>
            </c:otherwise>
        </c:choose>
        <div class="form-stack__actions">
            <%-- El enlace no inicia sesion: sin sesion en este navegador, el paso siguiente es entrar. --%>
            <sec:authorize access="isAnonymous()">
                <ui:button label="${loginLabel}" href="/login"/>
            </sec:authorize>
            <sec:authorize access="isAuthenticated()">
                <c:if test="${not verified}">
                    <sec:authorize access="!principal.verified">
                        <ui:resend-verification/>
                    </sec:authorize>
                </c:if>
                <ui:button label="${backLabel}" variant="${verified ? 'primary' : 'ghost'}" href="/"/>
            </sec:authorize>
        </div>
    </section>
</main>
</body>
</html>
```

### cart/index

Carrito agrupado por publicante. Mirá la URL de la tapa (línea 53).

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/views/cart/index.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/cart/index.jsp>), líneas 1–128.

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="form" uri="http://www.springframework.org/tags/form" %>
<%@ taglib prefix="sec" uri="http://www.springframework.org/security/tags" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<c:url value="/cart/checkout" var="checkoutUrl"/>
<c:url value="/profile" var="profileAddressesUrl"/>
<spring:message code="cart.heading" var="heading"/>
<spring:message code="cart.remove" var="removeLabel"/>
<spring:message code="cart.checkout" var="checkoutLabel" arguments="${cart.itemCount}"/>
<spring:message code="cart.empty.cta" var="emptyCtaLabel"/>
<spring:message code="post.contact.address.limit" var="addressLimitHint" arguments="${maxAddresses}"/>
<spring:message code="profile.addresses.label" var="addressesLabel"/>
<!DOCTYPE html>
<html lang="${pageContext.response.locale}">
<ui:head titleCode="cart.pageTitle"/>
<body>
<ui:site-header/>
<main class="page-shell">
    <ui:h1 text="${heading}"/>
    <c:if test="${not empty cartWarning}"><p class="notice notice--warning"><spring:message code="${cartWarning}"/></p></c:if>
    <c:if test="${addressLimitReached}">
        <p class="notice notice--warning"><c:out value="${addressLimitHint}"/></p>
    </c:if>
    <c:choose>
        <c:when test="${empty cart.groups}">
            <section class="surface cart-empty">
                <span class="cart-empty__icon"><ui:icon name="cart"/></span>
                <h2 class="text text-h3"><spring:message code="cart.empty.title"/></h2>
                <p class="text text-body cart-empty__text"><spring:message code="cart.empty"/></p>
                <ui:button label="${emptyCtaLabel}" href="/"/>
            </section>
        </c:when>
        <c:otherwise>
            <div class="contact-layout cart-layout">
                <div class="cart">
                    <p class="hint">
                        <%-- spring:argument y no arguments="a,b": la lista separada por comas llega como
                             texto y el choice del mensaje necesita numeros. --%>
                        <spring:message code="cart.summary">
                            <spring:argument value="${cart.itemCount}"/>
                            <spring:argument value="${cart.sellerCount}"/>
                        </spring:message>
                    </p>
                    <%-- Agrupado por Publicante: a cada uno le llega un solo correo con sus vinilos. --%>
                    <c:forEach items="${cart.groups}" var="group">
                        <section class="cart__seller">
                            <h2 class="text text-h3"><c:out value="${group.sellerUsername}"/></h2>
                            <ul class="inbox-list">
                                <c:forEach items="${group.items}" var="item">
                                    <c:choose>
                                        <c:when test="${item.coverImageId.present}"><c:url value="/post/${item.postId}/images/${item.coverImageId.get()}" var="coverUrl"/></c:when>
                                        <c:otherwise><c:url value="/images/covers/placeholder.svg" var="coverUrl"/></c:otherwise>
                                    </c:choose>
                                    <c:url value="/post/${item.postId}" var="postUrl"/>
                                    <c:url value="/cart/remove/${item.postId}" var="removeUrl"/>
                                    <spring:message code="vinylCard.cover.alt" var="coverAlt"><spring:argument value="${item.title}"/></spring:message>
                                    <spring:message code="vinylCard.open" var="openLabel"><spring:argument value="${item.title}"/></spring:message>
                                    <spring:message code="vinylCard.price.format" var="priceValue"><spring:argument value="${item.price}"/></spring:message>
                                    <spring:message code="cart.item.artistYear" var="artistYear"><spring:argument value="${item.artistName}"/><spring:argument value="${item.releaseYear}"/></spring:message>
                                    <li class="cart__item">
                                        <div class="inbox-group__post inbox-group__post--linked">
                                            <a class="inbox-group__anchor" href="<c:out value="${postUrl}"/>" aria-label="<c:out value="${openLabel}"/>"></a>
                                            <div class="inbox-group__cover"><img src="<c:out value="${coverUrl}"/>" alt="<c:out value="${coverAlt}"/>"/></div>
                                            <div class="inbox-group__title">
                                                <ui:h3 text="${item.title}" level="3"/>
                                                <ui:p text="${artistYear}" variant="lead"/>
                                            </div>
                                        </div>
                                        <span class="cart__price"><c:out value="${priceValue}"/></span>
                                        <form action="${removeUrl}" method="post">
                                            <sec:csrfInput/>
                                            <ui:button label="${removeLabel}" variant="ghost" size="sm" type="submit" icon="x"/>
                                        </form>
                                    </li>
                                </c:forEach>
                            </ul>
                        </section>
                    </c:forEach>
                </div>
                <form:form cssClass="surface form-stack" action="${checkoutUrl}" method="post" modelAttribute="checkoutForm" data-submit-once="true">
                    <fieldset class="address-choice">
                        <legend class="input-field__label"><spring:message code="post.contact.address.legend"/></legend>
                        <form:errors path="addressId" element="p" cssClass="input-field__error"/>
                        <c:forEach items="${addresses}" var="address">
                            <label class="address-choice__option">
                                <form:radiobutton path="addressId" value="${address.id}"/>
                                <ui:address address="${address}"/>
                            </label>
                        </c:forEach>
                        <c:choose>
                            <c:when test="${empty addresses}">
                                <%-- Sin libreta no hay nada que elegir: los campos se muestran directamente. --%>
                                <ui:address-fields/>
                            </c:when>
                            <c:when test="${canAddAddress}">
                                <label class="address-choice__option">
                                    <%-- Igual que en el contacto: form:radiobutton no marca el valor vacio,
                                         se arma a mano para que "nueva" quede elegida sin addressId. --%>
                                    <input type="radio" id="addressIdNew" name="addressId" value=""<c:if test="${empty checkoutForm.addressId}"> checked="checked"</c:if>/>
                                    <span><spring:message code="post.contact.address.new"/></span>
                                </label>
                                <div class="address-choice__new"><ui:address-fields/></div>
                            </c:when>
                            <c:otherwise>
                                <p class="hint"><c:out value="${addressLimitHint}"/> <a href="${profileAddressesUrl}#addresses"><c:out value="${addressesLabel}"/></a></p>
                            </c:otherwise>
                        </c:choose>
                        <%-- El mismo aviso que el contacto de un Post: es la misma direccion de envio. --%>
                        <p class="hint"><spring:message code="post.contact.address.hint"/></p>
                    </fieldset>
                    <p class="hint"><spring:message code="cart.checkout.hint"/></p>
                    <spring:message code="vinylCard.price.format" var="totalValue"><spring:argument value="${cart.totalPrice}"/></spring:message>
                    <div class="cart-total">
                        <span class="text text-body cart-total__label"><spring:message code="cart.total"/></span>
                        <span class="vinyl-card__price-value cart-total__value"><c:out value="${totalValue}"/></span>
                    </div>
                    <div class="form-stack__actions">
                        <ui:button label="${checkoutLabel}" type="submit"/>
                    </div>
                </form:form>
            </div>
        </c:otherwise>
    </c:choose>
</main>
</body>
</html>
```

### error/400

Pedido inválido.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/views/error/400.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/error/400.jsp>), líneas 1–28.

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

### error/403

Sin permiso.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/views/error/403.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/error/403.jsp>), líneas 1–18.

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

### error/404

No encontrado.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/views/error/404.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/error/404.jsp>), líneas 1–30.

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

### error/409

Conflicto: el estado cambió.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/views/error/409.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/error/409.jsp>), líneas 1–18.

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

### inquiry/detail

La página de la venta: acciones según estado y rol, conversación, reseña.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/views/inquiry/detail.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/inquiry/detail.jsp>), líneas 1–287.

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt" %>
<%@ taglib prefix="form" uri="http://www.springframework.org/tags/form" %>
<%@ taglib prefix="sec" uri="http://www.springframework.org/security/tags" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<c:set var="inquiry" value="${detail.inquiry}"/>
<c:choose>
    <c:when test="${detail.sale}">
        <c:set var="pageTitleCode" value="${detail.sellerView ? 'inquiry.sale.pageTitle.seller' : 'inquiry.sale.pageTitle.buyer'}"/>
        <spring:message code="${detail.sellerView ? 'inquiry.sale.heading.seller' : 'inquiry.sale.heading.buyer'}" var="heading"/>
    </c:when>
    <c:otherwise>
        <c:set var="pageTitleCode" value="inquiry.detail.pageTitle"/>
        <spring:message code="${detail.sellerView ? 'inquiry.detail.heading.seller' : 'inquiry.detail.heading.buyer'}" var="heading">
            <spring:argument value="${inquiry.buyerUsername}"/>
        </spring:message>
    </c:otherwise>
</c:choose>
<spring:message code="inquiry.heading" var="backLabel"/>
<spring:message code="inquiry.sale.receipt.submit" var="receiptSubmitLabel"/>
<spring:message code="inquiry.sale.confirm" var="confirmLabel"/>
<spring:message code="inquiry.sale.confirm.confirmation" var="confirmConfirmation"/>
<spring:message code="inquiry.sale.requestReceipt" var="requestReceiptLabel"/>
<spring:message code="inquiry.sale.requestReceipt.confirmation" var="requestReceiptConfirmation"/>
<spring:message code="${detail.sellerView ? 'inquiry.sale.cancel.seller' : 'inquiry.sale.cancel.buyer'}" var="cancelLabel"/>
<spring:message code="inquiry.sale.cancel.confirmation" var="cancelConfirmation"/>
<spring:message code="inquiry.accept" var="acceptLabel"/>
<spring:message code="inquiry.reject" var="rejectLabel"/>
<spring:message code="inquiry.accept.confirmation" var="acceptConfirmation">
    <spring:argument value="${inquiry.title}"/>
    <spring:argument value="${inquiry.artistName}"/>
</spring:message>
<spring:message code="inquiry.reject.confirmation" var="rejectConfirmation">
    <spring:argument value="${inquiry.buyerUsername}"/>
</spring:message>
<spring:message code="inquiry.conversation.you" var="youLabel"/>
<spring:message code="inquiry.conversation.label" var="messageLabel"/>
<spring:message code="inquiry.conversation.send" var="sendLabel"/>
<spring:message code="confirm.title" var="confirmTitle"/>
<spring:message code="confirm.action" var="confirmAction"/>
<c:url value="/inquiries/${inquiry.id}/receipt" var="receiptUrl"/>
<c:url value="/inquiries/${inquiry.id}/confirm" var="confirmUrl"/>
<c:url value="/inquiries/${inquiry.id}/request-receipt" var="requestReceiptUrl"/>
<c:url value="/inquiries/${inquiry.id}/cancel" var="cancelUrl"/>
<c:url value="/inquiries/${inquiry.id}/accept" var="acceptUrl"/>
<c:url value="/inquiries/${inquiry.id}/reject" var="rejectUrl"/>
<c:url value="/inquiries/${inquiry.id}/messages" var="messagesUrl"/>
<c:url value="/inquiries/${inquiry.id}/review" var="reviewUrl"/>
<c:url value="/inquiries/${inquiry.id}/review/remove" var="reviewRemoveUrl"/>
<c:url value="/inquiries/${inquiry.id}" var="detailUrl"/>
<spring:message code="${empty detail.ownReview ? 'review.save' : 'review.update'}" var="reviewSaveLabel"/>
<spring:message code="review.edit" var="reviewEditLabel"/>
<spring:message code="review.cancel" var="reviewCancelLabel"/>
<spring:message code="review.remove.confirmation" var="reviewRemoveConfirmation"/>
<spring:message code="review.remove" var="reviewRemoveLabel"/>
<spring:message code="review.rating.label" var="reviewRatingLabel"/>
<spring:message code="review.body.label" var="reviewBodyLabel"/>
<!DOCTYPE html>
<html lang="${pageContext.response.locale}">
<ui:head titleCode="${pageTitleCode}" pageScript="sale-detail"/>
<body>
<ui:site-header/>
<main class="page-shell sale-page">
    <ui:back-link href="${detail.sellerView ? '/inquiries' : '/inquiries/sent'}" label="${backLabel}"/>
    <ui:h1 text="${heading}"/>
    <c:if test="${not empty saleNotice}"><p class="notice"><spring:message code="${saleNotice}"/></p></c:if>
    <c:if test="${param.receiptTooLarge != null}"><p class="notice notice--error"><spring:message code="inquiry.receipt.invalid"/></p></c:if>

    <div class="sale-layout">
    <%-- La Conversacion: del Mensaje mas viejo al mas nuevo. Sin acciones de decision. --%>
    <section class="conversation" id="conversation">
        <header class="conversation__header">
            <h2 class="visually-hidden" id="conversation-title"><spring:message code="inquiry.conversation.heading"/></h2>
            <ui:user-byline userId="${detail.counterpartyId}" username="${detail.counterpartyUsername}" imageId="${detail.counterpartyAvatarImageId}"/>
        </header>
        <div class="conversation__history" tabindex="0" role="region" aria-labelledby="conversation-title" data-conversation-history>
        <c:choose>
            <c:when test="${empty detail.messages}">
                <p class="conversation__empty"><spring:message code="inquiry.conversation.empty"/></p>
            </c:when>
            <c:otherwise>
                <ol class="conversation__list">
                    <c:forEach items="${detail.messages}" var="message">
                        <c:set var="own" value="${message.senderId eq detail.viewerId}"/>
                        <li class="message${own ? ' message--own' : ''}">
                            <p class="message__meta">
                                <span class="message__author">
                                    <c:choose>
                                        <c:when test="${own}"><c:out value="${youLabel}"/></c:when>
                                        <c:when test="${message.senderId eq inquiry.buyerId}"><c:out value="${inquiry.buyerUsername}"/></c:when>
                                        <c:otherwise><c:out value="${inquiry.sellerUsername}"/></c:otherwise>
                                    </c:choose>
                                </span>
                                <fmt:formatDate value="${message.sentAt}" type="both" dateStyle="short" timeStyle="short" var="sentAt"/>
                                <span class="message__time"><c:out value="${sentAt}"/></span>
                            </p>
                            <p class="message__body"><c:out value="${message.body}"/></p>
                        </li>
                    </c:forEach>
                </ol>
            </c:otherwise>
        </c:choose>
        </div>
        <c:choose>
            <c:when test="${detail.canWrite}">
                <form:form action="${messagesUrl}#conversation" method="post" modelAttribute="messageForm" data-submit-once="true" data-focus-message="${messageSent ? 'true' : 'false'}" cssClass="form-stack conversation__form">
                    <ui:textarea path="body" id="message-body" label="${messageLabel}" maxLength="${maxMessageLength}" rows="2" hideLabel="true"/>
                    <div class="form-stack__actions">
                        <ui:button label="${sendLabel}" type="submit"/>
                    </div>
                </form:form>
            </c:when>
            <%-- Por que no se puede escribir: la publicacion ya no existe, o la Consulta se rechazo o
                 se cancelo. REJECTED + SOLD no alcanza para decir que se vendio a otra persona: el
                 rechazo pudo ser manual, o el mismo comprador pudo comprar con otra Consulta. --%>
            <c:when test="${inquiry.postDeleted}">
                <p class="notice"><spring:message code="inquiry.conversation.closed.postDeleted"/></p>
            </c:when>
            <c:otherwise>
                <p class="notice"><spring:message code="inquiry.conversation.closed"/></p>
            </c:otherwise>
        </c:choose>
    </section>
        <div class="sale-sidebar">
        <section class="sale-summary">
            <ui:inbox-group-header group="${inquiry}"/>
            <dl class="sale-facts" id="sale-actions">
                <c:if test="${not empty inquiry.price}">
                    <dt><spring:message code="inquiry.sale.price"/></dt>
                    <dd><spring:message code="vinylCard.price.format"><spring:argument value="${inquiry.price}"/></spring:message></dd>
                </c:if>
                <dt><spring:message code="${detail.sellerView ? 'inquiry.sale.buyer' : 'inquiry.sale.seller'}"/></dt>
                <dd><ui:user-byline userId="${detail.counterpartyId}" username="${detail.counterpartyUsername}" imageId="${detail.counterpartyAvatarImageId}"/></dd>
                <dt><spring:message code="inquiry.sale.status"/></dt>
                <dd><ui:inquiry-status status="${inquiry.status}"/></dd>
                <c:if test="${detail.addressVisible}">
                    <dt><spring:message code="inquiry.address.label"/></dt>
                    <dd>
                        <c:choose>
                            <c:when test="${empty inquiry.address}"><spring:message code="inquiry.address.none"/></c:when>
                            <c:otherwise>
                                <ui:address address="${inquiry.address}"/>
                                <c:if test="${inquiry.address.cityAndProvinceOnly and inquiry.pending}"><span class="hint"><spring:message code="inquiry.address.partial"/></span></c:if>
                            </c:otherwise>
                        </c:choose>
                    </dd>
                </c:if>
                <c:if test="${inquiry.hasReceipt}">
                    <dt><spring:message code="inquiry.sale.receipt"/></dt>
                    <dd><a href="<c:out value="${receiptUrl}"/>" target="_blank" rel="noopener"><spring:message code="inquiry.sale.receipt.open"/></a></dd>
                </c:if>
            </dl>

            <%-- Que se espera ahora, segun el lado y el estado. Presentacion: no decide acciones. --%>
            <c:choose>
                <c:when test="${detail.canReviewReceipt}"><p class="sale-summary__note"><spring:message code="inquiry.sale.review.hint"/></p></c:when>
                <c:when test="${not detail.sellerView and inquiry.paymentSubmitted}"><p class="sale-summary__note"><spring:message code="inquiry.sale.waitingSeller"/></p></c:when>
                <c:when test="${detail.sellerView and inquiry.awaitingPayment}"><p class="sale-summary__note"><spring:message code="inquiry.sale.waitingPayment"/></p></c:when>
                <c:when test="${inquiry.status eq 'ACCEPTED'}"><p class="sale-summary__note"><spring:message code="${detail.sellerView ? 'inquiry.sale.done.seller' : 'inquiry.sale.done.buyer'}"/></p></c:when>
            </c:choose>

            <c:if test="${detail.canReviewReceipt or detail.canCancel}">
                <div class="sale-summary__actions">
                    <c:if test="${detail.canReviewReceipt}">
                        <form action="<c:out value="${confirmUrl}"/>" method="post" data-confirm-message="<c:out value="${confirmConfirmation}"/>">
                            <sec:csrfInput/>
                            <ui:button label="${confirmLabel}" type="submit" icon="check"/>
                        </form>
                        <form action="<c:out value="${requestReceiptUrl}"/>" method="post" data-confirm-message="<c:out value="${requestReceiptConfirmation}"/>">
                            <sec:csrfInput/>
                            <ui:button label="${requestReceiptLabel}" variant="ghost" type="submit"/>
                        </form>
                    </c:if>
                    <c:if test="${detail.canCancel}">
                        <form class="sale-summary__cancel" action="<c:out value="${cancelUrl}"/>" method="post" data-confirm-message="<c:out value="${cancelConfirmation}"/>">
                            <sec:csrfInput/>
                            <ui:button label="${cancelLabel}" variant="danger-outline" type="submit" icon="x"/>
                        </form>
                    </c:if>
                </div>
            </c:if>
        </section>

        <%-- La decision es sobre la persona: nombra al Comprador y nunca aparece junto a un Mensaje. --%>
        <c:if test="${detail.canReject}">
            <section class="sale-decision">
                <h2 class="text text-h3">
                    <spring:message code="inquiry.detail.decision.heading" var="decisionHeading">
                        <spring:argument value="${inquiry.buyerUsername}"/>
                    </spring:message>
                    <c:out value="${decisionHeading}"/>
                </h2>
                <p class="sale-summary__note">
                    <spring:message code="inquiry.detail.decision.hint" var="decisionHint">
                        <spring:argument value="${inquiry.buyerUsername}"/>
                    </spring:message>
                    <c:out value="${decisionHint}"/>
                </p>
                <div class="sale-summary__actions">
                    <c:if test="${detail.canAccept}">
                        <form action="<c:out value="${acceptUrl}"/>" method="post" data-confirm-message="<c:out value="${acceptConfirmation}"/>">
                            <sec:csrfInput/>
                            <ui:button label="${acceptLabel}" type="submit" icon="check"/>
                        </form>
                    </c:if>
                    <form action="<c:out value="${rejectUrl}"/>" method="post" data-confirm-message="<c:out value="${rejectConfirmation}"/>">
                        <sec:csrfInput/>
                        <ui:button label="${rejectLabel}" variant="danger-outline" type="submit" icon="x"/>
                    </form>
                </div>
            </section>
        </c:if>

        <c:if test="${detail.canUploadReceipt}">
            <section class="form-stack sale-payment">
                <h2 class="text text-h3"><spring:message code="inquiry.sale.payment.heading"/></h2>
                <c:choose>
                    <c:when test="${detail.paymentInfoMissing}">
                        <p class="notice notice--warning"><spring:message code="inquiry.sale.payment.missing"/></p>
                    </c:when>
                    <c:otherwise>
                        <dl class="sale-facts sale-facts--payment">
                            <c:if test="${not empty inquiry.sellerPaymentInfo.cbu}">
                                <dt><spring:message code="profile.payment.cbu.label"/></dt>
                                <dd class="sale-facts__copyable"><c:out value="${inquiry.sellerPaymentInfo.cbu}"/></dd>
                            </c:if>
                            <c:if test="${not empty inquiry.sellerPaymentInfo.alias}">
                                <dt><spring:message code="profile.payment.alias.label"/></dt>
                                <dd class="sale-facts__copyable"><c:out value="${inquiry.sellerPaymentInfo.alias}"/></dd>
                            </c:if>
                        </dl>
                    </c:otherwise>
                </c:choose>
                <c:if test="${detail.receiptRequested}"><p class="notice notice--warning"><spring:message code="inquiry.sale.receiptRequested.buyer"/></p></c:if>
                <form:form action="${receiptUrl}" method="post" modelAttribute="receiptForm" enctype="multipart/form-data" data-submit-once="true" cssClass="form-stack">
                    <spring:bind path="receipt">
                        <div class="input-field ${status.error ? 'input-field--error' : ''}">
                            <form:label path="receipt" cssClass="input-field__label"><spring:message code="inquiry.sale.receipt.label"/></form:label>
                            <ui:input-control id="receipt" name="receipt" type="file" hasError="${status.error}"
                                              accept="application/pdf,image/png,image/jpeg,image/webp"/>
                            <p class="hint"><spring:message code="inquiry.receipt.hint"/></p>
                            <form:errors path="receipt" cssClass="input-field__error" element="p"/>
                        </div>
                    </spring:bind>
                    <div class="form-stack__actions">
                        <ui:button label="${receiptSubmitLabel}" type="submit"/>
                    </div>
                </form:form>
            </section>
        </c:if>

        <c:if test="${detail.canReview}">
            <section class="sale-review" id="review">
                <h2 class="text text-h3"><spring:message code="${empty detail.ownReview ? 'review.prompt' : 'review.published'}"/></h2>
                <c:if test="${reviewSaved}"><p class="notice" role="status"><spring:message code="review.saved"/></p></c:if>
                <c:if test="${reviewRemoved}"><p class="notice" role="status"><spring:message code="review.removed"/></p></c:if>
                <c:if test="${not empty detail.ownReview}">
                    <div class="sale-review__published"><ui:review-content maxRating="${maxRating}" review="${detail.ownReview}"/></div>
                </c:if>
                <spring:bind path="reviewForm.*"><c:set var="reviewHasErrors" value="${status.error}"/></spring:bind>
                <details class="sale-review__editor"<c:if test="${reviewHasErrors}"> open</c:if>>
                    <summary class="button button--ghost button--sm"><c:out value="${empty detail.ownReview ? reviewSaveLabel : reviewEditLabel}"/></summary>
                    <form:form action="${reviewUrl}#review" method="post" modelAttribute="reviewForm" data-submit-once="true" cssClass="form-stack" novalidate="novalidate">
                        <ui:star-rating-input path="rating" legend="${reviewRatingLabel}" max="${maxRating}" valueCode="review.rating.value"/>
                        <ui:textarea path="body" id="review-body" label="${reviewBodyLabel}" maxLength="${maxReviewLength}" rows="3"/>
                        <div class="form-stack__actions">
                            <ui:button label="${reviewSaveLabel}" type="submit"/>
                            <ui:button label="${reviewCancelLabel}" url="${detailUrl}" variant="ghost" data="cancel-review"/>
                        </div>
                    </form:form>
                </details>
                <c:if test="${not empty detail.ownReview}">
                    <form class="sale-review__remove" action="<c:out value="${reviewRemoveUrl}"/>" method="post" data-confirm-message="<c:out value="${reviewRemoveConfirmation}"/>" data-submit-once="true">
                        <sec:csrfInput/>
                        <ui:button label="${reviewRemoveLabel}" type="submit" variant="danger-outline" size="sm"/>
                    </form>
                </c:if>
            </section>
        </c:if>
        </div>
    </div>
</main>
<ui:confirm-dialog title="${confirmTitle}" confirmLabel="${confirmAction}"/>
</body>
</html>
```

### inquiry/received

Bandeja del vendedor, agrupada por publicación.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/views/inquiry/received.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/inquiry/received.jsp>), líneas 1–81.

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<spring:message code="inquiry.heading" var="heading"/>
<spring:message code="inquiry.viewSale" var="viewSaleLabel"/>
<spring:message code="inquiry.openConversation" var="openConversationLabel"/>
<spring:message code="inquiry.pagination" var="paginationLabel"/>
<spring:message code="inquiry.filter.label" var="filterLabel"/>
<jsp:useBean id="paginationParams" class="java.util.LinkedHashMap" scope="page"/>
<c:set target="${paginationParams}" property="status" value="${statusFilter}"/>
<!DOCTYPE html>
<html lang="${pageContext.response.locale}">
<ui:head titleCode="inquiry.received.pageTitle"/>
<body>
<ui:site-header/>
<main class="page-shell">
    <ui:h1 text="${heading}"/>
    <ui:inquiry-nav active="received" receivedCount="${receivedCount}" sentCount="${sentCount}"/>
    <c:if test="${filterCounts.total gt 0}">
        <ui:filter-chips baseUrl="/inquiries" paramName="status" values="${statusFilters}" active="${statusFilter}"
                         counts="${filterCounts.counts}" messagePrefix="inquiry.filter" label="${filterLabel}"/>
    </c:if>
    <c:if test="${inquiryRejected}"><p class="notice"><spring:message code="inquiry.rejected"/></p></c:if>

    <section class="inbox" id="inquiries">
        <c:choose>
            <c:when test="${empty receivedPage.groups}">
                <p class="empty-state"><spring:message code="${empty statusFilter ? 'inquiry.received.empty' : 'inquiry.filter.empty'}"/></p>
            </c:when>
            <c:otherwise>
                <c:forEach items="${receivedPage.groups}" var="group">
                    <section class="inbox-group">
                        <ui:inbox-group-header group="${group}"/>
                        <ul class="inbox-list">
                            <c:forEach items="${group.inquiries}" var="inquiry">
                                <li class="inbox-row">
                                    <span class="inbox-row__who"><c:out value="${inquiry.buyerUsername}"/></span>
                                    <ui:inbox-last-message inquiry="${inquiry}" viewerId="${inquiry.sellerId}"/>
                                    <div class="inbox-row__address">
                                        <c:choose>
                                            <c:when test="${empty inquiry.address}"><span class="inbox-row__msg--empty"><spring:message code="inquiry.address.none"/></span></c:when>
                                            <c:otherwise>
                                                <ui:address address="${inquiry.address}"/>
                                                <c:if test="${inquiry.address.cityAndProvinceOnly and inquiry.pending}"><span class="hint"><spring:message code="inquiry.address.partial"/></span></c:if>
                                            </c:otherwise>
                                        </c:choose>
                                    </div>
                                    <%-- Aceptar y rechazar viven en el detalle: la bandeja nunca los pone junto a un Mensaje. --%>
                                    <div class="inbox-row__end">
                                        <ui:inquiry-status status="${inquiry.status}"/>
                                        <c:choose>
                                            <c:when test="${inquiry.sale}">
                                                <ui:button label="${viewSaleLabel}" size="sm" href="/inquiries/${inquiry.id}"
                                                           variant="${inquiry.paymentSubmitted ? 'primary' : 'ghost'}"/>
                                            </c:when>
                                            <c:otherwise>
                                                <c:url value="/inquiries/${inquiry.id}" var="detailUrl"/>
                                                <ui:button label="${openConversationLabel}" size="sm" url="${detailUrl}#conversation"
                                                           variant="${inquiry.pending ? 'primary' : 'ghost'}"/>
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
                               baseUrl="/inquiries"
                               extraParams="${paginationParams}"
                               fragment="inquiries"
                               ariaLabel="${paginationLabel}"/>
            </c:otherwise>
        </c:choose>
    </section>
</main>
</body>
</html>
```

### inquiry/sent

Bandeja del comprador.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/views/inquiry/sent.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/inquiry/sent.jsp>), líneas 1–79.

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<spring:message code="inquiry.heading" var="heading"/>
<spring:message code="inquiry.pagination" var="paginationLabel"/>
<spring:message code="inquiry.filter.label" var="filterLabel"/>
<jsp:useBean id="paginationParams" class="java.util.LinkedHashMap" scope="page"/>
<c:set target="${paginationParams}" property="status" value="${statusFilter}"/>
<spring:message code="inquiry.viewSale" var="viewSaleLabel"/>
<spring:message code="inquiry.pay" var="payLabel"/>
<spring:message code="inquiry.openConversation" var="openConversationLabel"/>
<!DOCTYPE html>
<html lang="${pageContext.response.locale}">
<ui:head titleCode="inquiry.sent.pageTitle"/>
<body>
<ui:site-header/>
<main class="page-shell">
    <ui:h1 text="${heading}"/>
    <ui:inquiry-nav active="sent" receivedCount="${receivedCount}" sentCount="${sentCount}"/>
    <c:if test="${filterCounts.total gt 0}">
        <ui:filter-chips baseUrl="/inquiries/sent" paramName="status" values="${statusFilters}" active="${statusFilter}"
                         counts="${filterCounts.counts}" messagePrefix="inquiry.filter" label="${filterLabel}"/>
    </c:if>
    <c:if test="${inquirySubmitted}"><p class="notice"><spring:message code="inquiry.submitted"/></p></c:if>
    <c:if test="${not empty cartResult}">
        <p class="notice"><spring:message code="cart.result.sent" arguments="${cartResult.sentCount}"/></p>
        <c:if test="${cartResult.skippedCount > 0}">
            <p class="notice notice--warning"><spring:message code="cart.result.skipped" arguments="${cartResult.skippedCount}"/></p>
        </c:if>
    </c:if>

    <section class="inbox" id="inquiries">
        <c:choose>
            <c:when test="${empty sentPage.groups}">
                <p class="empty-state"><spring:message code="${empty statusFilter ? 'inquiry.sent.empty' : 'inquiry.filter.empty'}"/></p>
            </c:when>
            <c:otherwise>
                <c:forEach items="${sentPage.groups}" var="group">
                    <section class="inbox-group">
                        <ui:inbox-group-header group="${group}"/>
                        <ul class="inbox-list">
                            <c:forEach items="${group.inquiries}" var="inquiry">
                                <li class="inbox-row">
                                    <span class="inbox-row__who"><c:out value="${group.sellerUsername}"/></span>
                                    <ui:inbox-last-message inquiry="${inquiry}" viewerId="${inquiry.buyerId}"/>
                                    <div class="inbox-row__end">
                                        <ui:inquiry-status status="${inquiry.status}"/>
                                        <c:choose>
                                            <c:when test="${inquiry.sale}">
                                                <ui:button label="${inquiry.awaitingPayment ? payLabel : viewSaleLabel}" size="sm"
                                                           href="/inquiries/${inquiry.id}"
                                                           variant="${inquiry.awaitingPayment ? 'primary' : 'ghost'}"/>
                                            </c:when>
                                            <c:otherwise>
                                                <c:url value="/inquiries/${inquiry.id}" var="detailUrl"/>
                                                <ui:button label="${openConversationLabel}" size="sm" url="${detailUrl}#conversation"
                                                           variant="ghost"/>
                                            </c:otherwise>
                                        </c:choose>
                                    </div>
                                </li>
                            </c:forEach>
                        </ul>
                    </section>
                </c:forEach>
                <ui:pagination currentPage="${sentPage.pageNumber}"
                               hasPrevious="${sentPage.hasPrevious}"
                               hasNext="${sentPage.hasNext}"
                               baseUrl="/inquiries/sent"
                               extraParams="${paginationParams}"
                               fragment="inquiries"
                               ariaLabel="${paginationLabel}"/>
            </c:otherwise>
        </c:choose>
    </section>
</main>
</body>
</html>
```

### landing/index

Filtros, orden, grilla, estado vacío y paginación.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/views/landing/index.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/landing/index.jsp>), líneas 1–223.

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="form" uri="http://www.springframework.org/tags/form" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<spring:message code="landing.search.clear" var="searchClearLabel"/>
<spring:message code="landing.search.empty.heading" var="searchEmptyHeading"/>
<spring:message code="landing.search.new" var="searchNewLabel"/>
<spring:message code="nav.back" var="backLabel"/>
<spring:message code="landing.results.count" var="countText">
    <spring:argument value="${total}"/>
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
<%-- Toda busqueda sin resultados, por texto, por filtros o por ambas, muestra la misma
     pagina del disco. Solo cambian el mensaje y las acciones. --%>
<c:set var="searchIsEmpty" value="${empty posts and (not empty query or hasFilters) and not catalogFilterErrors}"/>
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
<ui:site-header query="${query}" formId="catalog-filters"/>
<main class="page-shell">
    <c:if test="${postDeleted}"><p class="notice"><spring:message code="post.deleted"/></p></c:if>
    <%-- Vuelve aca despues de agregar un vinilo al carrito desde su ficha. --%>
    <c:if test="${not empty cartNotice}"><p class="notice"><spring:message code="${cartNotice}"/></p></c:if>
    <div class="catalog">
    <aside class="catalog__filters">
        <details class="filters" open>
            <summary class="filters__summary"><spring:message code="landing.filters.heading"/></summary>
            <h2 class="filters__heading"><spring:message code="landing.filters.heading"/></h2>
            <%-- El campo de busqueda del header tambien pertenece a este formulario (atributo
                 form): la lupa y "Aplicar" mandan juntos la busqueda y los filtros en pantalla. --%>
            <form:form cssClass="filters__form" id="catalog-filters" action="${searchUrl}" method="get"
                       modelAttribute="catalogFilterForm" novalidate="novalidate">
                <c:if test="${sort ne 'NEWEST'}">
                    <input type="hidden" name="sort" value="<c:out value="${sort}"/>"/>
                </c:if>
                <c:if test="${not empty selectedArtistId}">
                    <input type="hidden" name="artistId" value="<c:out value="${selectedArtistId}"/>"/>
                </c:if>
                <ui:select path="genre" label="${genreLabel}" items="${genres}" messagePrefix="genre"
                           emptyLabel="${anyLabel}" />
                <spring:bind path="condition">
                    <c:set var="conditionErrorId" value="condition-filter-error"/>
                    <ui:segmented-control name="condition" legend="${conditionLabel}" items="${conditions}"
                                          messagePrefix="condition" selectedValue="${status.value}"
                                          emptyLabel="${anyLabel}" hasError="${status.error}"
                                          errorId="${conditionErrorId}" />
                    <c:if test="${status.error}">
                        <div class="input-field__errors" id="${conditionErrorId}" role="alert">
                            <c:forEach items="${status.errorMessages}" var="errorMessage">
                                <p class="input-field__error"><c:out value="${errorMessage}"/></p>
                            </c:forEach>
                        </div>
                    </c:if>
                </spring:bind>
                <ui:text-input path="year" label="${yearLabel}" type="number"
                               min="${minimumYear}" max="${currentYear}" />
                <fieldset class="filter-group">
                    <legend class="filter-group__legend"><c:out value="${priceLabel}"/></legend>
                    <div class="filter-group__range">
                        <ui:text-input path="minPrice" label="${priceMinLabel}" type="number"
                                       min="${minimumPrice}" max="${maximumPrice}"
                                       externalErrorsId="price-range-errors" />
                        <ui:text-input path="maxPrice" label="${priceMaxLabel}" type="number"
                                       min="${minimumPrice}" max="${maximumPrice}"
                                       externalErrorsId="price-range-errors" />
                    </div>
                    <jsp:useBean id="priceRangeErrors" class="java.util.LinkedHashMap" scope="page"/>
                    <spring:bind path="minPrice">
                        <c:forEach items="${status.errorMessages}" var="errorMessage">
                            <c:set target="${priceRangeErrors}" property="${errorMessage}" value="${errorMessage}"/>
                        </c:forEach>
                    </spring:bind>
                    <spring:bind path="maxPrice">
                        <c:forEach items="${status.errorMessages}" var="errorMessage">
                            <c:set target="${priceRangeErrors}" property="${errorMessage}" value="${errorMessage}"/>
                        </c:forEach>
                    </spring:bind>
                    <c:if test="${not empty priceRangeErrors}">
                        <div class="input-field__errors" id="price-range-errors" role="alert">
                            <c:forEach items="${priceRangeErrors}" var="priceError">
                                <p class="input-field__error"><c:out value="${priceError.value}"/></p>
                            </c:forEach>
                        </div>
                    </c:if>
                </fieldset>
                <ui:button label="${applyLabel}" type="submit" size="sm"/>
            </form:form>
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
                <c:choose>
                    <c:when test="${not empty query and hasFilters}">
                        <spring:message code="landing.search.empty.combined" var="searchEmptyMessage">
                            <spring:argument value="${query}"/>
                        </spring:message>
                    </c:when>
                    <c:when test="${not empty query}">
                        <spring:message code="landing.search.empty" var="searchEmptyMessage">
                            <spring:argument value="${query}"/>
                        </spring:message>
                    </c:when>
                    <c:otherwise>
                        <spring:message code="landing.search.empty.filters" var="searchEmptyMessage"/>
                    </c:otherwise>
                </c:choose>
                <section class="not-found not-found--catalog">
                    <a class="not-found__record" href="<c:out value="${searchUrl}"/>"
                       aria-label="<c:out value="${backLabel}"/>">
                        <span class="not-found__code" aria-hidden="true"></span>
                    </a>
                    <div class="not-found__intro">
                        <ui:h1 text="${searchEmptyHeading}" tone="accent"/>
                        <ui:p text="${searchEmptyMessage}" variant="lead"/>
                        <div class="not-found__actions">
                            <%-- "Quitar filtros" conserva el texto buscado; "Nueva busqueda"
                                 vuelve al catalogo completo. clearHref ya viene de c:url. --%>
                            <c:if test="${hasFilters}">
                                <ui:button label="${searchClearLabel}" url="${clearHref}"/>
                            </c:if>
                            <c:if test="${not empty query}">
                                <ui:button label="${searchNewLabel}" variant="${hasFilters ? 'ghost' : 'primary'}" href="/"/>
                            </c:if>
                        </div>
                    </div>
                </section>
            </c:when>
            <%-- Sin texto ni filtros: el catalogo todavia no tiene publicaciones. Con errores de
                 filtro no se muestra nada aca: los errores ya estan junto a cada campo. --%>
            <c:when test="${empty posts and not catalogFilterErrors}">
                <p class="empty-state"><spring:message code="landing.empty"/></p>
            </c:when>
            <c:when test="${empty posts}"/>
            <c:otherwise>
                <ul class="post-grid">
                    <c:forEach items="${posts}" var="post">
                        <li>
                            <ui:vinyl-card item="${post}" variant="editorial"
                                          href="/post/${post.id}${empty returnQuery ? '' : '?from='}${returnQuery}"/>
                        </li>
                    </c:forEach>
                </ul>
            </c:otherwise>
        </c:choose>
        <c:if test="${not catalogFilterErrors}">
            <ui:pagination currentPage="${postPage.pageNumber}"
                           hasPrevious="${postPage.hasPrevious}"
                           hasNext="${postPage.hasNext}"
                           baseUrl="/"
                           extraParams="${paginationParams}"
                           ariaLabel="${paginationLabel}"/>
        </c:if>
    </section>
    </div>
</main>
</body>
</html>
```

### post/contact

Mensaje y elección de dirección.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/views/post/contact.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/post/contact.jsp>), líneas 1–68.

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="form" uri="http://www.springframework.org/tags/form" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<c:url value="/post/${post.id}/contact" var="contactUrl"/>
<c:url value="/profile" var="profileAddressesUrl"/>
<spring:message code="post.contact.heading" var="heading"/>
<spring:message code="post.contact.message.label" var="messageLabel"/>
<spring:message code="post.contact.submit" var="submitLabel"/>
<spring:message code="form.cancel" var="cancelLabel"/>
<spring:message code="post.contact.address.limit" var="addressLimitHint" arguments="${maxAddresses}"/>
<spring:message code="profile.addresses.label" var="addressesLabel"/>
<!DOCTYPE html>
<html lang="${pageContext.response.locale}">
<ui:head titleCode="post.contact.pageTitle"/>
<body>
<ui:site-header/>
<main class="page-shell">
    <ui:h1 text="${heading}"/>
    <c:if test="${addressLimitReached}">
        <p class="notice notice--warning"><c:out value="${addressLimitHint}"/></p>
    </c:if>
    <div class="contact-layout">
        <ui:vinyl-card item="${post}" variant="compact"/>
        <form:form cssClass="surface form-stack" action="${contactUrl}" method="post" modelAttribute="contactForm" data-submit-once="true">
            <p><spring:message code="post.contact.identity"/></p>
            <fieldset class="address-choice">
                <legend class="input-field__label"><spring:message code="post.contact.address.legend"/></legend>
                <form:errors path="addressId" element="p" cssClass="input-field__error"/>
                <c:forEach items="${addresses}" var="address">
                    <label class="address-choice__option">
                        <form:radiobutton path="addressId" value="${address.id}"/>
                        <ui:address address="${address}"/>
                    </label>
                </c:forEach>
                <c:choose>
                    <c:when test="${empty addresses}">
                        <%-- Sin libreta no hay nada que elegir: los campos se muestran directamente. --%>
                        <ui:address-fields/>
                    </c:when>
                    <c:when test="${canAddAddress}">
                        <label class="address-choice__option">
                            <%-- form:radiobutton compara el valor bindeado (null) con "" como strings y
                                 nunca queda checked: se arma a mano para que la opcion "nueva" quede
                                 marcada cuando no hay addressId, sin tocar el preseleccionado del GET. --%>
                            <input type="radio" id="addressIdNew" name="addressId" value=""<c:if test="${empty contactForm.addressId}"> checked="checked"</c:if>/>
                            <span><spring:message code="post.contact.address.new"/></span>
                        </label>
                        <div class="address-choice__new"><ui:address-fields/></div>
                    </c:when>
                    <c:otherwise>
                        <%-- Ya esta en el tope de direcciones: no se ofrece cargar una nueva. --%>
                        <p class="hint"><c:out value="${addressLimitHint}"/> <a href="${profileAddressesUrl}#addresses"><c:out value="${addressesLabel}"/></a></p>
                    </c:otherwise>
                </c:choose>
                <p class="hint"><spring:message code="post.contact.address.hint"/></p>
            </fieldset>
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

### post/detail

Ficha: galería, vendedor, acciones según quién mira.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/views/post/detail.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/post/detail.jsp>), líneas 1–183.

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="sec" uri="http://www.springframework.org/security/tags" %>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<c:choose>
    <c:when test="${empty post.coverImageId}">
        <c:url value="/images/covers/placeholder.svg" var="coverUrl"/>
    </c:when>
    <c:otherwise>
        <c:url value="/post/${post.id}/images/${post.coverImageId}" var="coverUrl"/>
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
<spring:message code="post.openInquiry.action" var="openInquiryLabel"/>
<spring:message code="cart.add" var="cartAddLabel"/>
<spring:message code="cart.inCart" var="inCartLabel"/>
<spring:message code="post.edit.action" var="editLabel"/>
<spring:message code="post.delete.action" var="deleteLabel"/>
<spring:message code="nav.backToProfile" var="backToProfileLabel"/>
<spring:message code="post.delete.dialog.title" var="deleteDialogTitle"/>
<spring:message code="post.delete.confirmation" var="deleteConfirmation">
    <spring:argument value="${post.title}"/>
    <spring:argument value="${post.artistName}"/>
</spring:message>
<!DOCTYPE html>
<html lang="${pageContext.response.locale}">
<ui:head titleCode="post.detail.pageTitle" pageScript="post-gallery"/>
<body>
<ui:site-header/>
<main class="page-shell">
    <c:choose>
        <c:when test="${not empty returnProfilePath}">
            <ui:back-link href="${returnProfilePath}" page="${returnProfilePage}" postStatus="${returnPostStatus}"
                          fragment="posts" label="${backToProfileLabel}"/>
        </c:when>
        <c:otherwise><ui:back-link href="/${empty returnQuery ? '' : '?'}${returnQuery}"/></c:otherwise>
    </c:choose>
    <c:if test="${postCreated}"><p class="notice"><spring:message code="post.created"/></p></c:if>
    <c:if test="${postUpdated}"><p class="notice"><spring:message code="post.updated"/></p></c:if>
    <c:if test="${not empty cartNotice}"><p class="notice"><spring:message code="${cartNotice}"/></p></c:if>
    <c:if test="${not empty cartWarning}"><p class="notice notice--warning"><spring:message code="${cartWarning}"/></p></c:if>
    <c:if test="${not empty cartFullLimit}"><p class="notice notice--warning"><spring:message code="cart.error.full" arguments="${cartFullLimit}"/></p></c:if>
    <c:set var="seller" value="${detail.seller}"/>
    <c:set var="galleryImageIds" value="${detail.galleryImageIds}"/>
    <article class="detail">
        <div class="detail__gallery">
            <div class="detail__cover">
                <img class="detail__image" src="<c:out value="${coverUrl}"/>" alt="<c:out value="${coverAlt}"/>" data-gallery-main/>
            </div>
            <c:if test="${fn:length(galleryImageIds) gt 1}">
                <div class="detail__thumbnails">
                    <c:forEach items="${galleryImageIds}" var="imageId" varStatus="photoStatus">
                        <c:url value="/post/${post.id}/images/${imageId}" var="photoUrl"/>
                        <spring:message code="post.gallery.photo" var="photoLabel">
                            <spring:argument value="${photoStatus.index + 1}"/>
                        </spring:message>
                        <a class="detail__thumbnail" href="<c:out value="${photoUrl}"/>"
                           aria-label="<c:out value="${photoLabel}"/>" data-gallery-thumb
                           <c:if test="${photoStatus.first}">aria-current="true"</c:if>>
                            <img src="<c:out value="${photoUrl}"/>" alt=""/>
                        </a>
                    </c:forEach>
                </div>
            </c:if>
        </div>
        <div class="detail__body">
            <div class="detail__heading">
                <div class="detail__title">
                    <ui:h1 text="${post.title}"/>
                    <ui:post-badge status="${post.status}"/>
                </div>
                <c:if test="${detail.editable}">
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
            <c:if test="${not empty seller}">
                <ui:user-byline userId="${seller.id}" username="${seller.username}" imageId="${seller.avatarImageId}" />
            </c:if>
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
                <%-- Que se ofrece lo decide CartService, con o sin sesion: la vista solo lo muestra. --%>
                <sec:authorize access="isAnonymous()">
                    <c:if test="${contact.contactable}">
                        <ui:button label="${contactLabel}" href="/post/${post.id}/contact"/>
                    </c:if>
                </sec:authorize>
                <sec:authorize access="isAuthenticated()">
                    <c:choose>
                        <c:when test="${contact.ownPost}">
                            <p class="hint"><spring:message code="post.detail.own"/></p>
                        </c:when>
                        <c:when test="${contact.openInquiryId.present}">
                            <%-- Ya lo consulto: se sigue en esa Conversacion, no se abre otra. --%>
                            <c:url value="/inquiries/${contact.openInquiryId.get()}" var="openInquiryUrl"/>
                            <ui:button label="${openInquiryLabel}" url="${openInquiryUrl}#conversation"/>
                        </c:when>
                        <c:when test="${contact.contactable}">
                            <ui:button label="${contactLabel}" href="/post/${post.id}/contact"/>
                            <c:choose>
                                <c:when test="${contact.inCart}">
                                    <ui:button label="${inCartLabel}" variant="ghost" href="/cart" icon="cart"/>
                                </c:when>
                                <c:otherwise>
                                    <c:url value="/cart/add/${post.id}" var="cartAddUrl"/>
                                    <form action="${cartAddUrl}" method="post">
                                        <sec:csrfInput/>
                                        <%-- Para volver al listado de donde vino despues de agregar. --%>
                                        <c:if test="${not empty returnQuery}"><input type="hidden" name="from" value="<c:out value="${returnQuery}"/>"/></c:if>
                                        <ui:button label="${cartAddLabel}" variant="ghost" type="submit" icon="cart"/>
                                    </form>
                                </c:otherwise>
                            </c:choose>
                        </c:when>
                    </c:choose>
                </sec:authorize>
            </div>
        </div>
    </article>
</main>
<c:if test="${detail.editable}">
<ui:confirm-dialog title="${deleteDialogTitle}" confirmLabel="${deleteLabel}" confirmVariant="danger"/>
</c:if>
</body>
</html>
```

### profile/index

Perfil privado: cuenta, contraseña, cobro, direcciones, publicaciones.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/views/profile/index.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/profile/index.jsp>), líneas 1–341.

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
<c:url value="/profile/avatar" var="profileAvatarUrl" />
<c:url value="/profile/payment" var="paymentUrl" />
<c:url value="/logout" var="logoutUrl" />
<spring:message code="profile.heading" var="heading" />
<spring:message code="publicProfile.openOwn" var="openPublicProfileLabel" />
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
<spring:message code="profile.posts.filter.label" var="postFilterLabel" />
<jsp:useBean id="postPaginationParams" class="java.util.LinkedHashMap" scope="page" />
<c:set target="${postPaginationParams}" property="postStatus" value="${postStatusFilter}" />
<jsp:useBean id="postLinkParams" class="java.util.LinkedHashMap" scope="page" />
<c:set target="${postLinkParams}" property="origin" value="${postOrigin}" />
<c:set target="${postLinkParams}" property="originPage" value="${postPage.pageNumber}" />
<c:if test="${not empty postStatusFilter}">
    <c:set target="${postLinkParams}" property="postStatus" value="${postStatusFilter}" />
</c:if>
<spring:message code="auth.logout.action" var="logoutLabel" />
<spring:message code="profile.payment.label" var="paymentLabel" />
<spring:message code="profile.payment.edit" var="paymentEditLabel" />
<spring:message code="profile.payment.empty" var="paymentEmpty" />
<spring:message code="profile.payment.cbu.label" var="cbuLabel" />
<spring:message code="profile.payment.alias.label" var="aliasLabel" />
<spring:message code="profile.payment.hint" var="paymentHint" />
<spring:message code="profile.addresses.label" var="addressesLabel" />
<spring:message code="profile.addresses.edit" var="addressesEditLabel" />
<spring:message code="profile.addresses.add" var="addAddressLabel" />
<spring:message code="profile.addresses.editOne" var="editAddressLabel" />
<spring:message code="profile.addresses.delete" var="deleteAddressLabel" />
<spring:message code="profile.addresses.empty" var="addressesEmptyLabel" />
<spring:message code="profile.addresses.limit" var="addressLimitHint" arguments="${maxAddresses}" />
<spring:message code="profile.avatar.heading" var="avatarHeading" />
<spring:message code="profile.avatar.label" var="avatarChangeLabel" />
<spring:message code="profile.avatar.remove" var="removeAvatarLabel" />
<spring:message code="list.and" var="listAnd" />
<spring:message code="confirm.title" var="confirmTitle" />
<spring:message code="confirm.action" var="confirmAction" />
<!DOCTYPE html>
<html lang="${pageContext.response.locale}">
<ui:head titleCode="profile.pageTitle" pageScript="account-edit" />
<body>
<ui:site-header />
<main class="page-shell">
    <div class="profile-heading">
        <ui:h1 text="${heading}" />
        <ui:button label="${openPublicProfileLabel}" href="/users/${profileUser.id}" variant="ghost" size="sm" icon="arrow-up-right" />
    </div>
    <c:if test="${profileUpdated}">
        <p class="notice"><spring:message code="profile.updated" /></p>
    </c:if>
    <c:if test="${avatarUpdated}"><p class="notice"><spring:message code="profile.avatar.updated" /></p></c:if>
    <%-- Sin el dialogo el aviso va aca; con el dialogo se muestra adentro y el JS oculta este. --%>
    <c:if test="${avatarInvalid}"><p class="notice notice--warning" data-avatar-page-error><spring:message code="profile.avatar.invalid" /></p></c:if>
    <c:if test="${paymentUpdated}">
        <p class="notice"><spring:message code="profile.payment.updated" /></p>
    </c:if>
    <c:if test="${addressSaved}">
        <p class="notice"><spring:message code="profile.addresses.saved" /></p>
    </c:if>
    <c:if test="${addressDeleted}">
        <p class="notice"><spring:message code="profile.addresses.deleted" /></p>
    </c:if>
    <c:if test="${addressLimitReached}">
        <p class="notice notice--warning"><c:out value="${addressLimitHint}" /></p>
    </c:if>
    <c:if test="${paymentMissing}">
        <p class="notice notice--warning"><spring:message code="profile.payment.missing" /></p>
    </c:if>
    <section class="surface profile-account" id="account">
        <h2><spring:message code="profile.account.heading" /></h2>
        <div class="account-rows">
            <%-- Fila de la foto: solo la foto, que abre el dialogo para cambiarla o quitarla. Sin JS
                 (o sin soporte de dialogos) queda el form nativo; el JS lo cambia por la foto
                 recien cuando el dialogo esta listo. --%>
            <div class="account-row account-row--static" id="avatar">
                <div class="account-row__summary">
                    <span class="account-row__label"><c:out value="${avatarHeading}" /></span>
                    <div class="avatar-row">
                        <button type="button" class="avatar-row__open" aria-haspopup="dialog" aria-controls="avatar-dialog"
                                aria-label="<c:out value="${avatarChangeLabel}" />" title="<c:out value="${avatarChangeLabel}" />" data-avatar-open hidden>
                            <ui:avatar userId="${profileUser.id}" imageId="${accountAppearance.avatarImageId}" name="${profileUser.username}" size="md" alt="" />
                        </button>
                        <form action="<c:out value="${profileAvatarUrl}" />" method="post" enctype="multipart/form-data"
                              class="avatar-row__fallback" data-avatar-fallback>
                            <sec:csrfInput />
                            <ui:avatar userId="${profileUser.id}" imageId="${accountAppearance.avatarImageId}" name="${profileUser.username}" size="md" alt="" />
                            <ui:input-control id="avatar-file-fallback" name="avatar" type="file" ariaLabel="${avatarChangeLabel}"
                                              accept="${acceptedImageTypes}" />
                            <ui:button label="${saveLabel}" type="submit" size="sm" />
                            <c:if test="${not empty accountAppearance.avatarImageId}">
                                <ui:button label="${removeAvatarLabel}" type="submit" variant="ghost" size="sm" name="remove" value="true" />
                            </c:if>
                        </form>
                    </div>
                </div>
            </div>
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
            <details class="account-row" <c:if test="${paymentEditOpen}">open</c:if>>
                <summary class="account-row__summary">
                    <span class="account-row__label"><c:out value="${paymentLabel}" /></span>
                    <span class="account-row__value">
                        <c:choose>
                            <c:when test="${profileUser.hasPaymentInfo()}">
                                <c:if test="${not empty profileUser.paymentInfo.cbu}"><c:out value="${profileUser.paymentInfo.cbu}" /></c:if>
                                <c:if test="${not empty profileUser.paymentInfo.alias}"><span class="account-row__secondary"><c:out value="${profileUser.paymentInfo.alias}" /></span></c:if>
                            </c:when>
                            <c:otherwise><span class="account-row__empty"><c:out value="${paymentEmpty}" /></span></c:otherwise>
                        </c:choose>
                    </span>
                    <span class="account-row__edit" role="img" aria-label="<c:out value="${paymentEditLabel}" />"><ui:icon name="pencil"/></span>
                </summary>
                <form:form cssClass="account-row__form" action="${paymentUrl}" method="post" modelAttribute="paymentForm">
                    <c:if test="${not empty returnInquiryId}"><input type="hidden" name="returnInquiryId" value="<c:out value="${returnInquiryId}" />" /></c:if>
                    <ui:text-input path="cbu" label="${cbuLabel}" maxLength="30" autofocus="${paymentEditOpen}" />
                    <ui:text-input path="alias" label="${aliasLabel}" maxLength="20" />
                    <div class="account-row__actions">
                        <ui:button label="${saveLabel}" type="submit" />
                        <ui:button label="${cancelLabel}" variant="ghost" url="${cancelUrl}#account" data="cancel-edit" />
                    </div>
                    <p class="hint account-row__hint"><c:out value="${paymentHint}" /></p>
                    <input type="hidden" name="page" value="<c:out value="${postPage.pageNumber}" />" />
                </form:form>
            </details>
            <details class="account-row" id="addresses" <c:if test="${addressesOpen}">open</c:if>>
                <summary class="account-row__summary">
                    <span class="account-row__label"><c:out value="${addressesLabel}" /></span>
                    <c:choose>
                        <c:when test="${empty addresses}">
                            <span class="account-row__value"><c:out value="${addressesEmptyLabel}" /></span>
                        </c:when>
                        <c:otherwise>
                            <%-- Calle + altura de cada activa, mas nueva primero, con la conjuncion
                                 i18n antes de la ultima. Se arma en una var y recien se vuelca con
                                 c:out, que escapa tanto el texto visible como el title del hover. --%>
                            <c:set var="addressSummary" value="" />
                            <c:forEach items="${addresses}" var="summaryAddress" varStatus="summaryStatus">
                                <c:choose>
                                    <c:when test="${summaryStatus.first}">
                                        <c:set var="addressSummary" value="${summaryAddress.street} ${summaryAddress.streetNumber}" />
                                    </c:when>
                                    <c:when test="${summaryStatus.last}">
                                        <c:set var="addressSummary" value="${addressSummary} ${listAnd} ${summaryAddress.street} ${summaryAddress.streetNumber}" />
                                    </c:when>
                                    <c:otherwise>
                                        <c:set var="addressSummary" value="${addressSummary}, ${summaryAddress.street} ${summaryAddress.streetNumber}" />
                                    </c:otherwise>
                                </c:choose>
                            </c:forEach>
                            <span class="account-row__value account-row__value--truncate" title="<c:out value="${addressSummary}" />"><c:out value="${addressSummary}" /></span>
                        </c:otherwise>
                    </c:choose>
                    <span class="account-row__edit" role="img" aria-label="<c:out value="${addressesEditLabel}" />"><ui:icon name="pencil"/></span>
                </summary>
                <div class="account-row__form">
                    <c:if test="${not empty addresses}">
                        <ul class="address-list">
                            <c:forEach items="${addresses}" var="address">
                                <li class="address-list__item">
                                    <ui:address address="${address}" />
                                    <div class="address-list__actions">
                                        <c:url value="/profile" var="editAddressUrl"><c:param name="editAddress" value="${address.id}" /><c:param name="page" value="${postPage.pageNumber}" /></c:url>
                                        <ui:button label="${editAddressLabel}" variant="ghost" size="sm" url="${editAddressUrl}#addresses" icon="pencil" />
                                        <c:url value="/profile/addresses/${address.id}/delete" var="deleteAddressUrl" />
                                        <spring:message code="profile.addresses.delete.confirmation" var="deleteAddressConfirmation">
                                            <spring:argument value="${address.street} ${address.streetNumber}" />
                                        </spring:message>
                                        <form action="${deleteAddressUrl}" method="post" data-confirm-message="<c:out value="${deleteAddressConfirmation}" />">
                                            <sec:csrfInput />
                                            <ui:button label="${deleteAddressLabel}" variant="danger-outline" size="sm" type="submit" icon="trash" />
                                        </form>
                                    </div>
                                </li>
                            </c:forEach>
                        </ul>
                    </c:if>
                    <c:choose>
                        <%-- Editando siempre se muestra el formulario, aunque ya este en el tope:
                             es la unica forma de terminar esa edicion. --%>
                        <c:when test="${not empty editingAddressId or canAddAddress}">
                            <c:choose>
                                <c:when test="${not empty editingAddressId}"><c:url value="/profile/addresses/${editingAddressId}/edit" var="addressFormUrl" /></c:when>
                                <c:otherwise><c:url value="/profile/addresses" var="addressFormUrl" /></c:otherwise>
                            </c:choose>
                            <form:form cssClass="form-stack" action="${addressFormUrl}" method="post" modelAttribute="addressForm">
                                <h3 class="account-row__subheading"><c:out value="${empty editingAddressId ? addAddressLabel : editAddressLabel}" /></h3>
                                <ui:address-fields />
                                <div class="account-row__actions">
                                    <ui:button label="${saveLabel}" type="submit" />
                                    <%-- Editando, Cancelar navega: cerrar la fila por JS dejaria el formulario
                                         apuntando a la edicion, y un alta posterior reemplazaria esa direccion. --%>
                                    <ui:button label="${cancelLabel}" variant="ghost" url="${cancelUrl}#addresses" data="${empty editingAddressId ? 'cancel-edit' : ''}" />
                                </div>
                                <input type="hidden" name="page" value="<c:out value="${postPage.pageNumber}" />" />
                            </form:form>
                        </c:when>
                        <c:otherwise>
                            <p class="notice notice--warning"><c:out value="${addressLimitHint}" /></p>
                        </c:otherwise>
                    </c:choose>
                </div>
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
        <c:if test="${postStatusCounts.total gt 0}">
            <ui:filter-chips baseUrl="/profile" paramName="postStatus" values="${postStatuses}"
                             active="${postStatusFilter}" counts="${postStatusCounts.counts}"
                             messagePrefix="profile.posts.filter" label="${postFilterLabel}" fragment="posts"/>
        </c:if>
        <c:if test="${postDeleted}">
            <p class="notice"><spring:message code="post.deleted" /></p>
        </c:if>
        <c:choose>
            <c:when test="${empty postPage.posts}">
                <p class="empty-state"><spring:message code="${empty postStatusFilter ? 'profile.posts.empty' : 'profile.posts.filter.empty'}" /></p>
            </c:when>
            <c:otherwise>
                <ul class="post-grid profile-posts__grid">
                    <c:forEach items="${postPage.posts}" var="post">
                        <li>
                            <ui:vinyl-card item="${post}" variant="editorial" href="/post/${post.id}"
                                            hrefParams="${postLinkParams}" showStatus="${true}"/>
                        </li>
                    </c:forEach>
                </ul>
                <ui:pagination currentPage="${postPage.pageNumber}"
                               hasPrevious="${postPage.hasPrevious}"
                               hasNext="${postPage.hasNext}"
                               baseUrl="/profile"
                               extraParams="${postPaginationParams}"
                               fragment="posts"
                               ariaLabel="${paginationLabel}"/>
            </c:otherwise>
        </c:choose>
    </section>
</main>
<spring:message code="profile.avatar.close" var="avatarCloseLabel" />
<%-- Dialogo de la foto de perfil. Elegir, soltar o quitar la foto solo cambia la vista previa;
     Guardar manda el form (la imagen, o remove=true). Si el servidor rechazo la imagen, abre
     solo con el aviso, que es el mismo que muestra el JS al elegir una invalida. --%>
<dialog class="confirm-dialog avatar-dialog" id="avatar-dialog" aria-labelledby="avatar-dialog-title"
        <c:if test="${avatarInvalid}">data-open-on-load</c:if>>
    <%-- data-max-bytes es el mismo tope que valida el servidor: el JS solo avisa antes de subir. --%>
    <form action="<c:out value="${profileAvatarUrl}" />" method="post" enctype="multipart/form-data"
          class="confirm-dialog__content" data-avatar-form data-submit-once data-max-bytes="<c:out value="${maxImageBytes}" />">
        <sec:csrfInput />
        <div class="avatar-dialog__header">
            <h2 class="confirm-dialog__title" id="avatar-dialog-title"><c:out value="${avatarHeading}" /></h2>
            <button type="button" class="avatar-dialog__close" aria-label="<c:out value="${avatarCloseLabel}" />" data-avatar-close><ui:icon name="x" /></button>
        </div>
        <p class="notice notice--warning" data-avatar-error<c:if test="${not avatarInvalid}"> hidden</c:if>><spring:message code="profile.avatar.invalid" /></p>
        <ui:input-control id="avatar-file" name="avatar" type="file" ariaLabel="${avatarChangeLabel}"
                          cssClass="avatar-dialog__input" accept="${acceptedImageTypes}" describedBy="avatar-hint" />
        <label for="avatar-file" class="avatar-dropzone" data-avatar-dropzone>
            <ui:avatar userId="${profileUser.id}" imageId="${accountAppearance.avatarImageId}" name="${profileUser.username}" size="lg" alt="" preview="${true}" />
            <span class="avatar-dropzone__text" data-avatar-drop-text><spring:message code="profile.avatar.drop" /></span>
            <span class="avatar-dropzone__text" data-avatar-uploading hidden><spring:message code="profile.avatar.uploading" /></span>
            <span class="hint" id="avatar-hint"><spring:message code="profile.avatar.hint" /></span>
        </label>
        <input type="hidden" name="remove" value="false" data-avatar-remove-flag />
        <div class="confirm-dialog__actions avatar-dialog__actions">
            <ui:button label="${removeAvatarLabel}" variant="ghost" size="sm" icon="trash" data="avatar-remove" />
            <ui:button label="${cancelLabel}" variant="ghost" size="sm" data="avatar-close" />
            <ui:button label="${saveLabel}" type="submit" size="sm" data="avatar-save" />
        </div>
    </form>
</dialog>
<ui:confirm-dialog title="${confirmTitle}" confirmLabel="${confirmAction}" confirmVariant="danger" />
</body>
</html>
```

### profile/public

Perfil público: reputación, publicaciones, reseñas.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/views/profile/public.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/profile/public.jsp>), líneas 1–108.

```jsp
<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt" %>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="sec" uri="http://www.springframework.org/security/tags" %>
<%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %>
<c:set var="publicUser" value="${profile.user}" />
<c:set var="postPage" value="${profile.postPage}" />
<c:set var="reviewPage" value="${profile.reviewPage}" />
<c:set var="reviewStats" value="${reviewPage.stats}" />
<spring:message code="publicProfile.avatar.alt" var="avatarAlt"><spring:argument value="${publicUser.username}" /></spring:message>
<spring:message code="publicProfile.posts.pagination" var="paginationLabel" />
<spring:message code="publicProfile.editOwn" var="editOwnLabel" />
<spring:message code="publicProfile.reviews.role" var="roleLabel" />
<spring:message code="publicProfile.reviews.apply" var="applyReviewsLabel" />
<spring:message code="publicProfile.reviews.pagination" var="reviewsPaginationLabel" />
<c:url value="/users/${publicUser.id}" var="profileUrl"/>
<jsp:useBean id="postsPaginationParams" class="java.util.LinkedHashMap" scope="page" />
<c:set target="${postsPaginationParams}" property="reviewRole" value="${reviewPage.role}" />
<c:set target="${postsPaginationParams}" property="reviewPage" value="${reviewPage.pageNumber}" />
<jsp:useBean id="reviewsPaginationParams" class="java.util.LinkedHashMap" scope="page" />
<c:set target="${reviewsPaginationParams}" property="reviewRole" value="${reviewPage.role}" />
<c:set target="${reviewsPaginationParams}" property="page" value="${postPage.pageNumber}" />
<jsp:useBean id="postLinkParams" class="java.util.LinkedHashMap" scope="page" />
<c:set target="${postLinkParams}" property="origin" value="${postOrigin}" />
<c:set target="${postLinkParams}" property="originPage" value="${postPage.pageNumber}" />
<!DOCTYPE html>
<html lang="${pageContext.response.locale}">
<ui:head titleCode="publicProfile.pageTitle" />
<body>
<ui:site-header />
<main class="page-shell">
    <sec:authorize access="isAuthenticated()">
        <sec:authentication property="principal.id" var="currentUserId" scope="page" />
    </sec:authorize>
    <header class="profile-hero">
        <ui:avatar userId="${publicUser.id}" imageId="${publicUser.avatarImageId}" name="${publicUser.username}" size="xl" alt="${avatarAlt}" />
        <div class="profile-hero__body">
            <ui:h1 text="${publicUser.username}" />
            <c:if test="${reviewStats.count gt 0}">
                <fmt:formatNumber value="${reviewStats.average}" maxFractionDigits="1" minFractionDigits="1" var="averageRating"/>
                <spring:message code="publicProfile.reputation.summary" var="ratingSummary">
                    <spring:argument value="${averageRating}"/>
                    <spring:argument value="${reviewStats.count}"/>
                </spring:message>
                <p class="profile-reputation">
                    <span aria-hidden="true"><c:out value="${averageRating}"/></span>
                    <ui:rating value="${reviewStats.average}" maxRating="${maxRating}" label="${ratingSummary}"/>
                    <span class="text text--muted" aria-hidden="true"><spring:message code="publicProfile.reviews.count"><spring:argument value="${reviewStats.count}"/></spring:message></span>
                </p>
            </c:if>
        </div>
        <c:if test="${currentUserId eq publicUser.id}">
            <div class="profile-hero__actions">
                <ui:button label="${editOwnLabel}" href="/profile" variant="ghost" size="sm" icon="pencil" />
            </div>
        </c:if>
    </header>
    <section class="profile-posts" id="posts">
        <h2 class="text text-h3"><spring:message code="publicProfile.posts.heading" /></h2>
        <c:choose>
            <c:when test="${empty postPage.posts}"><p class="empty-state"><spring:message code="publicProfile.posts.empty" /></p></c:when>
            <c:otherwise>
                <ul class="post-grid profile-posts__grid">
                    <c:forEach items="${postPage.posts}" var="post">
                        <li><ui:vinyl-card item="${post}" variant="editorial" href="/post/${post.id}"
                                            hrefParams="${postLinkParams}" /></li>
                    </c:forEach>
                </ul>
                <%-- La ruta va sin c:url: pagination-link la arma con el context path. --%>
                <ui:pagination currentPage="${postPage.pageNumber}" hasPrevious="${postPage.hasPrevious}"
                               hasNext="${postPage.hasNext}" baseUrl="/users/${publicUser.id}" fragment="posts"
                               extraParams="${postsPaginationParams}" ariaLabel="${paginationLabel}" />
            </c:otherwise>
        </c:choose>
    </section>
    <section class="profile-reviews" id="reviews">
        <div class="profile-reviews__header">
            <h2 class="text text-h3"><spring:message code="publicProfile.reviews.heading" /></h2>
            <form method="get" action="<c:out value="${profileUrl}"/>#reviews"
                  class="profile-reviews__filter" data-auto-submit>
                <input type="hidden" name="page" value="<c:out value="${postPage.pageNumber}"/>"/>
                <ui:segmented-control name="reviewRole" legend="${roleLabel}" hideLegend="true" items="${reviewRoles}"
                                      messagePrefix="publicProfile.reviews.role" selectedValue="${reviewPage.role}"/>
                <ui:button label="${applyReviewsLabel}" type="submit" variant="secondary" size="sm"/>
            </form>
        </div>
            <c:choose>
                <c:when test="${reviewStats.count gt 0}">
                    <ul class="profile-reviews__list">
                        <c:forEach items="${reviewPage.reviews}" var="review">
                            <li class="profile-reviews__item">
                                <ui:review-content maxRating="${maxRating}" review="${review}" showAuthor="true"/>
                            </li>
                        </c:forEach>
                    </ul>
                    <ui:pagination currentPage="${reviewPage.pageNumber}" hasPrevious="${reviewPage.hasPrevious}"
                                   hasNext="${reviewPage.hasNext}" baseUrl="/users/${publicUser.id}" pageParam="reviewPage"
                                   extraParams="${reviewsPaginationParams}" fragment="reviews" ariaLabel="${reviewsPaginationLabel}"/>
                </c:when>
                <c:otherwise>
                    <p class="empty-state"><spring:message code="publicProfile.reviews.empty.${reviewPage.role}"/></p>
                </c:otherwise>
            </c:choose>
    </section>
</main>
</body>
</html>
```

### publish/index

Publicar y editar comparten vista.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/views/publish/index.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/publish/index.jsp>), líneas 1–155.

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
<spring:message code="publish.gallery.existing" var="existingImagesLabel"/>
<spring:message code="form.cancel" var="cancelLabel"/>
<c:choose>
    <c:when test="${not empty existingCoverImageId}">
        <c:url value="/post/${postId}/images/${existingCoverImageId}" var="previewCoverUrl"/>
    </c:when>
    <c:otherwise>
        <c:url value="/images/covers/placeholder.svg" var="previewCoverUrl"/>
    </c:otherwise>
</c:choose>
<c:choose>
    <c:when test="${not empty fallbackCoverImageId}">
        <c:url value="/post/${postId}/images/${fallbackCoverImageId}" var="fallbackCoverUrl"/>
    </c:when>
    <c:otherwise>
        <c:url value="/images/covers/placeholder.svg" var="fallbackCoverUrl"/>
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
                   data-publish-form="true" novalidate="novalidate">
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
                    <ui:text-input path="releaseYear" label="${releaseYearLabel}" type="number"
                                   min="${minimumYear}" max="${currentYear}"/>
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
                    <ui:text-input path="price" label="${priceLabel}" type="number"
                                   min="${minimumPrice}" max="${maximumPrice}"/>
                    <ui:text-input path="zone" label="${zoneLabel}" maxLength="100"/>
                    <ui:text-input path="pressingYear" label="${pressingYearLabel}" type="number"
                                   min="${minimumYear}" max="${currentYear}"/>
                </div>
                <div class="form-layout__row form-layout__row--content">
                    <ui:textarea path="description" label="${descriptionLabel}" maxLength="1000"/>
                    <div class="input-field">
                        <form:label path="covers" cssClass="input-field__label"><spring:message code="publish.cover.label"/></form:label>
                        <ui:input-control id="covers" name="covers" type="file" accept="${acceptedImageTypes}"
                                          multiple="${true}" />
                        <p class="hint"><spring:message code="publish.cover.hint"/></p>
                        <form:errors path="covers" cssClass="input-field__error" element="p"/>
                        <c:if test="${editing and not empty uploadedImageIds}">
                            <div class="publish-gallery" role="group" aria-label="<c:out value="${existingImagesLabel}"/>">
                                <c:forEach items="${uploadedImageIds}" var="imageId" varStatus="photoStatus">
                                    <c:url value="/post/${postId}/images/${imageId}" var="uploadedImageUrl"/>
                                    <spring:message code="publish.gallery.remove" var="removeImageLabel">
                                        <spring:argument value="${photoStatus.index + 1}"/>
                                    </spring:message>
                                    <spring:message code="publish.gallery.restore" var="restoreImageLabel">
                                        <spring:argument value="${photoStatus.index + 1}"/>
                                    </spring:message>
                                    <div class="publish-gallery__item">
                                        <img src="<c:out value="${uploadedImageUrl}"/>" alt="" data-existing-image/>
                                        <form:checkbox path="removedImageIds" value="${imageId}" id="remove-image-${imageId}"
                                                       cssClass="publish-gallery__remove-input"/>
                                        <label for="remove-image-<c:out value="${imageId}"/>" class="publish-gallery__remove">
                                            <span class="publish-gallery__remove-icon" aria-hidden="true"
                                                  title="<c:out value="${removeImageLabel}"/>">&times;</span>
                                            <span class="publish-gallery__restore-icon" aria-hidden="true"
                                                  title="<c:out value="${restoreImageLabel}"/>">&#8634;</span>
                                            <span class="visually-hidden"><c:out value="${removeImageLabel}"/></span>
                                        </label>
                                    </div>
                                </c:forEach>
                            </div>
                        </c:if>
                    </div>
                </div>
                <div class="form-stack__actions">
                    <ui:button label="${submitLabel}" type="submit"/>
                    <ui:button label="${cancelLabel}" variant="ghost" href="${cancelHref}"/>
                </div>
            </div>
        </form:form>
        <aside class="publish-preview" aria-labelledby="publish-preview-heading"
               data-fallback-cover="<c:out value="${fallbackCoverUrl}"/>"
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

## Código de los scripts

### account-edit.js

Filas editables del perfil y diálogo de la foto.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/js/account-edit.js](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/js/account-edit.js>), líneas 1–256.

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

        initAvatarDialog();
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
        // El form del propio boton: la fila de direcciones tiene tambien los de eliminar.
        var form = cancel.closest('form') || row.querySelector('form');
        if (form) {
            form.reset();
        }
        row.removeAttribute('open');
        var summary = row.querySelector('summary');
        if (summary) {
            summary.focus();
        }
    });
    // Foto de perfil: la foto de la fila abre el dialogo. Elegir, soltar o quitar la foto solo
    // cambia la vista previa; Guardar manda el form y Cancelar descarta el cambio. Los tipos
    // (accept del input) y el tope (data-max-bytes del form) los manda el servidor desde
    // ImageRules: es solo un aviso temprano, el servidor valida igual.
    function initAvatarDialog() {
        var dialog = document.getElementById('avatar-dialog');
        var openButton = document.querySelector('[data-avatar-open]');
        // Sin soporte de dialogos queda el form nativo de la fila, con el aviso arriba.
        if (!dialog || !openButton || typeof dialog.showModal !== 'function') {
            return;
        }
        var form = dialog.querySelector('[data-avatar-form]');
        var input = form.querySelector('input[type="file"]');
        var acceptedTypes = (input.getAttribute('accept') || '').split(',');
        var maxBytes = Number(form.getAttribute('data-max-bytes'));
        var dropzone = form.querySelector('[data-avatar-dropzone]');
        var error = form.querySelector('[data-avatar-error]');
        var image = form.querySelector('[data-avatar-preview]');
        var placeholder = form.querySelector('[data-avatar-placeholder]');
        var removeFlag = form.querySelector('[data-avatar-remove-flag]');
        var removeButton = form.querySelector('[data-avatar-remove]');
        var saveButton = form.querySelector('[data-avatar-save]');
        var dropText = form.querySelector('[data-avatar-drop-text]');
        var uploadingText = form.querySelector('[data-avatar-uploading]');
        var fallback = document.querySelector('[data-avatar-fallback]');
        var pageError = document.querySelector('[data-avatar-page-error]');
        var originalSrc = image.getAttribute('src');
        var stagedFiles = null;
        var objectUrl = null;
        var pressedOnBackdrop = false;

        // El dialogo reemplaza al form nativo y su aviso, en el mismo tick: sin parpadeo.
        openButton.hidden = false;
        if (fallback) {
            fallback.hidden = true;
        }
        if (pageError) {
            pageError.hidden = true;
        }

        function showPreview(src) {
            if (src) {
                image.src = src;
            } else {
                image.removeAttribute('src');
            }
            image.hidden = !src;
            placeholder.hidden = !!src;
            removeButton.hidden = !src;
        }

        function releaseObjectUrl() {
            if (objectUrl) {
                window.URL.revokeObjectURL(objectUrl);
                objectUrl = null;
            }
        }

        function showUploading(uploading) {
            dropText.hidden = uploading;
            uploadingText.hidden = !uploading;
        }

        function render() {
            var removing = removeFlag.value === 'true';
            releaseObjectUrl();
            if (stagedFiles) {
                objectUrl = window.URL.createObjectURL(stagedFiles[0]);
                showPreview(objectUrl);
            } else {
                showPreview(removing ? null : originalSrc);
            }
            saveButton.disabled = !stagedFiles && !removing;
        }

        function reset() {
            stagedFiles = null;
            removeFlag.value = 'false';
            input.value = '';
            error.hidden = true;
            render();
        }

        function stage(files) {
            var file = files && files[0];
            // Sin archivo (p. ej. una imagen arrastrada desde otra pagina), de otro tipo o mas
            // pesado que el tope: aviso, y se conserva lo que ya estaba elegido.
            if (!file || acceptedTypes.indexOf(file.type) === -1 || file.size > maxBytes) {
                error.hidden = false;
                if (stagedFiles) {
                    input.files = stagedFiles;
                } else {
                    input.value = '';
                }
                return;
            }
            if (input.files !== files) {
                input.files = files;
            }
            stagedFiles = input.files;
            removeFlag.value = 'false';
            error.hidden = true;
            render();
        }

        openButton.addEventListener('click', function () {
            dialog.showModal();
        });
        dialog.querySelectorAll('[data-avatar-close]').forEach(function (button) {
            button.addEventListener('click', function () {
                reset();
                dialog.close();
            });
        });
        // Clic en el fondo: el target es el propio dialog, no su contenido. Tiene que haber
        // empezado tambien en el fondo: un arrastre desde adentro (p. ej. seleccionando texto)
        // que se suelta afuera no descarta el cambio.
        dialog.addEventListener('pointerdown', function (event) {
            pressedOnBackdrop = event.target === dialog;
        });
        dialog.addEventListener('click', function (event) {
            var fromBackdrop = pressedOnBackdrop;
            pressedOnBackdrop = false;
            if (event.target === dialog && fromBackdrop) {
                dialog.close();
            }
        });
        // Esc tambien cierra: descarta el cambio. Si ya se reabrio, no pisa lo nuevo.
        dialog.addEventListener('close', function () {
            if (dialog.open) {
                return;
            }
            reset();
            openButton.focus();
        });

        removeButton.addEventListener('click', function () {
            stagedFiles = null;
            input.value = '';
            // Quitar algo que todavia no se guardo solo vuelve a la foto actual.
            removeFlag.value = originalSrc ? 'true' : 'false';
            error.hidden = true;
            render();
        });

        // submit-once.js deshabilita Guardar y marca aria-busy; aca solo cambia el texto. Si
        // submit-once frena un segundo envio, no hay nada que cambiar.
        form.addEventListener('submit', function (event) {
            if (!event.defaultPrevented) {
                showUploading(true);
            }
        });
        // Al volver desde bfcache, submit-once rehabilita Guardar (su pageshow se registra
        // antes que este): se vuelve a pintar para que quede deshabilitado si no hay cambio, y
        // con la vista previa de nuevo, porque pagehide libero su URL.
        window.addEventListener('pageshow', function () {
            showUploading(false);
            render();
        });

        input.addEventListener('change', function () {
            stage(input.files);
        });

        // Todo el dialogo (y el velo, cuyos eventos llegan al dialog) acepta soltar: si solo
        // aceptara la zona punteada, soltar al lado haria que el navegador abra el archivo.
        var dragDepth = 0;
        dialog.addEventListener('dragenter', function (event) {
            event.preventDefault();
            dragDepth++;
            dropzone.classList.add('avatar-dropzone--active');
        });
        dialog.addEventListener('dragover', function (event) {
            event.preventDefault();
            event.dataTransfer.dropEffect = 'copy';
        });
        dialog.addEventListener('dragleave', function () {
            dragDepth = Math.max(0, dragDepth - 1);
            if (dragDepth === 0) {
                dropzone.classList.remove('avatar-dropzone--active');
            }
        });
        dialog.addEventListener('drop', function (event) {
            event.preventDefault();
            dragDepth = 0;
            dropzone.classList.remove('avatar-dropzone--active');
            stage(event.dataTransfer.files);
        });
        // Con el dialogo abierto, un archivo soltado fuera de el no navega al archivo.
        ['dragover', 'drop'].forEach(function (type) {
            document.addEventListener(type, function (event) {
                if (dialog.open) {
                    event.preventDefault();
                }
            });
        });
        window.addEventListener('pagehide', releaseObjectUrl);

        render();
        if (dialog.hasAttribute('data-open-on-load')) {
            dialog.showModal();
        }
    }
})();
```

### autocomplete.js

Sugerencias: espera, número de secuencia, JSON y nodos armados con textContent.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/js/autocomplete.js](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/js/autocomplete.js>), líneas 1–370.

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

        function appendText(parent, className, text) {
            var span = document.createElement('span');
            span.className = className;
            span.textContent = text;
            parent.appendChild(span);
        }

        // Cada opcion toma el id de la lista en singular: site-search-suggestions -> site-search-suggestion-0.
        // El texto va siempre por textContent: un titulo con < o & se muestra tal cual.
        function createOption(item, index) {
            var option = document.createElement('li');
            option.className = 'autocomplete__option';
            option.id = list.id.replace(/s$/, '') + '-' + index;
            option.setAttribute('role', 'option');
            option.setAttribute('data-autocomplete-option', '');
            option.setAttribute('data-value', item.value);
            option.setAttribute('aria-selected', 'false');
            if (!item.typeLabel) {
                option.textContent = item.value;
                return option;
            }
            option.classList.add('autocomplete__option--rich');
            var main = document.createElement('span');
            main.className = 'autocomplete__option-main';
            appendText(main, 'autocomplete__option-value', item.value);
            if (item.detail) {
                appendText(main, 'autocomplete__option-detail', item.detail);
            }
            option.appendChild(main);
            appendText(option, 'autocomplete__option-type', item.typeLabel);
            return option;
        }

        function show(items) {
            list.replaceChildren.apply(list, items.map(createOption));
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
                headers: {'Accept': 'application/json', 'X-Requested-With': 'XMLHttpRequest'}
            }).then(function (response) {
                if (!response.ok) {
                    throw new Error('Could not load search suggestions');
                }
                return response.json();
            }).then(function (items) {
                if (sequence === requestSequence) {
                    show(Array.isArray(items) ? items : []);
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

### catalog.js

Envía el orden al cambiar el select; pliega filtros en pantallas angostas.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/js/catalog.js](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/js/catalog.js>), líneas 1–29.

```javascript
// Los formularios data-auto-submit envian selects y radios al cambiar: sin JS
// queda su boton como fallback. En pantallas angostas los filtros arrancan
// plegados para no tapar los resultados.
(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        var forms = document.querySelectorAll('form[data-auto-submit]');
        forms.forEach(function (form) {
            form.classList.add('is-enhanced');
            form.querySelectorAll('select, input[type="radio"]').forEach(function (control) {
                control.addEventListener('change', function () {
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

### confirm-action.js

Abre el diálogo antes de enviar un formulario destructivo.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/js/confirm-action.js](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/js/confirm-action.js>), líneas 1–63.

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

### post-gallery.js

Cambia la foto principal al tocar una miniatura.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/js/post-gallery.js](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/js/post-gallery.js>), líneas 1–21.

```javascript
(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        var mainImage = document.querySelector('[data-gallery-main]');
        var thumbnails = document.querySelectorAll('[data-gallery-thumb]');
        if (!mainImage || thumbnails.length < 2) {
            return;
        }
        thumbnails.forEach(function (thumbnail) {
            thumbnail.addEventListener('click', function (event) {
                event.preventDefault();
                mainImage.src = thumbnail.href;
                thumbnails.forEach(function (item) {
                    item.removeAttribute('aria-current');
                });
                thumbnail.setAttribute('aria-current', 'true');
            });
        });
    });
}());
```

### publish-preview.js

Vista previa de la tarjeta mientras se completa el formulario.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/js/publish-preview.js](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/js/publish-preview.js>), líneas 1–101.

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
        var coverInput = form.elements.covers;
        var existingImages = Array.prototype.slice.call(form.querySelectorAll('[data-existing-image]'));
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
        var fallbackCoverUrl = preview.getAttribute('data-fallback-cover') || (coverTarget ? coverTarget.src : '');

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
            for (var index = 0; index < existingImages.length; index++) {
                var item = existingImages[index].closest('.publish-gallery__item');
                var remove = item && item.querySelector('input[type="checkbox"]');
                if (!remove || !remove.checked) {
                    coverTarget.src = existingImages[index].src;
                    return;
                }
            }
            if (coverInput.files.length > 0) {
                coverObjectUrl = window.URL.createObjectURL(coverInput.files[0]);
                coverTarget.src = coverObjectUrl;
            } else {
                coverTarget.src = fallbackCoverUrl;
            }
        }

        [titleInput, artistInput, priceInput].forEach(function (input) {
            input.addEventListener('input', updateText);
            input.addEventListener('change', updateText);
        });
        coverInput.addEventListener('change', updateCover);
        form.querySelectorAll('input[name="removedImageIds"]').forEach(function (input) {
            input.addEventListener('change', updateCover);
        });
        window.addEventListener('pagehide', function () {
            if (coverObjectUrl) {
                window.URL.revokeObjectURL(coverObjectUrl);
            }
        });
        updateText();
        updateCover();
    }

    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('[data-publish-form]').forEach(initialize);
    });
}());
```

### sale-detail.js

Página de la venta: alto de la conversación, scroll al último mensaje, Enter para enviar y cancelar la edición de la reseña.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/js/sale-detail.js](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/js/sale-detail.js>), líneas 1–41.

```javascript
(function () {
    "use strict";

    const history = document.querySelector("[data-conversation-history]");
    const conversation = document.getElementById("conversation");
    function fitConversation() {
        if (!conversation || window.innerWidth <= 900) return;
        const top = conversation.getBoundingClientRect().top + window.scrollY;
        conversation.style.setProperty("--conversation-height", Math.max(288, window.innerHeight - top - 24) + "px");
    }
    fitConversation();
    window.addEventListener("resize", fitConversation);
    if (history) history.scrollTop = history.scrollHeight;

    const editor = document.getElementById("message-body");
    if (editor && editor.form) {
        if (editor.form.dataset.focusMessage === "true" || editor.getAttribute("aria-invalid") === "true") {
            window.addEventListener("pageshow", function () { editor.focus(); }, {once: true});
        }
        let composing = false;
        editor.addEventListener("compositionstart", function () { composing = true; });
        editor.addEventListener("compositionend", function () { composing = false; });
        editor.addEventListener("keydown", function (event) {
            if (event.key !== "Enter" || event.shiftKey || event.isComposing || composing || event.keyCode === 229) return;
            if (typeof editor.form.requestSubmit !== "function") return;
            event.preventDefault();
            editor.form.requestSubmit();
        });
    }

    document.querySelectorAll("[data-cancel-review]").forEach(function (cancel) {
        cancel.addEventListener("click", function (event) {
            const details = cancel.closest("details");
            if (!details) return;
            event.preventDefault();
            details.querySelector("form").reset();
            details.open = false;
            details.querySelector("summary").focus();
        });
    });
}());
```

### submit-once.js

Evita el doble envío.

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/js/submit-once.js](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/js/submit-once.js>), líneas 1–37.

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

## Imágenes

### placeholder.svg

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/images/covers/placeholder.svg](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/images/covers/placeholder.svg>), líneas 1–9.

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

### logo.svg

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/images/logo.svg](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/images/logo.svg>), líneas 1–29.

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

## Archivos para seguir el flujo

- [webapp/src/main/webapp/WEB-INF/views/auth/forgot-password.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/auth/forgot-password.jsp>)
- [webapp/src/main/webapp/WEB-INF/views/auth/login.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/auth/login.jsp>)
- [webapp/src/main/webapp/WEB-INF/views/auth/register.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/auth/register.jsp>)
- [webapp/src/main/webapp/WEB-INF/views/auth/reset-password.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/auth/reset-password.jsp>)
- [webapp/src/main/webapp/WEB-INF/views/auth/verify-required.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/auth/verify-required.jsp>)
- [webapp/src/main/webapp/WEB-INF/views/auth/verify.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/auth/verify.jsp>)
- [webapp/src/main/webapp/WEB-INF/views/cart/index.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/cart/index.jsp>)
- [webapp/src/main/webapp/WEB-INF/views/error/400.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/error/400.jsp>)
- [webapp/src/main/webapp/WEB-INF/views/error/403.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/error/403.jsp>)
- [webapp/src/main/webapp/WEB-INF/views/error/404.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/error/404.jsp>)
- [webapp/src/main/webapp/WEB-INF/views/error/409.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/error/409.jsp>)
- [webapp/src/main/webapp/WEB-INF/views/inquiry/detail.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/inquiry/detail.jsp>)
- [webapp/src/main/webapp/WEB-INF/views/inquiry/received.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/inquiry/received.jsp>)
- [webapp/src/main/webapp/WEB-INF/views/inquiry/sent.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/inquiry/sent.jsp>)
- [webapp/src/main/webapp/WEB-INF/views/landing/index.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/landing/index.jsp>)
- [webapp/src/main/webapp/WEB-INF/views/post/contact.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/post/contact.jsp>)
- [webapp/src/main/webapp/WEB-INF/views/post/detail.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/post/detail.jsp>)
- [webapp/src/main/webapp/WEB-INF/views/profile/index.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/profile/index.jsp>)
- [webapp/src/main/webapp/WEB-INF/views/profile/public.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/profile/public.jsp>)
- [webapp/src/main/webapp/WEB-INF/views/publish/index.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/publish/index.jsp>)
- [webapp/src/main/webapp/js/account-edit.js](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/js/account-edit.js>)
- [webapp/src/main/webapp/js/autocomplete.js](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/js/autocomplete.js>)
- [webapp/src/main/webapp/js/catalog.js](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/js/catalog.js>)
- [webapp/src/main/webapp/js/confirm-action.js](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/js/confirm-action.js>)
- [webapp/src/main/webapp/js/post-gallery.js](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/js/post-gallery.js>)
- [webapp/src/main/webapp/js/publish-preview.js](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/js/publish-preview.js>)
- [webapp/src/main/webapp/js/sale-detail.js](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/js/sale-detail.js>)
- [webapp/src/main/webapp/js/submit-once.js](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/js/submit-once.js>)
- [webapp/src/main/webapp/images/covers/placeholder.svg](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/images/covers/placeholder.svg>)
- [webapp/src/main/webapp/images/logo.svg](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/images/logo.svg>)

Fuente inspeccionada: `c3e2a4c`, 2026-10-05. Es evidencia estática; no implica ejecución de la aplicación. [[Source inventory]] · [[Roadmap de lectura]]
