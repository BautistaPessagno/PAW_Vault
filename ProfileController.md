---
title: "ProfileController"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ProfileController.java"]
---

# ProfileController

Perfil privado: nombre, foto, contraseña, datos de cobro y libreta de direcciones, con las publicaciones propias paginadas y filtrables por estado (`postStatus`). Cada fila es un POST propio. Si se llegó desde una venta (`returnInquiryId`), guardar los datos de cobro vuelve a esa venta. Ver [[Profile flow]], [[Addresses and payment flow]] y [[Status filters flow]].

## Guía de lectura

Datos y dependencias declaradas: `userService`, `postService`, `addressService`, `inquiryService`, `sessionRegistry`.

Operaciones para localizar en la fuente: `initBinder`, `addressForm`, `profile`, `update`, `updateAvatar`, `changePassword`, `updatePayment`, `createAddress`, `editAddress`, `deleteAddress`, `paymentView`, `paymentReturnId`, `profileView`, `paymentFormOf`, `fill`, `addressLimitExceeded`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Address]], [[AddressForm]], [[AddressLimitExceededException]], [[AddressService]], [[AuthenticatedUser]], [[AuthenticationSessions]], [[AvatarForm]], [[ChangePasswordForm]], [[ImageRules]], [[InquiryService]], [[InvalidCurrentPasswordException]], [[PaymentForm]], [[PaymentInfoRequiredException]], [[PostOrigin]], [[PostService]], [[PostStatus]], [[ProfileForm]], [[Province]], [[ShippingOptions]], [[UnchangedPasswordException]], [[User]], [[UserNotFoundException]], [[UserService]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ProfileController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ProfileController.java>), líneas 1–347.

