---
title: "Validation and errors"
categories: ["Web", "Services"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ErrorResponseAdvice.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/controller/CartExceptionAdvice.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ErrorController.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/security/MultipartExceptionHandlerFilter.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/security/VerificationAccessDeniedHandler.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/validation/MatchingPasswordsValidator.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/validation/PublishFormValidator.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/form/RegisterForm.java", "webapp/src/main/webapp/WEB-INF/web.xml"]
---

# Validation and errors

> [!summary] En una frase
> La entrada se valida dos veces con las mismas reglas (en el formulario para mostrar el error junto al campo, en el service como garantía) y cada rechazo de negocio es una excepción que la capa web traduce a un error de campo, una redirección con aviso o una página 400, 403, 404 o 409.

## Herramientas

| Herramienta | Para qué |
|---|---|
| Bean Validation 2.0 + Hibernate Validator 6.2 | Anotaciones sobre los formularios (`@NotBlank`, `@Size`, `@Email`, ...) |
| `@Valid` + `BindingResult` | Ejecutar la validación al ligar el formulario y recibir los errores sin excepción |
| `ConstraintValidator` propios | Reglas que cruzan campos o dependen de archivos |
| Clases `*Rules` en `models` | La regla en un solo lugar, usada por el formulario y por el service |
| `@InitBinder` + editores | Normalizar el texto antes de validar (recortar, unificar saltos de línea, ignorar enums inválidos) |
| `@ControllerAdvice` + `@ExceptionHandler` | Traducir excepciones de negocio a respuestas HTTP |
| `<error-page>` en `web.xml` | El 404 de rutas que ningún controller atiende |
| `<form:errors>` y `MessageSource` | Mostrar cada error en el idioma del request |

## Validación en tres capas

```mermaid
flowchart LR
    R[Request] --> B[Binding + editores]
    B --> V[Bean Validation sobre el form]
    V -->|errores| F[Se vuelve a mostrar el formulario]
    V -->|ok| S[Service: normaliza y vuelve a validar con *Rules]
    S -->|excepción de negocio| H[Handler o catch del controller]
    S -->|ok| D[DAO]
    D -->|restricción de la base| S
```

1. **Formulario.** Las anotaciones cubren lo que se ve en un campo: obligatorio, largo, formato. Los validadores de clase cubren lo que cruza campos.
2. **Service.** Vuelve a aplicar la regla con la misma clase `*Rules`. El formulario es una cortesía con quien usa el sitio; el service no confía en que la llamada haya pasado por él. Además aplica lo que el formulario no puede saber: estado actual, pertenencia, topes.
3. **Base.** Las restricciones (`UNIQUE`, `CHECK`, FK) son la última barrera para lo que dos pedidos simultáneos podrían romper ([[Database schema]]).

## Validadores propios

| Anotación | Validador | Qué controla |
|---|---|---|
| `@ValidPassword` | Compuesta, sin validador propio: `@NotBlank` + `@Size(min = 12, max = 72)` + dos `@Pattern` | Contraseña de 12 a 72 caracteres con al menos una letra y un número, definida una sola vez. 72 es el tope de BCrypt |
| `@MatchingPasswords` | [[MatchingPasswordsValidator]] | Que contraseña y repetición coincidan; el formulario implementa [[PasswordsMatching]] |
| `@ValidPublishForm` | [[PublishFormValidator]] | Años, precio, fotos: usa [[VinylInputRules]] e [[ImageRules]] |
| `@ValidCatalogFilters` | [[CatalogFilterValidator]] | Rango de precios y de años coherentes |
| `@ValidShippingAddress` | [[ShippingAddressValidator]] | O se elige una dirección guardada, o se completa una nueva entera. Compartido por contacto y carrito |
| `@ValidPaymentForm` | [[PaymentFormValidator]] | CBU y alias, con [[PaymentInfoRules]] |
| `@ValidReceipt` | [[ReceiptValidator]] | Que haya archivo y sea de un tipo y tamaño aceptados, con [[ReceiptRules]] |
| `@ValidAvatarForm` | [[AvatarFormValidator]] | Foto de perfil, con [[ImageRules]] |

Los validadores de clase agregan el error **al campo** que corresponde (`addPropertyNode`), no a la clase, para que `<form:errors path="...">` lo muestre al lado.

## Editores de binding

| Editor | Dónde | Efecto |
|---|---|---|
| `StringTrimmerEditor(true)` | Perfil, contacto, carrito, mensajes, reseñas | Recorta y convierte el texto vacío en `null` |
| `StringTrimmerEditor(false)` | Correo y nombre al registrarse o recuperar | Recorta, sin convertir en `null` |
| [[LineBreakNormalizingEditor]] | Mensaje de contacto y cuerpo de mensajes y reseñas | Unifica `\r\n` en `\n`, para que el largo que cuenta el servidor coincida con el del navegador |
| Editor que ignora inválidos | Filtros del catálogo | Un valor de enum o número mal formado en la URL se descarta en vez de dar 400 |

## De la excepción a la respuesta

| Excepción | Quién la traduce | Respuesta |
|---|---|---|
| `PostNotFoundException`, `InquiryNotFoundException`, `UserNotFoundException`, `PageNotFoundException`, `AddressNotFoundException`, `ReceiptNotFoundException` | [[ErrorResponseAdvice]] | 404 con `error/404` |
| `ForbiddenOperationException` | [[ErrorResponseAdvice]] | 403 con `error/403` |
| `InvalidImageException`, `InvalidReviewException`, parámetro con tipo inválido | [[ErrorResponseAdvice]] | 400 con `error/400` |
| `InvalidSearchQueryException` | [[LandingController]] | 400 |
| `InvalidInquiryStateException` | [[InquiryController]] | 409 con `error/409` |
| `PostUnavailableException` | [[PostContactController]], [[PublishController]] | 409 |
| `ImageNotFoundException` | [[ImageController]] | 404 sin cuerpo |
| `MissingPaymentInfoException` | [[InquiryController]] | Redirección al perfil, sección de cobro |
| `AddressLimitExceededException` | [[ProfileController]], [[CartExceptionAdvice]], `catch` en contacto | Redirección o formulario con aviso |
| `OpenInquiryExistsException` | [[PostContactController]], [[CartExceptionAdvice]] | Redirección a la consulta ya abierta, con aviso |
| `CartAddRejectedException`, `NothingToSendException` | [[CartExceptionAdvice]] | Redirección con aviso |
| `DuplicateUserException`, `UnchangedPasswordException`, `InvalidCurrentPasswordException`, `PaymentInfoRequiredException`, `DuplicatePostException`, `ConcurrentPublishException`, `InvalidMessageException`, `InvalidReceiptException` | `catch` en el controller | Error de campo o global en el mismo formulario |
| Acceso denegado por Spring Security | [[VerificationAccessDeniedHandler]] | Pantalla de verificación pendiente o 403 ([[Security and authorization]]) |
| Archivo que supera el tope del resolver | [[MultipartExceptionHandlerFilter]] | Redirección a la página de origen con aviso |
| Ruta sin controller | `<error-page>` → [[ErrorController]] | 404 |

Tres criterios ordenan la tabla:

- Si la persona puede **corregir y reintentar**, el error vuelve al formulario con lo que ya escribió.
- Si el recurso **no existe o no es suyo**, la respuesta es una página de error con el código correcto.
- Si **llegó tarde** (otro reservó, la conversación se cerró), es un 409: el pedido era válido pero el estado cambió.

`ErrorResponseAdvice` centraliza los casos comunes; los handlers dentro de un controller existen cuando la respuesta depende del contexto de esa pantalla. Un `@ExceptionHandler` local tiene prioridad sobre uno de un `@ControllerAdvice`.

## Decisiones y por qué

| Decisión | Motivo | Fuente |
|---|---|---|
| Reglas compartidas en `models` | Evitar que el formulario y el service diverjan | Commits `435733bc` y `3bef5983` |
| El service revalida | Un pedido armado a mano saltea el formulario | Inferencia sobre la estructura; regla de capas de `CLAUDE.md` |
| 403 y 404 centralizados | Observación de la cátedra en el sprint 2: un solo criterio | `docs/issues/observaciones-sprint-2/` y commit `0870c81d` |
| 404 (no 403) cuando el recurso no es de quien pregunta | No revelar que existe | Comportamiento de los `*AccessHandler` ([[Security and authorization]]) |
| El tope de archivo se maneja en un filtro | El error ocurre al leer el multipart, antes de llegar a un controller | Comentarios en [[MultipartExceptionHandlerFilter]] |
| Validación del correo solo en el servidor | Evitar dos criterios distintos entre navegador y servidor | Commit `1f3c858c` |

## Límites conocidos

- `InvalidPostDataException` e `InvalidPaymentInfoException` no tienen handler: solo se alcanzan salteando el formulario, y en ese caso la respuesta sería un 500.
- No hay página propia para el 500.
- El comentario de [[ReceiptValidator]] menciona un tope de 6 MB en el resolver; el valor real es 26 MiB ([[Known gaps and document drift]]).

## Preguntas de defensa

**¿Dónde validan?**
En el formulario con Bean Validation y otra vez en el service con las mismas clases de reglas; la base tiene restricciones para lo que puede romperse por concurrencia.

**¿Por qué validar dos veces?**
El formulario da el mensaje junto al campo; el service garantiza la regla aunque el pedido no venga del formulario.

**¿Cómo validan que dos contraseñas coincidan?**
Con una anotación de clase, `@MatchingPasswords`, cuyo validador compara los dos campos y agrega el error en la repetición.

**¿Cómo deciden entre 403 y 404?**
403 cuando la cuenta no tiene permiso para una acción sobre algo que puede ver; 404 cuando el recurso no existe o no le pertenece.

**¿Qué pasa si suben un archivo enorme?**
El resolver lanza la excepción al leer el multipart; un filtro la atrapa y redirige a la página de origen con un aviso.

## Evidencia de código

### Handlers globales

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ErrorResponseAdvice.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ErrorResponseAdvice.java>), líneas 1–50.

