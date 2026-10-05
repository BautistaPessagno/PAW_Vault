---
title: "WebConfig"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java"]
---

# WebConfig

Configuración de Spring: escaneo de componentes, `DataSource`, transacciones, Flyway al arrancar, resolver multipart, vistas JSP, `Locale`, i18n, validador, JavaMail, Thymeleaf para correos y el pool de hilos de `@Async`. Ver [[Startup and dependency injection]].

## Guía de lectura

Datos y dependencias declaradas: `LOGGER`, `SMTP_PROTOCOL`.

Operaciones para localizar en la fuente: `taskExecutor`, `dataSource`, `transactionManager`, `flyway`, `multipartResolver`, `viewResolver`, `localeResolver`, `mailSender`, `mailTemplateEngine`, `messageSource`, `validator`, `getValidator`, `addResourceHandlers`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[ImageRules]], [[SecurityConfig]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java>), líneas 1–204.

```java
package ar.edu.itba.paw.webapp.config;

import ar.edu.itba.paw.models.ImageRules;
import org.flywaydb.core.Flyway;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.context.MessageSource;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.PropertySource;
import org.springframework.context.annotation.Import;
import org.springframework.context.support.ReloadableResourceBundleMessageSource;
import org.springframework.core.env.Environment;
import org.springframework.core.task.TaskExecutor;
import org.springframework.jdbc.datasource.DataSourceTransactionManager;
import org.springframework.jdbc.datasource.DriverManagerDataSource;
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
import org.springframework.web.servlet.LocaleResolver;
import org.springframework.web.servlet.ViewResolver;
import org.springframework.web.servlet.config.annotation.EnableWebMvc;
import org.springframework.web.servlet.config.annotation.ResourceHandlerRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;
import org.springframework.web.servlet.i18n.AcceptHeaderLocaleResolver;
import org.springframework.web.servlet.view.InternalResourceViewResolver;
import org.springframework.web.servlet.view.JstlView;
import org.thymeleaf.spring5.SpringTemplateEngine;
import org.thymeleaf.templatemode.TemplateMode;
import org.thymeleaf.templateresolver.ClassLoaderTemplateResolver;

import javax.sql.DataSource;
import java.nio.charset.StandardCharsets;
import java.util.Locale;
import java.util.Properties;

@EnableWebMvc
@EnableTransactionManagement
@EnableAsync
@Import(SecurityConfig.class)
@ComponentScan({ "ar.edu.itba.paw.persistence", "ar.edu.itba.paw.webapp.controller", "ar.edu.itba.paw.services" })
@PropertySource(value = "classpath:database.properties", ignoreResourceNotFound = true)
@PropertySource(value = "classpath:mail.properties", ignoreResourceNotFound = true)
@Configuration
public class WebConfig implements WebMvcConfigurer {

  private static final Logger LOGGER = LoggerFactory.getLogger(WebConfig.class);

  private static final String SMTP_PROTOCOL = "smtp";

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
    // Un SMTP lento nunca debe trasladarse al hilo del request. Si el pool se satura,
    // el rechazo queda visible en logs y se descarta solamente ese aviso no critico.
    executor.setRejectedExecutionHandler((task, poolExecutor) ->
        LOGGER.warn("Mail task rejected: taskExecutor saturated, dropping email task"));
    executor.setWaitForTasksToCompleteOnShutdown(true);
    executor.setAwaitTerminationSeconds(30);
    return executor;
  }

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

  /*
   * Se conserva Commons FileUpload como resolver multipart de esta entrega. El nombre
   * del bean es obligatorio: DispatcherServlet lo busca como "multipartResolver".
   */
  @Bean
  public MultipartResolver multipartResolver() {
    final CommonsMultipartResolver multipartResolver = new CommonsMultipartResolver();
    multipartResolver.setMaxUploadSize(ImageRules.MAX_MULTIPART_BYTES);
    multipartResolver.setDefaultEncoding(StandardCharsets.UTF_8.name());
    // El filtro multipart externo traduce el limite excedido antes de entrar al controller.
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
  public LocaleResolver localeResolver() {
    final AcceptHeaderLocaleResolver localeResolver = new AcceptHeaderLocaleResolver();
    localeResolver.setDefaultLocale(Locale.forLanguageTag("es"));
    return localeResolver;
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
