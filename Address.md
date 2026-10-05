---
title: "Address"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/Address.java"]
---

# Address

Dirección de envío de una Cuenta: calle, altura, piso, ciudad, [[Province]], código postal y notas, más la marca `archived`. Es inmutable. `withCityAndProvinceOnly` devuelve una copia sin calle ni altura: es lo que ve el publicante mientras no hay una venta en curso. Ver [[Addresses and payment flow]].

## Guía de lectura

Datos y dependencias declaradas: `id`, `userId`, `street`, `streetNumber`, `apartment`, `city`, `province`, `postalCode`, `notes`, `archived`.

Operaciones para localizar en la fuente: `getId`, `getUserId`, `getStreet`, `getStreetNumber`, `getApartment`, `getCity`, `getProvince`, `getPostalCode`, `getNotes`, `isArchived`, `withCityAndProvinceOnly`, `isCityAndProvinceOnly`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Province]].

Referenciado por: [[AddressDao]], [[AddressJdbcDao]], [[AddressJdbcDaoTest]], [[AddressService]], [[AddressServiceImpl]], [[AddressServiceImplTest]], [[CartServiceImplTest]], [[EmailServiceImplTest]], [[InquiryJdbcDao]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]], [[InquirySummary]], [[ProfileController]], [[ShippingOptions]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [models/src/main/java/ar/edu/itba/paw/models/Address.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Address.java>), líneas 1–80.

```java
package ar.edu.itba.paw.models;

// apartment y notes son opcionales: null cuando no se cargaron.
public final class Address {
    private final long id;
    private final long userId;
    private final String street;
    private final String streetNumber;
    private final String apartment;
    private final String city;
    private final Province province;
    private final String postalCode;
    private final String notes;
    private final boolean archived;

    public Address(final long id, final long userId, final String street, final String streetNumber,
                   final String apartment, final String city, final Province province,
                   final String postalCode, final String notes, final boolean archived) {
        this.id = id;
        this.userId = userId;
        this.street = street;
        this.streetNumber = streetNumber;
        this.apartment = apartment;
        this.city = city;
        this.province = province;
        this.postalCode = postalCode;
        this.notes = notes;
        this.archived = archived;
    }

    public long getId() {
        return id;
    }

    public long getUserId() {
        return userId;
    }

    public String getStreet() {
        return street;
    }

    public String getStreetNumber() {
        return streetNumber;
    }

    public String getApartment() {
        return apartment;
    }

    public String getCity() {
        return city;
    }

    public Province getProvince() {
        return province;
    }

    public String getPostalCode() {
        return postalCode;
    }

    public String getNotes() {
        return notes;
    }

    public boolean isArchived() {
        return archived;
    }

    // Copia sin calle, altura, piso, codigo postal ni notas: lo que ve quien todavia no
    // tiene por que conocer el domicilio.
    public Address withCityAndProvinceOnly() {
        return new Address(id, userId, null, null, null, city, province, null, null, archived);
    }

    public boolean isCityAndProvinceOnly() {
        return street == null;
    }
}
```
