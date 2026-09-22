---
title: "Audit local 2026-09-17"
categories: [Testing, Operations, Web, Flows]
type: audit
module: cross-cutting
project: quieroVinilos
snapshot: "2026-09-17"
commit: "e5e926d4c1f2026494b3dc03768d984092b1052a"
status: verified-with-limits
---

# Audit local 2026-09-17

## Resultado y alcance

La base local quedó con **27 publicaciones disponibles, las 27 con imagen**, distribuidas entre dos cuentas Gmail activas: 14 publicaciones del usuario 1 y 13 del usuario 3. La cuenta ITBA fue eliminada. Hay **seis consultas pendientes, tres en cada dirección**; los seis avisos llegaron y se observaron en Apple Mail. No se aceptaron ventas ni se rechazaron consultas.

Se vaciaron las siete tablas de negocio antes de cargar el conjunto de prueba. Se conservó un respaldo previo fuera del vault, en `/private/tmp/quierovinilos-audit-20260917/before-reset.dump`; al estar en una carpeta temporal, no se considera un respaldo permanente. El vault no contiene contraseñas, tokens ni el respaldo de datos.

El servidor probado fue `http://localhost:8080`, ejecutado desde `/Users/bautistapessagno/workspaces/paw2026b/redesign-header-filtros`, commit `e5e926d4c1f2026494b3dc03768d984092b1052a`. El checkout principal estaba en `82a7b8d`, mientras el mapa anterior del vault describe `40328f0`. Este informe documenta la rama ejecutada; no equivale a una actualización completa del mapa de código. Véase [[Known gaps and document drift]].

Las publicaciones y las consultas se crearon mediante los formularios HTTP de la aplicación, con autenticación y CSRF. Se revisaron páginas en el navegador y la entrega en Apple Mail. Las imágenes pendientes se agregaron en la base local porque no hay un flujo de edición de publicaciones expuesto. Por tanto, la verificación final de todas las imágenes no demuestra que se hayan cargado todas mediante el selector de archivos de la interfaz.

Los títulos, artistas y años originales se contrastaron con fuentes del catálogo indicadas abajo. Precio, condición, zona y año de prensado son **datos de demostración**, no una tasación ni una afirmación sobre ejemplares reales. Las descripciones lo indican. Las portadas son imágenes de referencia del álbum, no fotografías del ejemplar vendido.

## Hallazgos reproducidos

Prioridades: P1 impide descubrir parte del catálogo; P2 afecta resultados o tareas habituales; P3 añade fricción.

### P1 — El catálogo oculta 11 publicaciones y presenta 16 como cantidad

Con 27 filas AVAILABLE, abrir `/` devuelve los posts 27 a 12 y muestra «16 vinilos» (o «16 records» según idioma). No hay navegación a una página siguiente. Las publicaciones restantes existen y pueden encontrarse con filtros o enlaces directos. El contador usa el tamaño del resultado limitado, lo que induce a pensar que el catálogo completo tiene 16 elementos.

Recomendación: paginar o permitir cargar más y calcular por separado el total de coincidencias.

Fuente: [services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java:25](</Users/bautistapessagno/workspaces/paw2026b/redesign-header-filtros/services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java:25>), revisión `e5e926d`.

```java
    private static final int RESULT_LIMIT = 16;
```

Fuente: [services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java:67](</Users/bautistapessagno/workspaces/paw2026b/redesign-header-filtros/services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java:67>), revisión `e5e926d`.

```java
        return new SearchResult(query, postDao.search(normalize(criteria, query), RESULT_LIMIT));
```

Fuente: [webapp/src/main/webapp/WEB-INF/views/landing/index.jsp:7](</Users/bautistapessagno/workspaces/paw2026b/redesign-header-filtros/webapp/src/main/webapp/WEB-INF/views/landing/index.jsp:7>), revisión `e5e926d`.

```jsp
<spring:message code="landing.results.count" var="countText">
    <spring:argument value="${fn:length(posts)}"/>
</spring:message>
```

