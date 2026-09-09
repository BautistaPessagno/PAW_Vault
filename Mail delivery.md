---
title: "Mail delivery"
categories: ["Services"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "services"]
sources: ["services/src/main/resources/mail/welcome.html", "services/src/main/resources/mail/post-interest.html"]
---

# Mail delivery

The application has two delivery policies implemented in [[EmailServiceImpl]]. Both use JavaMailSender, MimeMessageHelper and a Thymeleaf HTML template loaded by [[WebConfig]].

| Property | Welcome | Post interest |
|---|---|---|
| Trigger | A new User is created | A visitor submits a valid contact form |
| Execution | @Async through Spring proxy | Synchronous request call |
| Locale | Request Locale passed by caller | Always Spanish |
| To | User email | Publisher email from PostSummary |
| From | app.mail.from | app.mail.from |
| Reply-To | Not explicitly set | Contact email |
| Failure | Log and swallow in method body | Log and throw EmailDeliveryException |
| UI effect | No delivery status | 503 retry form or success redirect |

`createMessage` uses UTF-8 and `setText(body, true)` to mark HTML. Thymeleaf th:text escapes inserted text. The contact template contains a mailto link and the buyer's contact details. No attachments, arbitrary visitor-written message, CC, BCC or copy to the interested visitor is implemented.

The mail sender config maps connection-timeout-ms to JavaMail connectiontimeout, read-timeout-ms to timeout, and write-timeout-ms to writetimeout. Examples use 5000/10000/10000 milliseconds. These are separate operation timeouts, not a proven fixed upper bound for the whole request.

No durable queue, outbox, mail audit table or deduplication exists. SMTP acceptance is not final delivery confirmation. Welcome dispatch is not tied to transaction commit. The @Async body catches failures during rendering/sending; this does not prove that every possible failure to submit an async task is swallowed.

## Templates

### welcome.html

[services/src/main/resources/mail/welcome.html, lines 1–18](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/main/resources/mail/welcome.html>)

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
            <p style="margin: 0; font-size: 15px; line-height: 1.5;"
               th:text="#{email.welcome.body(${username})}">Gracias por registrarte.</p>
        </td>
    </tr>
</table>
</body>
</html>
```

### post-interest.html

[services/src/main/resources/mail/post-interest.html, lines 1–29](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/main/resources/mail/post-interest.html>)

```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org" lang="es">
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
            <p style="margin: 0; font-size: 15px;">
                <strong th:text="#{email.postInterest.album}">Álbum:</strong>
                <span th:text="${albumTitle}">Álbum</span> —
                <span th:text="${artistName}">Artista</span>
                (<span th:text="${releaseYear}">2026</span>)
            </p>
        </td>
    </tr>
</table>
</body>
</html>
```


[[Contact flow]] · [[Transactions and concurrency]] · [[EmailServiceImplTest]]
