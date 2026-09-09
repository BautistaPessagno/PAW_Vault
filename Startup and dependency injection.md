---
title: "Startup and dependency injection"
categories: ["Architecture"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
tags: ["codemap", "architecture"]
sources: ["webapp/src/main/webapp/WEB-INF/web.xml"]
---

# Startup and dependency injection

The servlet container reads `WEB-INF/web.xml`. Its ContextLoaderListener creates an AnnotationConfigWebApplicationContext configured with [[WebConfig]]. The DispatcherServlet handles `/` and uses the web context to resolve controller mappings. There is no `main` method starting the app.

```mermaid
flowchart LR
    C[Servlet container] --> X[web.xml]
    X --> L[ContextLoaderListener]
    L --> W[WebConfig]
    X --> D[DispatcherServlet]
    W --> B[Scanned Spring beans]
    W --> DS[DataSource]
    DS --> I[DataSourceInitializer]
    I --> SQL[schema.sql]
    D --> CT[Controller]
    CT --> V[ViewResolver]
    V --> JSP[JSP under WEB-INF/views]
```

## Bean connections

| Configuration | Result | Consumers |
|---|---|---|
| ComponentScan | Discovers @Repository, @Service and @Controller classes in the three configured packages | Constructor injection resolves interfaces to discovered implementations |
| dataSource | SimpleDriverDataSource using required db properties | All JDBC DAOs, schema initializer, transaction manager |
| transactionManager | DataSourceTransactionManager | Service @Transactional proxies |
| dataSourceInitializer | Executes classpath schema.sql | Table creation, username backfill and cover-column upgrade |
| taskExecutor | ThreadPoolTaskExecutor: core 2, max 5, queue 50, CallerRunsPolicy | Both EmailService @Async methods |
| multipartResolver | Lazy CommonsMultipartResolver, UTF-8, 6 MiB whole request | Publish form upload |
| viewResolver | JstlView, `/WEB-INF/views/` prefix, `.jsp` suffix | Logical controller view names |
| mailSender | JavaMailSenderImpl, SMTP auth/TLS/timeouts | [[EmailServiceImpl]] |
| mailTemplateEngine | Classpath `mail/` + name + `.html`, UTF-8 HTML | Welcome/contact rendering |
| messageSource | ReloadableResourceBundleMessageSource, `i18n/messages`, UTF-8 | JSP, validation, mail subjects and templates |
| validator/getValidator | LocalValidatorFactoryBean using that message source | @Valid form arguments |
| addResourceHandlers | `/css/**`, `/js/**`, `/images/**` to matching web directories | Styles and placeholder image |

@EnableTransactionManagement and @EnableAsync add proxy behavior. Direct `new` in tests does not activate them. WebConfig now declares a bounded async executor. CallerRunsPolicy can execute mail in the request thread under saturation. No connection pool or scheduler is defined. Configuration uses required classpath @PropertySource declarations; read [[Configuration and running]] for why environment-only deployment is not established by the README claim.

A logical `landing/index` view becomes `/WEB-INF/views/landing/index.jsp`. A `redirect:/` result initiates another HTTP request rather than resolving a JSP. See [[Views and assets]].

## Servlet descriptor

[webapp/src/main/webapp/WEB-INF/web.xml, lines 1–41](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/web.xml>)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<web-app id="PAW" version="2.4"
  xmlns="http://java.sun.com/xml/ns/j2ee"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://java.sun.com/xml/ns/j2ee http://java.sun.com/xml/ns/j2ee/web-app_2_4.xsd">
  <display-name>PAW test application</display-name>

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
</web-app>
```

[[WebConfig]] · [[Architecture]]

[[ImageController]] separately maps /covers/{id} to stored bytes; it does not use the static /images handler. [[Cover image flow]] distinguishes upload and retrieval.
