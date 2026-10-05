---
title: "PaymentInfo"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/PaymentInfo.java"]
---

# PaymentInfo

Datos de cobro de una Cuenta: CBU o CVU y alias, cualquiera de los dos opcional. `NONE` representa "sin datos", así `User.getPaymentInfo()` nunca es nulo. Ver [[Addresses and payment flow]].

## Guía de lectura

Datos y dependencias declaradas: `NONE`, `cbu`, `alias`.

Operaciones para localizar en la fuente: `getCbu`, `getAlias`, `isPresent`, `equals`, `hashCode`.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[InquiryJdbcDao]], [[InquiryServiceImplTest]], [[InquirySummary]], [[User]], [[UserDao]], [[UserJdbcDao]], [[UserJdbcDaoTest]], [[UserServiceImpl]], [[UserServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [models/src/main/java/ar/edu/itba/paw/models/PaymentInfo.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/PaymentInfo.java>), líneas 1–48.

```java
package ar.edu.itba.paw.models;

import java.util.Objects;

// Los datos con los que un Publicante cobra una venta: CBU o CVU, alias, o los dos.
public final class PaymentInfo {

    public static final PaymentInfo NONE = new PaymentInfo(null, null);

    // null cuando no se cargo.
    private final String cbu;
    private final String alias;

    public PaymentInfo(final String cbu, final String alias) {
        this.cbu = cbu;
        this.alias = alias;
    }

    public String getCbu() {
        return cbu;
    }

    public String getAlias() {
        return alias;
    }

    // Para cobrar alcanza con uno de los dos.
    public boolean isPresent() {
        return cbu != null || alias != null;
    }

    @Override
    public boolean equals(final Object other) {
        if (this == other) {
            return true;
        }
        if (!(other instanceof PaymentInfo)) {
            return false;
        }
        final PaymentInfo that = (PaymentInfo) other;
        return Objects.equals(cbu, that.cbu) && Objects.equals(alias, that.alias);
    }

    @Override
    public int hashCode() {
        return Objects.hash(cbu, alias);
    }
}
```
