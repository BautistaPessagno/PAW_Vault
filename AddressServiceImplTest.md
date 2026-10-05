---
title: "AddressServiceImplTest"
categories: ["Services", "Testing"]
type: "test"
module: "services"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["services/src/test/java/ar/edu/itba/paw/services/AddressServiceImplTest.java"]
---

# AddressServiceImplTest

Tests de `AddressServiceImpl` en `services`: 10 casos declarados. Cubre: opciones de envío, tope de direcciones, reemplazo, archivado y pertenencia. No se ejecutaron en esta actualización del Vault; ver [[Testing and evidence]].

## Guía de lectura

Datos y dependencias declaradas: `USER_ID`, `OTHER_USER_ID`, `ADDRESS_ID`, `addressDao`, `userService`, `addressService`.

Operaciones para localizar en la fuente: `setUp`, `address`.

Casos declarados: 10.

- `testFindActiveOwnedWhenAddressBelongsToAnotherUserReturnsEmpty`
- `testFindActiveOwnedWhenAddressIsArchivedReturnsEmpty`
- `testReplaceWhenAddressIsActiveReturnsNewAddress`
- `testReplaceWhenAddressWasAlreadyArchivedReturnsAddressNotFoundException`
- `testReplaceWhenAddressBelongsToAnotherUserReturnsForbiddenOperationException`
- `testArchiveWhenAddressBelongsToAnotherUserReturnsForbiddenOperationException`
- `testArchiveWhenAddressDoesNotExistReturnsAddressNotFoundException`
- `testCreateWhenActiveCountReachedLimitReturnsAddressLimitExceededException`
- `testFindShippingOptionsWhenAddressesReachedLimitReturnsNewestAsDefaultAndNoRoom`
- `testFindShippingOptionsWhenUserHasNoAddressesReturnsNoDefaultAndRoom`

## Conexiones

