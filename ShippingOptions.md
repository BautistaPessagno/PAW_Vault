---
title: "ShippingOptions"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/ShippingOptions.java"]
---

# ShippingOptions

Lo que necesita un formulario de envío en una sola lectura: las direcciones activas, la propuesta por defecto y si se puede sumar otra. Lo devuelve `AddressService.findShippingOptions`.

## Guía de lectura

Datos y dependencias declaradas: `addresses`, `defaultAddress`, `newAddressAllowed`.

Operaciones para localizar en la fuente: `getAddresses`, `getDefaultAddress`, `isNewAddressAllowed`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Address]].

Referenciado por: [[AddressService]], [[AddressServiceImpl]], [[AddressServiceImplTest]], [[CartCheckout]], [[CartServiceImplTest]], [[PostContactController]], [[ProfileController]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [models/src/main/java/ar/edu/itba/paw/models/ShippingOptions.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/ShippingOptions.java>), líneas 1–23.

```java
package ar.edu.itba.paw.models;

import java.util.List;
import java.util.Optional;

// Las direcciones entre las que elige quien consulta, la que se le propone y si puede sumar otra.
public final class ShippingOptions {
    private final List<Address> addresses;
    private final Address defaultAddress;
    private final boolean newAddressAllowed;

    public ShippingOptions(final List<Address> addresses, final Address defaultAddress,
                           final boolean newAddressAllowed) {
        this.addresses = List.copyOf(addresses);
        this.defaultAddress = defaultAddress;
        this.newAddressAllowed = newAddressAllowed;
    }

    public List<Address> getAddresses() { return addresses; }
    // Vacio si no tiene ninguna direccion activa.
    public Optional<Address> getDefaultAddress() { return Optional.ofNullable(defaultAddress); }
    public boolean isNewAddressAllowed() { return newAddressAllowed; }
}
```
