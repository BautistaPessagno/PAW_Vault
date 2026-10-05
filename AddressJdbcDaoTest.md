---
title: "AddressJdbcDaoTest"
categories: ["Persistence", "Testing"]
type: "test"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["persistence/src/test/java/ar/edu/itba/paw/persistence/AddressJdbcDaoTest.java"]
---

# AddressJdbcDaoTest

Tests de `AddressJdbcDao` en `persistence`: 6 casos declarados. Cubre: alta, activas por Cuenta, archivado con guarda y conteo. No se ejecutaron en esta actualización del Vault; ver [[Testing and evidence]].

## Guía de lectura

Datos y dependencias declaradas: `ADDRESSES_TABLE`, `addressDao`, `dataSource`, `jdbcTemplate`.

Operaciones para localizar en la fuente: `setUp`.

Casos declarados: 6.

- `testCreateWhenDataIsValidReturnsActiveAddress`
- `testFindActiveByUserIdWhenUserHasArchivedAddressReturnsOnlyActiveOnes`
- `testFindByIdWhenAddressIsArchivedReturnsArchivedAddress`
- `testArchiveWhenAddressIsActiveReturnsTrue`
- `testArchiveWhenAddressIsAlreadyArchivedReturnsFalse`
- `testCountActiveByUserIdWhenUserHasArchivedAddressReturnsOnlyActiveCount`

## Conexiones

Referencias estáticas a tipos del proyecto: [[Address]], [[AddressDao]], [[Province]], [[TestConfiguration]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [persistence/src/test/java/ar/edu/itba/paw/persistence/AddressJdbcDaoTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/AddressJdbcDaoTest.java>), líneas 1–122.

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Address;
import ar.edu.itba.paw.models.Province;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.test.annotation.Rollback;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.test.jdbc.JdbcTestUtils;
import org.springframework.transaction.annotation.Transactional;

import javax.sql.DataSource;
import java.util.List;
import java.util.Optional;

@Rollback
@Transactional
@ExtendWith(SpringExtension.class)
@ContextConfiguration(classes = TestConfiguration.class)
public class AddressJdbcDaoTest {

    private static final String ADDRESSES_TABLE = "addresses";

    @Autowired
    private AddressDao addressDao;

    @Autowired
    private DataSource dataSource;

    private JdbcTemplate jdbcTemplate;

    @BeforeEach
    public void setUp() {
        jdbcTemplate = new JdbcTemplate(dataSource);
    }

    @Test
    public void testCreateWhenDataIsValidReturnsActiveAddress() {
        // 1. Arrange
        final long userId = 2;

        // 2. Exercise
        final Address result = addressDao.create(userId, "Corrientes", "1500", null, "Buenos Aires",
                Province.CABA, "1042", "Portero");

        // 3. Assert
        Assertions.assertTrue(result.getId() > 0);
        Assertions.assertFalse(result.isArchived());
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, ADDRESSES_TABLE,
                "user_id = 2 AND street = 'Corrientes' AND province = 'CABA' AND archived = FALSE"));
    }

    @Test
    public void testFindActiveByUserIdWhenUserHasArchivedAddressReturnsOnlyActiveOnes() {
        // 1. Arrange
        final long userId = 1;

        // 2. Exercise
        final List<Address> result = addressDao.findActiveByUserId(userId);

        // 3. Assert
        Assertions.assertEquals(List.of(1L), result.stream().map(Address::getId).toList());
        Assertions.assertEquals(Province.CABA, result.get(0).getProvince());
    }

    @Test
    public void testFindByIdWhenAddressIsArchivedReturnsArchivedAddress() {
        // 1. Arrange
        final long archivedId = 2;

        // 2. Exercise
        final Optional<Address> result = addressDao.findById(archivedId);

        // 3. Assert
        Assertions.assertTrue(result.isPresent());
        Assertions.assertTrue(result.get().isArchived());
        Assertions.assertEquals("2B", result.get().getApartment());
    }

    @Test
    public void testArchiveWhenAddressIsActiveReturnsTrue() {
        // 1. Arrange
        final long activeId = 1;

        // 2. Exercise
        final boolean result = addressDao.archive(activeId);

        // 3. Assert
        Assertions.assertTrue(result);
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, ADDRESSES_TABLE,
                "id = 1 AND archived = TRUE"));
    }

    @Test
    public void testArchiveWhenAddressIsAlreadyArchivedReturnsFalse() {
        // 1. Arrange
        final long archivedId = 2;

        // 2. Exercise
        final boolean result = addressDao.archive(archivedId);

        // 3. Assert
        Assertions.assertFalse(result);
    }

    @Test
    public void testCountActiveByUserIdWhenUserHasArchivedAddressReturnsOnlyActiveCount() {
        // 1. Arrange
        final long userId = 1;

        // 2. Exercise
        final int result = addressDao.countActiveByUserId(userId);

        // 3. Assert
        Assertions.assertEquals(1, result);
    }
}
```