```java
package ar.edu.itba.paw.webapp.controller;

import ar.edu.itba.paw.services.AddressNotFoundException;
import ar.edu.itba.paw.services.ForbiddenOperationException;
import ar.edu.itba.paw.services.InquiryNotFoundException;
import ar.edu.itba.paw.services.InvalidImageException;
import ar.edu.itba.paw.services.InvalidReviewException;
import ar.edu.itba.paw.services.PageNotFoundException;
import ar.edu.itba.paw.services.PostNotFoundException;
import ar.edu.itba.paw.services.ReceiptNotFoundException;
import ar.edu.itba.paw.services.UserNotFoundException;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.method.annotation.MethodArgumentTypeMismatchException;
import org.springframework.web.servlet.ModelAndView;

/*
 * Unico lugar donde las excepciones de pertenencia, de recurso inexistente y de datos que los
 * formularios ya validan se vuelven respuestas: un recurso que no existe es 404, uno que existe
 * pero es ajeno, 403, y un dato que no cumple las reglas del dominio, 400.
 */
@ControllerAdvice
public class ErrorResponseAdvice {

    @ExceptionHandler({PostNotFoundException.class, InquiryNotFoundException.class,
            UserNotFoundException.class, PageNotFoundException.class, AddressNotFoundException.class,
            ReceiptNotFoundException.class})
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ModelAndView notFound() {
        return new ModelAndView("error/404");
    }

    @ExceptionHandler(ForbiddenOperationException.class)
    @ResponseStatus(HttpStatus.FORBIDDEN)
    public ModelAndView forbidden() {
        return new ModelAndView("error/403");
    }

    // Los formularios aplican las mismas ImageRules y ReviewRules: solo llega aca un POST que se
    // salteo la validacion. Un parametro de la URL que no es del tipo esperado (una pagina que no
    // es un numero, un origin desconocido) tambien es un pedido mal armado.
    @ExceptionHandler({InvalidImageException.class, InvalidReviewException.class,
            MethodArgumentTypeMismatchException.class})
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ModelAndView badRequest() {
        return new ModelAndView("error/400");
    }
}
```

