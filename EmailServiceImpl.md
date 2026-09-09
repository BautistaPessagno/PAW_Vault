---
title: "EmailServiceImpl"
categories: ["Services"]
type: "code"
module: "services"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "services"]
sources: ["services/src/main/java/ar/edu/itba/paw/services/EmailServiceImpl.java"]
---

# EmailServiceImpl

`sendWelcomeEmail` is `@Async`, uses the supplied Locale and welcome template, and catches MessagingException or RuntimeException without rethrowing. `sendPostInterestEmail` is synchronous, fixes Locale to Spanish, sets contact and album template variables, and translates delivery or rendering failure to [[EmailDeliveryException]]. `createMessage` sets configured From, destination To, optional Reply-To, localized subject and UTF-8 HTML body. No CC, BCC, queue or delivery database is implemented. Logs record user/post ID and failure class rather than addresses. See [[Mail delivery]].

## Connections

Project types referenced: [[EmailDeliveryException]], [[EmailService]], [[Post]], [[PostInterestNotification]], [[User]].

Referenced by: no other production Java type directly references this name; Spring discovers implementations through scanning.

Tests: [[EmailServiceImplTest]]. See [[Testing and evidence]].

## Exact source

[services/src/main/java/ar/edu/itba/paw/services/EmailServiceImpl.java, lines 1–102](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/EmailServiceImpl.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.User;
import ar.edu.itba.paw.services.exceptions.EmailDeliveryException;
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
    private static final Locale CONTACT_EMAIL_LOCALE = Locale.forLanguageTag("es");
    private static final String WELCOME_TEMPLATE = "welcome";
    private static final String POST_INTEREST_TEMPLATE = "post-interest";

    private final JavaMailSender mailSender;
    private final SpringTemplateEngine templateEngine;
    private final MessageSource messageSource;
    private final String from;

    @Autowired
    public EmailServiceImpl(final JavaMailSender mailSender, final SpringTemplateEngine templateEngine,
                            final MessageSource messageSource,
                            @Value("${app.mail.from}") final String from) {
        this.mailSender = mailSender;
        this.templateEngine = templateEngine;
        this.messageSource = messageSource;
        this.from = from;
    }

    @Async
    @Override
    public void sendWelcomeEmail(final User user, final Locale locale) {
        try {
            final Context context = new Context(locale);
            context.setVariable("username", user.getUsername());
            final String body = templateEngine.process(WELCOME_TEMPLATE, context);
            final String subject = messageSource.getMessage("email.welcome.subject", null, locale);
            final MimeMessage message = createMessage(user.getEmail(), null, subject, body);

            mailSender.send(message);
            LOGGER.info("Welcome email sent userId={}", user.getId());
        } catch (final MessagingException | RuntimeException exception) {
            LOGGER.error("Welcome email delivery failed userId={} cause={}", user.getId(),
                    exception.getClass().getName());
        }
    }

    @Override
    public void sendPostInterestEmail(final PostInterestNotification notification) {
        try {
            final Context context = new Context(CONTACT_EMAIL_LOCALE);
            context.setVariable("contactName", notification.getContactName());
            context.setVariable("contactEmail", notification.getContactEmail());
            context.setVariable("albumTitle", notification.getAlbumTitle());
            context.setVariable("artistName", notification.getArtistName());
            context.setVariable("releaseYear", notification.getReleaseYear());
            final String body = templateEngine.process(POST_INTEREST_TEMPLATE, context);
            final Object[] subjectArguments = {notification.getAlbumTitle()};
            final String subject = messageSource.getMessage(
                    "email.postInterest.subject", subjectArguments, CONTACT_EMAIL_LOCALE);
            final MimeMessage message = createMessage(notification.getPublisherEmail(),
                    notification.getContactEmail(), subject, body);

            mailSender.send(message);
            LOGGER.info("Post interest email sent postId={}", notification.getPostId());
        } catch (final MessagingException | RuntimeException exception) {
            LOGGER.error("Post interest email delivery failed postId={} cause={}", notification.getPostId(),
                    exception.getClass().getName());
            throw new EmailDeliveryException(
                    "Could not deliver post interest email for postId=" + notification.getPostId(), exception);
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

[[Architecture]] · [[Domain and identity]] · [[Source inventory]]
