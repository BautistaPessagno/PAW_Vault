---
title: "Startup and dependency injection"
categories: ["Architecture"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["webapp/src/main/webapp/WEB-INF/web.xml", "webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/config/SecurityConfig.java"]
---

# Startup and dependency injection

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

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/web.xml](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/web.xml>), líneas 1–123.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<web-app id="PAW" version="4.0"
  xmlns="http://xmlns.jcp.org/xml/ns/javaee"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee http://xmlns.jcp.org/xml/ns/javaee/web-app_4_0.xsd">
  <display-name>quieroVinilos</display-name>

  <context-param>
    <param-name>contextClass</param-name>
    <param-value>
      org.springframework.web.context.support.AnnotationConfigWebApplicationContext
</param-value>
  </context-param>
  <context-param>
    <param-name>contextConfigLocation</param-name>
    <param-value>
      ar.edu.itba.paw.webapp.config.WebConfig,
</param-value>
  </context-param>
  <filter>
    <filter-name>characterEncodingFilter</filter-name>
    <filter-class>org.springframework.web.filter.CharacterEncodingFilter</filter-class>
    <init-param>
      <param-name>encoding</param-name>
      <param-value>UTF-8</param-value>
    </init-param>
    <init-param>
      <param-name>forceEncoding</param-name>
      <param-value>true</param-value>
    </init-param>
  </filter>
  <filter-mapping>
    <filter-name>characterEncodingFilter</filter-name>
    <url-pattern>/*</url-pattern>
  </filter-mapping>
  <filter>
    <filter-name>multipartExceptionHandlerFilter</filter-name>
    <filter-class>ar.edu.itba.paw.webapp.security.MultipartExceptionHandlerFilter</filter-class>
  </filter>
  <filter-mapping>
    <filter-name>multipartExceptionHandlerFilter</filter-name>
    <url-pattern>/publish</url-pattern>
    <url-pattern>/post/*</url-pattern>
    <url-pattern>/inquiries/*</url-pattern>
    <url-pattern>/profile/avatar</url-pattern>
  </filter-mapping>
  <!--
    Corre antes de la cadena de Spring Security para que el token CSRF del form multipart
    de publicacion, edicion, comprobante o foto de perfil ya este parseado cuando se valida.
  -->
  <filter>
    <filter-name>multipartFilter</filter-name>
    <filter-class>org.springframework.web.multipart.support.MultipartFilter</filter-class>
    <init-param>
      <param-name>multipartResolverBeanName</param-name>
      <param-value>multipartResolver</param-value>
    </init-param>
  </filter>
  <filter-mapping>
    <filter-name>multipartFilter</filter-name>
    <url-pattern>/publish</url-pattern>
    <url-pattern>/post/*</url-pattern>
    <url-pattern>/inquiries/*</url-pattern>
    <url-pattern>/profile/avatar</url-pattern>
  </filter-mapping>
  <filter>
    <filter-name>springSecurityFilterChain</filter-name>
    <filter-class>org.springframework.web.filter.DelegatingFilterProxy</filter-class>
  </filter>
  <filter-mapping>
    <filter-name>springSecurityFilterChain</filter-name>
    <url-pattern>/*</url-pattern>
  </filter-mapping>
  <listener>
    <listener-class>
      org.springframework.web.context.ContextLoaderListener
</listener-class>
  </listener>
  <!--
    Publica la creacion, el cambio de id y la destruccion de cada sesion para que el
    SessionRegistry de SecurityConfig sepa que sesiones siguen vivas.
  -->
  <listener>
    <listener-class>org.springframework.security.web.session.HttpSessionEventPublisher</listener-class>
  </listener>

  <servlet>
    <servlet-name>dispatcher</servlet-name>
    <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
    <init-param>
      <param-name>contextClass</param-name>
      <param-value>
        org.springframework.web.context.support.AnnotationConfigWebApplicationContext
</param-value>
    </init-param>
    <load-on-startup>1</load-on-startup>
  </servlet>
  <servlet-mapping>
    <servlet-name>dispatcher</servlet-name>
    <url-pattern>/</url-pattern>
  </servlet-mapping>

  <!--
    Sin <secure>, el contenedor marca la cookie de sesion como Secure cuando el request
    llega por HTTPS y la deja utilizable en el desarrollo local sobre HTTP.
  -->
  <session-config>
    <cookie-config>
      <http-only>true</http-only>
    </cookie-config>
    <!--
      Solo cookie: sin esto el contenedor reescribe cada URL con ;jsessionid hasta confirmar
      que hay cookie, y el StrictHttpFirewall de Spring Security rechaza el ";" con un 500.
      Las hojas de estilo son las primeras en caer y la pagina queda sin CSS.
    -->
    <tracking-mode>COOKIE</tracking-mode>
  </session-config>

  <error-page>
    <error-code>404</error-code>
    <location>/error/404</location>
  </error-page>
</web-app>
```

### Anotaciones y escaneo

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java>), líneas 45–53.

```java
@EnableWebMvc
@EnableTransactionManagement
@EnableAsync
@Import(SecurityConfig.class)
@ComponentScan({ "ar.edu.itba.paw.persistence", "ar.edu.itba.paw.webapp.controller", "ar.edu.itba.paw.services" })
@PropertySource(value = "classpath:database.properties", ignoreResourceNotFound = true)
@PropertySource(value = "classpath:mail.properties", ignoreResourceNotFound = true)
@Configuration
public class WebConfig implements WebMvcConfigurer {
```

### DataSource, transacciones y Flyway

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java>), líneas 82–113.

```java
  @Bean
  public DataSource dataSource(final Environment environment) {
    final DriverManagerDataSource dataSource = new DriverManagerDataSource();
    dataSource.setDriverClassName(environment.getRequiredProperty("db.driver"));
    dataSource.setUrl(environment.getRequiredProperty("db.url"));
    dataSource.setUsername(environment.getRequiredProperty("db.username"));
    dataSource.setPassword(environment.getRequiredProperty("db.password"));
    return dataSource;
  }

  @Bean
  public PlatformTransactionManager transactionManager(final DataSource dataSource) {
    return new DataSourceTransactionManager(dataSource);
  }

  /*
   * Aplica al levantar el contexto las migraciones de persistence que la base todavia
   * no tiene. Si una falla, la aplicacion no arranca.
   *
   * Las bases anteriores a Flyway ya tienen el esquema inicial pero no la tabla de
   * historial: el baseline las marca en esa version sin ejecutarla y sigue desde la
   * siguiente. Una base vacia no hace baseline y corre todas.
   */
  @Bean(initMethod = "migrate")
  public Flyway flyway(final DataSource dataSource) {
    return Flyway.configure()
        .dataSource(dataSource)
        .locations("classpath:db/migration")
        .baselineOnMigrate(true)
        .baselineVersion("1")
        .load();
  }
