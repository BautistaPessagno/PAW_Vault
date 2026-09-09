---
title: "WebConfig"
categories: ["Operations"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "operations"]
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java"]
---

# WebConfig

The composition root. ComponentScan discovers DAO implementations, services and controllers. It enables MVC, transaction proxies and async proxies. It requires classpath database.properties and mail.properties. Beans wire the non-pooled SimpleDriverDataSource, JDBC transaction manager, startup schema initializer, JSP resolver, SMTP sender, Thymeleaf mail engine, message bundles and Bean Validation. Resource handlers map CSS, JS and images; there are no JavaScript source assets in this checkout. See [[Startup and dependency injection]] and [[Configuration and running]].

## Connections

Project types referenced: none.

Referenced by: no other production Java type directly references this name; Spring discovers implementations through scanning.

Tests: no direct test source reference. See [[Testing and evidence]].

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java, lines 1–146](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java>)

```java
package ar.edu.itba.paw.webapp.config;

import org.springframework.context.MessageSource;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.PropertySource;
import org.springframework.context.support.ReloadableResourceBundleMessageSource;
import org.springframework.core.env.Environment;
import org.springframework.core.io.ClassPathResource;
import org.springframework.jdbc.datasource.DataSourceTransactionManager;
import org.springframework.jdbc.datasource.SimpleDriverDataSource;
import org.springframework.jdbc.datasource.init.DataSourceInitializer;
import org.springframework.jdbc.datasource.init.ResourceDatabasePopulator;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.JavaMailSenderImpl;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.transaction.PlatformTransactionManager;
import org.springframework.transaction.annotation.EnableTransactionManagement;
import org.springframework.validation.Validator;
import org.springframework.validation.beanvalidation.LocalValidatorFactoryBean;
import org.springframework.web.servlet.ViewResolver;
import org.springframework.web.servlet.config.annotation.EnableWebMvc;
import org.springframework.web.servlet.config.annotation.ResourceHandlerRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;
import org.springframework.web.servlet.view.InternalResourceViewResolver;
import org.springframework.web.servlet.view.JstlView;
import org.thymeleaf.spring5.SpringTemplateEngine;
import org.thymeleaf.templatemode.TemplateMode;
import org.thymeleaf.templateresolver.ClassLoaderTemplateResolver;

import javax.sql.DataSource;
import java.nio.charset.StandardCharsets;
import java.sql.Driver;
import java.util.Properties;

@EnableWebMvc
@EnableTransactionManagement
@EnableAsync
@ComponentScan({ "ar.edu.itba.paw.persistence", "ar.edu.itba.paw.webapp.controller", "ar.edu.itba.paw.services" })
@PropertySource("classpath:database.properties")
@PropertySource("classpath:mail.properties")
@Configuration
public class WebConfig implements WebMvcConfigurer {

  private static final String SMTP_PROTOCOL = "smtp";

  @Bean
  public DataSource dataSource(final Environment environment) throws ClassNotFoundException {
    final SimpleDriverDataSource dataSource = new SimpleDriverDataSource();
    dataSource.setDriverClass(Class.forName(environment.getRequiredProperty("db.driver")).asSubclass(Driver.class));
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
   * Crea el esquema al levantar el contexto. El script vive en el modulo
   * persistence (es un detalle del DAO) y es idempotente, asi que correrlo en
   * cada arranque sobre una base ya poblada no rompe ni pierde datos.
   */
  @Bean
  public DataSourceInitializer dataSourceInitializer(final DataSource dataSource) {
    final ResourceDatabasePopulator populator = new ResourceDatabasePopulator();
    populator.addScript(new ClassPathResource("schema.sql"));

    final DataSourceInitializer dataSourceInitializer = new DataSourceInitializer();
    dataSourceInitializer.setDataSource(dataSource);
    dataSourceInitializer.setDatabasePopulator(populator);
    return dataSourceInitializer;
  }

  @Bean
  public ViewResolver viewResolver() {
    final InternalResourceViewResolver viewResolver = new InternalResourceViewResolver();
    viewResolver.setViewClass(JstlView.class);
    viewResolver.setPrefix("/WEB-INF/views/");
    viewResolver.setSuffix(".jsp");
    return viewResolver;
  }

  @Bean
  public JavaMailSender mailSender(final Environment environment) {
    final JavaMailSenderImpl mailSender = new JavaMailSenderImpl();
    mailSender.setHost(environment.getRequiredProperty("mail.host"));
    mailSender.setPort(environment.getRequiredProperty("mail.port", Integer.class));
    mailSender.setUsername(environment.getRequiredProperty("mail.username"));
    mailSender.setPassword(environment.getRequiredProperty("mail.password"));

    final Properties properties = mailSender.getJavaMailProperties();
    properties.put("mail.transport.protocol", SMTP_PROTOCOL);
    properties.put("mail.smtp.auth", environment.getRequiredProperty("mail.smtp.auth"));
    properties.put("mail.smtp.starttls.enable", environment.getRequiredProperty("mail.smtp.starttls.enable"));
    properties.put("mail.smtp.connectiontimeout", environment.getRequiredProperty("mail.smtp.connection-timeout-ms"));
    properties.put("mail.smtp.timeout", environment.getRequiredProperty("mail.smtp.read-timeout-ms"));
    properties.put("mail.smtp.writetimeout", environment.getRequiredProperty("mail.smtp.write-timeout-ms"));
    return mailSender;
  }

  @Bean
  public SpringTemplateEngine mailTemplateEngine(final MessageSource messageSource) {
    final ClassLoaderTemplateResolver templateResolver = new ClassLoaderTemplateResolver();
    templateResolver.setPrefix("mail/");
    templateResolver.setSuffix(".html");
    templateResolver.setTemplateMode(TemplateMode.HTML);
    templateResolver.setCharacterEncoding(StandardCharsets.UTF_8.name());

    final SpringTemplateEngine templateEngine = new SpringTemplateEngine();
    templateEngine.setTemplateResolver(templateResolver);
    templateEngine.setTemplateEngineMessageSource(messageSource);
    return templateEngine;
  }

  @Bean
  public MessageSource messageSource() {
    final ReloadableResourceBundleMessageSource messageSource = new ReloadableResourceBundleMessageSource();
    messageSource.setBasename("classpath:i18n/messages");
    messageSource.setDefaultEncoding(StandardCharsets.UTF_8.name());
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

## Context

[[Architecture]] · [[Domain and identity]] · [[Source inventory]]
