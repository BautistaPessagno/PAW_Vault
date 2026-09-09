---
title: "WebConfig"
categories: ["Operations", "Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
tags: ["codemap", "operations"]
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java"]
---

# WebConfig

Spring MVC composition root for scanned controllers, services and JDBC DAOs. Creates a SimpleDriverDataSource, transaction manager, startup schema initializer, JSP resolver, localized validation and mail rendering/sender beans. Adds a taskExecutor with core=2, max=5, queue=50 and CallerRunsPolicy, plus a lazy CommonsMultipartResolver limited to a 6 MiB whole request. Required database.properties and mail.properties remain classpath resources. Static /images resources serve the placeholder; [[ImageController]] serves stored bytes. See [[Startup and dependency injection]].

## Connections

Project types referenced: [[EmailService]], [[ImageService]].

Referenced by: no direct project type reference; implementations may be injected through interfaces.

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java, lines 1–189](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java>)

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
import org.springframework.core.task.TaskExecutor;
import org.springframework.jdbc.datasource.DataSourceTransactionManager;
import org.springframework.jdbc.datasource.SimpleDriverDataSource;
import org.springframework.jdbc.datasource.init.DataSourceInitializer;
import org.springframework.jdbc.datasource.init.ResourceDatabasePopulator;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.JavaMailSenderImpl;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;
import org.springframework.transaction.PlatformTransactionManager;
import org.springframework.transaction.annotation.EnableTransactionManagement;
import org.springframework.validation.Validator;
import org.springframework.validation.beanvalidation.LocalValidatorFactoryBean;
import org.springframework.web.multipart.MultipartResolver;
import org.springframework.web.multipart.commons.CommonsMultipartResolver;
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
import java.util.concurrent.ThreadPoolExecutor;
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

  // Tope del request multipart completo. ImageService rechaza portadas de mas de 5 MB con un
  // mensaje por campo; este margen extra deja pasar el resto del form sin cortar antes.
  private static final long MAX_UPLOAD_SIZE_BYTES = 6L * 1024 * 1024;

  /*
   * Pool para los metodos @Async de EmailService. Sin este bean, @EnableAsync cae al
   * SimpleAsyncTaskExecutor por defecto, que crea un hilo nuevo por cada envio y no lo
   * reusa nunca: bajo carga eso agota los hilos de la maquina.
   *
   * El nombre del bean tiene que ser taskExecutor, que es el que busca Spring por defecto.
   */
  @Bean
  public TaskExecutor taskExecutor() {
    final ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
    executor.setCorePoolSize(2);
    executor.setMaxPoolSize(5);
    executor.setQueueCapacity(50);
    executor.setThreadNamePrefix("mail-");
    // Si la cola se llena, el envio pasa al hilo que llama en vez de descartarse.
    executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
    return executor;
  }

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

  /*
   * servlet-api 2.5 no trae multipart nativo, por eso Commons FileUpload. El nombre del
   * bean es obligatorio: DispatcherServlet lo busca como "multipartResolver".
   */
  @Bean
  public MultipartResolver multipartResolver() {
    final CommonsMultipartResolver multipartResolver = new CommonsMultipartResolver();
    multipartResolver.setMaxUploadSize(MAX_UPLOAD_SIZE_BYTES);
    multipartResolver.setDefaultEncoding(StandardCharsets.UTF_8.name());
    // Sin esto el resolver parsea el request antes de elegir el handler, y un upload
    // demasiado grande termina en un 500 sin pasar por el @ExceptionHandler del controller.
    multipartResolver.setResolveLazily(true);
    return multipartResolver;
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

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