### Validador de clase

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/validation/MatchingPasswordsValidator.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/validation/MatchingPasswordsValidator.java>), líneas 1–20.

```java
package ar.edu.itba.paw.webapp.validation;

import javax.validation.ConstraintValidator;
import javax.validation.ConstraintValidatorContext;

public class MatchingPasswordsValidator implements ConstraintValidator<MatchingPasswords, PasswordsMatching> {

    @Override
    public boolean isValid(final PasswordsMatching form, final ConstraintValidatorContext context) {
        if (form == null || form.getPassword() == null
                || form.getPassword().equals(form.getPasswordConfirmation())) {
            return true;
        }
        context.disableDefaultConstraintViolation();
        context.buildConstraintViolationWithTemplate(context.getDefaultConstraintMessageTemplate())
                .addPropertyNode("passwordConfirmation")
                .addConstraintViolation();
        return false;
    }
}
```

### Filtro para archivos demasiado grandes

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/security/MultipartExceptionHandlerFilter.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/security/MultipartExceptionHandlerFilter.java>), líneas 1–50.

```java
package ar.edu.itba.paw.webapp.security;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.filter.OncePerRequestFilter;
import org.springframework.web.multipart.MaxUploadSizeExceededException;

import javax.servlet.FilterChain;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

public final class MultipartExceptionHandlerFilter extends OncePerRequestFilter {

    private static final Logger LOGGER = LoggerFactory.getLogger(MultipartExceptionHandlerFilter.class);

    @Override
    protected void doFilterInternal(final HttpServletRequest request, final HttpServletResponse response,
                                    final FilterChain filterChain) throws ServletException, IOException {
        try {
            filterChain.doFilter(request, response);
        } catch (final ServletException | RuntimeException exception) {
            /*
             * El resolver multipart parsea de forma lazy, asi que el limite excedido puede
             * saltar dentro del DispatcherServlet y llegar aca envuelto en una
             * NestedServletException. Por eso tambien se mira la causa directa.
             */
            if (!(exception instanceof MaxUploadSizeExceededException)
                    && !(exception.getCause() instanceof MaxUploadSizeExceededException)) {
                throw exception;
            }
            LOGGER.warn("Rejected a multipart request over the size limit uri={}", request.getRequestURI());
            final String servletPath = request.getServletPath();
            // El comprobante vuelve a la pagina de la Venta, que muestra el aviso.
            if (servletPath.matches("/inquiries/[0-9]+/receipt")) {
                final String salePath = servletPath.substring(0, servletPath.length() - "/receipt".length());
                response.sendRedirect(request.getContextPath() + salePath + "?receiptTooLarge");
                return;
            }
            // La foto de perfil vuelve al perfil, que reabre el dialogo con el aviso.
            if ("/profile/avatar".equals(servletPath)) {
                response.sendRedirect(request.getContextPath() + "/profile?avatarTooLarge#avatar");
                return;
            }
            final String target = servletPath.matches("/post/[0-9]+/edit") ? servletPath : "/publish";
            response.sendRedirect(request.getContextPath() + target + "?coverTooLarge");
        }
    }
}
```

