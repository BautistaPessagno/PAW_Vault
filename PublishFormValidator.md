---
title: "PublishFormValidator"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/validation/PublishFormValidator.java"]
---

# PublishFormValidator

Reglas cruzadas de publicar: años válidos y no futuros, precio en rango, prensado no anterior al lanzamiento y hasta 5 fotos válidas.

## Guía de lectura

Operaciones para localizar en la fuente: `isValid`, `validateCovers`, `validateYear`, `validatePrice`, `violation`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[ImageFiles]], [[ImageRules]], [[PublishForm]], [[ValidPublishForm]], [[VinylInputRules]].

Referenciado por: [[ValidPublishForm]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/validation/PublishFormValidator.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/validation/PublishFormValidator.java>), líneas 1–91.

```java
package ar.edu.itba.paw.webapp.validation;

import ar.edu.itba.paw.models.ImageRules;
import ar.edu.itba.paw.models.VinylInputRules;
import ar.edu.itba.paw.webapp.form.ImageFiles;
import ar.edu.itba.paw.webapp.form.PublishForm;
import org.springframework.web.multipart.MultipartFile;

import javax.validation.ConstraintValidator;
import javax.validation.ConstraintValidatorContext;
import java.util.Arrays;
import java.util.List;

public class PublishFormValidator implements ConstraintValidator<ValidPublishForm, PublishForm> {

    @Override
    public boolean isValid(final PublishForm form, final ConstraintValidatorContext context) {
        if (form == null) {
            return true;
        }

        boolean valid = true;
        context.disableDefaultConstraintViolation();

        valid = validateYear(context, "releaseYear", form.getReleaseYear(),
                "{publish.releaseYear.future}") && valid;
        valid = validatePrice(context, form.getPrice()) && valid;
        final boolean pressingYearValid = validateYear(context, "pressingYear", form.getPressingYear(),
                "{publish.pressingYear.future}");
        valid = pressingYearValid && valid;

        if (pressingYearValid && form.getReleaseYear() != null
                && VinylInputRules.classifyYear(form.getReleaseYear()) == VinylInputRules.YearValidity.VALID
                && !VinylInputRules.isPressingYearOrdered(form.getReleaseYear(), form.getPressingYear())) {
            violation(context, "pressingYear", "{publish.pressingYear.order}");
            valid = false;
        }
        return validateCovers(context, form.getCovers()) && valid;
    }

    // Al editar, el tope cuenta tambien las fotos que se conservan: eso lo chequea PostService.
    private static boolean validateCovers(final ConstraintValidatorContext context, final MultipartFile[] covers) {
        final List<MultipartFile> chosen = covers == null ? List.of()
                : Arrays.stream(covers).filter(ImageFiles::isPresent).toList();
        if (chosen.size() > ImageRules.MAX_GALLERY_IMAGES || !chosen.stream().allMatch(ImageFiles::isValid)) {
            violation(context, "covers", "{publish.cover.invalid}");
            return false;
        }
        return true;
    }

    private static boolean validateYear(final ConstraintValidatorContext context, final String property,
                                        final Integer year, final String futureMessage) {
        if (year == null) {
            return true;
        }
        final VinylInputRules.YearValidity yearValidity = VinylInputRules.classifyYear(year);
        if (yearValidity == VinylInputRules.YearValidity.FUTURE) {
            violation(context, property, futureMessage);
            return false;
        }
        if (yearValidity == VinylInputRules.YearValidity.INVALID) {
            violation(context, property, "{validation.year.invalid}");
            return false;
        }
        return true;
    }

    private static boolean validatePrice(final ConstraintValidatorContext context, final Integer price) {
        if (price == null) {
            return true;
        }
        final VinylInputRules.PriceValidity priceValidity = VinylInputRules.classifyPrice(price);
        if (priceValidity == VinylInputRules.PriceValidity.NOT_POSITIVE) {
            violation(context, "price", "{validation.price.positive}");
            return false;
        }
        if (priceValidity == VinylInputRules.PriceValidity.INVALID) {
            violation(context, "price", "{validation.price.invalid}");
            return false;
        }
        return true;
    }

    private static void violation(final ConstraintValidatorContext context, final String property,
                                  final String message) {
        context.buildConstraintViolationWithTemplate(message)
                .addPropertyNode(property)
                .addConstraintViolation();
    }
}
```