### P2 — Buscar sin tilde pierde coincidencias

`/?q=Cancion` devuelve cero publicaciones; `/?q=Canci%C3%B3n` devuelve los posts 21 y 7, ambos de Canción Animal. Convertir a minúsculas no resuelve las diferencias de acentuación.

Recomendación: normalizar acentos para las búsquedas y conservar el texto original para mostrarlo.

Fuente: [persistence/src/main/java/ar/edu/itba/paw/persistence/PostJdbcDao.java:105](</Users/bautistapessagno/workspaces/paw2026b/redesign-header-filtros/persistence/src/main/java/ar/edu/itba/paw/persistence/PostJdbcDao.java:105>), revisión `e5e926d`.

```java
            final String pattern = "%" + escapeLike(criteria.getQuery().toLowerCase(Locale.ROOT)) + "%";
            clauses.add("(LOWER(a.title) LIKE ? " + LIKE_ESCAPE_CLAUSE
                    + " OR LOWER(ar.name) LIKE ? " + LIKE_ESCAPE_CLAUSE + ")");
```

### P2 — Un rango de precios invertido se descarta sin avisar

Abrir `/?minPrice=90000&maxPrice=10000` devuelve los mismos 16 posts del catálogo sin filtrar, aunque el rango es imposible y la interfaz sigue mostrando la opción de quitar filtros. La respuesta es 200; no hay error de validación visible.

Recomendación: indicar junto a los campos que el mínimo debe ser menor o igual al máximo, conservando lo ingresado.

Fuente: [services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java:79](</Users/bautistapessagno/workspaces/paw2026b/redesign-header-filtros/services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java:79>), revisión `e5e926d`.

```java
        final boolean invertedRange = minPrice != null && maxPrice != null && minPrice > maxPrice;
        return new PostSearchCriteria(query,
                criteria.getSort() == null ? PostSort.NEWEST : criteria.getSort(),
                criteria.getGenre(), criteria.getCondition(), artistId,
                insideRange(criteria.getReleaseYear(), MIN_YEAR, MAX_YEAR),
                invertedRange ? null : minPrice,
                invertedRange ? null : maxPrice);
```

### P2 — No hay edición de una publicación existente

Agregar una portada después de publicar requirió actualizar los datos locales. La interfaz de detalle del propietario muestra un aviso, pero no ofrece editar título, descripción, precio o foto. La inspección de rutas de esta revisión tampoco encontró un flujo de edición.

Recomendación: incorporar «Mis publicaciones» y edición con control de propietario. Esta es una carencia funcional; no se afirma que haya fallado una función de edición ya existente.

Fuente: [webapp/src/main/webapp/WEB-INF/views/post/detail.jsp:100](</Users/bautistapessagno/workspaces/paw2026b/redesign-header-filtros/webapp/src/main/webapp/WEB-INF/views/post/detail.jsp:100>), revisión `e5e926d`.

```jsp
                            <c:when test="${currentUserId eq post.userId}">
                                <p class="hint"><spring:message code="post.detail.own"/></p>
                            </c:when>
```

### P2 — Los nombres pierden su escritura original

Se enviaron «Abbey Road» y «The Beatles», pero se guardan y muestran «abbey road» y «the beatles». Ocurre también con otros títulos y artistas. Esto degrada nombres propios y siglas.

Recomendación: separar la clave normalizada para comparación del valor que se presenta al usuario.

Fuente: [services/src/main/java/ar/edu/itba/paw/services/AlbumServiceImpl.java:28](</Users/bautistapessagno/workspaces/paw2026b/redesign-header-filtros/services/src/main/java/ar/edu/itba/paw/services/AlbumServiceImpl.java:28>), revisión `e5e926d`.

```java
        final String normalizedTitle = title.trim().toLowerCase(Locale.ROOT);
```

Fuente: [services/src/main/java/ar/edu/itba/paw/services/ArtistServiceImpl.java:25](</Users/bautistapessagno/workspaces/paw2026b/redesign-header-filtros/services/src/main/java/ar/edu/itba/paw/services/ArtistServiceImpl.java:25>), revisión `e5e926d`.

