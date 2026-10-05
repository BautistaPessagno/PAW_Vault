---
title: "MessageJdbcDao"
categories: ["Persistence"]
type: "code"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["persistence/src/main/java/ar/edu/itba/paw/persistence/MessageJdbcDao.java"]
---

# MessageJdbcDao

Mensajes con Spring JDBC. Al crear relee la fila para devolver la fecha que puso la base. Ordena por id. El mapper es de paquete para que [[InquiryJdbcDao]] lo reutilice.

## Guía de lectura

Datos y dependencias declaradas: `ROW_MAPPER`, `SELECT`, `jdbcTemplate`, `jdbcInsert`.

Operaciones para localizar en la fuente: `columns`, `create`, `findByInquiryId`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Message]], [[MessageDao]].

Referenciado por: [[InquiryJdbcDao]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [persistence/src/main/java/ar/edu/itba/paw/persistence/MessageJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/MessageJdbcDao.java>), líneas 1–66.

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Message;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.jdbc.core.simple.SimpleJdbcInsert;
import org.springframework.stereotype.Repository;

import javax.sql.DataSource;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Repository
public class MessageJdbcDao implements MessageDao {

    // Package-private: InquiryJdbcDao trae el ultimo Mensaje de cada Consulta por JOIN con los
    // mismos alias y lo mapea con este mismo mapper, igual que hace con las direcciones.
    static final RowMapper<Message> ROW_MAPPER = (resultSet, rowNum) -> new Message(
            resultSet.getLong("message_id"),
            resultSet.getLong("message_inquiry_id"),
            resultSet.getLong("message_sender_id"),
            resultSet.getString("message_body"),
            resultSet.getTimestamp("message_created_at").toLocalDateTime()
    );

    private static final String SELECT = "SELECT " + columns("m") + " FROM inquiry_messages m ";

    // Las columnas que espera ROW_MAPPER, con el alias de tabla que use cada consulta.
    static String columns(final String alias) {
        return alias + ".id AS message_id, " + alias + ".inquiry_id AS message_inquiry_id, "
                + alias + ".sender_id AS message_sender_id, " + alias + ".body AS message_body, "
                + alias + ".created_at AS message_created_at";
    }

    private final JdbcTemplate jdbcTemplate;
    private final SimpleJdbcInsert jdbcInsert;

    @Autowired
    public MessageJdbcDao(final DataSource dataSource) {
        this.jdbcTemplate = new JdbcTemplate(dataSource);
        this.jdbcInsert = new SimpleJdbcInsert(dataSource)
                .withTableName("inquiry_messages")
                .usingColumns("inquiry_id", "sender_id", "body")
                .usingGeneratedKeyColumns("id");
    }

    // Relee la fila para devolver la fecha que puso la base, que es la que se va a mostrar.
    @Override
    public Message create(final long inquiryId, final long senderId, final String body) {
        final Map<String, Object> parameters = new HashMap<>();
        parameters.put("inquiry_id", inquiryId);
        parameters.put("sender_id", senderId);
        parameters.put("body", body);
        final long id = jdbcInsert.executeAndReturnKey(parameters).longValue();
        return jdbcTemplate.queryForObject(SELECT + "WHERE m.id = ?", ROW_MAPPER, id);
    }

    // El id es serial: ordenar por id es ordenar por llegada aunque dos compartan created_at.
    @Override
    public List<Message> findByInquiryId(final long inquiryId) {
        return List.copyOf(jdbcTemplate.query(SELECT + "WHERE m.inquiry_id = ? ORDER BY m.id", ROW_MAPPER,
                inquiryId));
    }
}
```
