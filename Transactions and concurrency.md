---
title: "Transactions and concurrency"
categories: ["Services", "Persistence"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["services/src/main/java/ar/edu/itba/paw/services/TransactionCallbacks.java", "services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java", "services/src/main/java/ar/edu/itba/paw/services/InquiryServiceImpl.java", "services/src/main/java/ar/edu/itba/paw/services/CartServiceImpl.java", "services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java", "services/src/main/java/ar/edu/itba/paw/services/AddressServiceImpl.java", "persistence/src/main/java/ar/edu/itba/paw/persistence/PostJdbcDao.java", "persistence/src/main/java/ar/edu/itba/paw/persistence/ArtistJdbcDao.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java"]
---

# Transactions and concurrency

> [!summary] En una frase
> Cada operación de negocio es un método de service `@Transactional`; cuando dos pedidos pueden pisarse, el service bloquea una fila con `SELECT ... FOR UPDATE` o usa un `UPDATE` condicional, y lo que no se puede deshacer (un correo) se ejecuta recién después del commit.

## Herramientas

| Herramienta | Para qué |
|---|---|
| `DataSourceTransactionManager` | Abre, confirma y revierte transacciones JDBC sobre el `DataSource` |
| `@EnableTransactionManagement` + `@Transactional` | Spring envuelve cada service en un proxy que abre la transacción al entrar y hace commit o rollback al salir |
| `readOnly = true` | Marca las lecturas; documenta intención y permite optimizaciones del driver |
| `Propagation.MANDATORY` | El método exige que ya haya una transacción; si no, falla |
| `SELECT ... FOR UPDATE` | Bloqueo pesimista de fila hasta el fin de la transacción |
| `UPDATE ... WHERE status = ?` | Transición condicional: el número de filas afectadas dice si ganó |
| `Savepoint` JDBC | Recuperarse de una violación de unicidad sin perder la transacción |
| `TransactionSynchronizationManager` | Registrar acciones para después del commit ([[TransactionCallbacks]]) |

## Cómo funciona `@Transactional`

1. El controller llama al método a través de la interfaz. Lo que recibe es un proxy.
2. El proxy pide una conexión al `DataSource`, desactiva el autocommit y la deja asociada al hilo.
3. Todos los `JdbcTemplate` que se usen en ese hilo reutilizan esa conexión: por eso varios DAO participan de la misma transacción sin pasarse nada.
4. Si el método termina bien, commit. Si lanza una `RuntimeException`, rollback. Las excepciones de negocio del proyecto son todas `RuntimeException`, así que cualquier rechazo deshace lo hecho.
5. Un método `@Transactional` que llama a otro service `@Transactional` se **suma** a la transacción existente (propagación `REQUIRED`, la de por defecto).

Consecuencia que conviene conocer: una llamada a un método del **mismo** objeto no pasa por el proxy, así que su anotación no se aplica. En el proyecto, los métodos internos son privados y heredan la transacción del método público que los llama.

`@Transactional` aparece solo en services (85 anotaciones, 39 de ellas `readOnly`). Ningún DAO ni controller la lleva.

## Los tres mecanismos de concurrencia

### 1. Bloqueo de fila

| Qué se bloquea | Quién | Para qué |
|---|---|---|
| La fila del **post** | `InquiryServiceImpl.submit`, las transiciones de la venta y `CartServiceImpl.add`, vía `PostService.lockById`; editar y eliminar, vía `PostDao.findByIdForUpdate` | Que dos consultas, una consulta y una aceptación, o un agregado al carrito y una venta sobre el mismo ejemplar se ordenen entre sí |
| Varios posts, **en orden de id** | `CartServiceImpl` al enviar el carrito, vía `PostService.lockByIds` | Lo mismo para muchos; el orden fijo evita interbloqueos entre dos carritos con posts en común |
| La fila de la **cuenta** | `AddressServiceImpl` (tope de tres direcciones), `CartServiceImpl.add` (tope de veinte), `InquiryServiceImpl` al aceptar (datos de cobro) | Serializar por cuenta un "contar y después insertar" |
| La fila de la **consulta** | `InquiryServiceImpl.lockConfirmedSale`, vía `InquiryDao.findByIdForUpdate` | Que dos guardados o quitados de reseña de la misma parte se ordenen entre sí ([[Reviews flow]]) |

**Orden entre tablas.** Cuando una transacción toma el post y la Cuenta, siempre toma primero el post: contacto, aceptación, envío del carrito y, desde el PR #52 (`e12c0e39`), también agregar al carrito. Hasta `8929aea` `CartServiceImpl.add` bloqueaba solo la Cuenta y después insertaba la clave foránea al post, el orden inverso; dos transacciones con órdenes opuestos pueden esperarse mutuamente.

Los métodos que bloquean llevan `Propagation.MANDATORY`: fuera de una transacción el bloqueo se soltaría apenas vuelve el método y no protegería nada. Que falle es mejor que simular protección.

### 2. Transición condicional

Reservar, liberar y vender una publicación son un `UPDATE posts SET status = ? WHERE id = ? AND status = ?`. Si devuelve cero filas, otro llegó antes y el service lanza el conflicto. No hace falta leer antes: la comparación y el cambio son una sola sentencia atómica. Lo mismo para los estados de la consulta y para consumir un token (`DELETE ... WHERE token = ?` devuelve 1 solo al primero).

### 3. Restricción única como árbitro

Cuando dos registros simultáneos del mismo correo, o dos publicaciones del mismo álbum, llegan al `INSERT`, la restricción única deja pasar uno. El otro recibe `DuplicateKeyException` y el service la traduce a una excepción de negocio.

En PostgreSQL una sentencia fallida **aborta toda la transacción**: no se puede seguir consultando. Hay dos respuestas en el código:

- [[ArtistJdbcDao]] usa un **savepoint**: si el `INSERT` choca, vuelve al savepoint y relee la fila que ganó. Así `findOrCreate` devuelve el artista existente y la publicación continúa.
- Para cualquier otro choque al publicar (por ejemplo, el mismo álbum creado a la vez), [[PostServiceImpl]] no puede releer, así que traduce a [[ConcurrentPublishException]] y pide reintentar: la otra transacción ya confirmó, de modo que el reintento encuentra los datos.

## Después del commit

Un correo no se puede deshacer. Si se enviara dentro de la transacción y después hubiera rollback, alguien recibiría un aviso de algo que no pasó. [[TransactionCallbacks]] registra la acción en `TransactionSynchronizationManager` y Spring la ejecuta solo si el commit tuvo éxito. Se usa para todos los correos y para los logs de éxito ([[Mail delivery]]).

Si no hay transacción activa (por ejemplo, en un test con mocks), la acción corre de inmediato.

## Decisiones y por qué

| Decisión | Motivo | Fuente |
|---|---|---|
| Transacciones en services, nunca en DAO ni controllers | La unidad de trabajo es la operación de negocio, que cruza varios DAO | `CLAUDE.md` del repo |
| `MANDATORY` en los métodos que bloquean o transicionan | Sin transacción externa el bloqueo no protege | Comentarios en [[PostServiceImpl]], [[UserServiceImpl]], [[ReviewServiceImpl]] |
| Bloquear la fila del post, no una fila por consulta | Es el recurso por el que compiten todas las consultas del mismo ejemplar | Comentario en [[PostServiceImpl]] |
| Bloqueo en orden de id en el carrito | Evitar interbloqueos | Comentario en [[PostJdbcDao]] |
| Siempre post antes que Cuenta | Un orden único entre tablas evita interbloqueos entre contacto, carrito y venta | Comentario en [[CartServiceImpl]]; commit `e12c0e39` |
| Savepoint en `findOrCreate` | PostgreSQL inutiliza la transacción tras una violación de unicidad | Comentario en [[ArtistJdbcDao]] |
| Correo después del commit | No avisar algo que se revirtió | Estructura de [[TransactionCallbacks]]; inferencia |
| Nivel de aislamiento por defecto (`READ COMMITTED` en PostgreSQL) | No se configura otro; los bloqueos explícitos cubren los casos críticos | Ausencia de configuración; inferencia |

## Límites conocidos

- `DriverManagerDataSource` abre una conexión por transacción; no hay pool.
- El bloqueo de fila espera sin tope: no hay `lock_timeout` ni `NOWAIT`.
- Si el proceso muere entre el commit y el envío del correo, el correo se pierde: no hay cola persistente.
- Los tests de services usan mocks, así que no ejercitan bloqueos reales; los de persistence corren en HSQLDB, que no reproduce la concurrencia de PostgreSQL. La concurrencia está razonada, no probada con ejecución.

## Preguntas de defensa

**¿Dónde ponen `@Transactional` y por qué?**
En los métodos públicos de los services: es donde una operación de negocio completa tiene que confirmarse o deshacerse entera.

**¿Qué pasa si dos compradores consultan el mismo vinilo a la vez?**
Los dos bloquean la fila del post; uno espera. Cada uno crea su consulta: varias consultas pendientes sobre un post son válidas. Lo que no puede pasar dos veces es la reserva.

**¿Y si el vendedor acepta dos consultas a la vez?**
La segunda transacción espera el bloqueo, y cuando entra el `UPDATE ... WHERE status = 'AVAILABLE'` afecta cero filas: recibe un conflicto.

**¿Por qué el correo sale después del commit?**
Porque no se puede revertir. Se registra una sincronización y Spring la corre solo si el commit fue exitoso.

**¿Qué es `Propagation.MANDATORY`?**
Exige una transacción ya abierta. Lo usan los métodos cuyo efecto solo tiene sentido dentro de una operación más grande.

**¿Por qué un savepoint?**
Porque en PostgreSQL un error dentro de la transacción la deja inutilizable; el savepoint permite volver atrás solo esa sentencia.

## Evidencia de código

### Bloqueos y transiciones del post

Fuente exacta en `c3e2a4c`: [services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java>), líneas 81–112.

```java
    // Bloquea la fila del post dentro de la transaccion del llamador: las consultas del mismo
    // ejemplar compiten por ella y se ordenan entre si. MANDATORY porque sin una transaccion
    // de afuera el lock se soltaria apenas vuelve el metodo; lo mismo para las transiciones.
    @Override
    @Transactional(propagation = Propagation.MANDATORY)
    public PostSummary lockById(final long postId) {
        return postDao.findByIdForUpdate(postId).orElseThrow(PostNotFoundException::new);
    }

    @Override
    @Transactional(propagation = Propagation.MANDATORY)
    public List<PostSummary> lockByIds(final Collection<Long> postIds) {
        return postDao.findByIdsForUpdate(postIds);
    }

    @Override
    @Transactional(propagation = Propagation.MANDATORY)
    public boolean reserve(final long postId) {
        return postDao.updateStatus(postId, PostStatus.AVAILABLE, PostStatus.RESERVED);
    }

    @Override
    @Transactional(propagation = Propagation.MANDATORY)
    public boolean release(final long postId) {
        return postDao.updateStatus(postId, PostStatus.RESERVED, PostStatus.AVAILABLE);
    }

    @Override
    @Transactional(propagation = Propagation.MANDATORY)
    public boolean markSold(final long postId) {
        return postDao.updateStatus(postId, PostStatus.RESERVED, PostStatus.SOLD);
    }
```

### Bloqueo de varios posts en orden

Fuente exacta en `c3e2a4c`: [persistence/src/main/java/ar/edu/itba/paw/persistence/PostJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/PostJdbcDao.java>), líneas 297–318.

```java
    @Override
    public Optional<PostSummary> findByIdForUpdate(final long id) {
        if (jdbcTemplate.queryForList("SELECT id FROM posts WHERE id = ? FOR UPDATE", Long.class, id).isEmpty()) {
            return Optional.empty();
        }
        return findById(id);
    }

    // Dos sentencias fijas para cualquier cantidad de posts: el bloqueo en orden de id y
    // despues los summaries, sin un findById por post.
    @Override
    public List<PostSummary> findByIdsForUpdate(final Collection<Long> ids) {
        if (ids.isEmpty()) {
            return List.of();
        }
        final String placeholders = String.join(", ", Collections.nCopies(ids.size(), "?"));
        final Object[] parameters = ids.toArray();
        jdbcTemplate.queryForList("SELECT id FROM posts WHERE id IN (" + placeholders + ") ORDER BY id FOR UPDATE",
                Long.class, parameters);
        return List.copyOf(jdbcTemplate.query(SUMMARY_SELECT + "WHERE p.id IN (" + placeholders + ") ORDER BY p.id",
                ROW_MAPPER, parameters));
    }
```

### Savepoint en `findOrCreate`

Fuente exacta en `c3e2a4c`: [persistence/src/main/java/ar/edu/itba/paw/persistence/ArtistJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/ArtistJdbcDao.java>), líneas 72–95.

```java
    @Override
    public Artist findOrCreate(final String displayName, final String normalizedName) {
        final Optional<Artist> existing = findByNormalizedName(normalizedName);
        if (existing.isPresent()) {
            return existing.get();
        }
        return jdbcTemplate.execute((ConnectionCallback<Artist>) connection -> {
            // PostgreSQL deja la transaccion inutilizable despues de una violacion
            // de unicidad. El savepoint permite releer la fila que gano la carrera.
            final Savepoint savepoint = connection.getAutoCommit() ? null : connection.setSavepoint();
            try {
                return create(displayName, normalizedName);
            } catch (final DuplicateKeyException e) {
                if (savepoint != null) {
                    connection.rollback(savepoint);
                }
                return findByNormalizedName(normalizedName).orElseThrow(() -> e);
            } finally {
                if (savepoint != null) {
                    connection.releaseSavepoint(savepoint);
                }
            }
        });
    }
```

### Traducción del choque al publicar

Fuente exacta en `c3e2a4c`: [services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java>), líneas 273–281.

```java
        } catch (final DuplicatePostKeyException e) {
            throw new DuplicatePostException();
        } catch (final DataIntegrityViolationException e) {
            // Otra publicacion simultanea creo el mismo artista o album.
            // PostgreSQL ya aborto esta transaccion, asi que no se puede releer desde
            // aca: solo traducimos. Su transaccion ya commiteo, asi que reintentar anda.
            throw new ConcurrentPublishException();
        }
    }
```

### Después del commit

Fuente exacta en `c3e2a4c`: [services/src/main/java/ar/edu/itba/paw/services/TransactionCallbacks.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/TransactionCallbacks.java>), líneas 1–24.

```java
package ar.edu.itba.paw.services;

import org.springframework.transaction.support.TransactionSynchronization;
import org.springframework.transaction.support.TransactionSynchronizationManager;

final class TransactionCallbacks {

    private TransactionCallbacks() {
        throw new AssertionError("No instances");
    }

    static void afterCommit(final Runnable action) {
        if (!TransactionSynchronizationManager.isSynchronizationActive()) {
            action.run();
            return;
        }
        TransactionSynchronizationManager.registerSynchronization(new TransactionSynchronization() {
            @Override
            public void afterCommit() {
                action.run();
            }
        });
    }
}
```

## Archivos para seguir el flujo

- [services/src/main/java/ar/edu/itba/paw/services/TransactionCallbacks.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/TransactionCallbacks.java>) · [[TransactionCallbacks]]
- [services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java>) · [[PostServiceImpl]]
- [services/src/main/java/ar/edu/itba/paw/services/InquiryServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/InquiryServiceImpl.java>) · [[InquiryServiceImpl]]
- [services/src/main/java/ar/edu/itba/paw/services/CartServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/CartServiceImpl.java>) · [[CartServiceImpl]]
- [services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java>) · [[UserServiceImpl]]
- [services/src/main/java/ar/edu/itba/paw/services/AddressServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/AddressServiceImpl.java>) · [[AddressServiceImpl]]
- [persistence/src/main/java/ar/edu/itba/paw/persistence/PostJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/PostJdbcDao.java>) · [[PostJdbcDao]]
- [persistence/src/main/java/ar/edu/itba/paw/persistence/ArtistJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/ArtistJdbcDao.java>) · [[ArtistJdbcDao]]
- [webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java>) · [[WebConfig]]

Fuente inspeccionada: `c3e2a4c`, 2026-10-05. Es evidencia estática; no implica ejecución de la aplicación. [[Source inventory]] · [[Roadmap de lectura]]