```java
        return artistDao.findOrCreate(name.trim().toLowerCase(Locale.ROOT));
```

### P3 — Las consultas y sus correos no llevan directamente al ejemplar

La página `/inquiries` no contiene enlaces `/post/{id}`. El título se muestra como encabezado sin enlace; para comparar ejemplares del mismo álbum es necesario volver al catálogo. Los seis correos llegaron, pero su botón lleva a la portada del sitio.

Recomendación: enlazar el ejemplar y la consulta desde el correo; mostrar en la consulta datos que permitan distinguir el ejemplar, como precio y zona.

Fuente: [webapp/src/main/webapp/WEB-INF/views/inquiry/index.jsp:39](</Users/bautistapessagno/workspaces/paw2026b/redesign-header-filtros/webapp/src/main/webapp/WEB-INF/views/inquiry/index.jsp:39>), revisión `e5e926d`.

```jsp
                                <ui:h3 text="${itemTitle}"/>
                                <ui:p text="${buyerText}"/>
                                <c:if test="${not empty inquiry.message}"><ui:p text="${inquiry.message}"/></c:if>
                                <ui:p text="${statusLabel}" variant="muted"/>
```

Fuente: [services/src/main/java/ar/edu/itba/paw/services/EmailServiceImpl.java:99](</Users/bautistapessagno/workspaces/paw2026b/redesign-header-filtros/services/src/main/java/ar/edu/itba/paw/services/EmailServiceImpl.java:99>), revisión `e5e926d`.

```java
            context.setVariable("homeUrl", baseUrl + "/");
```

Fuente: [services/src/main/resources/mail/post-interest.html:29](</Users/bautistapessagno/workspaces/paw2026b/redesign-header-filtros/services/src/main/resources/mail/post-interest.html:29>), revisión `e5e926d`.

```html
            <a th:href="${homeUrl}" href="#"
               style="display: inline-block; padding: 12px 24px; background-color: #1f2933; color: #ffffff; text-decoration: none; border-radius: 6px; font-size: 15px;"
               th:text="#{email.postInterest.cta}">Ver quieroVinilos</a>
```

### P3 — Los títulos largos desalinean los precios

En el catálogo de escritorio observado, el título de Sgt. Pepper ocupa varias líneas y desplaza el precio respecto de las tarjetas contiguas. La comparación rápida de precios se vuelve más difícil. Recomendación: reservar un espacio consistente para el título o alinear los datos comerciales en la tarjeta. Observación visual de escritorio; no se hizo una evaluación móvil.

## Controles que funcionaron

| Comprobación | Evidencia obtenida |
|---|---|
| Cuentas | Dos usuarios activos; cuenta ITBA ausente; inicio de sesión con ambos Gmail |
| Publicaciones | 27 disponibles; 14 del usuario 1 y 13 del usuario 3; datos comerciales completos |
| Imágenes | 27 de 27 vinculadas; cada endpoint respondió 200 con contenido JPEG; portadas visibles en el catálogo |
| Interés cruzado | Seis consultas PENDING persistidas: usuario 1 a posts 15, 19 y 21; usuario 3 a posts 2, 3 y 6 |
| Correo | Seis mensajes de interés observados en Apple Mail, tres por cuenta |
| Publicar sin sesión | Redirección al inicio de sesión |
| Acceso administrativo | `/admin` respondió 403 para un usuario común |
| Contactarse a sí mismo | `/post/1/contact` respondió 403 para su propietario |
| Publicación inexistente | `/post/999999` respondió 404 |
| Filtro de jazz | Devolvió los posts 3, 9, 17 y 23, los cuatro esperados |
| Detalle | `/post/2` respondió 200 y presentó los datos del ejemplar |

## Catálogo y fuentes

