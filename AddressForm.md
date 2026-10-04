---
title: "AddressForm"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/form/AddressForm.java"]
---

# AddressForm

Formulario de una dirección de la libreta: calle, altura, ciudad, provincia y código postal obligatorios, con sus largos máximos.

## Guía de lectura

Datos y dependencias declaradas: `street`, `streetNumber`, `apartment`, `city`, `province`, `postalCode`, `notes`.

Operaciones para localizar en la fuente: `getStreet`, `setStreet`, `getStreetNumber`, `setStreetNumber`, `getApartment`, `setApartment`, `getCity`, `setCity`, `getProvince`, `setProvince`, `getPostalCode`, `setPostalCode`, `getNotes`, `setNotes`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Province]].

Referenciado por: [[ProfileController]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/form/AddressForm.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/AddressForm.java>), líneas 1–91.

```java
package ar.edu.itba.paw.webapp.form;

import ar.edu.itba.paw.models.Province;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;

public class AddressForm {

    @NotBlank(message = "{address.required}")
    @Size(max = 100, message = "{address.size}")
    private String street;

    @NotBlank(message = "{address.required}")
    @Size(max = 10, message = "{address.size}")
    private String streetNumber;

    @Size(max = 20, message = "{address.size}")
    private String apartment;

    @NotBlank(message = "{address.required}")
    @Size(max = 100, message = "{address.size}")
    private String city;

    @NotNull(message = "{address.required}")
    private Province province;

    @NotBlank(message = "{address.required}")
    @Size(max = 10, message = "{address.size}")
    private String postalCode;

    @Size(max = 200, message = "{address.size}")
    private String notes;

    public String getStreet() {
        return street;
    }

    public void setStreet(final String street) {
        this.street = street;
    }

    public String getStreetNumber() {
        return streetNumber;
    }

    public void setStreetNumber(final String streetNumber) {
        this.streetNumber = streetNumber;
    }

    public String getApartment() {
        return apartment;
    }

    public void setApartment(final String apartment) {
        this.apartment = apartment;
    }

    public String getCity() {
        return city;
    }

    public void setCity(final String city) {
        this.city = city;
    }

    public Province getProvince() {
        return province;
    }

    public void setProvince(final Province province) {
        this.province = province;
    }

    public String getPostalCode() {
        return postalCode;
    }

    public void setPostalCode(final String postalCode) {
        this.postalCode = postalCode;
    }

    public String getNotes() {
        return notes;
    }

    public void setNotes(final String notes) {
        this.notes = notes;
    }
}
```
