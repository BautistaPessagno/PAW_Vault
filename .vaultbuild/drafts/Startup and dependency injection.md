@title: Startup and dependency injection
@categories: Architecture
@files: webapp/src/main/webapp/WEB-INF/web.xml, webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java, webapp/src/main/java/ar/edu/itba/paw/webapp/config/SecurityConfig.java

> [!summary] En una frase
> El contenedor lee `web.xml`, crea un contexto de Spring a partir de `WebConfig`, que escanea los tres paquetes, aplica las migraciones Flyway y deja listos seguridad, vistas, i18n y correo; el `DispatcherServlet` atiende todo lo que no es estático.

## Herramientas

| Herramienta | Para qué |
|---|---|
| Servlet 4.0 (`web.xml`) | Declarar filtros, listeners, el servlet y la sesión |
| `ContextLoaderListener` + `AnnotationConfigWebApplicationContext` | Crear el contexto raíz desde una clase `@Configuration` |
| `DispatcherServlet` | Front controller de Spring MVC |
| `@ComponentScan` | Descubrir `@Repository`, `@Service` y `@Controller` |
| Inyección por constructor (`@Autowired`) | Todas las dependencias son `final` |
| Flyway (`@Bean(initMethod = "migrate")`) | Aplicar el esquema al arrancar |

## Secuencia de arranque

1. Tomcat (o Jetty en desarrollo) despliega `app.war` y lee `web.xml`.
2. `ContextLoaderListener` crea el contexto raíz con `WebConfig`.
3. `WebConfig` importa `SecurityConfig` y escanea `ar.edu.itba.paw.persistence`, `ar.edu.itba.paw.services` y `ar.edu.itba.paw.webapp.controller`.
4. Lee `database.properties` y `mail.properties` del classpath (`ignoreResourceNotFound`, pero cada valor se pide con `getRequiredProperty`: si falta una key, el arranque falla).
5. Crea el `DataSource` y el bean `flyway`, cuyo `initMethod` corre `migrate()`: aplica las migraciones que la base todavía no tiene. Si una falla, la aplicación no arranca.
6. Crea el resto de los beans (tabla siguiente) e inyecta por constructor.
7. `HttpSessionEventPublisher` queda escuchando el ciclo de vida de las sesiones.
8. `DispatcherServlet` se carga con `load-on-startup` y queda mapeado a `/`.

## Beans de `WebConfig`

| Bean | Configuración | Para qué |
|---|---|---|
| `taskExecutor` | `ThreadPoolTaskExecutor` 2–5 hilos, cola 50, descarta al saturarse | Hilos de los métodos `@Async` de correo ([[Mail delivery]]) |
| `dataSource` | `DriverManagerDataSource` con `db.*` | Conexiones JDBC. No es un pool: abre una conexión por uso |
| `transactionManager` | `DataSourceTransactionManager` | Respaldo de `@Transactional` ([[Transactions and concurrency]]) |
| `flyway` | `classpath:db/migration`, `baselineOnMigrate`, `baselineVersion("1")` | Esquema ([[Database schema]]) |
| `multipartResolver` | Commons FileUpload, tope de 26 MiB, perezoso | Archivos ([[Cover image flow]]) |
| `viewResolver` | `/WEB-INF/views/` + nombre + `.jsp`, `JstlView` | Vistas |
| `localeResolver` | `AcceptHeaderLocaleResolver`, español por defecto | Idioma del request ([[Localization]]) |
| `mailSender` | `JavaMailSenderImpl` con `mail.*` y tres timeouts | SMTP |
| `mailTemplateEngine` | Thymeleaf, `mail/*.html`, mismo `MessageSource` | HTML de los correos |
| `messageSource` | `classpath:i18n/messages`, UTF-8, sin fallback al idioma del sistema | Textos |
| `validator` | `LocalValidatorFactoryBean` con ese `MessageSource` | Mensajes de Bean Validation desde los bundles |
| Recursos estáticos | `/css/**`, `/js/**`, `/images/**` | Servidos sin pasar por un controller |

Anotaciones de la clase: `@EnableWebMvc`, `@EnableTransactionManagement`, `@EnableAsync`.

## Beans de `SecurityConfig`

`passwordEncoder` (BCrypt 12), `passwordHasher` (adaptador para `services`), `userDetailsService`, `addressAccess`, `inquiryAccess`, `postAccess`, `sessionRegistry` y `securityFilterChain`. Detalle en [[Security and authorization]].

## Decisiones y por qué

| Decisión | Motivo | Fuente |
|---|---|---|
| Spring 5 sin Spring Boot, con `web.xml` | Requisito de la cátedra para esta etapa | `docs/setup.md` |
| Un solo contexto para todo | `WebConfig` es a la vez contexto raíz y configuración de MVC; el servlet no declara configuración propia | `web.xml` |
| Flyway con `baselineOnMigrate` en la versión 1 | Las bases anteriores a Flyway ya tenían el esquema inicial: se las marca en V1 sin ejecutarla y siguen desde V2. Una base vacía corre todas | Comentario en [[WebConfig]] |
| `getRequiredProperty` | Falla fuerte al arrancar si falta configuración, en vez de fallar en el primer uso | `CLAUDE.md` del repo |
| Nombres de bean fijos (`taskExecutor`, `multipartResolver`) | Son los que Spring busca por convención | Comentarios en [[WebConfig]] |
| Sesión solo por cookie y `HttpOnly` | Seguridad y compatibilidad con el firewall de Spring Security | Comentario en `web.xml` |

## Límites conocidos

- `DriverManagerDataSource` no reutiliza conexiones: cada transacción abre una. Es suficiente para el volumen del TP; un pool sería el siguiente paso.
- No hay perfiles de Spring: la diferencia entre local y servidor está en los archivos de propiedades y en el perfil Maven `pampero` ([[Configuration and running]]).

## Preguntas de defensa

**¿Cómo se crean las tablas?**
Flyway corre al levantar el contexto y aplica las migraciones `V<n>__*.sql` que falten, anotándolas en su tabla de historial.

**¿Qué pasa si falta `mail.properties`?**
El archivo es opcional, pero las keys no: `getRequiredProperty` lanza una excepción y la aplicación no arranca.

**¿Cómo se inyectan las dependencias?**
Por constructor, con `@Autowired`, contra interfaces. Spring encuentra las implementaciones por `@ComponentScan`.

**¿Por qué `@EnableAsync` y `@EnableTransactionManagement`?**
Para que Spring envuelva los beans en proxies que interpretan `@Async` y `@Transactional`.

## Evidencia de código

### web.xml

{{file:webapp/src/main/webapp/WEB-INF/web.xml}}

### Anotaciones y escaneo

{{code:webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java:45-53}}

### DataSource, transacciones y Flyway

{{code:webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java:82-113}}

### Vistas, idioma, i18n y validación

{{code:webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java:129-143}}

{{code:webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java:177-204}}