Los IDs separados por una barra representan ejemplares de las dos cuentas. Las páginas enlazadas respaldan la identidad del álbum; no avalan los precios ni el estado físico de los datos de demostración. Para las imágenes se usaron portadas de páginas oficiales y Apple Music; la portada de The Dark Side of the Moon se tomó de [Parsonics](https://parsonics.com/products/dark-side-of-the-moon). Se verificó la correspondencia con el álbum, no una edición comercial particular.

| Álbum | Artista | Año original | Posts | Fuente |
|---|---|---:|---|---|
| Abbey Road | The Beatles | 1969 | 1 / 15 | [Catálogo](https://www.thebeatles.com/abbey-road) |
| The Dark Side of the Moon | Pink Floyd | 1973 | 2 / 16 | [Catálogo](https://www.pinkfloyd.com/albums/the-dark-side-of-the-moon/) |
| Kind of Blue | Miles Davis | 1959 | 3 / 17 | [Catálogo](https://www.milesdavis.com/albums/kind-of-blue/) |
| Revolver | The Beatles | 1966 | 4 / 18 | [Catálogo](https://www.thebeatles.com/revolver) |
| Random Access Memories | Daft Punk | 2013 | 5 / 19 | [Catálogo](https://www.daftpunk.com/randomaccessmemories/) |
| Legend | Bob Marley & The Wailers | 1984 | 6 / 20 | [Catálogo](https://www.bobmarley.com/release/legend-1984/) |
| Canción Animal | Soda Stereo | 1990 | 7 / 21 | [Catálogo](https://sodastereo.com/timeline/) |
| Wish You Were Here | Pink Floyd | 1975 | 8 / 22 | [Catálogo](https://www.pinkfloyd.com/albums/wish-you-were-here/) |
| Bitches Brew | Miles Davis | 1970 | 9 / 23 | [Catálogo](https://www.milesdavis.com/albums/bitches-brew/) |
| Rubber Soul | The Beatles | 1965 | 10 / 24 | [Catálogo](https://www.thebeatles.com/rubber-soul) |
| Sgt. Pepper's Lonely Hearts Club Band | The Beatles | 1967 | 11 / 25 | [Catálogo](https://www.thebeatles.com/sgt-peppers-lonely-hearts-club-band-0) |
| Let It Be | The Beatles | 1970 | 12 / 26 | [Catálogo](https://www.thebeatles.com/let-it-be-0) |
| Help! | The Beatles | 1965 | 13 / 27 | [Catálogo](https://www.thebeatles.com/albums/help) |
| Please Please Me | The Beatles | 1963 | 14 | [Catálogo](https://www.thebeatles.com/please-please-me) |

## Límites de la auditoría

No se modificó código de la aplicación ni se corrigieron los hallazgos. No se ejecutaron Maven, pruebas de concurrencia, aceptación/rechazo de venta, fallo de SMTP, pruebas negativas de CSRF ni auditoría móvil o de accesibilidad completa. La revisión se centra en carga de datos, búsqueda, detalle, consultas y portadas.

Las pruebas de envío duplicado y archivo sobredimensionado no se ejecutaron: la revisión automática de herramientas bloqueó esos envíos porque podían crear publicaciones adicionales o persistir datos de prueba no deseados. Se continuó con comprobaciones de lectura. Un error del navegador automatizado durante el selector de archivos tampoco se atribuye a la aplicación sin evidencia independiente.

La confirmación de correo se limita a los seis mensajes observados; no garantiza entrega futura ni tratamiento de fallos. Las fuentes y fragmentos de código citados pertenecen a la rama ejecutada, y la cobertura histórica de [[Source inventory]] no se recalculó para esa rama.

[[Home]] · [[Landing flow]] · [[Publish flow]] · [[Cover image flow]] · [[Contact flow]] · [[Inquiry and sale flow]] · [[Mail delivery]] · [[Testing and evidence]] · [[Verification record]]

## Estado posterior del código

Esta sección no modifica los resultados del audit. El mapa del vault se actualizó a `f12af08` el 2026-09-22 mediante lectura estática del código, sin repetir estas pruebas. La tabla de [[Known gaps and document drift]] contrasta cada hallazgo con esa revisión.
