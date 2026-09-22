---
title: "Mail delivery"
categories: ["Services"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["services/src/main/resources/mail/welcome.html", "services/src/main/resources/mail/email-verification.html", "services/src/main/resources/mail/post-interest.html", "services/src/main/resources/mail/inquiry-accepted.html", "services/src/main/resources/mail/password-changed.html", "services/src/main/resources/mail/password-reset.html", "services/src/main/java/ar/edu/itba/paw/services/EmailServiceImpl.java", "services/src/main/java/ar/edu/itba/paw/services/TransactionCallbacks.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java"]
---

# Mail delivery

EmailServiceImpl has six @Async operations using Thymeleaf HTML and JavaMailSender. Each receives Locale explicitly and catches and logs rendering or SMTP exceptions. Every caller now registers the send through [[TransactionCallbacks]], so the async task is submitted only after the service transaction commits.

| Message | Trigger | Language | Link / reply |
|---|---|---|---|
| Verification | Register new or pending account | Request locale | app.base-url + /verify?token= |
| Welcome | Successful account activation | Verification request locale | Home link |
| Post interest | Persist initial inquiry | Seller preferred locale | /inquiries; authenticated buyer as Reply-To |
| Inquiry accepted | Seller accepts an inquiry and sells the post | Buyer preferred locale | /inquiries/sent |
| Password changed | Profile password change or successful reset | Request locale | No link; asks to reply if it was not the user |
| Password reset | Recovery request for an enabled account | Request locale | app.base-url + /reset-password?token=, valid one hour |

All use app.mail.from and UTF-8 HTML. The interest template includes the optional buyer message as escaped Thymeleaf text. The constructor removes one trailing slash from app.base-url; deployments must include their context path, which the Pampero example already does. No attachment, copy to the buyer, rejection email, deletion notice or conversation reply delivery is implemented.

The pool has core 2, max 5 and queue 50. The rejection handler no longer uses CallerRunsPolicy: when the pool and queue are full it logs `Mail task rejected` and drops that email, so SMTP latency never moves onto a request thread. On shutdown the executor waits up to 30 seconds for queued sends. There is still no durable queue, outbox or delivery acknowledgment, so a dropped or failed message is not retried. SMTP example timeouts apply to individual operations; their sum is not a measured end-to-end bound.

Because dispatch follows commit, a rollback no longer produces mail for data that was never stored. The reverse gap remains: a committed inquiry, sale or reset can exist without its email. Flash and query-string notices report normal service completion, not delivery.

## After-commit dispatch

[services/src/main/java/ar/edu/itba/paw/services/TransactionCallbacks.java, lines 12–23](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/TransactionCallbacks.java>)

```java
    static void afterCommit(final Runnable action) {
        if (!TransactionSynchronizationManager.isSynchronizationActive()) {
            action.run();
            return;
        }
        TransactionSynchronizationManager.registerSynchronization(new TransactionSynchronization() {
            @Override
            public void afterCommit() {
                action.run();
            }
        });
    }
```

## welcome template

[services/src/main/resources/mail/welcome.html, lines 1–21](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/main/resources/mail/welcome.html>)

```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org" th:lang="${#locale.language}" lang="es">
<head>
    <meta charset="UTF-8"/>
    <title th:text="#{email.welcome.subject}">quieroVinilos</title>
</head>
<body style="margin: 0; padding: 24px; background-color: #f4f4f4; font-family: Arial, Helvetica, sans-serif; color: #222222;">
<table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="max-width: 480px; margin: 0 auto; background-color: #ffffff; border-radius: 8px;">
    <tr>
        <td style="padding: 32px;">
            <h1 style="margin: 0 0 16px; font-size: 20px;" th:text="#{email.welcome.subject}">Bienvenido a quieroVinilos</h1>
            <p style="margin: 0 0 28px; font-size: 15px; line-height: 1.5;"
               th:text="#{email.welcome.body(${username})}">Gracias por registrarte.</p>
            <a th:href="${homeUrl}" href="#"
               style="display: inline-block; padding: 12px 24px; background-color: #1f2933; color: #ffffff; text-decoration: none; border-radius: 6px; font-size: 15px;"
               th:text="#{email.welcome.cta}">Ver quieroVinilos</a>
        </td>
    </tr>
</table>
</body>
</html>
```

## email-verification template

[services/src/main/resources/mail/email-verification.html, lines 1–21](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/main/resources/mail/email-verification.html>)

```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org" th:lang="${#locale.language}" lang="es">
<head>
    <meta charset="UTF-8"/>
    <title th:text="#{email.verification.subject}">Confirmá tu correo</title>
</head>
<body style="margin: 0; padding: 24px; background-color: #f4f4f4; font-family: Arial, Helvetica, sans-serif; color: #222222;">
<table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="max-width: 480px; margin: 0 auto; background-color: #ffffff; border-radius: 8px;">
    <tr>
        <td style="padding: 32px;">
            <h1 style="margin: 0 0 16px; font-size: 20px;" th:text="#{email.verification.subject}">Confirmá tu correo</h1>
            <p style="margin: 0 0 28px; font-size: 15px; line-height: 1.5;"
               th:text="#{email.verification.body}">Confirmá tu correo para elegir tus credenciales y activar tu cuenta.</p>
            <a th:href="${verificationUrl}" href="#"
               style="display: inline-block; padding: 12px 24px; background-color: #1f2933; color: #ffffff; text-decoration: none; border-radius: 6px; font-size: 15px;"
               th:text="#{email.verification.cta}">Confirmar correo</a>
        </td>
    </tr>
</table>
</body>
</html>
```

## post-interest template

[services/src/main/resources/mail/post-interest.html, lines 1–36](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/main/resources/mail/post-interest.html>)

```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org" th:lang="${#locale.language}" lang="es">
<head>
    <meta charset="UTF-8"/>
    <title th:text="#{email.postInterest.heading}">Interés en tu publicación</title>
</head>
<body style="margin: 0; padding: 24px; background-color: #f4f4f4; font-family: Arial, Helvetica, sans-serif; color: #222222;">
<table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="max-width: 560px; margin: 0 auto; background-color: #ffffff; border-radius: 8px;">
    <tr>
        <td style="padding: 32px;">
            <h1 style="margin: 0 0 16px; font-size: 20px;" th:text="#{email.postInterest.heading}">Interés en tu publicación</h1>
            <p style="margin: 0 0 20px; font-size: 15px; line-height: 1.5;"
               th:text="#{email.postInterest.intro(${contactName})}">Alguien está interesado en tu publicación.</p>
            <p style="margin: 0 0 8px; font-size: 15px;">
                <strong th:text="#{email.postInterest.contact}">Contacto:</strong>
                <span th:text="${contactName}">Nombre</span>
                &lt;<a th:href="|mailto:${contactEmail}|" th:text="${contactEmail}">contacto@example.com</a>&gt;
            </p>
            <p style="margin: 0 0 28px; font-size: 15px;">
                <strong th:text="#{email.postInterest.album}">Álbum:</strong>
                <span th:text="${albumTitle}">Álbum</span><br/>
                <span th:text="${artistName}">Artista</span>
                (<span th:text="${releaseYear}">2026</span>)
            </p>
            <p th:if="${message != null}" style="margin: 0 0 28px; font-size: 15px; line-height: 1.5;">
                <strong th:text="#{email.postInterest.message}">Mensaje:</strong><br/>
                <span style="white-space: pre-line;" th:text="${message}">Mensaje del interesado</span>
            </p>
            <a th:href="${inquiriesUrl}" href="#"
               style="display: inline-block; padding: 12px 24px; background-color: #1f2933; color: #ffffff; text-decoration: none; border-radius: 6px; font-size: 15px;"
               th:text="#{email.postInterest.cta}">Ver quieroVinilos</a>
        </td>
    </tr>
</table>
</body>
</html>
```

## inquiry-accepted template

[services/src/main/resources/mail/inquiry-accepted.html, lines 1–27](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/main/resources/mail/inquiry-accepted.html>)

```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org" th:lang="${#locale.language}" lang="es">
<head>
    <meta charset="UTF-8"/>
    <title th:text="#{email.inquiryAccepted.heading}">Tu consulta fue aceptada</title>
</head>
<body style="margin: 0; padding: 24px; background-color: #f4f4f4; font-family: Arial, Helvetica, sans-serif; color: #222222;">
<table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="max-width: 560px; margin: 0 auto; background-color: #ffffff; border-radius: 8px;">
    <tr>
        <td style="padding: 32px;">
            <h1 style="margin: 0 0 16px; font-size: 20px;" th:text="#{email.inquiryAccepted.heading}">Tu consulta fue aceptada</h1>
            <p style="margin: 0 0 20px; font-size: 15px; line-height: 1.5;"
               th:text="#{email.inquiryAccepted.intro(${albumTitle})}">Tu consulta fue aceptada.</p>
            <p style="margin: 0 0 28px; font-size: 15px;">
                <strong th:text="#{email.inquiryAccepted.album}">Álbum:</strong>
                <span th:text="${albumTitle}">Álbum</span><br/>
                <span th:text="${artistName}">Artista</span>
                (<span th:text="${releaseYear}">2026</span>)
            </p>
            <a th:href="${inquiriesUrl}" href="#"
               style="display: inline-block; padding: 12px 24px; background-color: #1f2933; color: #ffffff; text-decoration: none; border-radius: 6px; font-size: 15px;"
               th:text="#{email.inquiryAccepted.cta}">Ver mis consultas</a>
        </td>
    </tr>
</table>
</body>
</html>
```

## password-changed template

[services/src/main/resources/mail/password-changed.html, lines 1–20](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/main/resources/mail/password-changed.html>)

```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org" th:lang="${#locale.language}" lang="es">
<head>
    <meta charset="UTF-8"/>
    <title th:text="#{email.passwordChanged.subject}">quieroVinilos</title>
</head>
<body style="margin: 0; padding: 24px; background-color: #f4f4f4; font-family: Arial, Helvetica, sans-serif; color: #222222;">
<table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="max-width: 480px; margin: 0 auto; background-color: #ffffff; border-radius: 8px;">
    <tr>
        <td style="padding: 32px;">
            <h1 style="margin: 0 0 16px; font-size: 20px;" th:text="#{email.passwordChanged.subject}">Tu contraseña fue cambiada</h1>
            <p style="margin: 0 0 16px; font-size: 15px; line-height: 1.5;"
               th:text="#{email.passwordChanged.body(${username})}">Tu contraseña fue cambiada.</p>
            <p style="margin: 0; font-size: 15px; line-height: 1.5;"
               th:text="#{email.passwordChanged.notice}">Si no fuiste vos, respondé a este correo.</p>
        </td>
    </tr>
</table>
</body>
</html>
```

## password-reset template

[services/src/main/resources/mail/password-reset.html, lines 1–23](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/main/resources/mail/password-reset.html>)

```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org" th:lang="${#locale.language}" lang="es">
<head>
    <meta charset="UTF-8"/>
    <title th:text="#{email.passwordReset.subject}">Recuperá tu contraseña</title>
</head>
<body style="margin: 0; padding: 24px; background-color: #f4f4f4; font-family: Arial, Helvetica, sans-serif; color: #222222;">
<table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="max-width: 480px; margin: 0 auto; background-color: #ffffff; border-radius: 8px;">
    <tr>
        <td style="padding: 32px;">
            <h1 style="margin: 0 0 16px; font-size: 20px;" th:text="#{email.passwordReset.subject}">Recuperá tu contraseña</h1>
            <p style="margin: 0 0 28px; font-size: 15px; line-height: 1.5;"
               th:text="#{email.passwordReset.body}">Entrá al enlace para elegir una contraseña nueva. Vence en una hora.</p>
            <a th:href="${resetUrl}" href="#"
               style="display: inline-block; padding: 12px 24px; background-color: #1f2933; color: #ffffff; text-decoration: none; border-radius: 6px; font-size: 15px;"
               th:text="#{email.passwordReset.cta}">Elegir contraseña nueva</a>
            <p style="margin: 28px 0 0; font-size: 15px; line-height: 1.5;"
               th:text="#{email.passwordReset.notice}">Si no lo pediste, ignorá este correo: tu contraseña no cambia.</p>
        </td>
    </tr>
</table>
</body>
</html>
```

[[Authentication flow]] · [[Contact flow]] · [[Inquiry and sale flow]] · [[Password recovery flow]] · [[Profile flow]] · [[EmailServiceImplTest]]

## Evidencia local anterior, 2026-09-17

[[Audit local 2026-09-17]] observó seis entregas reales de avisos de interés sobre la rama `e5e926d`, anterior a `f12af08`. Esa evidencia no cubre los cuatro correos nuevos ni el envío posterior al commit.
