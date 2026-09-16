---
title: "Localization"
categories: ["Web"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["webapp/src/main/resources/i18n/messages.properties", "webapp/src/main/resources/i18n/messages_en.properties", "webapp/src/main/resources/i18n/messages_es.properties", "webapp/src/main/resources/i18n/messages_fr.properties"]
---

# Localization

WebConfig configures AcceptHeaderLocaleResolver with Spanish default. The shared UTF-8 message source uses classpath:i18n/messages and disables fallback to the machine locale. JSP text, Bean Validation and Thymeleaf messages share these bundles.

| Bundle | Role |
|---|---|
| messages.properties | Full Spanish default |
| messages_es.properties | Empty override, inherits the default |
| messages_en.properties | English |
| messages_fr.properties | French |

The bundles now include authentication, verification, inquiries, sale states, commercial details, search/filter/sort choices and 400/403/404/409 pages. Default keys must exist in English/French; the checker permits an empty Spanish override. Key parity does not establish translation quality.

Registration saves a supported language code using SupportedLocales, falling back to es for unsupported/null input. Interest mail uses the seller's saved language. Verification/welcome use their caller's request Locale. There is no UI locale switch route or profile preference editor.

## Exact default catalog

[webapp/src/main/resources/i18n/messages.properties, lines 1–203](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/resources/i18n/messages.properties>)

```properties
# Default bundle — español. messages_es hereda de este (ver CLAUDE.md).
landing.pageTitle=quieroVinilos
landing.heading=quieroVinilos
vinylCard.cover.alt=Portada de {0}
landing.empty=Todavía no hay vinilos publicados. Sé el primero en publicar uno.
landing.publish=Publicar un álbum
landing.search.label=Buscar
landing.search.placeholder=Álbum o artista
landing.search.submit=Buscar
landing.search.clear=Ver todos
landing.search.results=Resultados para "{0}"
landing.search.empty=No encontramos vinilos para "{0}". Probá con otro álbum o artista.
landing.sort.label=Ordenar por
landing.filter.genre=Género
landing.filter.condition=Condición
landing.filter.artist=Artista
landing.filter.year=Año
landing.filter.minPrice=Precio mínimo
landing.filter.maxPrice=Precio máximo
landing.filter.any=Cualquiera
landing.filter.empty=No encontramos vinilos con esos filtros. Probá con otra combinación.
landing.sort.NEWEST=Más recientes
landing.sort.OLDEST=Más antiguas
landing.sort.PRICE_ASC=Precio: menor a mayor
landing.sort.PRICE_DESC=Precio: mayor a menor
landing.sort.TITLE_ASC=Álbum: A a Z
landing.sort.TITLE_DESC=Álbum: Z a A
landing.sort.ARTIST_ASC=Artista: A a Z
landing.sort.ARTIST_DESC=Artista: Z a A
landing.sort.RELEASE_YEAR_DESC=Año de lanzamiento: más nuevo
landing.sort.RELEASE_YEAR_ASC=Año de lanzamiento: más viejo
publish.pageTitle=Publicar álbum | quieroVinilos
publish.heading=Publicar un álbum
publish.title.label=Título
publish.artistName.label=Artista
publish.releaseYear.label=Año
publish.submit=Publicar
publish.back=Volver al catálogo
publish.concurrent=Hubo un conflicto momentáneo al publicar. Probá de nuevo.
publish.duplicate=Ya publicaste este álbum.
publish.title.required=El título es obligatorio.
publish.title.size=El título no puede superar los 255 caracteres.
publish.artistName.required=El artista es obligatorio.
publish.artistName.size=El artista no puede superar los 255 caracteres.
publish.releaseYear.required=El año es obligatorio.
publish.releaseYear.range=El año debe estar entre 1000 y 9999.
publish.cover.label=Portada (opcional)
publish.cover.hint=PNG, JPEG o WebP de hasta 5 MB.
publish.cover.invalid=La portada tiene que ser una imagen PNG, JPEG o WebP de hasta 5 MB.
publish.cover.tooLarge=El archivo supera el tamaño máximo. Elegí una portada de hasta 5 MB.
typeMismatch.publishForm.releaseYear=El año debe ser un número entero.

landing.contact.sent=Listo: le avisamos al publicante que te interesa su álbum.
post.contact.action=Me interesa comprarlo
post.contact.pageTitle=Contactar al publicante | quieroVinilos
post.contact.heading=Me interesa comprarlo
post.contact.message.label=Mensaje para quien publica (opcional)
post.contact.submit=Enviar consulta
post.contact.back=Volver al catálogo
post.contact.message.size=El mensaje no puede superar los 500 caracteres.

email.welcome.subject=Bienvenido a quieroVinilos
email.welcome.body=Hola {0}, gracias por registrarte.
email.welcome.cta=Ver quieroVinilos
email.postInterest.subject=Alguien está interesado en {0}
email.postInterest.heading=Hay interés en tu publicación
email.postInterest.intro={0} está interesado en tu publicación.
email.postInterest.contact=Contacto:
email.postInterest.album=Álbum:
email.postInterest.message=Mensaje:
email.postInterest.cta=Ver quieroVinilos

vinylCard.year=Año
vinylCard.price=Precio
vinylCard.price.format=$ {0,number,integer}
vinylCard.price.unavailable=Consultar
vinylCard.condition=Condición
vinylCard.zone=Zona
vinylCard.genre=Género
vinylCard.pressingYear=Prensada
vinylCard.open=Ver {0}

publish.genre.label=Género (opcional)
publish.genre.empty=Sin especificar
publish.price.label=Precio en pesos
publish.price.required=El precio es obligatorio.
publish.price.range=El precio debe ser un entero entre 1 y 99.999.999.
publish.condition.label=Condición (opcional)
publish.condition.empty=Sin especificar
publish.zone.label=Zona (opcional)
publish.zone.size=La zona no puede superar los 100 caracteres.
publish.pressingYear.label=Año de la prensada (opcional)
publish.pressingYear.range=El año de la prensada debe estar entre 1000 y 9999.
publish.description.label=Descripción (opcional)
publish.description.size=La descripción no puede superar los 1000 caracteres.
typeMismatch.publishForm.price=El precio debe ser un número entero.
typeMismatch.publishForm.pressingYear=El año de la prensada debe ser un número entero.
typeMismatch.publishForm.genre=Elegí un género de la lista.
typeMismatch.publishForm.condition=Elegí una condición de la lista.

condition.NEW=Nuevo
condition.USED=Usado

genre.ROCK=Rock
genre.POP=Pop
genre.JAZZ=Jazz
genre.BLUES=Blues
genre.SOUL_FUNK=Soul / Funk
genre.HIP_HOP=Hip hop
genre.ELECTRONIC=Electrónica
genre.CLASSICAL=Clásica
genre.TANGO=Tango
genre.FOLKLORE=Folklore
genre.CUMBIA=Cumbia
genre.REGGAE=Reggae
genre.METAL=Metal
genre.PUNK=Punk
genre.OTHER=Otro

error.notFound.pageTitle=Página no encontrada | quieroVinilos
error.notFound.code=404
error.notFound.heading=Esta página no está en el catálogo
error.notFound.message=El enlace que seguiste no existe, o el álbum que buscabas ya no está publicado.
error.notFound.back=Volver al catálogo
error.notFound.publish=Publicar un álbum

error.badRequest.pageTitle=Búsqueda inválida | quieroVinilos
error.badRequest.code=400
error.badRequest.heading=Esa búsqueda es demasiado larga
error.badRequest.message=El texto que buscás no puede superar los 255 caracteres. Probá con el nombre del álbum o del artista.
error.badRequest.back=Volver al catálogo
auth.navigation.label=Cuenta
auth.login.action=Iniciar sesión
auth.register.action=Crear cuenta
auth.logout.action=Cerrar sesión
auth.admin.action=Administración
auth.username.label=Nombre de usuario
auth.email.label=Correo electrónico
auth.password.label=Contraseña
auth.passwordConfirmation.label=Repetir contraseña
auth.login.pageTitle=Iniciar sesión | quieroVinilos
auth.login.heading=Iniciar sesión
auth.login.submit=Entrar
auth.login.invalid=El correo o la contraseña son incorrectos.
auth.login.loggedOut=Cerraste la sesión correctamente.
auth.login.verificationSent=Te enviamos un enlace para confirmar tu correo y activar la cuenta.
auth.login.verified=Tu correo fue confirmado. Ya podés iniciar sesión.
auth.register.pageTitle=Crear cuenta | quieroVinilos
auth.register.heading=Crear cuenta
auth.register.submit=Registrarme
auth.register.verification.hint=Te enviaremos un enlace para que elijas tu nombre de usuario y contraseña después de confirmar el correo.
auth.register.username.required=El nombre de usuario es obligatorio.
auth.register.username.size=El nombre de usuario no puede superar los 100 caracteres.
auth.register.email.required=El correo electrónico es obligatorio.
auth.register.email.invalid=Ingresá un correo electrónico válido.
auth.register.email.size=El correo electrónico no puede superar los 100 caracteres.
auth.register.email.duplicate=Ya existe una cuenta con ese correo electrónico.
auth.register.password.required=La contraseña es obligatoria.
auth.register.password.size=La contraseña debe tener entre 12 y 72 caracteres.
auth.register.password.letter=La contraseña debe incluir una letra.
auth.register.password.number=La contraseña debe incluir un número.
auth.register.password.mismatch=Las contraseñas no coinciden.
auth.register.password.hint=Usá entre 12 y 72 caracteres, con al menos una letra y un número.
auth.verify.pageTitle=Verificar correo | quieroVinilos
auth.verify.heading=Confirmá tu correo
auth.verify.hint=Elegí tu nombre de usuario y contraseña para completar la verificación.
auth.verify.submit=Verificar cuenta
auth.verify.invalid=El enlace venció o ya fue utilizado.
auth.verify.token.required=Falta el token de verificación.
auth.admin.pageTitle=Administración | quieroVinilos
auth.admin.heading=Administración
auth.admin.message=Esta sección está disponible únicamente para administradores.
email.verification.subject=Confirmá tu correo en quieroVinilos
email.verification.body=Confirmá tu correo para elegir tus credenciales y activar tu cuenta.
email.verification.cta=Confirmar correo
post.contact.identity=La consulta se enviará con el nombre y el correo de tu cuenta.
inquiry.navigation=Mis consultas
inquiry.pageTitle=Mis consultas | quieroVinilos
inquiry.heading=Mis consultas
inquiry.received.heading=Consultas recibidas
inquiry.received.empty=Todavía no recibiste consultas.
inquiry.sent.heading=Consultas enviadas
inquiry.sent.empty=Todavía no enviaste consultas.
inquiry.from=De: {0}
inquiry.to=Para: {0}
inquiry.item.title={0} — {1}
inquiry.accept=Aceptar y vender
inquiry.reject=Rechazar
inquiry.accepted=La consulta fue aceptada y la publicación quedó vendida.
inquiry.rejected=La consulta fue rechazada.
inquiry.status.PENDING=Pendiente
inquiry.status.ACCEPTED=Aceptada
inquiry.status.REJECTED=Rechazada
error.conflict.pageTitle=El estado cambió | quieroVinilos
error.conflict.code=409
error.conflict.heading=La publicación ya cambió de estado
error.conflict.message=Otra acción cambió la publicación o la consulta. Buscá otro ejemplar en el catálogo.
error.conflict.back=Volver al catálogo
error.forbidden.pageTitle=Acceso denegado | quieroVinilos
error.forbidden.code=403
error.forbidden.heading=No tenés permiso para entrar acá
error.forbidden.message=Tu cuenta está autenticada, pero no tiene el permiso necesario para esta acción.
error.forbidden.back=Volver al catálogo
```

- [messages_en.properties](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/resources/i18n/messages_en.properties>)
- [messages_es.properties](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/resources/i18n/messages_es.properties>)
- [messages_fr.properties](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/resources/i18n/messages_fr.properties>)

[[SupportedLocales]] · [[Mail delivery]] · [[Validation and errors]]
