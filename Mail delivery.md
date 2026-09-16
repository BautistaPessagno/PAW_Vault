---
title: "Mail delivery"
categories: ["Services"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["services/src/main/resources/mail/welcome.html", "services/src/main/resources/mail/email-verification.html", "services/src/main/resources/mail/post-interest.html", "services/src/main/java/ar/edu/itba/paw/services/EmailServiceImpl.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java"]
---

# Mail delivery

EmailServiceImpl has three @Async operations using Thymeleaf HTML and JavaMailSender. Each receives Locale explicitly and catches/logs rendering or SMTP exceptions.

| Message | Trigger | Language | Link / reply |
|---|---|---|---|
| Verification | Register new/pending account | Request locale | app.base-url + /verify?token= |
| Welcome | Successful account activation | Verification request locale | Home link |
| Post interest | Persist initial inquiry | Seller preferred locale, normalized by SupportedLocales | Home link; authenticated buyer Reply-To |

All use app.mail.from and UTF-8 HTML. The interest template includes the optional buyer message using escaped Thymeleaf text. The constructor removes one trailing slash from app.base-url; deployments must include their context path. No attachment, copy to buyer, acceptance/rejection email or conversation reply delivery is implemented.

The pool has core 2, max 5, queue 50 and CallerRunsPolicy. Saturation can run work in the caller. Registration, verification and inquiry submission invoke mail before database commit. There is no durable queue, outbox, after-commit event or delivery acknowledgment. SMTP example timeouts apply to individual operations; their sum is not a measured end-to-end bound.

The inquiry remains readable after a worker delivery failure if its transaction committed. Login verificationSent and landing contactSent feedback do not establish delivery. Old synchronous 503/retry requirements remain historical.

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
                <span th:text="${albumTitle}">Álbum</span> —
                <span th:text="${artistName}">Artista</span>
                (<span th:text="${releaseYear}">2026</span>)
            </p>
            <p th:if="${message != null}" style="margin: 0 0 28px; font-size: 15px; line-height: 1.5;">
                <strong th:text="#{email.postInterest.message}">Mensaje:</strong><br/>
                <span style="white-space: pre-line;" th:text="${message}">Mensaje del interesado</span>
            </p>
            <a th:href="${homeUrl}" href="#"
               style="display: inline-block; padding: 12px 24px; background-color: #1f2933; color: #ffffff; text-decoration: none; border-radius: 6px; font-size: 15px;"
               th:text="#{email.postInterest.cta}">Ver quieroVinilos</a>
        </td>
    </tr>
</table>
</body>
</html>
```

[[Authentication flow]] · [[Contact flow]] · [[EmailServiceImplTest]]