## Archivos para seguir el flujo

- [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ErrorResponseAdvice.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ErrorResponseAdvice.java>) · [[ErrorResponseAdvice]]
- [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/CartExceptionAdvice.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/CartExceptionAdvice.java>) · [[CartExceptionAdvice]]
- [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ErrorController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ErrorController.java>) · [[ErrorController]]
- [webapp/src/main/java/ar/edu/itba/paw/webapp/security/MultipartExceptionHandlerFilter.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/security/MultipartExceptionHandlerFilter.java>) · [[MultipartExceptionHandlerFilter]]
- [webapp/src/main/java/ar/edu/itba/paw/webapp/security/VerificationAccessDeniedHandler.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/security/VerificationAccessDeniedHandler.java>) · [[VerificationAccessDeniedHandler]]
- [webapp/src/main/java/ar/edu/itba/paw/webapp/validation/MatchingPasswordsValidator.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/validation/MatchingPasswordsValidator.java>) · [[MatchingPasswordsValidator]]
- [webapp/src/main/java/ar/edu/itba/paw/webapp/validation/PublishFormValidator.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/validation/PublishFormValidator.java>) · [[PublishFormValidator]]
- [webapp/src/main/java/ar/edu/itba/paw/webapp/form/RegisterForm.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/RegisterForm.java>) · [[RegisterForm]]
- [webapp/src/main/webapp/WEB-INF/web.xml](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/web.xml>)

Fuente inspeccionada: `8929aea`, 2026-10-04. Es evidencia estática; no implica ejecución de la aplicación. [[Source inventory]] · [[Roadmap de lectura]]
