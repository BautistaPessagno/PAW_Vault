---
title: "Localization"
categories: ["Web"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "041ce34404963b689d05443ca00abb7e75aa7f15"
status: "documented"
tags: ["codemap", "web"]
sources: ["webapp/src/main/resources/i18n/messages.properties", "webapp/src/main/resources/i18n/messages_en.properties", "webapp/src/main/resources/i18n/messages_es.properties", "webapp/src/main/resources/i18n/messages_fr.properties"]
---

# Localization

[[WebConfig]] creates a UTF-8 ReloadableResourceBundleMessageSource at `classpath:i18n/messages`. JSP spring:message, validation messages and Thymeleaf mail messages share it. Request Locale follows the MVC request locale behavior; no application locale-switch controller or custom LocaleResolver is declared.

| File | Role |
|---|---|
| messages.properties | Spanish default text |
| messages_es.properties | Spanish overrides for publishing, contact and email; remaining keys inherit default |
| messages_en.properties | English translations |
| messages_fr.properties | French translations |

The project check requires every default key in English and French and rejects keys defined only in a locale override. It permits an empty Spanish override. Passing key parity does not prove translation quality or that every literal UI string is localized. Legacy user JSPs contain literal English.

Publishing and contact field annotations use `{message.key}` syntax. The year conversion error uses `typeMismatch.publishForm.releaseYear`. Welcome subject/body use caller Locale; contact mail fixes Spanish independently of browser language.

## Exact default message catalog

[webapp/src/main/resources/i18n/messages.properties, lines 1–54](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/resources/i18n/messages.properties>)

```properties
# Default bundle — español. messages_es hereda de este (ver CLAUDE.md).
landing.pageTitle=quieroVinilos
landing.heading=quieroVinilos
vinylCard.cover.alt=Portada de {0}
landing.empty=Todavia no hay vinilos publicados. Se el primero en publicar uno.
landing.publish=Publicar un álbum
publish.pageTitle=Publicar álbum | quieroVinilos
publish.heading=Publicar un álbum
publish.username.label=Nombre de usuario
publish.publisherEmail.label=Email
publish.title.label=Título
publish.artistName.label=Artista
publish.releaseYear.label=Año
publish.submit=Publicar
publish.back=Volver al catálogo
publish.username.required=El nombre de usuario es obligatorio.
publish.username.size=El nombre de usuario no puede superar los 100 caracteres.
publish.publisherEmail.required=El email es obligatorio.
publish.publisherEmail.invalid=Ingresá un email válido.
publish.publisherEmail.size=El email no puede superar los 100 caracteres.
publish.concurrent=Hubo un conflicto momentáneo al publicar. Probá de nuevo.
publish.duplicate=Ya publicaste este álbum.
publish.title.required=El título es obligatorio.
publish.title.size=El título no puede superar los 255 caracteres.
publish.artistName.required=El artista es obligatorio.
publish.artistName.size=El artista no puede superar los 255 caracteres.
publish.releaseYear.required=El año es obligatorio.
publish.releaseYear.range=El año debe estar entre 1000 y 9999.
typeMismatch.publishForm.releaseYear=El año debe ser un número entero.

landing.contact.sent=Listo: le avisamos al publicante que te interesa su álbum.
post.contact.action=Me interesa comprarlo
post.contact.pageTitle=Contactar al publicante | quieroVinilos
post.contact.heading=Me interesa comprarlo
post.contact.name.label=Tu nombre
post.contact.email.label=Tu email
post.contact.submit=Enviar consulta
post.contact.back=Volver al catálogo
post.contact.deliveryFailed=No pudimos enviar tu consulta en este momento. Probá de nuevo en unos minutos.
post.contact.name.required=El nombre es obligatorio.
post.contact.name.size=El nombre no puede superar los 100 caracteres.
post.contact.email.required=El email es obligatorio.
post.contact.email.invalid=Ingresá un email válido.
post.contact.email.size=El email no puede superar los 100 caracteres.

email.welcome.subject=Bienvenido a quieroVinilos
email.welcome.body=Hola {0}, gracias por registrarte.
email.postInterest.subject=Alguien está interesado en {0}
email.postInterest.heading=Hay interés en tu publicación
email.postInterest.intro={0} está interesado en tu publicación.
email.postInterest.contact=Contacto:
email.postInterest.album=Álbum:

vinylCard.year=Año
```

## Other bundles

- [messages_en.properties](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/resources/i18n/messages_en.properties>)
- [messages_es.properties](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/resources/i18n/messages_es.properties>)
- [messages_fr.properties](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/resources/i18n/messages_fr.properties>)

[[Views and assets]] · [[Validation and errors]] · [[Development tools]]

## Committed UI messages

The UI merge renames landing.cover.alt to vinylCard.cover.alt and adds vinylCard.year in default, English and French. publish.back is present in all four bundles. [[UI components]] uses the cover and year keys; [[Publish flow]] uses the return label. wishlist.add from the earlier working-tree snapshot is absent. The Spanish override is not empty; it defines publishing, contact and email text, inheriting missing keys such as vinylCard.cover.alt and vinylCard.year from the default bundle.
