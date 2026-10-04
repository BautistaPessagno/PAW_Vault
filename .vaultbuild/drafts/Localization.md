@title: Localization
@categories: Web, Operations
@files: webapp/src/main/resources/i18n/messages.properties, webapp/src/main/resources/i18n/messages_en.properties, webapp/src/main/resources/i18n/messages_fr.properties, webapp/src/main/resources/i18n/messages_es.properties, webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java, services/src/main/java/ar/edu/itba/paw/services/SupportedLocales.java, services/src/main/java/ar/edu/itba/paw/services/EmailServiceImpl.java, tools/paw_checks.py

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

{{code:webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java:138-143}}

{{code:webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java:177-184}}

### Idiomas soportados

{{file:services/src/main/java/ar/edu/itba/paw/services/SupportedLocales.java}}

### Chequeo de paridad

{{code:tools/paw_checks.py:56-79}}
