---
title: "AddressDao"
categories: ["Persistence"]
type: "code"
module: "persistence-contracts"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/AddressDao.java"]
---

# AddressDao

Contrato de persistencia de direcciones: crear, buscar por id, listar activas de una Cuenta, archivar y contar activas. Lo implementa [[AddressJdbcDao]].

## Guía de lectura

Operaciones para localizar en la fuente: `create`, `findById`, `findActiveByUserId`, `archive`, `countActiveByUserId`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Address]], [[Province]].

Referenciado por: [[AddressJdbcDao]], [[AddressJdbcDaoTest]], [[AddressServiceImpl]], [[AddressServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/AddressDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/AddressDao.java>), líneas 1–24.

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Address;
import ar.edu.itba.paw.models.Province;

import java.util.List;
import java.util.Optional;

public interface AddressDao {
    Address create(long userId, String street, String streetNumber, String apartment, String city,
                   Province province, String postalCode, String notes);

    // Incluye archivadas: las consultas viejas siguen resolviendo su direccion.
    Optional<Address> findById(long id);

    // Solo las vigentes, de la mas nueva a la mas vieja.
    List<Address> findActiveByUserId(long userId);

    // Unica baja posible. Devuelve false si ya estaba archivada.
    boolean archive(long id);

    // Para el tope de direcciones activas por usuario.
    int countActiveByUserId(long userId);
}
```