```java
package ar.edu.itba.paw.webapp.controller;

import ar.edu.itba.paw.models.Address;
import ar.edu.itba.paw.models.ImageRules;
import ar.edu.itba.paw.models.PostStatus;
import ar.edu.itba.paw.models.Province;
import ar.edu.itba.paw.models.ShippingOptions;
import ar.edu.itba.paw.models.User;
import ar.edu.itba.paw.services.AddressLimitExceededException;
import ar.edu.itba.paw.services.AddressService;
import ar.edu.itba.paw.services.InvalidCurrentPasswordException;
import ar.edu.itba.paw.services.InquiryService;
import ar.edu.itba.paw.services.PaymentInfoRequiredException;
import ar.edu.itba.paw.services.PostService;
import ar.edu.itba.paw.services.UnchangedPasswordException;
import ar.edu.itba.paw.services.UserNotFoundException;
import ar.edu.itba.paw.services.UserService;
import ar.edu.itba.paw.webapp.form.AddressForm;
import ar.edu.itba.paw.webapp.form.AvatarForm;
import ar.edu.itba.paw.webapp.form.ChangePasswordForm;
import ar.edu.itba.paw.webapp.form.PaymentForm;
import ar.edu.itba.paw.webapp.form.ProfileForm;
import ar.edu.itba.paw.webapp.security.AuthenticatedUser;
import ar.edu.itba.paw.webapp.security.AuthenticationSessions;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.propertyeditors.StringTrimmerEditor;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.session.SessionRegistry;
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
import org.springframework.web.servlet.ModelAndView;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.validation.Valid;
import java.io.IOException;
import java.util.Locale;
import java.util.Optional;

@Controller
@RequestMapping("/profile")
public class ProfileController {

    private final UserService userService;
    private final PostService postService;
    private final AddressService addressService;
    private final InquiryService inquiryService;
    private final SessionRegistry sessionRegistry;

    @Autowired
    public ProfileController(final UserService userService, final PostService postService,
                             final AddressService addressService, final SessionRegistry sessionRegistry,
                             final InquiryService inquiryService) {
        this.userService = userService;
        this.postService = postService;
        this.addressService = addressService;
        this.sessionRegistry = sessionRegistry;
        this.inquiryService = inquiryService;
    }

    // Solo los formularios nuevos: en changePasswordForm, recortar espacios cambiaria la clave que se valida.
    @InitBinder({"paymentForm", "addressForm"})
    public void initBinder(final WebDataBinder binder) {
        binder.registerCustomEditor(String.class, new StringTrimmerEditor(true));
    }

    // Todo handler que dibuja el perfil tiene el formulario de la libreta, vacio salvo que lo edite.
    @ModelAttribute("addressForm")
    public AddressForm addressForm() {
        return new AddressForm();
    }

    @RequestMapping(method = RequestMethod.GET)
    public ModelAndView profile(@AuthenticationPrincipal final AuthenticatedUser currentUser,
                                @ModelAttribute("profileForm") final ProfileForm form,
                                @ModelAttribute("changePasswordForm") final ChangePasswordForm changePasswordForm,
                                @ModelAttribute("addressForm") final AddressForm addressForm,
                                @RequestParam(name = "editAddress", required = false) final Long editAddressId,
                                @RequestParam(name = "missingPayment", required = false) final String missingPayment,
                                @RequestParam(name = "returnInquiryId", required = false) final String returnInquiryId,
                                @RequestParam(name = "addressLimit", required = false) final String addressLimit,
                                @RequestParam(name = "avatarTooLarge", required = false) final String avatarTooLarge,
                                @RequestParam(name = "postStatus", required = false) final PostStatus postStatus,
                                @RequestParam(name = "page", defaultValue = "1") final int pageNumber) {
        form.setUsername(currentUser.getDisplayName());
        // Editar precarga el formulario de la libreta con la direccion elegida, si es propia y vigente.
        final Optional<Address> editing = editAddressId == null ? Optional.empty()
                : addressService.findActiveOwned(editAddressId, currentUser.getId());
        editing.ifPresent(address -> fill(addressForm, address));
        final OpenSection openSection;
        if (missingPayment != null) {
            openSection = OpenSection.PAYMENT_MISSING;
        } else if (addressLimit != null) {
            openSection = OpenSection.ADDRESSES;
        } else {
            openSection = editing.isPresent() ? OpenSection.ADDRESSES : OpenSection.NONE;
        }
        final ModelAndView modelAndView = profileView(currentUser.getId(), openSection, pageNumber,
                editing.map(Address::getId).orElse(null), postStatus);
        modelAndView.addObject("returnInquiryId", paymentReturnId(returnInquiryId, currentUser.getId()));
        if (addressLimit != null) {
            modelAndView.addObject("addressLimitReached", true);
        }
        // Una foto que supera el limite del multipart ni llega al controller: el filtro redirige aca.
        if (avatarTooLarge != null) {
            modelAndView.addObject("avatarInvalid", true);
        }
        return modelAndView;
    }

    @RequestMapping(method = RequestMethod.POST)
    public ModelAndView update(@AuthenticationPrincipal final AuthenticatedUser currentUser,
                               @Valid @ModelAttribute("profileForm") final ProfileForm form,
                               final BindingResult bindingResult,
                               @ModelAttribute("changePasswordForm") final ChangePasswordForm changePasswordForm,
                               final RedirectAttributes redirectAttributes,
                               @RequestParam(name = "page", defaultValue = "1") final int pageNumber) {
        if (bindingResult.hasErrors()) {
            return profileView(currentUser.getId(), OpenSection.USERNAME, pageNumber, null);
        }

        final User updatedUser = userService.updateUsername(currentUser.getId(), form.getUsername());
        AuthenticationSessions.refreshIfCurrent(updatedUser);
        redirectAttributes.addFlashAttribute("profileUpdated", true);
        return new ModelAndView("redirect:/profile");
    }

    // La foto se cambia desde un dialogo: el error vuelve como aviso en el perfil, que reabre el dialogo.
    @RequestMapping(value = "/avatar", method = RequestMethod.POST)
    public ModelAndView updateAvatar(@AuthenticationPrincipal final AuthenticatedUser currentUser,
                                     @Valid @ModelAttribute("avatarForm") final AvatarForm form,
                                     final BindingResult bindingResult,
                                     final RedirectAttributes redirectAttributes) throws IOException {
        if (bindingResult.hasErrors()) {
            redirectAttributes.addFlashAttribute("avatarInvalid", true);
        } else {
            userService.updateAvatar(currentUser.getId(), form.toImageUpload());
            redirectAttributes.addFlashAttribute("avatarUpdated", true);
        }
        return new ModelAndView("redirect:/profile#avatar");
    }

    @RequestMapping(value = "/password", method = RequestMethod.POST)
    public ModelAndView changePassword(@AuthenticationPrincipal final AuthenticatedUser currentUser,
                                       @Valid @ModelAttribute("changePasswordForm") final ChangePasswordForm form,
                                       final BindingResult bindingResult,
                                       @ModelAttribute("profileForm") final ProfileForm profileForm,
                                       final HttpServletRequest request, final HttpServletResponse response,
                                       final Locale locale,
                                       @RequestParam(name = "page", defaultValue = "1") final int pageNumber) {
        profileForm.setUsername(currentUser.getDisplayName());
        if (bindingResult.hasErrors()) {
            return profileView(currentUser.getId(), OpenSection.PASSWORD, pageNumber, null);
        }
        final User updatedUser;
        try {
            updatedUser = userService.changePassword(currentUser.getId(), form.getCurrentPassword(),
                    form.getPassword(), locale);
        } catch (final InvalidCurrentPasswordException e) {
            bindingResult.rejectValue("currentPassword", "profile.password.current.invalid");
            return profileView(currentUser.getId(), OpenSection.PASSWORD, pageNumber, null);
        } catch (final UnchangedPasswordException e) {
            bindingResult.rejectValue("password", "profile.password.unchanged");
            return profileView(currentUser.getId(), OpenSection.PASSWORD, pageNumber, null);
        }
        AuthenticationSessions.logoutEverywhere(updatedUser, request, response, sessionRegistry);
        return new ModelAndView("redirect:/login?passwordChanged");
    }

    @RequestMapping(value = "/payment", method = RequestMethod.POST)
    public ModelAndView updatePayment(@AuthenticationPrincipal final AuthenticatedUser currentUser,
                                      @Valid @ModelAttribute("paymentForm") final PaymentForm form,
                                      final BindingResult bindingResult,
                                      @ModelAttribute("profileForm") final ProfileForm profileForm,
                                      @ModelAttribute("changePasswordForm") final ChangePasswordForm changePasswordForm,
                                      final RedirectAttributes redirectAttributes,
                                      @RequestParam(name = "returnInquiryId", required = false) final String returnInquiryId,
                                      @RequestParam(name = "page", defaultValue = "1") final int pageNumber) {
        profileForm.setUsername(currentUser.getDisplayName());
        final Long destination = paymentReturnId(returnInquiryId, currentUser.getId());
        if (bindingResult.hasErrors()) {
            return paymentView(currentUser.getId(), pageNumber, destination);
        }
        final User updatedUser;
        try {
            updatedUser = userService.updatePaymentInfo(currentUser.getId(), form.getCbu(), form.getAlias());
        } catch (final PaymentInfoRequiredException e) {
            bindingResult.rejectValue("cbu", "payment.required.openSale");
            return paymentView(currentUser.getId(), pageNumber, destination);
        }
        if (destination != null) {
            if (!updatedUser.hasPaymentInfo()) {
                final ModelAndView view = paymentView(currentUser.getId(), pageNumber, destination);
                view.addObject("paymentMissing", true);
                return view;
            }
            redirectAttributes.addFlashAttribute("saleNotice", "inquiry.sale.payment.updated");
            return new ModelAndView("redirect:/inquiries/" + destination + "#sale-actions");
        }
        redirectAttributes.addFlashAttribute("paymentUpdated", true);
        return new ModelAndView("redirect:/profile#account");
    }

    @RequestMapping(value = "/addresses", method = RequestMethod.POST)
    public ModelAndView createAddress(@AuthenticationPrincipal final AuthenticatedUser currentUser,
                                      @Valid @ModelAttribute("addressForm") final AddressForm form,
                                      final BindingResult bindingResult,
                                      @ModelAttribute("profileForm") final ProfileForm profileForm,
                                      @ModelAttribute("changePasswordForm") final ChangePasswordForm changePasswordForm,
                                      final RedirectAttributes redirectAttributes,
                                      @RequestParam(name = "page", defaultValue = "1") final int pageNumber) {
        profileForm.setUsername(currentUser.getDisplayName());
        if (bindingResult.hasErrors()) {
            return profileView(currentUser.getId(), OpenSection.ADDRESSES, pageNumber, null);
        }
        addressService.create(currentUser.getId(), form.getStreet(), form.getStreetNumber(), form.getApartment(),
                form.getCity(), form.getProvince(), form.getPostalCode(), form.getNotes());
        redirectAttributes.addFlashAttribute("addressSaved", true);
        return new ModelAndView("redirect:/profile#addresses");
    }

    @PreAuthorize("@addressAccess.isOwner(authentication, #addressId)")
    @RequestMapping(value = "/addresses/{addressId:[0-9]+}/edit", method = RequestMethod.POST)
    public ModelAndView editAddress(@PathVariable("addressId") final long addressId,
                                    @AuthenticationPrincipal final AuthenticatedUser currentUser,
                                    @Valid @ModelAttribute("addressForm") final AddressForm form,
                                    final BindingResult bindingResult,
                                    @ModelAttribute("profileForm") final ProfileForm profileForm,
                                    @ModelAttribute("changePasswordForm") final ChangePasswordForm changePasswordForm,
                                    final RedirectAttributes redirectAttributes,
                                    @RequestParam(name = "page", defaultValue = "1") final int pageNumber) {
        profileForm.setUsername(currentUser.getDisplayName());
        if (bindingResult.hasErrors()) {
            return profileView(currentUser.getId(), OpenSection.ADDRESSES, pageNumber, addressId);
        }
        addressService.replace(addressId, currentUser.getId(), form.getStreet(), form.getStreetNumber(),
                form.getApartment(), form.getCity(), form.getProvince(), form.getPostalCode(), form.getNotes());
        redirectAttributes.addFlashAttribute("addressSaved", true);
        return new ModelAndView("redirect:/profile#addresses");
    }

    @PreAuthorize("@addressAccess.isOwner(authentication, #addressId)")
    @RequestMapping(value = "/addresses/{addressId:[0-9]+}/delete", method = RequestMethod.POST)
    public ModelAndView deleteAddress(@PathVariable("addressId") final long addressId,
                                      @AuthenticationPrincipal final AuthenticatedUser currentUser,
                                      final RedirectAttributes redirectAttributes) {
        addressService.archive(addressId, currentUser.getId());
        redirectAttributes.addFlashAttribute("addressDeleted", true);
        return new ModelAndView("redirect:/profile#addresses");
    }

    private ModelAndView paymentView(final long userId, final int pageNumber, final Long returnInquiryId) {
        final ModelAndView view = profileView(userId, OpenSection.PAYMENT, pageNumber, null);
        view.addObject("returnInquiryId", returnInquiryId);
        return view;
    }

    // Un valor mal formado solo pierde el regreso a la venta: no debe impedir abrir el perfil.
    private Long paymentReturnId(final String value, final long userId) {
        if (value == null) {
            return null;
        }
        try {
            return inquiryService.findSaleToResume(Long.parseLong(value), userId).orElse(null);
        } catch (final NumberFormatException e) {
            return null;
        }
    }

    // Los POST que re-renderizan el perfil con un error vuelven al listado sin filtro.
    private ModelAndView profileView(final long userId, final OpenSection openSection, final int pageNumber,
                                     final Long editingAddressId) {
        return profileView(userId, openSection, pageNumber, editingAddressId, null);
    }

    private ModelAndView profileView(final long userId, final OpenSection openSection, final int pageNumber,
                                     final Long editingAddressId, final PostStatus postStatus) {
        final User user = userService.findById(userId).orElseThrow(UserNotFoundException::new);
        final ShippingOptions shipping = addressService.findShippingOptions(userId);
        final ModelAndView modelAndView = new ModelAndView("profile/index");
        modelAndView.addObject("profileUser", user);
        modelAndView.addObject("accountAppearance", userService.findAccountAppearanceById(userId)
                .orElseThrow(UserNotFoundException::new));
        modelAndView.addObject("postPage", postService.findByPublisherId(userId, postStatus, pageNumber));
        modelAndView.addObject("postStatusFilter", postStatus);
        modelAndView.addObject("postStatusCounts", postService.countByStatusForPublisher(userId));
        modelAndView.addObject("postStatuses", PostStatus.values());
        modelAndView.addObject("postOrigin", PostOrigin.PRIVATE_PROFILE);
        modelAndView.addObject("acceptedImageTypes", ImageRules.ACCEPTED_CONTENT_TYPES);
        modelAndView.addObject("maxImageBytes", ImageRules.MAX_IMAGE_BYTES);
        modelAndView.addObject("addresses", shipping.getAddresses());
        modelAndView.addObject("provinces", Province.values());
        modelAndView.addObject("editingAddressId", editingAddressId);
        modelAndView.addObject("profileEditOpen", openSection == OpenSection.USERNAME);
        modelAndView.addObject("passwordEditOpen", openSection == OpenSection.PASSWORD);
        modelAndView.addObject("paymentEditOpen",
                openSection == OpenSection.PAYMENT || openSection == OpenSection.PAYMENT_MISSING);
        modelAndView.addObject("paymentMissing", openSection == OpenSection.PAYMENT_MISSING);
        modelAndView.addObject("addressesOpen", openSection == OpenSection.ADDRESSES);
        modelAndView.addObject("canAddAddress", shipping.isNewAddressAllowed());
        modelAndView.addObject("maxAddresses", AddressService.MAX_ACTIVE_ADDRESSES);
        // Salvo que se este corrigiendo, el formulario de cobro muestra lo guardado: vacio, guardar
        // sin tocarlo borraria los datos de cobro.
        if (openSection != OpenSection.PAYMENT) {
            modelAndView.addObject("paymentForm", paymentFormOf(user));
        }
        return modelAndView;
    }

    private static PaymentForm paymentFormOf(final User user) {
        final PaymentForm form = new PaymentForm();
        form.setCbu(user.getPaymentInfo().getCbu());
        form.setAlias(user.getPaymentInfo().getAlias());
        return form;
    }

    private static void fill(final AddressForm form, final Address address) {
        form.setStreet(address.getStreet());
        form.setStreetNumber(address.getStreetNumber());
        form.setApartment(address.getApartment());
        form.setCity(address.getCity());
        form.setProvince(address.getProvince());
        form.setPostalCode(address.getPostalCode());
        form.setNotes(address.getNotes());
    }

    /*
     * PAYMENT es corregir el formulario de cobro con errores: el form ligado ya esta en el modelo.
     * PAYMENT_MISSING abre la misma fila al rebotar un Aceptar sin datos de cobro, precargada.
     */
    private enum OpenSection { NONE, USERNAME, PASSWORD, PAYMENT, PAYMENT_MISSING, ADDRESSES }

    @ExceptionHandler(AddressLimitExceededException.class)
    public ModelAndView addressLimitExceeded() {
        return new ModelAndView("redirect:/profile?addressLimit#addresses");
    }
}
```