Referencias estáticas a tipos del proyecto: [[Address]], [[AddressDao]], [[AddressLimitExceededException]], [[AddressNotFoundException]], [[AddressService]], [[AddressServiceImpl]], [[ForbiddenOperationException]], [[Province]], [[ShippingOptions]], [[UserService]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [services/src/test/java/ar/edu/itba/paw/services/AddressServiceImplTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/AddressServiceImplTest.java>), líneas 1–178.

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Address;
import ar.edu.itba.paw.models.Province;
import ar.edu.itba.paw.models.ShippingOptions;
import ar.edu.itba.paw.persistence.AddressDao;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.api.function.Executable;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.List;
import java.util.Optional;

@ExtendWith(MockitoExtension.class)
public class AddressServiceImplTest {

    private static final long USER_ID = 1;
    private static final long OTHER_USER_ID = 2;
    private static final long ADDRESS_ID = 5;

    @Mock
    private AddressDao addressDao;

    @Mock
    private UserService userService;

    private AddressServiceImpl addressService;

    @BeforeEach
    public void setUp() {
        addressService = new AddressServiceImpl(addressDao, userService);
    }

    @Test
    public void testFindActiveOwnedWhenAddressBelongsToAnotherUserReturnsEmpty() {
        // 1. Arrange
        Mockito.when(addressDao.findById(ADDRESS_ID)).thenReturn(Optional.of(address(ADDRESS_ID, OTHER_USER_ID, false)));

        // 2. Exercise
        final Optional<Address> result = addressService.findActiveOwned(ADDRESS_ID, USER_ID);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
    }

    @Test
    public void testFindActiveOwnedWhenAddressIsArchivedReturnsEmpty() {
        // 1. Arrange
        Mockito.when(addressDao.findById(ADDRESS_ID)).thenReturn(Optional.of(address(ADDRESS_ID, USER_ID, true)));

        // 2. Exercise
        final Optional<Address> result = addressService.findActiveOwned(ADDRESS_ID, USER_ID);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
    }

    @Test
    public void testReplaceWhenAddressIsActiveReturnsNewAddress() {
        // 1. Arrange
        final Address created = address(6, USER_ID, false);
        Mockito.when(addressDao.findById(ADDRESS_ID)).thenReturn(Optional.of(address(ADDRESS_ID, USER_ID, false)));
        Mockito.when(addressDao.archive(ADDRESS_ID)).thenReturn(true);
        Mockito.when(addressDao.create(USER_ID, "Corrientes", "1500", null, "Buenos Aires", Province.CABA,
                "1042", null)).thenReturn(created);

        // 2. Exercise
        final Address result = addressService.replace(ADDRESS_ID, USER_ID, "Corrientes", "1500", null,
                "Buenos Aires", Province.CABA, "1042", null);

        // 3. Assert
        Assertions.assertSame(created, result);
    }

    @Test
    public void testReplaceWhenAddressWasAlreadyArchivedReturnsAddressNotFoundException() {
        // 1. Arrange
        Mockito.when(addressDao.findById(ADDRESS_ID)).thenReturn(Optional.of(address(ADDRESS_ID, USER_ID, true)));
        Mockito.when(addressDao.archive(ADDRESS_ID)).thenReturn(false);

        // 2. Exercise
        final Executable replace = () -> addressService.replace(ADDRESS_ID, USER_ID, "Corrientes", "1500",
                null, "Buenos Aires", Province.CABA, "1042", null);

        // 3. Assert
        Assertions.assertThrows(AddressNotFoundException.class, replace);
    }

    @Test
    public void testReplaceWhenAddressBelongsToAnotherUserReturnsForbiddenOperationException() {
        // 1. Arrange
        Mockito.when(addressDao.findById(ADDRESS_ID)).thenReturn(Optional.of(address(ADDRESS_ID, OTHER_USER_ID, false)));

        // 2. Exercise
        final Executable replace = () -> addressService.replace(ADDRESS_ID, USER_ID, "Corrientes", "1500",
                null, "Buenos Aires", Province.CABA, "1042", null);

        // 3. Assert
        Assertions.assertThrows(ForbiddenOperationException.class, replace);
    }

    @Test
    public void testArchiveWhenAddressBelongsToAnotherUserReturnsForbiddenOperationException() {
        // 1. Arrange
        Mockito.when(addressDao.findById(ADDRESS_ID)).thenReturn(Optional.of(address(ADDRESS_ID, OTHER_USER_ID, false)));

        // 2. Exercise
        final Executable archive = () -> addressService.archive(ADDRESS_ID, USER_ID);

        // 3. Assert
        Assertions.assertThrows(ForbiddenOperationException.class, archive);
    }

    @Test
    public void testArchiveWhenAddressDoesNotExistReturnsAddressNotFoundException() {
        // 1. Arrange
        Mockito.when(addressDao.findById(ADDRESS_ID)).thenReturn(Optional.empty());

        // 2. Exercise
        final Executable archive = () -> addressService.archive(ADDRESS_ID, USER_ID);

        // 3. Assert
        Assertions.assertThrows(AddressNotFoundException.class, archive);
    }

    @Test
    public void testCreateWhenActiveCountReachedLimitReturnsAddressLimitExceededException() {
        // 1. Arrange
        Mockito.when(addressDao.countActiveByUserId(USER_ID)).thenReturn(AddressService.MAX_ACTIVE_ADDRESSES);

        // 2. Exercise
        final Executable create = () -> addressService.create(USER_ID, "Corrientes", "1500", null,
                "Buenos Aires", Province.CABA, "1042", null);

        // 3. Assert
        Assertions.assertThrows(AddressLimitExceededException.class, create);
    }

    @Test
    public void testFindShippingOptionsWhenAddressesReachedLimitReturnsNewestAsDefaultAndNoRoom() {
        // 1. Arrange
        final List<Address> addresses = List.of(address(3, USER_ID, false), address(2, USER_ID, false),
                address(1, USER_ID, false));
        Mockito.when(addressDao.findActiveByUserId(USER_ID)).thenReturn(addresses);

        // 2. Exercise
        final ShippingOptions result = addressService.findShippingOptions(USER_ID);

        // 3. Assert
        Assertions.assertEquals(addresses, result.getAddresses());
        Assertions.assertEquals(3L, result.getDefaultAddress().map(Address::getId).orElseThrow());
        Assertions.assertFalse(result.isNewAddressAllowed());
    }

    @Test
    public void testFindShippingOptionsWhenUserHasNoAddressesReturnsNoDefaultAndRoom() {
        // 1. Arrange
        Mockito.when(addressDao.findActiveByUserId(USER_ID)).thenReturn(List.of());

        // 2. Exercise
        final ShippingOptions result = addressService.findShippingOptions(USER_ID);

        // 3. Assert
        Assertions.assertTrue(result.getAddresses().isEmpty());
        Assertions.assertTrue(result.getDefaultAddress().isEmpty());
        Assertions.assertTrue(result.isNewAddressAllowed());
    }

    private static Address address(final long id, final long userId, final boolean archived) {
        return new Address(id, userId, "Av. Madero", "399", null, "Buenos Aires", Province.CABA, "1106",
                null, archived);
    }
}
```
