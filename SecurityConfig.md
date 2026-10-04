---
title: "SecurityConfig"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/config/SecurityConfig.java"]
---

# SecurityConfig

Configuración de Spring Security: BCrypt 12 y su adaptador `PasswordHasher`, beans de pertenencia para `@PreAuthorize`, la lista única de rutas de Cuenta verificada, form login por correo, logout, registro de sesiones y el handler que distingue "verificá tu correo" de 403. Ver [[Security and authorization]].

## Guía de lectura

Datos y dependencias declaradas: `BCRYPT_STRENGTH`, `VERIFIED_PATHS`.

Operaciones para localizar en la fuente: `passwordEncoder`, `passwordHasher`, `hash`, `matches`, `userDetailsService`, `addressAccess`, `inquiryAccess`, `postAccess`, `sessionRegistry`, `securityFilterChain`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[AddressAccessHandler]], [[AddressService]], [[AuthenticatedUser]], [[AuthenticatedUserDetailsService]], [[InquiryAccessHandler]], [[InquiryService]], [[PasswordHasher]], [[PostAccessHandler]], [[PostService]], [[UserService]], [[VerificationAccessDeniedHandler]].

Referenciado por: [[WebConfig]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/config/SecurityConfig.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/config/SecurityConfig.java>), líneas 1–153.

