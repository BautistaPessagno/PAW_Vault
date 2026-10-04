---
title: "AddressJdbcDao"
categories: ["Persistence"]
type: "code"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["persistence/src/main/java/ar/edu/itba/paw/persistence/AddressJdbcDao.java"]
---

# AddressJdbcDao

Direcciones con Spring JDBC. El `RowMapper` y la lista de columnas son de paquete para que [[InquiryJdbcDao]] los reutilice al traer la dirección por `JOIN`. Archivar es un `UPDATE ... WHERE archived = FALSE`.

## Guía de lectura

Datos y dependencias declaradas: `ROW_MAPPER`, `SELECT`, `jdbcTemplate`, `jdbcInsert`.

Operaciones para localizar en la fuente: `columns`, `create`, `findById`, `findActiveByUserId`, `archive`, `countActiveByUserId`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Address]], [[AddressDao]], [[Province]].

Referenciado por: [[InquiryJdbcDao]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [persistence/src/main/java/ar/edu/itba/paw/persistence/AddressJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/AddressJdbcDao.java>), líneas 1–100.

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Address;
import ar.edu.itba.paw.models.Province;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.jdbc.core.simple.SimpleJdbcInsert;
import org.springframework.stereotype.Repository;

import javax.sql.DataSource;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

@Repository
public class AddressJdbcDao implements AddressDao {

    // Package-private: InquiryJdbcDao trae la direccion por JOIN con los mismos alias y la
    // mapea con este mismo mapper, asi una columna nueva se agrega en un solo lugar.
    static final RowMapper<Address> ROW_MAPPER = (resultSet, rowNum) -> new Address(
            resultSet.getLong("address_id"),
            resultSet.getLong("address_user_id"),
            resultSet.getString("address_street"),
            resultSet.getString("address_street_number"),
            resultSet.getString("address_apartment"),
            resultSet.getString("address_city"),
            Province.valueOf(resultSet.getString("address_province")),
            resultSet.getString("address_postal_code"),
            resultSet.getString("address_notes"),
            resultSet.getBoolean("address_archived")
    );

    private static final String SELECT = "SELECT " + columns("a") + " FROM addresses a ";

    // Las columnas que espera ROW_MAPPER, con el alias de tabla que use cada consulta.
    static String columns(final String alias) {
        return alias + ".id AS address_id, " + alias + ".user_id AS address_user_id, "
                + alias + ".street AS address_street, " + alias + ".street_number AS address_street_number, "
                + alias + ".apartment AS address_apartment, " + alias + ".city AS address_city, "
                + alias + ".province AS address_province, " + alias + ".postal_code AS address_postal_code, "
                + alias + ".notes AS address_notes, " + alias + ".archived AS address_archived";
    }

    private final JdbcTemplate jdbcTemplate;
    private final SimpleJdbcInsert jdbcInsert;

    @Autowired
    public AddressJdbcDao(final DataSource dataSource) {
        this.jdbcTemplate = new JdbcTemplate(dataSource);
        this.jdbcInsert = new SimpleJdbcInsert(dataSource)
                .withTableName("addresses")
                .usingColumns("user_id", "street", "street_number", "apartment", "city", "province",
                        "postal_code", "notes")
                .usingGeneratedKeyColumns("id");
    }

    @Override
    public Address create(final long userId, final String street, final String streetNumber,
                          final String apartment, final String city, final Province province,
                          final String postalCode, final String notes) {
        final Map<String, Object> parameters = new HashMap<>();
        parameters.put("user_id", userId);
        parameters.put("street", street);
        parameters.put("street_number", streetNumber);
        parameters.put("apartment", apartment);
        parameters.put("city", city);
        parameters.put("province", province.name());
        parameters.put("postal_code", postalCode);
        parameters.put("notes", notes);
        final Number id = jdbcInsert.executeAndReturnKey(parameters);
        return new Address(id.longValue(), userId, street, streetNumber, apartment, city, province,
                postalCode, notes, false);
    }

    @Override
    public Optional<Address> findById(final long id) {
        return jdbcTemplate.query(SELECT + "WHERE a.id = ?", ROW_MAPPER, id).stream().findFirst();
    }

    @Override
    public List<Address> findActiveByUserId(final long userId) {
        return List.copyOf(jdbcTemplate.query(
                SELECT + "WHERE a.user_id = ? AND a.archived = FALSE ORDER BY a.id DESC",
                ROW_MAPPER, userId));
    }

    @Override
    public boolean archive(final long id) {
        return jdbcTemplate.update("UPDATE addresses SET archived = TRUE WHERE id = ? AND archived = FALSE", id) == 1;
    }

    @Override
    public int countActiveByUserId(final long userId) {
        final Integer count = jdbcTemplate.queryForObject(
                "SELECT COUNT(*) FROM addresses WHERE user_id = ? AND archived = FALSE", Integer.class, userId);
        return count == null ? 0 : count;
    }
}
```
