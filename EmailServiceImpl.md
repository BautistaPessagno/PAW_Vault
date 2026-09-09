---
title: "EmailServiceImpl"
categories: ["Services"]
type: "code"
module: "services"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
tags: ["codemap", "services"]
sources: ["services/src/main/java/ar/edu/itba/paw/services/EmailServiceImpl.java"]
---

# EmailServiceImpl

Both sendWelcomeEmail and sendPostInterestEmail are @Async. Each builds a Thymeleaf Context using the supplied Locale, sets homeUrl from required app.base-url, and sends UTF-8 HTML. One trailing slash is removed from baseUrl before adding /. Interest mail goes to the publisher with contact email in Reply-To. Both methods catch MessagingException and RuntimeException and log the full exception without returning delivery status. [[WebConfig]] supplies the bounded executor; its CallerRunsPolicy can run mail in the caller under saturation. See [[Mail delivery]].

## Connections

Project types referenced: [[EmailService]], [[Post]], [[PostInterestNotification]], [[User]].

Referenced by: [[EmailServiceImplTest]].

## Exact source

[services/src/main/java/ar/edu/itba/paw/services/EmailServiceImpl.java, lines 1–108](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/EmailServiceImpl.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.User;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.MessageSource;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.MimeMessageHelper;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import org.thymeleaf.context.Context;
import org.thymeleaf.spring5.SpringTemplateEngine;

import javax.mail.MessagingException;
import javax.mail.internet.MimeMessage;
import java.nio.charset.StandardCharsets;
import java.util.Locale;

@Service
public class EmailServiceImpl implements EmailService {

    private static final Logger LOGGER = LoggerFactory.getLogger(EmailServiceImpl.class);
    private static final String WELCOME_TEMPLATE = "welcome";
    private static final String POST_INTEREST_TEMPLATE = "post-interest";

    private final JavaMailSender mailSender;
    private final SpringTemplateEngine templateEngine;
    private final MessageSource messageSource;
    private final String from;
    private final String baseUrl;

    @Autowired
    public EmailServiceImpl(final JavaMailSender mailSender, final SpringTemplateEngine templateEngine,
                            final MessageSource messageSource,
                            @Value("${app.mail.from}") final String from,
                            @Value("${app.base-url}") final String baseUrl) {
        this.mailSender = mailSender;
        this.templateEngine = templateEngine;
        this.messageSource = messageSource;
        this.from = from;
        // Sin la barra final, asi concatenar un path que empieza con "/" no la duplica.
        this.baseUrl = baseUrl.endsWith("/") ? baseUrl.substring(0, baseUrl.length() - 1) : baseUrl;
    }

    @Async
    @Override
    public void sendWelcomeEmail(final User user, final Locale locale) {
        try {
            final Context context = new Context(locale);
            context.setVariable("username", user.getUsername());
            context.setVariable("homeUrl", baseUrl + "/");
            final String body = templateEngine.process(WELCOME_TEMPLATE, context);
            final String subject = messageSource.getMessage("email.welcome.subject", null, locale);
            final MimeMessage message = createMessage(user.getEmail(), null, subject, body);

            mailSender.send(message);
            LOGGER.info("Welcome email sent userId={}", user.getId());
        } catch (final MessagingException | RuntimeException exception) {
            LOGGER.error("Welcome email delivery failed userId={}", user.getId(), exception);
        }
    }

    /*
     * @Async para no bloquear el request: entre los timeouts de conexion y de lectura, una
     * entrega SMTP lenta puede tardar hasta 15 segundos. Como corre en otro hilo, la
     * excepcion no puede volver al controller, asi que se loguea y se corta aca.
     */
    @Async
    @Override
    public void sendPostInterestEmail(final PostInterestNotification notification, final Locale locale) {
        try {
            final Context context = new Context(locale);
            context.setVariable("contactName", notification.getContactName());
            context.setVariable("contactEmail", notification.getContactEmail());
            context.setVariable("albumTitle", notification.getAlbumTitle());
            context.setVariable("artistName", notification.getArtistName());
            context.setVariable("releaseYear", notification.getReleaseYear());
            context.setVariable("homeUrl", baseUrl + "/");
            final String body = templateEngine.process(POST_INTEREST_TEMPLATE, context);
            final Object[] subjectArguments = {notification.getAlbumTitle()};
            final String subject = messageSource.getMessage(
                    "email.postInterest.subject", subjectArguments, locale);
            final MimeMessage message = createMessage(notification.getPublisherEmail(),
                    notification.getContactEmail(), subject, body);

            mailSender.send(message);
            LOGGER.info("Post interest email sent postId={}", notification.getPostId());
        } catch (final MessagingException | RuntimeException exception) {
            LOGGER.error("Post interest email delivery failed postId={}", notification.getPostId(), exception);
        }
    }

    private MimeMessage createMessage(final String recipient, final String replyTo, final String subject,
                                      final String body) throws MessagingException {
        final MimeMessage message = mailSender.createMimeMessage();
        final MimeMessageHelper helper = new MimeMessageHelper(message, StandardCharsets.UTF_8.name());
        helper.setFrom(from);
        helper.setTo(recipient);
        if (replyTo != null) {
            helper.setReplyTo(replyTo);
        }
        helper.setSubject(subject);
        helper.setText(body, true);
        return message;
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
