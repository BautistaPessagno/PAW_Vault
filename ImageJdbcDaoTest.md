---
title: "ImageJdbcDaoTest"
categories: ["Testing"]
type: "test"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
sources: ["persistence/src/test/java/ar/edu/itba/paw/persistence/ImageJdbcDaoTest.java"]
---

# ImageJdbcDaoTest

Three transactional HSQLDB tests cover binary lookup, missing image and binary insert with generated ID and row count. Uses short byte fixtures and checks byte equality; it does not establish that the fixture decodes as a full image.

## Test methods

- `testFindByIdWhenImageExistsReturnsImage`
- `testFindByIdWhenImageDoesNotExistReturnsEmpty`
- `testCreateWhenDataIsValidReturnsPersistedImage`

These are source assertions, not a fresh passing test run.

## Connections

Project types referenced: [[Image]], [[ImageDao]], [[TestConfiguration]].

Referenced by: no direct project type reference; implementations may be injected through interfaces.

## Exact source

[persistence/src/test/java/ar/edu/itba/paw/persistence/ImageJdbcDaoTest.java, lines 1–90](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/ImageJdbcDaoTest.java>)

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Image;
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
import java.util.Optional;

@Rollback
@Transactional
@ExtendWith(SpringExtension.class)
@ContextConfiguration(classes = TestConfiguration.class)
public class ImageJdbcDaoTest {

    private static final long IMAGE_ID = 1;
    private static final String IMAGE_CONTENT_TYPE = "image/png";
    private static final byte[] IMAGE_DATA = {
            (byte) 0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A
    };
    private static final long MISSING_IMAGE_ID = 999;
    private static final String IMAGES_TABLE = "images";

    @Autowired
    private ImageDao imageDao;

    @Autowired
    private DataSource dataSource;

    private JdbcTemplate jdbcTemplate;

    @BeforeEach
    public void setUp() {
        jdbcTemplate = new JdbcTemplate(dataSource);
    }

    @Test
    public void testFindByIdWhenImageExistsReturnsImage() {
        // 1. Arrange
        // No inserts — using data from populator.sql

        // 2. Exercise
        final Optional<Image> result = imageDao.findById(IMAGE_ID);

        // 3. Assert
        Assertions.assertTrue(result.isPresent());
        Assertions.assertEquals(IMAGE_ID, result.get().getId());
        Assertions.assertEquals(IMAGE_CONTENT_TYPE, result.get().getContentType());
        Assertions.assertArrayEquals(IMAGE_DATA, result.get().getData());
    }

    @Test
    public void testFindByIdWhenImageDoesNotExistReturnsEmpty() {
        // 1. Arrange
        // No inserts — using data from populator.sql

        // 2. Exercise
        final Optional<Image> result = imageDao.findById(MISSING_IMAGE_ID);

        // 3. Assert
        Assertions.assertFalse(result.isPresent());
    }

    @Test
    public void testCreateWhenDataIsValidReturnsPersistedImage() {
        // 1. Arrange
        final String contentType = "image/jpeg";
        final byte[] data = {(byte) 0xFF, (byte) 0xD8, (byte) 0xFF, (byte) 0xE0};

        // 2. Exercise
        final Image result = imageDao.create(contentType, data);

        // 3. Assert
        Assertions.assertTrue(result.getId() > 0);
        Assertions.assertEquals(contentType, result.getContentType());
        Assertions.assertArrayEquals(data, result.getData());
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, IMAGES_TABLE,
                "id = " + result.getId() + " AND content_type = '" + contentType + "'"));
        Assertions.assertEquals(2, JdbcTestUtils.countRowsInTable(jdbcTemplate, IMAGES_TABLE));
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
