---
title: "EmailServiceImplTest"
categories: ["Testing"]
type: "test"
module: "services"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "testing"]
sources: ["services/src/test/java/ar/edu/itba/paw/services/EmailServiceImplTest.java"]
---

# EmailServiceImplTest

Constructs a real EmailServiceImpl and Thymeleaf engine with a StaticMessageSource and a capturing fake JavaMailSender. It checks recipient, Reply-To, subject, HTML content, propagated contact failure and swallowed welcome failure. Direct construction bypasses Spring async proxies, so these tests do not prove background scheduling.

Production connections: [[EmailDeliveryException]], [[EmailServiceImpl]], [[PostInterestNotification]], [[User]].

## Test cases

- `testSendPostInterestEmailWhenDeliverySucceedsBuildsExpectedMessage`
- `testSendPostInterestEmailWhenDeliveryFailsThrowsEmailDeliveryException`
- `testSendWelcomeEmailWhenDeliverySucceedsBuildsExpectedMessage`
- `testSendWelcomeEmailWhenDeliveryFailsDoesNotPropagateFailure`

## Exact test source

[services/src/test/java/ar/edu/itba/paw/services/EmailServiceImplTest.java, lines 1–164](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/EmailServiceImplTest.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.User;
import ar.edu.itba.paw.services.exceptions.EmailDeliveryException;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.context.support.StaticMessageSource;
import org.springframework.mail.MailException;
import org.springframework.mail.MailSendException;
import org.springframework.mail.javamail.JavaMailSenderImpl;
import org.thymeleaf.spring5.SpringTemplateEngine;
import org.thymeleaf.templatemode.TemplateMode;
import org.thymeleaf.templateresolver.ClassLoaderTemplateResolver;

import javax.mail.Address;
import javax.mail.Message;
import javax.mail.MessagingException;
import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeMessage;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.Locale;

public class EmailServiceImplTest {

    private static final String FROM_EMAIL = "app@example.com";
    private static final String PUBLISHER_EMAIL = "publisher@example.com";
    private static final String CONTACT_EMAIL = "buyer@example.com";
    private static final Locale SPANISH = Locale.forLanguageTag("es");

    private CapturingMailSender mailSender;
    private EmailServiceImpl emailService;

    @BeforeEach
    public void setUp() {
        mailSender = new CapturingMailSender();
        emailService = new EmailServiceImpl(mailSender, templateEngine(), messageSource(), FROM_EMAIL);
    }

    @Test
    public void testSendPostInterestEmailWhenDeliverySucceedsBuildsExpectedMessage()
            throws MessagingException, IOException {
        // 1. Arrange
        final PostInterestNotification notification = new PostInterestNotification(
                42L, PUBLISHER_EMAIL, "Ana", CONTACT_EMAIL, "Artaud", "Pescado Rabioso", 1973);

        // 2. Exercise
        emailService.sendPostInterestEmail(notification);

        // 3. Assert
        final MimeMessage message = mailSender.getLastMessage();
        Assertions.assertNotNull(message);
        Assertions.assertEquals(FROM_EMAIL, firstAddress(message.getFrom()));
        Assertions.assertEquals(PUBLISHER_EMAIL, firstAddress(message.getRecipients(Message.RecipientType.TO)));
        Assertions.assertEquals(CONTACT_EMAIL, firstAddress(message.getReplyTo()));
        Assertions.assertEquals("Alguien está interesado en Artaud", message.getSubject());
        final String body = message.getContent().toString();
        Assertions.assertTrue(body.contains("Ana"));
        Assertions.assertTrue(body.contains(CONTACT_EMAIL));
        Assertions.assertTrue(body.contains("Artaud"));
        Assertions.assertTrue(body.contains("Pescado Rabioso"));
        Assertions.assertTrue(body.contains("1973"));
    }

    @Test
    public void testSendPostInterestEmailWhenDeliveryFailsThrowsEmailDeliveryException() {
        // 1. Arrange
        mailSender.failNextDelivery();
        final PostInterestNotification notification = new PostInterestNotification(
                42L, PUBLISHER_EMAIL, "Ana", CONTACT_EMAIL, "Artaud", "Pescado Rabioso", 1973);

        // 2. Exercise
        final EmailDeliveryException exception = Assertions.assertThrows(
                EmailDeliveryException.class, () -> emailService.sendPostInterestEmail(notification));

        // 3. Assert
        Assertions.assertInstanceOf(MailSendException.class, exception.getCause());
        Assertions.assertTrue(exception.getMessage().contains("postId=42"));
    }

    @Test
    public void testSendWelcomeEmailWhenDeliverySucceedsBuildsExpectedMessage()
            throws MessagingException, IOException {
        // 1. Arrange
        final User user = new User(7L, "Luz", CONTACT_EMAIL);

        // 2. Exercise
        emailService.sendWelcomeEmail(user, SPANISH);

        // 3. Assert
        final MimeMessage message = mailSender.getLastMessage();
        Assertions.assertNotNull(message);
        Assertions.assertEquals(CONTACT_EMAIL, firstAddress(message.getRecipients(Message.RecipientType.TO)));
        Assertions.assertEquals("Bienvenido a quieroVinilos", message.getSubject());
        Assertions.assertTrue(message.getContent().toString().contains("Luz"));
    }

    @Test
    public void testSendWelcomeEmailWhenDeliveryFailsDoesNotPropagateFailure() {
        // 1. Arrange
        mailSender.failNextDelivery();
        final User user = new User(7L, "Luz", CONTACT_EMAIL);

        // 2. Exercise
        Assertions.assertDoesNotThrow(() -> emailService.sendWelcomeEmail(user, SPANISH));

        // 3. Assert
        Assertions.assertNull(mailSender.getLastMessage());
    }

    private static SpringTemplateEngine templateEngine() {
        final ClassLoaderTemplateResolver resolver = new ClassLoaderTemplateResolver();
        resolver.setPrefix("mail/");
        resolver.setSuffix(".html");
        resolver.setTemplateMode(TemplateMode.HTML);
        resolver.setCharacterEncoding(StandardCharsets.UTF_8.name());

        final SpringTemplateEngine engine = new SpringTemplateEngine();
        engine.setTemplateResolver(resolver);
        engine.setTemplateEngineMessageSource(messageSource());
        return engine;
    }

    private static StaticMessageSource messageSource() {
        final StaticMessageSource source = new StaticMessageSource();
        source.addMessage("email.welcome.subject", SPANISH, "Bienvenido a quieroVinilos");
        source.addMessage("email.welcome.body", SPANISH, "Hola {0}, gracias por registrarte.");
        source.addMessage("email.postInterest.subject", SPANISH, "Alguien está interesado en {0}");
        source.addMessage("email.postInterest.heading", SPANISH, "Hay interés en tu publicación");
        source.addMessage("email.postInterest.intro", SPANISH, "{0} está interesado en tu publicación.");
        source.addMessage("email.postInterest.contact", SPANISH, "Contacto:");
        source.addMessage("email.postInterest.album", SPANISH, "Álbum:");
        return source;
    }

    private static String firstAddress(final Address[] addresses) {
        Assertions.assertNotNull(addresses);
        Assertions.assertTrue(addresses.length > 0);
        return ((InternetAddress) addresses[0]).getAddress();
    }

    private static final class CapturingMailSender extends JavaMailSenderImpl {

        private MimeMessage lastMessage;
        private boolean failNextDelivery;

        @Override
        public void send(final MimeMessage mimeMessage) throws MailException {
            if (failNextDelivery) {
                throw new MailSendException("Simulated SMTP failure");
            }
            lastMessage = mimeMessage;
        }

        public MimeMessage getLastMessage() {
            return lastMessage;
        }

        public void failNextDelivery() {
            failNextDelivery = true;
        }
    }
}
```

[[Testing and evidence]] · [[Source inventory]]
