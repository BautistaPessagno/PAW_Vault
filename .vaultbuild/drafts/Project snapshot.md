@title: Project snapshot
@categories: Navigation
@tags: codemap, navigation
@files: README.md, CONTEXT.md, pom.xml, webapp/src/main/java/ar/edu/itba/paw/webapp/config/SecurityConfig.java, services/src/main/java/ar/edu/itba/paw/services/InquiryServiceImpl.java, services/src/main/java/ar/edu/itba/paw/services/CartServiceImpl.java

> [!summary] En una frase
> quieroVinilos es un marketplace de vinilos usados entre particulares, hecho por el grupo 14 de PAW (ITBA, 2026B); este vault lo describe en el commit `c3e2a4c` del 5 de octubre de 2026, en la etapa JDBC de la cursada.

## Qué versión describe el vault

| | |
|---|---|
| Commit | `c3e2a4cd23337bd35175d14ef551ba12a758a59d` |
| Qué es | Merge del PR #62 sobre `main` |
| Fecha | 5 de octubre de 2026 |
| Mapa anterior | `8929aea`, 4 de octubre: 60 commits atrás ([[Recent changes 2026-10-05]]). El anterior a ese, `f12af08` del 22 de septiembre ([[Recent changes 2026-10-04]]) |
| Archivos versionados | 472, de ellos 238 Java |
| Evidencia | Lectura estática del código. No se ejecutó la aplicación ni los tests |

El clon local tenía `main` en `1368153` (PR #57) y `origin/main` ya traía `c3e2a4c` (PR #59 a #62). El vault se generó desde los objetos de `c3e2a4c`, sin tocar la copia de trabajo. El único cambio local sin commitear era `.gitignore`, que queda fuera.

## Qué hace hoy

**Sin cuenta.** Ver el catálogo de publicaciones disponibles, buscar con sugerencias, filtrar por género, estado, precio y año, ordenar, abrir la ficha de una publicación con sus fotos y ver perfiles públicos con reseñas.

**Con cuenta sin verificar.** Lo mismo, con sesión iniciada. Para operar hay que abrir el enlace de verificación que llega por correo.

**Con cuenta verificada.**

- Publicar un vinilo con hasta cinco fotos, editarlo (quitando fotos con una X) y eliminarlo.
- Consultar por un vinilo eligiendo dirección de envío, o juntar varios en el carrito y enviar todas las consultas juntas.
- Conversar con la otra parte dentro de la consulta.
- Filtrar sus bandejas de consultas y sus publicaciones por estado, con la cantidad de cada uno.
- Como vendedor: aceptar (reserva el vinilo y fija el precio de la venta), rechazar, pedir otro comprobante, confirmar el pago (lo marca vendido) o cancelar.
- Como comprador: subir el comprobante de la transferencia o cancelar antes de subirlo.
- Calificar a la otra parte después de una venta confirmada. El perfil público separa las reseñas recibidas como vendedor y como comprador.
- Administrar su perfil: nombre, foto, contraseña, datos de cobro y hasta tres direcciones.

**Administrador.** Editar y eliminar publicaciones disponibles de cualquier cuenta.

Cada cambio de estado y cada mensaje avisan por correo a la otra parte.

## Con qué está hecho

| Capa | Tecnología |
|---|---|
| Lenguaje y build | Java 21, Maven, seis módulos |
| Web | Spring MVC 5.3, JSP con JSTL, Spring Security 5.8 |
| Persistencia | Spring JDBC sobre PostgreSQL, migraciones Flyway V1–V11 |
| Correo | JavaMail con plantillas Thymeleaf, envío asíncrono |
| Tests | JUnit 5, Mockito, HSQLDB en memoria |
| Despliegue | Un WAR en Tomcat, en el servidor de la cátedra |

Sin Spring Boot y sin JPA: están prohibidos en esta etapa. Detalle en [[Build and dependencies]] y [[Architecture]].

## Qué no tiene

- Pasarela de pago: la transferencia se hace por fuera y el comprobante se revisa a mano.
- Stock: cada publicación es un ejemplar único.
- Mensajería en tiempo real: la conversación se recarga con la página.
- Panel de administración.
- Cola persistente de correo.

La lista completa de límites y de posibles defectos está en [[Known gaps and document drift]].

## Por dónde seguir

- Para entender el producto: [[Domain and identity]].
- Para ubicar una funcionalidad: [[Feature map]].
- Para leer el código en orden: [[Roadmap de lectura]].
- Para preparar una defensa: [[Defense guide]].
