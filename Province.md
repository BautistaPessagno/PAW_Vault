---
title: "Province"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/Province.java"]
---

# Province

Las 24 jurisdicciones de Argentina. El nombre visible sale de i18n (`province.<VALOR>`).

## Guía de lectura

Sin campos ni métodos propios: el archivo completo está abajo.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[Address]], [[AddressDao]], [[AddressForm]], [[AddressJdbcDao]], [[AddressJdbcDaoTest]], [[AddressService]], [[AddressServiceImpl]], [[AddressServiceImplTest]], [[CartController]], [[CartService]], [[CartServiceImpl]], [[CartServiceImplTest]], [[InquiryService]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]], [[PostContactController]], [[ProfileController]], [[ShippingAddressForm]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [models/src/main/java/ar/edu/itba/paw/models/Province.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Province.java>), líneas 1–8.

```java
package ar.edu.itba.paw.models;

// Las 24 jurisdicciones de Argentina. El nombre visible sale de i18n (province.<VALOR>).
public enum Province {
    BUENOS_AIRES, CABA, CATAMARCA, CHACO, CHUBUT, CORDOBA, CORRIENTES, ENTRE_RIOS, FORMOSA,
    JUJUY, LA_PAMPA, LA_RIOJA, MENDOZA, MISIONES, NEUQUEN, RIO_NEGRO, SALTA, SAN_JUAN,
    SAN_LUIS, SANTA_CRUZ, SANTA_FE, SANTIAGO_DEL_ESTERO, TIERRA_DEL_FUEGO, TUCUMAN
}
```
