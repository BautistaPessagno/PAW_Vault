---
title: "CatalogFilterValidator"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/validation/CatalogFilterValidator.java"]
---

# CatalogFilterValidator

Valida año y precios de los filtros y que el rango esté ordenado, colgando cada error de su campo.

## Guía de lectura

Operaciones para localizar en la fuente: `isValid`, `validatePrice`, `violation`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[CatalogFilterForm]], [[ValidCatalogFilters]], [[VinylInputRules]].

Referenciado por: [[ValidCatalogFilters]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/validation/CatalogFilterValidator.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/validation/CatalogFilterValidator.java>), líneas 1–66.

```java
package ar.edu.itba.paw.webapp.validation;

import ar.edu.itba.paw.models.VinylInputRules;
import ar.edu.itba.paw.webapp.form.CatalogFilterForm;

import javax.validation.ConstraintValidator;
import javax.validation.ConstraintValidatorContext;

public class CatalogFilterValidator implements ConstraintValidator<ValidCatalogFilters, CatalogFilterForm> {

    @Override
    public boolean isValid(final CatalogFilterForm form, final ConstraintValidatorContext context) {
        if (form == null) {
            return true;
        }

        boolean valid = true;
        context.disableDefaultConstraintViolation();

        if (form.getYear() != null) {
            final VinylInputRules.YearValidity yearValidity = VinylInputRules.classifyYear(form.getYear());
            if (yearValidity == VinylInputRules.YearValidity.FUTURE) {
                violation(context, "year", "{validation.year.future}");
                valid = false;
            } else if (yearValidity == VinylInputRules.YearValidity.INVALID) {
                violation(context, "year", "{validation.year.invalid}");
                valid = false;
            }
        }

        final boolean minPriceValid = validatePrice(context, "minPrice", form.getMinPrice());
        final boolean maxPriceValid = validatePrice(context, "maxPrice", form.getMaxPrice());
        valid = valid && minPriceValid && maxPriceValid;

        if (minPriceValid && maxPriceValid
                && !VinylInputRules.isPriceRangeOrdered(form.getMinPrice(), form.getMaxPrice())) {
            violation(context, "maxPrice", "{validation.price.order}");
            valid = false;
        }
        return valid;
    }

    private static boolean validatePrice(final ConstraintValidatorContext context, final String property,
                                         final Integer price) {
        if (price == null) {
            return true;
        }
        final VinylInputRules.PriceValidity priceValidity = VinylInputRules.classifyPrice(price);
        if (priceValidity == VinylInputRules.PriceValidity.NOT_POSITIVE) {
            violation(context, property, "{validation.price.positive}");
            return false;
        }
        if (priceValidity == VinylInputRules.PriceValidity.INVALID) {
            violation(context, property, "{validation.price.invalid}");
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