```

### Vistas, idioma, i18n y validación

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java>), líneas 129–143.

```java
  @Bean
  public ViewResolver viewResolver() {
    final InternalResourceViewResolver viewResolver = new InternalResourceViewResolver();
    viewResolver.setViewClass(JstlView.class);
    viewResolver.setPrefix("/WEB-INF/views/");
    viewResolver.setSuffix(".jsp");
    return viewResolver;
  }

  @Bean
  public LocaleResolver localeResolver() {
    final AcceptHeaderLocaleResolver localeResolver = new AcceptHeaderLocaleResolver();
    localeResolver.setDefaultLocale(Locale.forLanguageTag("es"));
    return localeResolver;
  }
```

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java>), líneas 177–204.

```java
  @Bean
  public MessageSource messageSource() {
    final ReloadableResourceBundleMessageSource messageSource = new ReloadableResourceBundleMessageSource();
    messageSource.setBasename("classpath:i18n/messages");
    messageSource.setDefaultEncoding(StandardCharsets.UTF_8.name());
    messageSource.setFallbackToSystemLocale(false);
    return messageSource;
  }

  @Bean
  public LocalValidatorFactoryBean validator() {
    final LocalValidatorFactoryBean validator = new LocalValidatorFactoryBean();
    validator.setValidationMessageSource(messageSource());
    return validator;
  }

  @Override
  public Validator getValidator() {
    return validator();
  }

  @Override
  public void addResourceHandlers(final ResourceHandlerRegistry registry) {
    registry.addResourceHandler("/css/**").addResourceLocations("/css/");
    registry.addResourceHandler("/js/**").addResourceLocations("/js/");
    registry.addResourceHandler("/images/**").addResourceLocations("/images/");
  }
}
```

## Archivos para seguir el flujo

- [webapp/src/main/webapp/WEB-INF/web.xml](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/web.xml>)
- [webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java>) · [[WebConfig]]
- [webapp/src/main/java/ar/edu/itba/paw/webapp/config/SecurityConfig.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/config/SecurityConfig.java>) · [[SecurityConfig]]

Fuente inspeccionada: `c3e2a4c`, 2026-10-05. Es evidencia estática; no implica ejecución de la aplicación. [[Source inventory]] · [[Roadmap de lectura]]
