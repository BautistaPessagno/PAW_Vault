---
title: "InquiryController"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/InquiryController.java"]
---

# InquiryController

Bandejas, página de la consulta y un endpoint por transición de la venta, además de mensajes, reseñas y descarga del comprobante con headers de seguridad. Cada endpoint lleva su `@PreAuthorize`. Ver [[Inquiry and sale flow]].

## Guía de lectura

Datos y dependencias declaradas: `inquiryService`.

Operaciones para localizar en la fuente: `initTextBinder`, `received`, `sent`, `accept`, `reject`, `detail`, `detailView`, `sendMessage`, `saveReview`, `removeReview`, `uploadReceipt`, `receipt`, `confirm`, `requestReceipt`, `cancel`, `missingPaymentInfo`, `invalidState`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[AuthenticatedUser]], [[InquiryDetail]], [[InquiryService]], [[InvalidInquiryStateException]], [[InvalidMessageException]], [[InvalidReceiptException]], [[LineBreakNormalizingEditor]], [[MessageForm]], [[MessageRules]], [[MissingPaymentInfoException]], [[Receipt]], [[ReceiptForm]], [[ReviewForm]], [[ReviewRules]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/InquiryController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/InquiryController.java>), líneas 1–279.

```java
package ar.edu.itba.paw.webapp.controller;

import ar.edu.itba.paw.models.InquiryDetail;
import ar.edu.itba.paw.models.MessageRules;
import ar.edu.itba.paw.models.Receipt;
import ar.edu.itba.paw.models.ReviewRules;
import ar.edu.itba.paw.services.InquiryService;
import ar.edu.itba.paw.services.InvalidInquiryStateException;
import ar.edu.itba.paw.services.InvalidMessageException;
import ar.edu.itba.paw.services.InvalidReceiptException;
import ar.edu.itba.paw.services.MissingPaymentInfoException;
import ar.edu.itba.paw.webapp.form.LineBreakNormalizingEditor;
import ar.edu.itba.paw.webapp.form.MessageForm;
import ar.edu.itba.paw.webapp.form.ReceiptForm;
import ar.edu.itba.paw.webapp.form.ReviewForm;
import ar.edu.itba.paw.webapp.security.AuthenticatedUser;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.propertyeditors.StringTrimmerEditor;
import org.springframework.http.CacheControl;
import org.springframework.http.ContentDisposition;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.stereotype.Controller;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.WebDataBinder;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.InitBinder;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.servlet.ModelAndView;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import javax.validation.Valid;
import java.io.IOException;

/*
 * Las bandejas son de cualquier cuenta con sesion y toda accion sobre una consulta exige cuenta
 * verificada (ver SecurityConfig). La pertenencia de la publicacion que se acepta o se rechaza la
 * verifica el service. El detalle, la Conversacion y los endpoints de la Venta llevan ademas su
 * @PreAuthorize con @inquiryAccess; el service vuelve a chequear al actor antes de escribir.
 */
@Controller
@RequestMapping("/inquiries")
public class InquiryController {

    private final InquiryService inquiryService;

    @Autowired
    public InquiryController(final InquiryService inquiryService) {
        this.inquiryService = inquiryService;
    }

    // Igual que el formulario de contacto: el Mensaje y el comentario de la Resena llegan sin CRLF
    // ni espacios de mas, asi @Size mide lo mismo que el maxlength del textarea.
    @InitBinder({"messageForm", "reviewForm"})
    public void initTextBinder(final WebDataBinder binder) {
        binder.registerCustomEditor(String.class, new StringTrimmerEditor(true));
        binder.registerCustomEditor(String.class, "body", new LineBreakNormalizingEditor());
    }

    // Cada vista trae su propia pagina, y los dos totales de la sub-nav salen del service.
    @RequestMapping(method = RequestMethod.GET)
    public ModelAndView received(@AuthenticationPrincipal final AuthenticatedUser currentUser,
                                 @RequestParam(name = "page", defaultValue = "1") final int pageNumber) {
        final long userId = currentUser.getId();
        final ModelAndView modelAndView = new ModelAndView("inquiry/received");
        modelAndView.addObject("receivedPage", inquiryService.findReceivedGroupedByPost(userId, pageNumber));
        modelAndView.addObject("receivedCount", inquiryService.countReceivedBy(userId));
        modelAndView.addObject("sentCount", inquiryService.countSentBy(userId));
        return modelAndView;
    }

    @RequestMapping(value = "/sent", method = RequestMethod.GET)
    public ModelAndView sent(@AuthenticationPrincipal final AuthenticatedUser currentUser,
                             @RequestParam(name = "page", defaultValue = "1") final int pageNumber) {
        final long userId = currentUser.getId();
        final ModelAndView modelAndView = new ModelAndView("inquiry/sent");
        modelAndView.addObject("sentPage", inquiryService.findSentGroupedByPost(userId, pageNumber));
        modelAndView.addObject("sentCount", inquiryService.countSentBy(userId));
        modelAndView.addObject("receivedCount", inquiryService.countReceivedBy(userId));
        return modelAndView;
    }

    @PreAuthorize("@inquiryAccess.isSeller(authentication, #inquiryId)")
    @RequestMapping(value = "/{inquiryId:[0-9]+}/accept", method = RequestMethod.POST)
    public ModelAndView accept(@PathVariable("inquiryId") final long inquiryId,
                               @AuthenticationPrincipal final AuthenticatedUser currentUser,
                               final RedirectAttributes redirectAttributes) {
        inquiryService.accept(inquiryId, currentUser.getId());
        redirectAttributes.addFlashAttribute("saleNotice", "inquiry.sale.accepted");
        return new ModelAndView("redirect:/inquiries/" + inquiryId);
    }

    @PreAuthorize("@inquiryAccess.isSeller(authentication, #inquiryId)")
    @RequestMapping(value = "/{inquiryId:[0-9]+}/reject", method = RequestMethod.POST)
    public ModelAndView reject(@PathVariable("inquiryId") final long inquiryId,
                               @AuthenticationPrincipal final AuthenticatedUser currentUser,
                               final RedirectAttributes redirectAttributes) {
        inquiryService.reject(inquiryId, currentUser.getId());
        redirectAttributes.addFlashAttribute("inquiryRejected", true);
        return new ModelAndView("redirect:/inquiries");
    }

    // La Consulta en cualquier estado, para las dos partes, con su Conversacion al pie. La Resena
    // vigente, si la hay, precarga su formulario.
    @PreAuthorize("@inquiryAccess.isParty(authentication, #inquiryId)")
    @RequestMapping(value = "/{inquiryId:[0-9]+}", method = RequestMethod.GET)
    public ModelAndView detail(@PathVariable("inquiryId") final long inquiryId,
                               @AuthenticationPrincipal final AuthenticatedUser currentUser) {
        final InquiryDetail detail = inquiryService.findDetail(inquiryId, currentUser.getId());
        return detailView(detail, new ReceiptForm(), new MessageForm(), ReviewForm.of(detail.getOwnReview()));
    }

    // Al re-renderizar desde un POST con errores, el form enviado vuelve tal como llego. Si no se
    // envio la Resena (reviewForm null), su formulario vuelve precargado con la vigente.
    private ModelAndView detailView(final long inquiryId, final long viewerId, final ReceiptForm receiptForm,
                                    final MessageForm messageForm, final ReviewForm reviewForm) {
        final InquiryDetail detail = inquiryService.findDetail(inquiryId, viewerId);
        return detailView(detail, receiptForm, messageForm,
                reviewForm == null ? ReviewForm.of(detail.getOwnReview()) : reviewForm);
    }

    private static ModelAndView detailView(final InquiryDetail detail, final ReceiptForm receiptForm,
                                           final MessageForm messageForm, final ReviewForm reviewForm) {
        final ModelAndView modelAndView = new ModelAndView("inquiry/detail");
        modelAndView.addObject("detail", detail);
        modelAndView.addObject("receiptForm", receiptForm);
        modelAndView.addObject("messageForm", messageForm);
        modelAndView.addObject("reviewForm", reviewForm);
        modelAndView.addObject("maxRating", ReviewRules.MAX_RATING);
        modelAndView.addObject("maxReviewLength", ReviewRules.MAX_BODY_LENGTH);
        modelAndView.addObject("maxMessageLength", MessageRules.MAX_LENGTH);
        return modelAndView;
    }

    /*
     * Una Conversacion cerrada cae en el handler de InvalidInquiryStateException: 409. El service
     * se llama aun con errores de validacion: decide el cierre antes que el texto, y el form
     * aplica las mismas MessageRules, asi que un texto invalido nunca llega a guardarse.
     */
    @PreAuthorize("@inquiryAccess.isParty(authentication, #inquiryId)")
    @RequestMapping(value = "/{inquiryId:[0-9]+}/messages", method = RequestMethod.POST)
    public ModelAndView sendMessage(@PathVariable("inquiryId") final long inquiryId,
                                    @AuthenticationPrincipal final AuthenticatedUser currentUser,
                                    @Valid @ModelAttribute("messageForm") final MessageForm messageForm,
                                    final BindingResult bindingResult) {
        try {
            inquiryService.sendMessage(inquiryId, currentUser.getId(), messageForm.getBody());
        } catch (final InvalidMessageException e) {
            if (!bindingResult.hasErrors()) {
                bindingResult.rejectValue("body", "inquiry.message.body.size");
            }
            return detailView(inquiryId, currentUser.getId(), new ReceiptForm(), messageForm, null);
        }
        return new ModelAndView("redirect:/inquiries/" + inquiryId + "#conversation");
    }

    @PreAuthorize("@inquiryAccess.isParty(authentication, #inquiryId)")
    @RequestMapping(value = "/{inquiryId:[0-9]+}/review", method = RequestMethod.POST)
    public ModelAndView saveReview(@PathVariable("inquiryId") final long inquiryId,
                                   @AuthenticationPrincipal final AuthenticatedUser currentUser,
                                   @Valid @ModelAttribute("reviewForm") final ReviewForm form,
                                   final BindingResult bindingResult,
                                   final RedirectAttributes redirectAttributes) {
        if (bindingResult.hasErrors()) {
            return detailView(inquiryId, currentUser.getId(), new ReceiptForm(), new MessageForm(), form);
        }
        inquiryService.saveReview(inquiryId, currentUser.getId(), form.getRating(), form.getBody());
        redirectAttributes.addFlashAttribute("reviewSaved", true);
        return new ModelAndView("redirect:/inquiries/" + inquiryId);
    }

    @PreAuthorize("@inquiryAccess.isParty(authentication, #inquiryId)")
    @RequestMapping(value = "/{inquiryId:[0-9]+}/review/remove", method = RequestMethod.POST)
    public ModelAndView removeReview(@PathVariable("inquiryId") final long inquiryId,
                                     @AuthenticationPrincipal final AuthenticatedUser currentUser,
                                     final RedirectAttributes redirectAttributes) {
        inquiryService.removeReview(inquiryId, currentUser.getId());
        redirectAttributes.addFlashAttribute("reviewRemoved", true);
        return new ModelAndView("redirect:/inquiries/" + inquiryId);
    }

    @PreAuthorize("@inquiryAccess.isBuyer(authentication, #inquiryId)")
    @RequestMapping(value = "/{inquiryId:[0-9]+}/receipt", method = RequestMethod.POST)
    public ModelAndView uploadReceipt(@PathVariable("inquiryId") final long inquiryId,
                                      @AuthenticationPrincipal final AuthenticatedUser currentUser,
                                      @Valid @ModelAttribute("receiptForm") final ReceiptForm receiptForm,
                                      final BindingResult bindingResult,
                                      final RedirectAttributes redirectAttributes) throws IOException {
        if (bindingResult.hasErrors()) {
            return detailView(inquiryId, currentUser.getId(), receiptForm, new MessageForm(), null);
        }
        try {
            inquiryService.uploadReceipt(inquiryId, currentUser.getId(), receiptForm.getReceipt().getContentType(),
                    receiptForm.getReceipt().getBytes());
        } catch (final InvalidReceiptException e) {
            bindingResult.rejectValue("receipt", "inquiry.receipt.invalid");
            return detailView(inquiryId, currentUser.getId(), receiptForm, new MessageForm(), null);
        }
        redirectAttributes.addFlashAttribute("saleNotice", "inquiry.sale.receiptUploaded");
        return new ModelAndView("redirect:/inquiries/" + inquiryId);
    }

    /*
     * El comprobante lo sube un usuario: nosniff y sin cache para que el navegador no lo
     * reinterprete ni lo guarde en disco. Las imagenes van ademas con sandbox. Los PDF no: el
     * visor integrado de Chrome se niega a abrir un documento con sandbox, y el PDF es el
     * comprobante mas comun. Por eso al subirlo se exige que empiece con la firma %PDF-, y sus
     * scripts corren en el sandbox propio del visor, sin acceso al origen. El nombre lleva la
     * extension del tipo para que al guardarlo quede un archivo que se pueda abrir.
     */
    @PreAuthorize("@inquiryAccess.isParty(authentication, #inquiryId)")
    @RequestMapping(value = "/{inquiryId:[0-9]+}/receipt", method = RequestMethod.GET)
    public ResponseEntity<byte[]> receipt(@PathVariable("inquiryId") final long inquiryId,
                                          @AuthenticationPrincipal final AuthenticatedUser currentUser) {
        final Receipt receipt = inquiryService.findReceipt(inquiryId, currentUser.getId());
        final MediaType mediaType = MediaType.parseMediaType(receipt.getContentType());
        final ResponseEntity.BodyBuilder response = ResponseEntity.ok()
                .contentType(mediaType)
                .cacheControl(CacheControl.noStore().cachePrivate())
                .header("X-Content-Type-Options", "nosniff")
                .header(HttpHeaders.CONTENT_DISPOSITION,
                        ContentDisposition.inline().filename(receipt.getFilename()).build().toString());
        if (!MediaType.APPLICATION_PDF.equalsTypeAndSubtype(mediaType)) {
            response.header("Content-Security-Policy", "sandbox");
        }
        return response.body(receipt.getData());
    }

    @PreAuthorize("@inquiryAccess.isSeller(authentication, #inquiryId)")
    @RequestMapping(value = "/{inquiryId:[0-9]+}/confirm", method = RequestMethod.POST)
    public ModelAndView confirm(@PathVariable("inquiryId") final long inquiryId,
                                @AuthenticationPrincipal final AuthenticatedUser currentUser,
                                final RedirectAttributes redirectAttributes) {
        inquiryService.confirm(inquiryId, currentUser.getId());
        redirectAttributes.addFlashAttribute("saleNotice", "inquiry.sale.confirmed");
        return new ModelAndView("redirect:/inquiries/" + inquiryId);
    }

    @PreAuthorize("@inquiryAccess.isSeller(authentication, #inquiryId)")
    @RequestMapping(value = "/{inquiryId:[0-9]+}/request-receipt", method = RequestMethod.POST)
    public ModelAndView requestReceipt(@PathVariable("inquiryId") final long inquiryId,
                                       @AuthenticationPrincipal final AuthenticatedUser currentUser,
                                       final RedirectAttributes redirectAttributes) {
        inquiryService.requestNewReceipt(inquiryId, currentUser.getId());
        redirectAttributes.addFlashAttribute("saleNotice", "inquiry.sale.receiptRequested");
        return new ModelAndView("redirect:/inquiries/" + inquiryId);
    }

    @PreAuthorize("@inquiryAccess.isParty(authentication, #inquiryId)")
    @RequestMapping(value = "/{inquiryId:[0-9]+}/cancel", method = RequestMethod.POST)
    public ModelAndView cancel(@PathVariable("inquiryId") final long inquiryId,
                               @AuthenticationPrincipal final AuthenticatedUser currentUser,
                               final RedirectAttributes redirectAttributes) {
        inquiryService.cancel(inquiryId, currentUser.getId());
        redirectAttributes.addFlashAttribute("saleNotice", "inquiry.sale.cancelled");
        return new ModelAndView("redirect:/inquiries/" + inquiryId);
    }

    // Sin datos de cobro no se puede aceptar: el perfil abre la fila para cargarlos.
    @ExceptionHandler(MissingPaymentInfoException.class)
    public ModelAndView missingPaymentInfo() {
        return new ModelAndView("redirect:/profile?missingPayment#account");
    }

    @ExceptionHandler(InvalidInquiryStateException.class)
    @ResponseStatus(HttpStatus.CONFLICT)
    public ModelAndView invalidState() {
        return new ModelAndView("error/409");
    }
}
```
