---
title: "EmailServiceImplTest"
categories: ["Services", "Testing"]
type: "test"
module: "services"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["services/src/test/java/ar/edu/itba/paw/services/EmailServiceImplTest.java"]
---

# EmailServiceImplTest

Tests de `EmailServiceImpl` en `services`: 17 casos declarados. Cubre: plantillas reales con un remitente falso: enlaces, asuntos por idioma, escape del texto, un vinilo o varios, y errores que no se propagan. No se ejecutaron en esta actualización del Vault; ver [[Testing and evidence]].

## Guía de lectura

Datos y dependencias declaradas: `FROM_EMAIL`, `PUBLISHER_EMAIL`, `CONTACT_EMAIL`, `CONTACT_MESSAGE`, `ESCAPED_CONTACT_MESSAGE`, `BASE_URL`, `SPANISH`, `ENGLISH`, `ARTAUD`, `KAMIKAZE`, `mailSender`, `emailService`, `lastMessage`, `failNextDelivery`.

Operaciones para localizar en la fuente: `setUp`, `templateEngine`, `messageSource`, `firstAddress`, `send`, `getLastMessage`, `failNextDelivery`.

Casos declarados: 17.

- `testSendPostInterestEmailWhenDeliverySucceedsBuildsExpectedMessage`
- `testSendPostInterestEmailWhenLocaleIsEnglishUsesEnglishCopy`
- `testSendPostInterestEmailWhenDeliverySucceedsLinksToTheInquiryDetail`
- `testSendPostInterestEmailWhenMessageIsPresentReturnsBodyWithMessage`
- `testSendPostInterestEmailWhenMessageIsMissingReturnsBodyWithoutMessage`
- `testSendPostInterestEmailWhenSeveralPostsReturnsOneMessageLinkingEachInquiry`
- `testSendPostInterestEmailWhenDeliveryFailsDoesNotPropagateFailure`
- `testSendInquiryUpdateEmailWhenSaleIsAcceptedReturnsEmailLinkedToTheSale`
- `testSendInquiryUpdateEmailWhenInquiryIsRejectedReturnsEmailLinkedToSentInbox`
- `testSendInquiryUpdateEmailWhenDeliveryFailsReturnsWithoutPropagatingFailure`
- `testSendMessageEmailWhenDeliverySucceedsBuildsExpectedMessage`
- `testSendMessageEmailWhenBodyHasMarkupReturnsEscapedBodyWithLineBreaks`
- `testSendMessageEmailWhenLocaleIsEnglishReturnsEnglishSubject`
- `testSendMessageEmailWhenDeliveryFailsReturnsWithoutPropagatingFailure`
- `testSendWelcomeEmailWhenDeliverySucceedsBuildsExpectedMessage`
- `testSendWelcomeEmailWhenDeliveryFailsDoesNotPropagateFailure`
- `testSendVerificationEmailWhenDeliverySucceedsReturnsEmailWithSingleUseLink`

## Conexiones

