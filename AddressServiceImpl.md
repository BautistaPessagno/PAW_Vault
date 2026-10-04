---
title: "AddressServiceImpl"
categories: ["Services"]
type: "code"
module: "services"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["services/src/main/java/ar/edu/itba/paw/services/AddressServiceImpl.java"]
---

# AddressServiceImpl

Libreta de direcciones con tope de 3 activas. `findShippingOptions` devuelve lista, propuesta y cupo en una lectura; `hasRoom` es la única definición del tope. El alta bloquea la Cuenta; editar archiva y crea; la pertenencia se vuelve a chequear acá. Ver [[Addresses and payment flow]].

## Guía de lectura

Datos y dependencias declaradas: `LOGGER`, `addressDao`, `userService`.

Operaciones para localizar en la fuente: `findActiveOwned`, `findShippingOptions`, `create`, `replace`, `archive`, `findById`, `hasRoom`, `archiveOwned`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Address]], [[AddressDao]], [[AddressLimitExceededException]], [[AddressNotFoundException]], [[AddressService]], [[ForbiddenOperationException]], [[Province]], [[ShippingOptions]], [[UserService]].

Referenciado por: [[AddressServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [services/src/main/java/ar/edu/itba/paw/services/AddressServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/AddressServiceImpl.java>), líneas 1–106.

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Address;
import ar.edu.itba.paw.models.Province;
import ar.edu.itba.paw.models.ShippingOptions;
import ar.edu.itba.paw.persistence.AddressDao;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
public class AddressServiceImpl implements AddressService {

    private static final Logger LOGGER = LoggerFactory.getLogger(AddressServiceImpl.class);

    private final AddressDao addressDao;
    private final UserService userService;

    @Autowired
    public AddressServiceImpl(final AddressDao addressDao, final UserService userService) {
        this.addressDao = addressDao;
        this.userService = userService;
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<Address> findActiveOwned(final long addressId, final long userId) {
        return addressDao.findById(addressId)
                .filter(address -> address.getUserId() == userId && !address.isArchived());
    }

    @Override
    @Transactional(readOnly = true)
    public ShippingOptions findShippingOptions(final long userId) {
        final List<Address> addresses = addressDao.findActiveByUserId(userId);
        // findActiveByUserId ya viene de la mas nueva a la mas vieja: la primera es la propuesta. El
        // cupo se deriva de la misma lista, asi la lista y el cupo no pueden contradecirse.
        return new ShippingOptions(addresses, addresses.isEmpty() ? null : addresses.get(0),
                hasRoom(addresses.size()));
    }

    @Override
    @Transactional
    public Address create(final long userId, final String street, final String streetNumber,
                          final String apartment, final String city, final Province province,
                          final String postalCode, final String notes) {
        // Bloquear la cuenta serializa las altas simultaneas: la segunda espera y cuenta despues,
        // ya con la direccion de la primera.
        userService.lockById(userId);
        if (!hasRoom(addressDao.countActiveByUserId(userId))) {
            throw new AddressLimitExceededException();
        }
        final Address address = addressDao.create(userId, street, streetNumber, apartment, city, province,
                postalCode, notes);
        LOGGER.info("Created address addressId={} userId={}", address.getId(), userId);
        return address;
    }

    @Override
    @Transactional
    public Address replace(final long addressId, final long userId, final String street,
                           final String streetNumber, final String apartment, final String city,
                           final Province province, final String postalCode, final String notes) {
        archiveOwned(addressId, userId);
        final Address address = addressDao.create(userId, street, streetNumber, apartment, city, province,
                postalCode, notes);
        LOGGER.info("Replaced address oldId={} newId={} userId={}", addressId, address.getId(), userId);
        return address;
    }

    @Override
    @Transactional
    public void archive(final long addressId, final long userId) {
        archiveOwned(addressId, userId);
        LOGGER.info("Archived address addressId={} userId={}", addressId, userId);
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<Address> findById(final long addressId) {
        return addressDao.findById(addressId);
    }

    // Unica definicion del tope: la usan la vista (findShippingOptions) y el alta (create).
    private static boolean hasRoom(final int activeCount) {
        return activeCount < MAX_ACTIVE_ADDRESSES;
    }

    // La pertenencia se chequea aca y no solo en el @PreAuthorize: el service no confia en
    // que todo llamador pase por el controller. El UPDATE condicional cubre la carrera con
    // otra baja de la misma direccion.
    private void archiveOwned(final long addressId, final long userId) {
        final Address address = addressDao.findById(addressId).orElseThrow(AddressNotFoundException::new);
        if (address.getUserId() != userId) {
            throw new ForbiddenOperationException();
        }
        if (!addressDao.archive(addressId)) {
            throw new AddressNotFoundException();
        }
    }
}
```
