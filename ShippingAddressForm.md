---
title: "ShippingAddressForm"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/form/ShippingAddressForm.java"]
---

# ShippingAddressForm

Dirección de envío de una Consulta: una guardada (`addressId`) o una nueva con estos mismos campos. Los campos no llevan `@NotBlank` porque solo son obligatorios al cargar una nueva. Lo usan el contacto y el carrito.

## Guía de lectura

Datos y dependencias declaradas: `addressId`, `street`, `streetNumber`, `apartment`, `city`, `province`, `postalCode`, `notes`.

Operaciones para localizar en la fuente: `getAddressId`, `setAddressId`, `getStreet`, `setStreet`, `getStreetNumber`, `setStreetNumber`, `getApartment`, `setApartment`, `getCity`, `setCity`, `getProvince`, `setProvince`, `getPostalCode`, `setPostalCode`, `getNotes`, `setNotes`, `isNewAddress`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Province]], [[ValidShippingAddress]].

Referenciado por: [[CartController]], [[ContactForm]], [[ShippingAddressValidator]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/form/ShippingAddressForm.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/ShippingAddressForm.java>), líneas 1–105.

```java
package ar.edu.itba.paw.webapp.form;

import ar.edu.itba.paw.models.Province;
import ar.edu.itba.paw.webapp.validation.ValidShippingAddress;

import javax.validation.constraints.Size;

// La direccion de envio de una Consulta: una guardada (addressId) o una nueva con estos mismos
// campos. Sin addressId se esta cargando una nueva: por eso los campos no llevan
// @NotBlank/@NotNull, los valida ShippingAddressValidator solo cuando hace falta. Lo usan el
// contacto de un Post y el envio del carrito.
@ValidShippingAddress
public class ShippingAddressForm {

    private Long addressId;

    @Size(max = 100, message = "{address.size}")
    private String street;

    @Size(max = 10, message = "{address.size}")
    private String streetNumber;

    @Size(max = 20, message = "{address.size}")
    private String apartment;

    @Size(max = 100, message = "{address.size}")
    private String city;

    private Province province;

    @Size(max = 10, message = "{address.size}")
    private String postalCode;

    @Size(max = 200, message = "{address.size}")
    private String notes;

    public Long getAddressId() {
        return addressId;
    }

    public void setAddressId(final Long addressId) {
        this.addressId = addressId;
    }

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

    // Sin direccion guardada elegida, se carga una nueva con los campos del formulario.
    public boolean isNewAddress() {
        return addressId == null;
    }
}
```
