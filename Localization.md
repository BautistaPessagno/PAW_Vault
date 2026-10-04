---
title: "Localization"
categories: ["Web", "Operations"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["webapp/src/main/resources/i18n/messages.properties", "webapp/src/main/resources/i18n/messages_en.properties", "webapp/src/main/resources/i18n/messages_fr.properties", "webapp/src/main/resources/i18n/messages_es.properties", "webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java", "services/src/main/java/ar/edu/itba/paw/services/SupportedLocales.java", "services/src/main/java/ar/edu/itba/paw/services/EmailServiceImpl.java", "tools/paw_checks.py"]
---

# Localization

> [!summary] En una frase
> La interfaz habla español, inglés y francés según el encabezado `Accept-Language` del navegador; los correos usan el idioma que la cuenta tenía al registrarse, porque se envían fuera del request.

## Herramientas

| Herramienta | Para qué |
|---|---|
| `ReloadableResourceBundleMessageSource` | Leer los bundles `i18n/messages*.properties` en UTF-8 |
| `AcceptHeaderLocaleResolver` | Elegir el idioma de cada request según el navegador; español si no hay encabezado |
| `<spring:message>` | Texto en las JSP (357 usos) |
| `<form:errors>` + `LocalValidatorFactoryBean` | Mensajes de validación desde los mismos bundles |
| `MessageSource.getMessage(key, args, locale)` | Texto desde Java: asuntos de correo, etiquetas de sugerencias |
| Thymeleaf `#{key}` | Texto en las plantillas de correo |
| `tools/paw_checks.py i18n` | Verificar que los tres bundles tengan las mismas keys |

## Los cuatro bundles

| Archivo | Keys | Rol |
|---|---|---|
| `messages.properties` | 494 | Por defecto, en español |
| `messages_en.properties` | 494 | Inglés |
| `messages_fr.properties` | 494 | Francés |
| `messages_es.properties` | 0 | Vacío a propósito |

`messages_es` existe para que un navegador en español encuentre un bundle `es` y no caiga a otro idioma por la cadena de búsqueda; al estar vacío, cada key se resuelve en el bundle por defecto, que ya es español. `setFallbackToSystemLocale(false)` evita que un idioma no soportado termine en el idioma del sistema operativo del servidor en vez del bundle por defecto.

Las keys se agrupan por prefijo: `inquiry.*`, `auth.*`, `profile.*`, `email.*`, `publish.*`, `landing.*`, `post.*`, `cart.*`, `error.*`, `review.*`, y catálogos como `province.*`, `genre.*` y `condition.*` para mostrar enums.

## Cómo se elige el idioma

### En una página

1. `AcceptHeaderLocaleResolver` lee `Accept-Language` y fija el `Locale` del request.
2. `<spring:message code="...">` busca la key en el bundle de ese idioma y, si no está, en el por defecto.
3. Los errores de validación llevan una key (`{auth.password.size}`) y pasan por el mismo `MessageSource`.
4. Los enums se muestran armando la key: `genre.ROCK`, `province.CABA`.

No hay selector de idioma en la interfaz ni se guarda la preferencia en la sesión: manda el navegador.

### En un correo

El correo se arma en un hilo `@Async`, donde no hay request ni `Locale` asociado. Por eso:

1. Al registrarse, [[UserServiceImpl]] guarda en `users.preferred_locale` el idioma del request, normalizado por [[SupportedLocales]] a `es`, `en` o `fr`.
2. Cuando una operación dispara un correo, el service resuelve el `Locale` **antes** de entrar al hilo asíncrono y lo pasa como parámetro.
3. Los correos de la propia cuenta (verificación, recuperación) usan el idioma del request en curso; los avisos a **otra** persona (consulta recibida, cambio de estado, mensaje nuevo) usan el `preferred_locale` del destinatario, que los DAO traen en el mismo `JOIN`.

Detalle en [[Mail delivery]].

## Reglas del proyecto

- Ningún texto visible va literal en una JSP: siempre `<spring:message>`.
- Toda key nueva se agrega en `messages`, `_en` y `_fr` en el mismo cambio.
- Los argumentos van con `{0}`, `{1}`. Las comillas simples se duplican (`''`) en mensajes con argumentos, por las reglas de `MessageFormat`.

Sobre la segunda regla hay dos casos distintos:

- Si la key falta **solo en `_en` o `_fr`**, no hay error: se resuelve en el bundle por defecto y aparece un texto en español en medio de una página en otro idioma.
- Si la key **no está en el bundle por defecto** (por ejemplo, se agregó solo en `_en`), los demás idiomas no la encuentran, Spring lanza `NoSuchMessageException` y la página falla con una `JasperException`.

El chequeo de paridad trata los dos casos como error antes del commit.

## Decisiones y por qué

| Decisión | Motivo | Fuente |
|---|---|---|
| Idioma por `Accept-Language`, sin selector | Seguir la preferencia que el navegador ya declara | `docs/setup.md` |
| Español por defecto, sin caer al idioma del servidor | Comportamiento predecible en cualquier máquina | `docs/setup.md`, [[WebConfig]] |
| `messages_es` vacío | Heredar del bundle por defecto sin duplicar textos | Comentario en `messages.properties`, `CLAUDE.md` del repo |
| Guardar el idioma de la cuenta | El correo sale sin request; hace falta saber en qué idioma escribirle | Comentario en [[SupportedLocales]] |
| Normalizar a tres idiomas antes de guardar | Que un idioma no soportado no llegue a la base ni al correo | Comentario en [[SupportedLocales]] |
| Paridad verificada por script y hook | Las keys faltantes llegaban commiteadas y fallaban en ejecución | `tools/paw_checks.py` |

## Límites conocidos

- `preferred_locale` se fija al registrarse y no se actualiza después: si alguien cambia el idioma de su navegador, los avisos que recibe siguen en el idioma original.
- Los nombres propios (álbum, artista, descripción) no se traducen: son datos cargados por quienes publican.
- Fechas y precios se formatean en las JSP; no hay conversión de moneda.

## Preguntas de defensa

**¿Cómo decide la aplicación en qué idioma responder?**
Por el encabezado `Accept-Language`, con español por defecto.

**¿En qué idioma llega un correo?**
En el del destinatario: el que tenía su navegador al registrarse, guardado en la cuenta. Se resuelve antes de pasar al hilo asíncrono.

**¿Qué pasa si falta una traducción?**
Si falta en inglés o francés, se muestra el texto en español del bundle por defecto. Si falta en el bundle por defecto, la página falla al renderizar. Un chequeo previo al commit exige las mismas keys en los tres bundles para evitar los dos casos.

**¿Por qué hay un `messages_es` vacío?**
Para que el español herede del bundle por defecto sin repetir los textos.

## Evidencia de código

### Bundles y resolución del idioma

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java>), líneas 138–143.