Referencias estáticas a tipos del proyecto: [[Address]], [[EmailServiceImpl]], [[InquiryEvent]], [[InquiryUpdateNotification]], [[Message]], [[MessageNotification]], [[PostInterestNotification]], [[User]], [[UserRole]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [services/src/test/java/ar/edu/itba/paw/services/EmailServiceImplTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/EmailServiceImplTest.java>), líneas 1–448.

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.User;
import ar.edu.itba.paw.models.UserRole;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.function.Executable;
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
import java.util.List;
import java.util.Locale;

public class EmailServiceImplTest {

    private static final String FROM_EMAIL = "app@example.com";
    private static final String PUBLISHER_EMAIL = "publisher@example.com";
    private static final String CONTACT_EMAIL = "buyer@example.com";
    private static final String CONTACT_MESSAGE = "Te ofrezco <b>35000</b>,\nlo paso a buscar el sabado.";
    private static final String ESCAPED_CONTACT_MESSAGE =
            "Te ofrezco &lt;b&gt;35000&lt;/b&gt;,\nlo paso a buscar el sabado.";
    private static final String BASE_URL = "http://pawserver.it.itba.edu.ar/paw-2026b-14";
    private static final Locale SPANISH = Locale.forLanguageTag("es");
    private static final Locale ENGLISH = Locale.forLanguageTag("en");
    private static final PostInterestNotification.InterestedPost ARTAUD =
            new PostInterestNotification.InterestedPost(42L, 9L, "Artaud", "Pescado Rabioso", 1973);
    private static final PostInterestNotification.InterestedPost KAMIKAZE =
            new PostInterestNotification.InterestedPost(43L, 10L, "Kamikaze", "Luis Alberto Spinetta", 1982);

    private CapturingMailSender mailSender;
    private EmailServiceImpl emailService;

    @BeforeEach
    public void setUp() {
        mailSender = new CapturingMailSender();
        emailService = new EmailServiceImpl(mailSender, templateEngine(), messageSource(), FROM_EMAIL, BASE_URL);
    }

    @Test
    public void testSendPostInterestEmailWhenDeliverySucceedsBuildsExpectedMessage()
            throws MessagingException, IOException {
        // 1. Arrange
        final PostInterestNotification notification = new PostInterestNotification(
                PUBLISHER_EMAIL, "Ana", null, List.of(ARTAUD));

        // 2. Exercise
        emailService.sendPostInterestEmail(notification, SPANISH);

        // 3. Assert
        final MimeMessage message = mailSender.getLastMessage();
        Assertions.assertNotNull(message);
        Assertions.assertEquals(FROM_EMAIL, firstAddress(message.getFrom()));
        Assertions.assertEquals(PUBLISHER_EMAIL, firstAddress(message.getRecipients(Message.RecipientType.TO)));
        // Sin Reply-To explicito JavaMail devuelve el From: el Publicante no ve el correo del comprador.
        Assertions.assertEquals(FROM_EMAIL, firstAddress(message.getReplyTo()));
        Assertions.assertEquals("Alguien está interesado en Artaud", message.getSubject());
        final String body = message.getContent().toString();
        Assertions.assertTrue(body.contains("Ana"));
        Assertions.assertFalse(body.contains(CONTACT_EMAIL));
        Assertions.assertTrue(body.contains("Artaud"));
        Assertions.assertTrue(body.contains("Pescado Rabioso"));
        Assertions.assertTrue(body.contains("1973"));
    }

    @Test
    public void testSendPostInterestEmailWhenLocaleIsEnglishUsesEnglishCopy()
            throws MessagingException, IOException {
        // 1. Arrange
        final PostInterestNotification notification = new PostInterestNotification(
                PUBLISHER_EMAIL, "Ana", null, List.of(ARTAUD));

        // 2. Exercise
        emailService.sendPostInterestEmail(notification, ENGLISH);

        // 3. Assert
        final MimeMessage message = mailSender.getLastMessage();
        Assertions.assertEquals("Someone is interested in Artaud", message.getSubject());
        Assertions.assertTrue(message.getContent().toString().contains("Reply on quieroVinilos"));
    }

    @Test
    public void testSendPostInterestEmailWhenDeliverySucceedsLinksToTheInquiryDetail()
            throws MessagingException, IOException {
        // 1. Arrange
        final PostInterestNotification notification = new PostInterestNotification(
                PUBLISHER_EMAIL, "Ana", null, List.of(ARTAUD));

        // 2. Exercise
        emailService.sendPostInterestEmail(notification, SPANISH);

        // 3. Assert
        final String body = mailSender.getLastMessage().getContent().toString();
        Assertions.assertTrue(body.contains("href=\"" + BASE_URL + "/inquiries/9\""));
    }

    @Test
    public void testSendPostInterestEmailWhenMessageIsPresentReturnsBodyWithMessage()
            throws MessagingException, IOException {
        // 1. Arrange
        final PostInterestNotification notification = new PostInterestNotification(
                PUBLISHER_EMAIL, "Ana", CONTACT_MESSAGE, List.of(ARTAUD));

        // 2. Exercise
        emailService.sendPostInterestEmail(notification, SPANISH);

        // 3. Assert
        final String body = mailSender.getLastMessage().getContent().toString();
        Assertions.assertTrue(body.contains("Mensaje:"));
        // El pre-line va en el span y no en el <p>, para que el unico salto de linea que se
        // respete sea el del mensaje y no la indentacion del template.
        Assertions.assertTrue(body.contains(
                "<span style=\"white-space: pre-line;\">" + ESCAPED_CONTACT_MESSAGE + "</span>"));
    }

    @Test
    public void testSendPostInterestEmailWhenMessageIsMissingReturnsBodyWithoutMessage()
            throws MessagingException, IOException {
        // 1. Arrange
        final PostInterestNotification notification = new PostInterestNotification(
                PUBLISHER_EMAIL, "Ana", null, List.of(ARTAUD));

        // 2. Exercise
        emailService.sendPostInterestEmail(notification, SPANISH);

        // 3. Assert
        final String body = mailSender.getLastMessage().getContent().toString();
        Assertions.assertFalse(body.contains("Mensaje:"));
    }

    @Test
    public void testSendPostInterestEmailWhenSeveralPostsReturnsOneMessageLinkingEachInquiry()
            throws MessagingException, IOException {
        // 1. Arrange
        final PostInterestNotification notification = new PostInterestNotification(
                PUBLISHER_EMAIL, "Ana", null, List.of(ARTAUD, KAMIKAZE));

        // 2. Exercise
        emailService.sendPostInterestEmail(notification, SPANISH);

        // 3. Assert
        final MimeMessage message = mailSender.getLastMessage();
        Assertions.assertEquals("Alguien está interesado en 2 de tus vinilos", message.getSubject());
        final String body = message.getContent().toString();
        Assertions.assertTrue(body.contains("Ana está interesado en 2 de tus vinilos."));
        Assertions.assertTrue(body.contains("Artaud"));
        Assertions.assertTrue(body.contains("Kamikaze"));
        Assertions.assertTrue(body.contains("href=\"" + BASE_URL + "/inquiries/9\""));
        Assertions.assertTrue(body.contains("href=\"" + BASE_URL + "/inquiries/10\""));
    }

    @Test
    public void testSendPostInterestEmailWhenDeliveryFailsDoesNotPropagateFailure() {
        // 1. Arrange
        mailSender.failNextDelivery();
        final PostInterestNotification notification = new PostInterestNotification(
                PUBLISHER_EMAIL, "Ana", null, List.of(ARTAUD));

        // 2. Exercise
        Assertions.assertDoesNotThrow(() -> emailService.sendPostInterestEmail(notification, SPANISH));

        // 3. Assert
        Assertions.assertNull(mailSender.getLastMessage());
    }

    @Test
    public void testSendInquiryUpdateEmailWhenSaleIsAcceptedReturnsEmailLinkedToTheSale()
            throws MessagingException, IOException {
        // 1. Arrange
        final InquiryUpdateNotification notification = new InquiryUpdateNotification(
                InquiryEvent.ACCEPTED, 9L, CONTACT_EMAIL, "Artaud", "Pescado Rabioso", 1973);

        // 2. Exercise
        emailService.sendInquiryUpdateEmail(notification, SPANISH);

        // 3. Assert
        final MimeMessage message = mailSender.getLastMessage();
        Assertions.assertEquals(CONTACT_EMAIL, firstAddress(message.getRecipients(Message.RecipientType.TO)));
        Assertions.assertEquals("Tu consulta por Artaud fue aceptada", message.getSubject());
        final String body = message.getContent().toString();
        Assertions.assertTrue(body.contains("Pescado Rabioso"));
        Assertions.assertTrue(body.contains("href=\"" + BASE_URL + "/inquiries/9\""));
    }

    @Test
    public void testSendInquiryUpdateEmailWhenInquiryIsRejectedReturnsEmailLinkedToSentInbox()
            throws MessagingException, IOException {
        // 1. Arrange
        final InquiryUpdateNotification notification = new InquiryUpdateNotification(
                InquiryEvent.REJECTED, 9L, CONTACT_EMAIL, "Artaud", "Pescado Rabioso", 1973);

        // 2. Exercise
        emailService.sendInquiryUpdateEmail(notification, ENGLISH);

        // 3. Assert
        final MimeMessage message = mailSender.getLastMessage();
        Assertions.assertEquals("Your inquiry about Artaud was declined", message.getSubject());
        Assertions.assertTrue(message.getContent().toString().contains("href=\"" + BASE_URL + "/inquiries/sent\""));
    }

    @Test
    public void testSendInquiryUpdateEmailWhenDeliveryFailsReturnsWithoutPropagatingFailure() {
        // 1. Arrange
        mailSender.failNextDelivery();
        final InquiryUpdateNotification notification = new InquiryUpdateNotification(
                InquiryEvent.CONFIRMED, 9L, CONTACT_EMAIL, "Artaud", "Pescado Rabioso", 1973);

        // 2. Exercise
        final Executable send = () -> emailService.sendInquiryUpdateEmail(notification, SPANISH);

        // 3. Assert
        Assertions.assertDoesNotThrow(send);
        Assertions.assertNull(mailSender.getLastMessage());
    }

    @Test
    public void testSendMessageEmailWhenDeliverySucceedsBuildsExpectedMessage()
            throws MessagingException, IOException {
        // 1. Arrange
        final MessageNotification notification = new MessageNotification(
                9L, PUBLISHER_EMAIL, "Ana", "Sigue disponible?", "Artaud", "Pescado Rabioso", 1973);

        // 2. Exercise
        emailService.sendMessageEmail(notification, SPANISH);

        // 3. Assert
        final MimeMessage message = mailSender.getLastMessage();
        Assertions.assertEquals(PUBLISHER_EMAIL, firstAddress(message.getRecipients(Message.RecipientType.TO)));
        Assertions.assertEquals(FROM_EMAIL, firstAddress(message.getReplyTo()));
        Assertions.assertEquals("Nuevo mensaje sobre Artaud", message.getSubject());
        final String body = message.getContent().toString();
        Assertions.assertTrue(body.contains("Ana te escribió:"));
        Assertions.assertTrue(body.contains("Sigue disponible?"));
        Assertions.assertTrue(body.contains("Pescado Rabioso"));
        Assertions.assertTrue(body.contains("1973"));
        Assertions.assertTrue(body.contains("href=\"" + BASE_URL + "/inquiries/9#conversation\""));
    }

    @Test
    public void testSendMessageEmailWhenBodyHasMarkupReturnsEscapedBodyWithLineBreaks()
            throws MessagingException, IOException {
        // 1. Arrange
        final MessageNotification notification = new MessageNotification(
                9L, CONTACT_EMAIL, "Ana", CONTACT_MESSAGE, "Artaud", "Pescado Rabioso", 1973);

        // 2. Exercise
        emailService.sendMessageEmail(notification, SPANISH);

        // 3. Assert
        final String body = mailSender.getLastMessage().getContent().toString();
        Assertions.assertFalse(body.contains("<b>35000</b>"));
        Assertions.assertTrue(body.contains(
                "<span style=\"white-space: pre-line;\">" + ESCAPED_CONTACT_MESSAGE + "</span>"));
    }

    @Test
    public void testSendMessageEmailWhenLocaleIsEnglishReturnsEnglishSubject()
            throws MessagingException, IOException {
        // 1. Arrange
        final MessageNotification notification = new MessageNotification(
                9L, CONTACT_EMAIL, "Ana", "Hi", "Artaud", "Pescado Rabioso", 1973);

        // 2. Exercise
        emailService.sendMessageEmail(notification, ENGLISH);

        // 3. Assert
        final MimeMessage message = mailSender.getLastMessage();
        Assertions.assertEquals(CONTACT_EMAIL, firstAddress(message.getRecipients(Message.RecipientType.TO)));
        Assertions.assertEquals("New message about Artaud", message.getSubject());
        Assertions.assertTrue(message.getContent().toString().contains("Ana wrote to you:"));
    }

    @Test
    public void testSendMessageEmailWhenDeliveryFailsReturnsWithoutPropagatingFailure() {
        // 1. Arrange
        mailSender.failNextDelivery();
        final MessageNotification notification = new MessageNotification(
                9L, CONTACT_EMAIL, "Ana", "Hola", "Artaud", "Pescado Rabioso", 1973);

        // 2. Exercise
        final Executable send = () -> emailService.sendMessageEmail(notification, SPANISH);

        // 3. Assert
        Assertions.assertDoesNotThrow(send);
        Assertions.assertNull(mailSender.getLastMessage());
    }

    @Test
    public void testSendWelcomeEmailWhenDeliverySucceedsBuildsExpectedMessage()
            throws MessagingException, IOException {
        // 1. Arrange
        final User user = new User(7L, "Luz", CONTACT_EMAIL, "hash", UserRole.USER, true, "es");

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
        final User user = new User(7L, "Luz", CONTACT_EMAIL, "hash", UserRole.USER, true, "es");

        // 2. Exercise
        Assertions.assertDoesNotThrow(() -> emailService.sendWelcomeEmail(user, SPANISH));

        // 3. Assert
        Assertions.assertNull(mailSender.getLastMessage());
    }

    @Test
    public void testSendVerificationEmailWhenDeliverySucceedsReturnsEmailWithSingleUseLink()
            throws MessagingException, IOException {
        // 1. Arrange
        final User user = new User(7L, "Luz", CONTACT_EMAIL, null,
                UserRole.USER, false, "es");
        final String token = "safe-token";

        // 2. Exercise
        emailService.sendVerificationEmail(user, token, SPANISH);

        // 3. Assert
        final MimeMessage message = mailSender.getLastMessage();
        Assertions.assertNotNull(message);
        Assertions.assertEquals(CONTACT_EMAIL, firstAddress(message.getRecipients(Message.RecipientType.TO)));
        Assertions.assertEquals("Confirmá tu correo en quieroVinilos", message.getSubject());
        Assertions.assertTrue(message.getContent().toString()
                .contains("href=\"" + BASE_URL + "/verify?token=" + token + "\""));
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
        source.addMessage("email.welcome.cta", SPANISH, "Ver quieroVinilos");
        source.addMessage("email.verification.subject", SPANISH, "Confirmá tu correo en quieroVinilos");
        source.addMessage("email.verification.body", SPANISH, "Hola {0}, confirmá tu correo para activar tu cuenta.");
        source.addMessage("email.verification.cta", SPANISH, "Confirmar correo");
        source.addMessage("email.postInterest.subject", SPANISH, "Alguien está interesado en {0}");
        source.addMessage("email.postInterest.heading", SPANISH, "Hay interés en tu publicación");
        source.addMessage("email.postInterest.intro", SPANISH, "{0} está interesado en tu publicación.");
        source.addMessage("email.postInterest.subject.many", SPANISH, "Alguien está interesado en {0} de tus vinilos");
        source.addMessage("email.postInterest.intro.many", SPANISH, "{0} está interesado en {1} de tus vinilos.");
        source.addMessage("email.postInterest.contact", SPANISH, "Contacto:");
        source.addMessage("email.postInterest.album", SPANISH, "Álbum:");
        source.addMessage("email.postInterest.message", SPANISH, "Mensaje:");
        source.addMessage("email.postInterest.cta", SPANISH, "Responder en quieroVinilos");
        source.addMessage("email.message.subject", SPANISH, "Nuevo mensaje sobre {0}");
        source.addMessage("email.message.heading", SPANISH, "Tenés un mensaje nuevo");
        source.addMessage("email.message.intro", SPANISH, "{0} te escribió:");
        source.addMessage("email.message.cta", SPANISH, "Responder en quieroVinilos");
        source.addMessage("email.inquiryUpdate.album", SPANISH, "Publicación:");
        source.addMessage("email.inquiryUpdate.cta", SPANISH, "Ver la consulta");
        source.addMessage("email.inquiryUpdate.ACCEPTED.subject", SPANISH, "Tu consulta por {0} fue aceptada");
        source.addMessage("email.inquiryUpdate.ACCEPTED.heading", SPANISH, "Tu consulta fue aceptada");
        source.addMessage("email.inquiryUpdate.ACCEPTED.body", SPANISH,
                "Quien vende aceptó tu consulta por {0} y lo reservó para vos. "
                        + "Entrá para ver a dónde transferir y subir el comprobante.");
        source.addMessage("email.inquiryUpdate.REJECTED.subject", SPANISH, "Tu consulta por {0} fue rechazada");
        source.addMessage("email.inquiryUpdate.REJECTED.heading", SPANISH, "Tu consulta fue rechazada");
        source.addMessage("email.inquiryUpdate.REJECTED.body", SPANISH,
                "Quien vende no va a avanzar con tu consulta por {0}.");

        source.addMessage("email.postInterest.subject", ENGLISH, "Someone is interested in {0}");
        source.addMessage("email.postInterest.heading", ENGLISH, "Someone is interested in your post");
        source.addMessage("email.postInterest.intro", ENGLISH, "{0} is interested in your post.");
        source.addMessage("email.postInterest.contact", ENGLISH, "Contact:");
        source.addMessage("email.postInterest.album", ENGLISH, "Album:");
        source.addMessage("email.postInterest.message", ENGLISH, "Message:");
        source.addMessage("email.postInterest.cta", ENGLISH, "Reply on quieroVinilos");
        source.addMessage("email.message.subject", ENGLISH, "New message about {0}");
        source.addMessage("email.message.heading", ENGLISH, "You have a new message");
        source.addMessage("email.message.intro", ENGLISH, "{0} wrote to you:");
        source.addMessage("email.message.cta", ENGLISH, "Reply on quieroVinilos");
        source.addMessage("email.inquiryUpdate.album", ENGLISH, "Listing:");
        source.addMessage("email.inquiryUpdate.cta", ENGLISH, "View inquiry");
        source.addMessage("email.inquiryUpdate.ACCEPTED.subject", ENGLISH, "Your inquiry about {0} was accepted");
        source.addMessage("email.inquiryUpdate.ACCEPTED.heading", ENGLISH, "Your inquiry was accepted");
        source.addMessage("email.inquiryUpdate.ACCEPTED.body", ENGLISH,
                "The seller accepted your inquiry about {0} and reserved it for you. "
                        + "Open it to see where to transfer and upload the receipt.");
        source.addMessage("email.inquiryUpdate.REJECTED.subject", ENGLISH, "Your inquiry about {0} was declined");
        source.addMessage("email.inquiryUpdate.REJECTED.heading", ENGLISH, "Your inquiry was declined");
        source.addMessage("email.inquiryUpdate.REJECTED.body", ENGLISH,
                "The seller will not go ahead with your inquiry about {0}.");
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
