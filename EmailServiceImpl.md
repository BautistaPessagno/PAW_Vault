---
title: "EmailServiceImpl"
categories: ["Services"]
type: "code"
module: "services"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["services/src/main/java/ar/edu/itba/paw/services/EmailServiceImpl.java"]
---

# EmailServiceImpl

Arma y envía los siete correos: plantilla Thymeleaf, asunto de i18n, `MimeMessage` HTML en UTF-8. Cada método es `@Async` y atrapa sus errores para loguearlos. La URL base sale de `app.base-url`. Ver [[Mail delivery]].

## Guía de lectura

Datos y dependencias declaradas: `LOGGER`, `WELCOME_TEMPLATE`, `VERIFICATION_TEMPLATE`, `POST_INTEREST_TEMPLATE`, `INQUIRY_UPDATE_TEMPLATE`, `INQUIRY_UPDATE_PREFIX`, `MESSAGE_TEMPLATE`, `CONVERSATION_ANCHOR`, `PASSWORD_CHANGED_TEMPLATE`, `PASSWORD_RESET_TEMPLATE`, `mailSender`, `templateEngine`, `messageSource`, `from`, `baseUrl`.

Operaciones para localizar en la fuente: `sendWelcomeEmail`, `sendVerificationEmail`, `sendPostInterestEmail`, `sendInquiryUpdateEmail`, `sendMessageEmail`, `sendPasswordChangedEmail`, `sendPasswordResetEmail`, `inquiryUrl`, `inquiriesUrl`, `createMessage`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[EmailService]], [[InquiryEvent]], [[InquiryUpdateNotification]], [[MessageNotification]], [[PostInterestNotification]], [[User]].