```java
package ar.edu.itba.paw.webapp.config;

import ar.edu.itba.paw.services.AddressService;
import ar.edu.itba.paw.services.InquiryService;
import ar.edu.itba.paw.services.PasswordHasher;
import ar.edu.itba.paw.services.PostService;
import ar.edu.itba.paw.services.UserService;
import ar.edu.itba.paw.webapp.security.AddressAccessHandler;
import ar.edu.itba.paw.webapp.security.AuthenticatedUser;
import ar.edu.itba.paw.webapp.security.AuthenticatedUserDetailsService;
import ar.edu.itba.paw.webapp.security.InquiryAccessHandler;
import ar.edu.itba.paw.webapp.security.PostAccessHandler;
import ar.edu.itba.paw.webapp.security.VerificationAccessDeniedHandler;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.core.session.SessionRegistry;
import org.springframework.security.core.session.SessionRegistryImpl;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.util.matcher.AntPathRequestMatcher;
import org.springframework.security.web.util.matcher.OrRequestMatcher;
import org.springframework.security.web.util.matcher.RequestMatcher;

@Configuration
@EnableWebSecurity
@EnableMethodSecurity
public class SecurityConfig {

    // Costo 12: es el que ya tienen los hashes guardados, subirlo los invalidaria.
    private static final int BCRYPT_STRENGTH = 12;

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder(BCRYPT_STRENGTH);
    }

    /*
     * Los services hashean la clave elegida al registrarse, pero no pueden
     * depender de spring-security: el modulo services no la tiene en su classpath. Este
     * bean adapta el encoder a la interfaz PasswordHasher de services-contracts.
     */
    @Bean
    public PasswordHasher passwordHasher(final PasswordEncoder passwordEncoder) {
        return new PasswordHasher() {
            @Override
            public String hash(final String rawPassword) {
                return passwordEncoder.encode(rawPassword);
            }

            @Override
            public boolean matches(final String rawPassword, final String passwordHash) {
                return passwordEncoder.matches(rawPassword, passwordHash);
            }
        };
    }

    @Bean
    public UserDetailsService userDetailsService(final UserService userService) {
        return new AuthenticatedUserDetailsService(userService);
    }

    // El nombre del bean es el que usan las expresiones: @addressAccess.isOwner(...).
    @Bean
    public AddressAccessHandler addressAccess(final AddressService addressService) {
        return new AddressAccessHandler(addressService);
    }

    // @inquiryAccess.isBuyer / isSeller / isParty: la pertenencia de cada endpoint de la Venta.
    @Bean
    public InquiryAccessHandler inquiryAccess(final InquiryService inquiryService) {
        return new InquiryAccessHandler(inquiryService);
    }

    // @postAccess.isPublisher: junto con hasRole('ADMIN'), quien edita o elimina una publicacion.
    @Bean
    public PostAccessHandler postAccess(final PostService postService) {
        return new PostAccessHandler(postService);
    }

    /*
     * Regla por capa: aca se decide quien puede entrar a cada URL (anonimo, cuenta con sesion o
     * cuenta verificada). Quien puede operar sobre un recurso ajeno lo decide un @PreAuthorize en
     * el controller: @postAccess (Publicante o administrador) para editar y eliminar un Post, y
     * @inquiryAccess y @addressAccess para la Venta y la libreta. Los services vuelven a chequear la
     * pertenencia de la Venta y de la libreta antes de escribir, y responden 403 o 404.
     *
     * Las rutas de cuenta verificada se definen una sola vez: las usan la regla de acceso y el
     * AccessDeniedHandler que manda a la pagina de "verifica tu correo".
     *
     * El perfil y las bandejas de consultas tambien piden la cuenta verificada: cualquiera puede
     * registrar un correo ajeno, y esa sesion no tiene que ver los datos de cobro, las
     * direcciones ni las consultas que el dueno real del correo cargue despues.
     */
    private static final RequestMatcher VERIFIED_PATHS = new OrRequestMatcher(
            new AntPathRequestMatcher("/publish/**"),
            new AntPathRequestMatcher("/post/*/edit"),
            new AntPathRequestMatcher("/post/*/delete"),
            new AntPathRequestMatcher("/post/*/contact"),
            new AntPathRequestMatcher("/cart"),
            new AntPathRequestMatcher("/cart/**"),
            new AntPathRequestMatcher("/profile/**"),
            new AntPathRequestMatcher("/inquiries"),
            new AntPathRequestMatcher("/inquiries/sent"),
            // Toda accion sobre una consulta: aceptar, rechazar y las que se sumen despues.
            new AntPathRequestMatcher("/inquiries/{inquiryId:[0-9]+}/**"));

    private static final String FORBIDDEN_PAGE = "/error/403";

    /*
     * Lleva la cuenta de las sesiones abiertas de cada usuario para poder cerrarlas cuando
     * cambia la clave. HttpSessionEventPublisher (web.xml) le avisa cuando una sesion muere o
     * cambia de id.
     */
    @Bean
    public SessionRegistry sessionRegistry() {
        return new SessionRegistryImpl();
    }

    @Bean
    public SecurityFilterChain securityFilterChain(final HttpSecurity http, final SessionRegistry sessionRegistry)
            throws Exception {
        http
                .authorizeHttpRequests(authorize -> authorize
                        .requestMatchers(VERIFIED_PATHS).hasAuthority(AuthenticatedUser.VERIFIED)
                        .antMatchers("/verify/resend", "/verify/required").authenticated()
                        .anyRequest().permitAll())
                .formLogin(login -> login
                        .loginPage("/login")
                        .usernameParameter("email")
                        .passwordParameter("password")
                        .defaultSuccessUrl("/", false)
                        .failureUrl("/login?error")
                        .permitAll())
                .logout(logout -> logout
                        .logoutUrl("/logout")
                        .logoutSuccessUrl("/login?logout")
                        .invalidateHttpSession(true)
                        .deleteCookies("JSESSIONID"))
                // Sin limite de sesiones por cuenta: el registro solo sirve para expirarlas.
                .sessionManagement(session -> session
                        .maximumSessions(-1)
                        .sessionRegistry(sessionRegistry)
                        .expiredUrl("/login?sessionExpired"))
                .exceptionHandling(exceptions -> exceptions.accessDeniedHandler(
                        new VerificationAccessDeniedHandler(VERIFIED_PATHS, FORBIDDEN_PAGE)));
        return http.build();
    }
}
```
