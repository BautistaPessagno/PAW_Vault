---
title: "Mail delivery"
categories: ["Services"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
tags: ["codemap", "services"]
sources: ["services/src/main/resources/mail/welcome.html", "services/src/main/resources/mail/post-interest.html", "services/src/main/java/ar/edu/itba/paw/services/EmailServiceImpl.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java"]
---

# Mail delivery

Both mail operations in [[EmailServiceImpl]] use @Async, JavaMailSender, MimeMessageHelper and Thymeleaf HTML. Both receive the request Locale explicitly and log/catch rendering or sending failures.

| Property | Welcome | Post interest |
|---|---|---|
| Trigger | New publisher user | Valid contact submission |
| To | User email | Publisher address resolved from PostSummary |
| From | app.mail.from | app.mail.from |
| Reply-To | Not explicitly set | Contact email |
| Locale | Caller Locale | Caller Locale |
| Link | app.base-url + / | app.base-url + / |
| Failure | Log and swallow | Log and swallow |

## Execution and feedback

[[WebConfig]] provides taskExecutor with core pool 2, maximum 5, queue capacity 50 and mail- thread prefix. CallerRunsPolicy runs rejected work in the caller under saturation rather than discarding it in that condition. Normal delivery runs in a worker, but the request can still wait for mail when this fallback applies.

The contact controller immediately redirects after a normal service return with contactSent=true. This is not SMTP delivery confirmation. The old 503 retry view and EmailDeliveryException have been removed. Failures inside the async method do not propagate back to that form. Failures before entering the method are not proven covered by its catch.

app.base-url is a required configuration value for absolute home links outside request context. The constructor removes one trailing slash. UTF-8 HTML messages and th:text escape supplied text; interest email includes a mailto link, name, email and album details. No attachment, visitor-written body, CC, BCC or copy to the visitor is implemented.

The SMTP example specifies 5000 ms connection and 10000 ms read/write timeouts. These are individual operation limits rather than a proven end-to-end duration. There is no durable queue, retry history or outbox, and welcome dispatch can precede a later database rollback.

## Welcome template

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

## Interest template

[services/src/main/resources/mail/post-interest.html, lines 1–32](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/main/resources/mail/post-interest.html>)

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
            <a th:href="${homeUrl}" href="#"
               style="display: inline-block; padding: 12px 24px; background-color: #1f2933; color: #ffffff; text-decoration: none; border-radius: 6px; font-size: 15px;"
               th:text="#{email.postInterest.cta}">Ver quieroVinilos</a>
        </td>
    </tr>
</table>
</body>
</html>
```

[[Contact flow]] · [[EmailServiceImplTest]] · [[Configuration and running]]
