---
title: "AddressService"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/AddressService.java"]
---

# AddressService

Contrato de la libreta: direcciones activas y opciones de envío en una lectura, alta con tope de 3, reemplazo (archiva y crea) y baja lógica.

## Guía de lectura

Operaciones para localizar en la fuente: `findActiveOwned`, `findShippingOptions`, `create`, `replace`, `archive`, `findById`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Address]], [[Province]], [[ShippingOptions]].

Referenciado por: [[AddressAccessHandler]], [[AddressServiceImpl]], [[AddressServiceImplTest]], [[CartController]], [[CartServiceImpl]], [[CartServiceImplTest]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]], [[PostContactController]], [[ProfileController]], [[SecurityConfig]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [services-contracts/src/main/java/ar/edu/itba/paw/services/AddressService.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/AddressService.java>), líneas 1–35.

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Address;
import ar.edu.itba.paw.models.Province;
import ar.edu.itba.paw.models.ShippingOptions;

import java.util.Optional;

public interface AddressService {

    // Tope de direcciones activas por usuario: create() lo hace cumplir.
    int MAX_ACTIVE_ADDRESSES = 3;

    // Vacio si no existe, es de otra cuenta o esta archivada.
    Optional<Address> findActiveOwned(long addressId, long userId);

    // Las activas, la que se propone y si create() aceptaria otra ahora mismo, en una lectura.
    ShippingOptions findShippingOptions(long userId);

    // Lanza AddressLimitExceededException si el usuario ya tiene MAX_ACTIVE_ADDRESSES activas.
    Address create(long userId, String street, String streetNumber, String apartment, String city,
                   Province province, String postalCode, String notes);

    // Editar archiva la anterior y crea otra: las consultas que la usan conservan la original.
    // Lanza AddressNotFoundException si no existe o ya estaba archivada, y
    // ForbiddenOperationException si es de otra cuenta.
    Address replace(long addressId, long userId, String street, String streetNumber, String apartment,
                    String city, Province province, String postalCode, String notes);

    // Mismas excepciones que replace().
    void archive(long addressId, long userId);

    // Incluye archivadas. Para AddressAccessHandler: devuelve un hecho, no decide.
    Optional<Address> findById(long addressId);
}
```
