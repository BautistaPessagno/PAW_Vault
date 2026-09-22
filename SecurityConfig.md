---
title: "SecurityConfig"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/config/SecurityConfig.java"]
---

# SecurityConfig

Configures Spring Security route access, email/password form login, logout and the access-denied page. /admin/** requires ADMIN; /publish/**, /post/*/edit, /post/*/delete, /profile/**, /post/*/contact and /inquiries/** require authentication. Everything else, including /post/{id}, password recovery and suggestion fragments, is public. CSRF remains enabled. BCrypt strength is 12, and the PasswordHasher bean exposes both hash and matches.

## Connections

Project types referenced: [[AuthenticatedUserDetailsService]], [[PasswordHasher]], [[UserService]].

Referenced by: [[WebConfig]].

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/config/SecurityConfig.java, lines 1–78](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/config/SecurityConfig.java>)

```java
package ar.edu.itba.paw.webapp.config;

import ar.edu.itba.paw.services.PasswordHasher;
import ar.edu.itba.paw.services.UserService;
import ar.edu.itba.paw.webapp.security.AuthenticatedUserDetailsService;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
@EnableWebSecurity
public class SecurityConfig {

    // Costo 12: es el que ya tienen los hashes guardados, subirlo los invalidaria.
    private static final int BCRYPT_STRENGTH = 12;

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder(BCRYPT_STRENGTH);
    }

    /*
     * Los services hashean la clave elegida al verificar el correo, pero no pueden
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

    @Bean
    public SecurityFilterChain securityFilterChain(final HttpSecurity http) throws Exception {
        http
                .authorizeHttpRequests(authorize -> authorize
                        .antMatchers("/admin/**").hasRole("ADMIN")
                        .antMatchers("/publish/**").authenticated()
                        .antMatchers("/post/*/edit", "/post/*/delete").authenticated()
                        .antMatchers("/profile/**").authenticated()
                        .antMatchers("/post/*/contact").authenticated()
                        .antMatchers("/inquiries/**").authenticated()
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
                .exceptionHandling(exceptions -> exceptions.accessDeniedPage("/error/403"));
        return http.build();
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