Referenciado por: [[EmailServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [services/src/main/java/ar/edu/itba/paw/services/EmailServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/EmailServiceImpl.java>), líneas 1–235.

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
import java.util.List;
import java.util.Locale;

@Service
public class EmailServiceImpl implements EmailService {

    private static final Logger LOGGER = LoggerFactory.getLogger(EmailServiceImpl.class);
    private static final String WELCOME_TEMPLATE = "welcome";
    private static final String VERIFICATION_TEMPLATE = "email-verification";
    private static final String POST_INTEREST_TEMPLATE = "post-interest";
    private static final String INQUIRY_UPDATE_TEMPLATE = "inquiry-update";
    private static final String INQUIRY_UPDATE_PREFIX = "email.inquiryUpdate.";
    private static final String MESSAGE_TEMPLATE = "inquiry-message";
    // La Conversacion esta al pie del detalle de la Consulta: el mail de Mensaje nuevo va directo a ella.
    private static final String CONVERSATION_ANCHOR = "#conversation";
    private static final String PASSWORD_CHANGED_TEMPLATE = "password-changed";
    private static final String PASSWORD_RESET_TEMPLATE = "password-reset";

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

    @Async
    @Override
    public void sendVerificationEmail(final User user, final String token, final Locale locale) {
        try {
            final Context context = new Context(locale);
            context.setVariable("verificationUrl", baseUrl + "/verify?token=" + token);
            final String body = templateEngine.process(VERIFICATION_TEMPLATE, context);
            final String subject = messageSource.getMessage("email.verification.subject", null, locale);
            final MimeMessage message = createMessage(user.getEmail(), null, subject, body);

            mailSender.send(message);
            LOGGER.info("Verification email sent userId={}", user.getId());
        } catch (final MessagingException | RuntimeException exception) {
            LOGGER.error("Verification email delivery failed userId={}", user.getId(), exception);
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
        final List<Long> inquiryIds = notification.getPosts().stream()
                .map(PostInterestNotification.InterestedPost::getInquiryId)
                .toList();
        try {
            final List<PostInterestNotification.InterestedPost> posts = notification.getPosts();
            final Context context = new Context(locale);
            context.setVariable("contactName", notification.getContactName());
            context.setVariable("message", notification.getMessage());
            context.setVariable("posts", posts);
            // Cada vinilo enlaza a su Consulta: el template le suma el id.
            context.setVariable("inquiriesUrl", inquiriesUrl());
            final String body = templateEngine.process(POST_INTEREST_TEMPLATE, context);
            // Con un vinilo el asunto lo nombra; con varios, dice cuantos son.
            final String subject = posts.size() == 1
                    ? messageSource.getMessage("email.postInterest.subject",
                            new Object[] {posts.get(0).getAlbumTitle()}, locale)
                    : messageSource.getMessage("email.postInterest.subject.many",
                            new Object[] {posts.size()}, locale);
            final MimeMessage message = createMessage(notification.getPublisherEmail(), null, subject, body);

            mailSender.send(message);
            LOGGER.info("Post interest email sent inquiryIds={}", inquiryIds);
        } catch (final MessagingException | RuntimeException exception) {
            LOGGER.error("Post interest email delivery failed inquiryIds={}", inquiryIds, exception);
        }
    }

    /*
     * Un solo template para todos los cambios de una consulta: el evento elige el asunto,
     * el titulo y el texto. Los datos de cobro y la direccion no viajan por correo: se ven
     * en la pagina de la venta, que es a donde lleva el enlace.
     */
    @Async
    @Override
    public void sendInquiryUpdateEmail(final InquiryUpdateNotification notification, final Locale locale) {
        try {
            final String prefix = INQUIRY_UPDATE_PREFIX + notification.getEvent().name();
            final Object[] titleArgument = {notification.getAlbumTitle()};
            final Context context = new Context(locale);
            context.setVariable("heading", messageSource.getMessage(prefix + ".heading", null, locale));
            context.setVariable("body", messageSource.getMessage(prefix + ".body", titleArgument, locale));
            context.setVariable("albumTitle", notification.getAlbumTitle());
            context.setVariable("artistName", notification.getArtistName());
            context.setVariable("releaseYear", notification.getReleaseYear());
            // Un rechazo ya no tiene nada que hacer en la venta: lleva a la bandeja del comprador.
            final String path = notification.getEvent() == InquiryEvent.REJECTED
                    ? "/inquiries/sent" : "/inquiries/" + notification.getInquiryId();
            context.setVariable("actionUrl", baseUrl + path);
            final String body = templateEngine.process(INQUIRY_UPDATE_TEMPLATE, context);
            final String subject = messageSource.getMessage(prefix + ".subject", titleArgument, locale);
            mailSender.send(createMessage(notification.getRecipientEmail(), null, subject, body));
            LOGGER.info("Inquiry update email sent inquiryId={} event={}", notification.getInquiryId(),
                    notification.getEvent());
        } catch (final MessagingException | RuntimeException exception) {
            LOGGER.error("Inquiry update email delivery failed inquiryId={} event={}", notification.getInquiryId(),
                    notification.getEvent(), exception);
        }
    }

    // El texto viaja escapado por Thymeleaf y con sus saltos de linea. El log no lo registra.
    @Async
    @Override
    public void sendMessageEmail(final MessageNotification notification, final Locale locale) {
        try {
            final Context context = new Context(locale);
            context.setVariable("senderUsername", notification.getSenderUsername());
            context.setVariable("body", notification.getBody());
            context.setVariable("albumTitle", notification.getAlbumTitle());
            context.setVariable("artistName", notification.getArtistName());
            context.setVariable("releaseYear", notification.getReleaseYear());
            context.setVariable("actionUrl", inquiryUrl(notification.getInquiryId()) + CONVERSATION_ANCHOR);
            final String body = templateEngine.process(MESSAGE_TEMPLATE, context);
            final Object[] titleArgument = {notification.getAlbumTitle()};
            final String subject = messageSource.getMessage("email.message.subject", titleArgument, locale);
            mailSender.send(createMessage(notification.getRecipientEmail(), null, subject, body));
            LOGGER.info("Message email sent inquiryId={}", notification.getInquiryId());
        } catch (final MessagingException | RuntimeException exception) {
            LOGGER.error("Message email delivery failed inquiryId={}", notification.getInquiryId(), exception);
        }
    }

    @Async
    @Override
    public void sendPasswordChangedEmail(final User user, final Locale locale) {
        try {
            final Context context = new Context(locale);
            context.setVariable("username", user.getUsername());
            final String body = templateEngine.process(PASSWORD_CHANGED_TEMPLATE, context);
            final String subject = messageSource.getMessage("email.passwordChanged.subject", null, locale);
            final MimeMessage message = createMessage(user.getEmail(), null, subject, body);

            mailSender.send(message);
            LOGGER.info("Password changed email sent userId={}", user.getId());
        } catch (final MessagingException | RuntimeException exception) {
            LOGGER.error("Password changed email delivery failed userId={}", user.getId(), exception);
        }
    }

    @Async
    @Override
    public void sendPasswordResetEmail(final User user, final String token, final Locale locale) {
        try {
            final Context context = new Context(locale);
            context.setVariable("resetUrl", baseUrl + "/reset-password?token=" + token);
            final String body = templateEngine.process(PASSWORD_RESET_TEMPLATE, context);
            final String subject = messageSource.getMessage("email.passwordReset.subject", null, locale);
            final MimeMessage message = createMessage(user.getEmail(), null, subject, body);

            mailSender.send(message);
            LOGGER.info("Password reset email sent userId={}", user.getId());
        } catch (final MessagingException | RuntimeException exception) {
            LOGGER.error("Password reset email delivery failed userId={}", user.getId(), exception);
        }
    }

    private String inquiryUrl(final long inquiryId) {
        return inquiriesUrl() + inquiryId;
    }

    private String inquiriesUrl() {
        return baseUrl + "/inquiries/";
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
