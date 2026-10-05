---
title: "MessageJdbcDaoTest"
categories: ["Persistence", "Testing"]
type: "test"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["persistence/src/test/java/ar/edu/itba/paw/persistence/MessageJdbcDaoTest.java"]
---

# MessageJdbcDaoTest

Tests de `MessageJdbcDao` en `persistence`: 3 casos declarados. Cubre: alta de mensajes y orden por llegada. No se ejecutaron en esta actualización del Vault; ver [[Testing and evidence]].

## Guía de lectura

Datos y dependencias declaradas: `MESSAGES_TABLE`, `messageDao`, `dataSource`, `jdbcTemplate`.

Operaciones para localizar en la fuente: `setUp`.

Casos declarados: 3.

- `testCreateWhenInquiryExistsReturnsPersistedMessage`
- `testFindByInquiryIdWhenConversationHasMessagesReturnsOldestFirst`
- `testFindByInquiryIdWhenConversationIsEmptyReturnsEmptyList`

## Conexiones

Referencias estáticas a tipos del proyecto: [[Message]], [[MessageDao]], [[TestConfiguration]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [persistence/src/test/java/ar/edu/itba/paw/persistence/MessageJdbcDaoTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/MessageJdbcDaoTest.java>), líneas 1–86.

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Message;
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

@Rollback
@Transactional
@ExtendWith(SpringExtension.class)
@ContextConfiguration(classes = TestConfiguration.class)
public class MessageJdbcDaoTest {

    private static final String MESSAGES_TABLE = "inquiry_messages";

    @Autowired
    private MessageDao messageDao;

    @Autowired
    private DataSource dataSource;

    private JdbcTemplate jdbcTemplate;

    @BeforeEach
    public void setUp() {
        jdbcTemplate = new JdbcTemplate(dataSource);
    }

    @Test
    public void testCreateWhenInquiryExistsReturnsPersistedMessage() {
        // 1. Arrange
        final long emptyConversationId = 2;
        final long buyerId = 3;
        final String body = "Hola,\nsigue disponible?";

        // 2. Exercise
        final Message result = messageDao.create(emptyConversationId, buyerId, body);

        // 3. Assert
        Assertions.assertTrue(result.getId() > 0);
        Assertions.assertEquals(emptyConversationId, result.getInquiryId());
        Assertions.assertEquals(buyerId, result.getSenderId());
        Assertions.assertEquals(body, result.getBody());
        Assertions.assertNotNull(result.getCreatedAt());
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, MESSAGES_TABLE,
                "id = " + result.getId() + " AND inquiry_id = 2 AND sender_id = 3 AND created_at IS NOT NULL"));
    }

    @Test
    public void testFindByInquiryIdWhenConversationHasMessagesReturnsOldestFirst() {
        // 1. Arrange
        final long inquiryId = 1;

        // 2. Exercise
        final List<Message> result = messageDao.findByInquiryId(inquiryId);

        // 3. Assert
        Assertions.assertEquals(List.of(1L, 2L), result.stream().map(Message::getId).toList());
        Assertions.assertEquals("¿Aceptarías una oferta?", result.get(0).getBody());
        Assertions.assertEquals(1L, result.get(0).getSenderId());
        Assertions.assertEquals(2L, result.get(1).getSenderId());
    }

    @Test
    public void testFindByInquiryIdWhenConversationIsEmptyReturnsEmptyList() {
        // 1. Arrange
        final long emptyConversationId = 2;

        // 2. Exercise
        final List<Message> result = messageDao.findByInquiryId(emptyConversationId);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
    }
}
```
