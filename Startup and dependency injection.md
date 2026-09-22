---
title: "Startup and dependency injection"
categories: ["Architecture"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["webapp/src/main/webapp/WEB-INF/web.xml", "webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/config/SecurityConfig.java"]
---

# Startup and dependency injection

The Servlet 4.0 descriptor creates a root AnnotationConfigWebApplicationContext with WebConfig. DispatcherServlet maps / and resolves MVC controllers and JSP logical names. WebConfig imports SecurityConfig and scans persistence, services and controllers.

Request filters are declared in this order: UTF-8 CharacterEncodingFilter for all paths, MultipartExceptionHandlerFilter and MultipartFilter for /publish and now also /post/*, then the Spring Security DelegatingFilterProxy for all paths. Multipart parsing precedes security so the CSRF token in the publish and edit forms can be read. A lazy overflow is translated by the outer exception filter, which redirects back to the originating form.

| Bean | Configuration |
|---|---|
| DataSource | DriverManagerDataSource, required db properties, no pool |
| Transaction manager | DataSourceTransactionManager |
| Schema initializer | classpath schema.sql, including backfills and constraint additions |
| taskExecutor | Core 2, max 5, queue 50, mail- prefix; a saturated pool logs and drops the task; waits up to 30 s on shutdown |
| Multipart resolver | CommonsMultipartResolver, UTF-8, lazy parsing, 6 MiB request limit |
| Locale resolver | AcceptHeaderLocaleResolver, Spanish default |
| Message source | UTF-8 i18n/messages, no system-locale fallback |
| View resolver | JstlView, /WEB-INF/views/ + name + .jsp |
| Mail template engine | Thymeleaf, classpath mail/*.html |
| Security beans | BCrypt encoder, PasswordHasher adapter with hash and matches, UserDetailsService, SecurityFilterChain |

PropertySource files are optional; missing required values still fail Environment lookups. @Transactional and @Async operate through Spring proxies; services additionally register after-commit synchronizations through [[TransactionCallbacks]]. The descriptor sets HttpOnly session cookies and, new in this range, `tracking-mode COOKIE`: without it the container could rewrite URLs with `;jsessionid`, which Spring Security's StrictHttpFirewall rejects, and stylesheets were the first requests to fail. Unmatched 404 errors route through ErrorController. Cover bytes use ImageController; /css, /js and /images use static resource handlers.

## Servlet descriptor

[webapp/src/main/webapp/WEB-INF/web.xml, lines 1–112](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/web.xml>)

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
  </filter-mapping>
  <!--
    Corre antes de la cadena de Spring Security para que el token CSRF del form multipart
    de publicacion o edicion ya este parseado cuando se valida.
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

[[WebConfig]] · [[SecurityConfig]] · [[Configuration and running]]