```java
  @Bean
  public LocaleResolver localeResolver() {
    final AcceptHeaderLocaleResolver localeResolver = new AcceptHeaderLocaleResolver();
    localeResolver.setDefaultLocale(Locale.forLanguageTag("es"));
    return localeResolver;
  }
```

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java>), líneas 177–184.

```java
  @Bean
  public MessageSource messageSource() {
    final ReloadableResourceBundleMessageSource messageSource = new ReloadableResourceBundleMessageSource();
    messageSource.setBasename("classpath:i18n/messages");
    messageSource.setDefaultEncoding(StandardCharsets.UTF_8.name());
    messageSource.setFallbackToSystemLocale(false);
    return messageSource;
  }
```

### Idiomas soportados

Fuente exacta en `8929aea`: [services/src/main/java/ar/edu/itba/paw/services/SupportedLocales.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/SupportedLocales.java>), líneas 1–35.

```java
package ar.edu.itba.paw.services;

import java.util.List;
import java.util.Locale;

/*
 * Idiomas que la aplicacion sabe hablar, los mismos que tienen bundle de i18n. Los services
 * normalizan contra esta lista antes de tocar la base, asi un idioma que no soportamos nunca
 * llega a users.preferred_locale ni al mail.
 */
final class SupportedLocales {

    private static final String DEFAULT_LANGUAGE = "es";

    private static final List<String> SUPPORTED_LANGUAGES = List.of(DEFAULT_LANGUAGE, "en", "fr");

    private SupportedLocales() {
        // Clase de utilidad.
    }

    // Idioma persistible: lo que guarda users.preferred_locale.
    static String languageOf(final Locale locale) {
        if (locale == null) {
            return DEFAULT_LANGUAGE;
        }
        final String language = locale.getLanguage();
        return SUPPORTED_LANGUAGES.contains(language) ? language : DEFAULT_LANGUAGE;
    }

    // Locale con el que se resuelven los bundles, a partir de lo guardado en la base.
    static Locale localeOf(final String languageTag) {
        final Locale locale = languageTag == null ? null : Locale.forLanguageTag(languageTag);
        return Locale.forLanguageTag(languageOf(locale));
    }
}
```

### Chequeo de paridad

Fuente exacta en `8929aea`: [tools/paw_checks.py](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/tools/paw_checks.py>), líneas 56–79.

```python
def check_i18n():
    """Paridad de bundles. Regla del equipo (CLAUDE.md): messages.properties es el
    default (es); _en y _fr deben tener TODAS sus keys; _es puede estar vacío (hereda).
    Una key presente solo en un bundle hijo tampoco sirve: los demás locales caen al default
    y no la encuentran → JasperException."""
    errors = []
    default = parse_properties_keys(I18N_DIR / "messages.properties")
    if not default:
        return ["i18n: no pude leer keys de messages.properties (¿path correcto? %s)" % I18N_DIR]
    for loc in ("en", "fr"):
        missing = default - parse_properties_keys(I18N_DIR / f"messages_{loc}.properties")
        if missing:
            listed = ", ".join(sorted(missing)[:MAX_LISTED_KEYS])
            extra = "" if len(missing) <= MAX_LISTED_KEYS else f" (+{len(missing) - MAX_LISTED_KEYS} más)"
            errors.append(f"i18n: messages_{loc}.properties — faltan {len(missing)} keys: {listed}{extra}")
    for loc in ("es", "en", "fr"):
        orphans = parse_properties_keys(I18N_DIR / f"messages_{loc}.properties") - default
        if orphans:
            listed = ", ".join(sorted(orphans)[:MAX_LISTED_KEYS])
            errors.append(
                f"i18n: messages_{loc}.properties — {len(orphans)} keys huérfanas (no están en el "
                f"default, los otros locales las resuelven a missing): {listed}"
            )
    return errors
```

## Archivos para seguir el flujo

- [webapp/src/main/resources/i18n/messages.properties](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/resources/i18n/messages.properties>)
- [webapp/src/main/resources/i18n/messages_en.properties](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/resources/i18n/messages_en.properties>)
- [webapp/src/main/resources/i18n/messages_fr.properties](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/resources/i18n/messages_fr.properties>)
- [webapp/src/main/resources/i18n/messages_es.properties](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/resources/i18n/messages_es.properties>)
- [webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java>) · [[WebConfig]]
- [services/src/main/java/ar/edu/itba/paw/services/SupportedLocales.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/SupportedLocales.java>) · [[SupportedLocales]]
- [services/src/main/java/ar/edu/itba/paw/services/EmailServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/EmailServiceImpl.java>) · [[EmailServiceImpl]]
- [tools/paw_checks.py](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/tools/paw_checks.py>)

Fuente inspeccionada: `8929aea`, 2026-10-04. Es evidencia estática; no implica ejecución de la aplicación. [[Source inventory]] · [[Roadmap de lectura]]
