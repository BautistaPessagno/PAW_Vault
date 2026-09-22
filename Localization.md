---
title: "Localization"
categories: ["Web"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
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

Since `40328f0` the bundles gained keys for the post detail page, edit/delete actions and confirmations, publish/edit notices and preview, the profile page, password change and recovery, the split inbox with tabs, pagination labels, inquiry status labels, search suggestion types, and three new emails (inquiry accepted, password changed, password reset). Password validation messages moved from `auth.register.password.*` to shared `auth.password.*` keys used by [[ValidPassword]] and [[MatchingPasswords]]. Default keys must exist in English and French; the checker permits the empty Spanish override. Key parity does not establish translation quality.

Registration saves a supported language code using SupportedLocales, falling back to es for unsupported or null input. Interest mail uses the seller's saved language and acceptance mail the buyer's. Verification, welcome, password-changed and reset emails use the requesting browser's Locale. There is still no UI locale switch or profile language editor.

## Exact default catalog

[webapp/src/main/resources/i18n/messages.properties, lines 1–287](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/resources/i18n/messages.properties>)

```properties
# Default bundle — español. messages_es hereda de este (ver CLAUDE.md).
landing.pageTitle=quieroVinilos
landing.heading=quieroVinilos
vinylCard.cover.alt=Portada de {0}
landing.empty=Todavía no hay vinilos publicados. Sé el primero en publicar uno.
landing.publish=Publicar un vinilo
landing.search.label=Buscar
landing.search.placeholder=Álbum o artista
landing.search.submit=Buscar
landing.search.clear=Quitar filtros
landing.search.results=Resultados para "{0}"
landing.search.empty.heading=Este lado del disco está vacío
landing.search.empty=No encontramos "{0}" en el catálogo. Dalo vuelta y probá con otra búsqueda.
landing.results.count={0,choice,0#Sin vinilos|1#Mostrando 1 vinilo|1<Mostrando {0} vinilos}
landing.pagination=Páginas del catálogo
landing.sort.label=Ordenar por
landing.sort.submit=Ordenar
landing.filters.heading=Filtros
landing.filters.apply=Aplicar filtros
landing.filter.genre=Género
landing.filter.condition=Condición
landing.filter.year=Año
landing.filter.price=Precio
landing.filter.priceMin=Desde
landing.filter.priceMax=Hasta
landing.filter.any=Cualquiera
landing.filter.empty=No encontramos vinilos con esos filtros. Probá con otra combinación.
search.suggestion.ARTIST=Artista
search.suggestion.ALBUM=Álbum
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
publish.pageTitle=Publicar vinilo | quieroVinilos
publish.heading=Publicar un vinilo
publish.edit.pageTitle=Editar publicación | quieroVinilos
publish.edit.heading=Editar publicación
publish.edit.submit=Publicar cambios
publish.preview.heading=Vista previa
publish.preview.titlePlaceholder=Título del álbum
publish.preview.artistPlaceholder=Nombre del artista
publish.preview.pricePlaceholder=$ —
publish.title.label=Título
publish.artistName.label=Artista
publish.releaseYear.label=Año
publish.submit=Publicar
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

post.contact.action=Me interesa comprarlo
post.edit.action=Editar
post.delete.action=Eliminar
post.delete.dialog.title=Eliminar publicación
post.delete.confirmation=¿Eliminás la publicación de "{0}" ({1})? Las consultas pendientes se cerrarán y no se puede deshacer.
post.deleted=La publicación fue eliminada.
post.created=La publicación fue creada.
post.updated=Los cambios de la publicación se guardaron.
post.detail.deleted=Publicación eliminada
post.contact.pageTitle=Contactar al publicante | quieroVinilos
post.contact.heading=Me interesa comprarlo
post.contact.message.label=Mensaje para quien publica (opcional)
post.contact.submit=Enviar consulta
post.contact.message.size=El mensaje no puede superar los 500 caracteres.
post.detail.pageTitle=Detalle del vinilo | quieroVinilos
post.detail.sold=Vendido
post.detail.own=Esta publicación es tuya.
post.detail.description=Descripción

email.welcome.subject=Bienvenido a quieroVinilos
email.welcome.body=Hola {0}, gracias por registrarte.
email.welcome.cta=Ver quieroVinilos
email.passwordChanged.subject=Tu contraseña fue cambiada en quieroVinilos
email.passwordChanged.body=Hola {0}, tu contraseña fue cambiada correctamente.
email.passwordChanged.notice=Si no fuiste vos, respondé a este correo.
email.postInterest.subject=Alguien está interesado en {0}
email.postInterest.heading=Hay interés en tu publicación
email.postInterest.intro={0} está interesado en tu publicación.
email.postInterest.contact=Contacto:
email.postInterest.album=Álbum:
email.postInterest.message=Mensaje:
email.postInterest.cta=Ver mis consultas
email.inquiryAccepted.subject=Tu consulta por {0} fue aceptada
email.inquiryAccepted.heading=Tu consulta fue aceptada
email.inquiryAccepted.intro=El vendedor aceptó tu consulta por {0}.
email.inquiryAccepted.album=Publicación:
email.inquiryAccepted.cta=Ver mis consultas

vinylCard.year=Año
vinylCard.price.format=$ {0,number,integer}
vinylCard.condition=Condición
vinylCard.zone=Zona
vinylCard.genre=Género
vinylCard.pressingYear=Prensada
vinylCard.open=Ver {0}

publish.genre.label=Género
publish.genre.placeholder=Seleccioná un género
publish.genre.required=El género es obligatorio.
publish.price.label=Precio en pesos
publish.price.required=El precio es obligatorio.
publish.price.range=El precio debe ser un entero entre 1 y 99.999.999.
publish.condition.label=Condición
publish.condition.required=La condición es obligatoria.
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
error.notFound.publish=Publicar un vinilo

error.badRequest.pageTitle=Búsqueda inválida | quieroVinilos
error.badRequest.code=400
error.badRequest.heading=Esa búsqueda es demasiado larga
error.badRequest.message=El texto que buscás no puede superar los 255 caracteres. Probá con el nombre del álbum o del artista.
auth.navigation.label=Cuenta
auth.login.action=Iniciar sesión
auth.register.action=Crear cuenta
auth.logout.action=Cerrar sesión
profile.pageTitle=Mi perfil | quieroVinilos
profile.heading=Mi perfil
profile.account.heading=Datos de la cuenta
profile.username.label=Nombre de usuario
profile.email.label=Correo electrónico
profile.username.edit=Editar nombre de usuario
profile.updated=El nombre de usuario se actualizó correctamente.
profile.password.label=Contraseña
profile.password.masked=••••••••
profile.password.edit=Cambiar contraseña
profile.password.current.label=Contraseña actual
profile.password.new.label=Contraseña nueva
profile.password.current.required=Ingresá tu contraseña actual.
profile.password.current.invalid=La contraseña actual es incorrecta.
profile.password.unchanged=La contraseña nueva tiene que ser distinta de la actual.
profile.edit.save=Guardar
profile.edit.cancel=Cancelar
profile.posts.heading=Mis publicaciones
profile.posts.empty=Todavía no publicaste ningún vinilo.
profile.posts.pagination=Páginas de mis publicaciones
pagination.previous=Anterior
pagination.next=Siguiente
pagination.page=Página {0}
profile.post.available=Disponible
auth.admin.action=Administración
auth.username.label=Nombre de usuario
auth.email.label=Correo electrónico
auth.password.label=Contraseña
auth.passwordConfirmation.label=Repetir contraseña
auth.password.required=La contraseña es obligatoria.
auth.password.size=La contraseña debe tener entre 12 y 72 caracteres.
auth.password.letter=La contraseña debe incluir una letra.
auth.password.number=La contraseña debe incluir un número.
auth.password.mismatch=Las contraseñas no coinciden.
auth.password.hint=Usá entre 12 y 72 caracteres, con al menos una letra y un número.
auth.password.invalid=La contraseña no cumple los requisitos.
auth.login.pageTitle=Iniciar sesión | quieroVinilos
auth.login.heading=Iniciar sesión
auth.login.submit=Entrar
auth.login.invalid=El correo o la contraseña son incorrectos.
auth.login.loggedOut=Cerraste la sesión correctamente.
auth.login.verificationSent=Te enviamos un enlace para confirmar tu correo y activar la cuenta.
auth.login.verified=Tu correo fue confirmado. Ya podés iniciar sesión.
auth.login.passwordChanged=Tu contraseña fue cambiada. Iniciá sesión con la nueva.
auth.login.resetLinkSent=Si hay una cuenta con ese correo, te enviamos un enlace para elegir una contraseña nueva.
auth.login.passwordReset=Tu contraseña fue restablecida. Iniciá sesión con la nueva.
auth.login.forgotPasswordLink=¿Olvidaste tu contraseña?
auth.login.registerPrompt=¿Es tu primera vez en quieroVinilos?
auth.login.registerLink=Registrate
auth.register.pageTitle=Crear cuenta | quieroVinilos
auth.register.heading=Crear cuenta
auth.register.submit=Registrarme
auth.register.loginPrompt=¿Ya tenés cuenta?
auth.register.username.required=El nombre de usuario es obligatorio.
auth.register.username.size=El nombre de usuario no puede superar los 100 caracteres.
auth.register.email.required=El correo electrónico es obligatorio.
auth.register.email.invalid=Ingresá un correo electrónico válido.
auth.register.email.size=El correo electrónico no puede superar los 100 caracteres.
auth.register.email.duplicate=Ya existe una cuenta con ese correo electrónico.
auth.verify.pageTitle=Verificar correo | quieroVinilos
auth.verify.heading=Confirmá tu correo
auth.verify.hint=Elegí tu nombre de usuario y contraseña para completar la verificación.
auth.verify.submit=Verificar cuenta
auth.verify.invalid=El enlace venció o ya fue utilizado.
auth.verify.token.required=Falta el token de verificación.
auth.forgotPassword.pageTitle=Recuperar contraseña | quieroVinilos
auth.forgotPassword.heading=Recuperar contraseña
auth.forgotPassword.hint=Ingresá el correo de tu cuenta y te enviamos un enlace para elegir una contraseña nueva.
auth.forgotPassword.submit=Enviar enlace
auth.resetPassword.pageTitle=Elegir contraseña nueva | quieroVinilos
auth.resetPassword.heading=Elegí una contraseña nueva
auth.resetPassword.hint=Elegí la contraseña con la que vas a iniciar sesión de ahora en más.
auth.resetPassword.submit=Guardar contraseña
auth.resetPassword.invalid=El enlace venció o ya fue utilizado.
auth.resetPassword.unchanged=La contraseña nueva tiene que ser distinta de la actual.
auth.resetPassword.token.required=Falta el token de recuperación.
auth.resetPassword.expiredPrompt=¿El enlace ya no sirve?
auth.resetPassword.expiredLink=Pedí uno nuevo
auth.admin.pageTitle=Administración | quieroVinilos
auth.admin.heading=Administración
auth.admin.message=Esta sección está disponible únicamente para administradores.
email.verification.subject=Confirmá tu correo en quieroVinilos
email.verification.body=Confirmá tu correo para elegir tus credenciales y activar tu cuenta.
email.verification.cta=Confirmar correo
email.passwordReset.subject=Recuperá tu contraseña de quieroVinilos
email.passwordReset.body=Entrá al enlace para elegir una contraseña nueva. Vence dentro de una hora.
email.passwordReset.cta=Elegir contraseña nueva
email.passwordReset.notice=Si no lo pediste, ignorá este correo: tu contraseña no cambia.
post.contact.identity=La consulta se enviará con el nombre y el correo de tu cuenta.
inquiry.navigation=Mis consultas
inquiry.received.pageTitle=Consultas recibidas | quieroVinilos
inquiry.sent.pageTitle=Consultas enviadas | quieroVinilos
inquiry.nav.label=Secciones de consultas
inquiry.nav.count=({0})
inquiry.heading=Mis consultas
inquiry.received.heading=Consultas recibidas
inquiry.received.empty=Todavía no recibiste consultas.
inquiry.sent.heading=Consultas enviadas
inquiry.sent.empty=Todavía no enviaste consultas.
inquiry.accept=Aceptar y vender
inquiry.reject=Rechazar
inquiry.accept.dialog.title=Confirmar venta
inquiry.message.empty=Sin mensaje
inquiry.pagination=Páginas de consultas
inquiry.submitted=Tu consulta fue enviada. Podés seguirla desde acá.
inquiry.accept.confirmation=¿Confirmás la venta de "{0}" ({1})? La publicación dejará de estar disponible y se rechazarán las demás consultas pendientes.
inquiry.accepted=La venta quedó confirmada y las demás consultas pendientes se cerraron.
inquiry.rejected=La consulta fue rechazada.
inquiry.status.PENDING=Pendiente
inquiry.status.ACCEPTED=Aceptada
inquiry.status.REJECTED=Rechazada
error.conflict.pageTitle=El estado cambió | quieroVinilos
error.conflict.code=409
error.conflict.heading=La publicación ya cambió de estado
error.conflict.message=Otra acción cambió la publicación o la consulta. Buscá otro ejemplar en el catálogo.
error.forbidden.pageTitle=Acceso denegado | quieroVinilos
error.forbidden.code=403
error.forbidden.heading=No tenés permiso para entrar acá
error.forbidden.message=Tu cuenta está autenticada, pero no tiene el permiso necesario para esta acción.

# Navegacion comun a todas las vistas.
nav.back=Volver al catálogo
form.cancel=Cancelar
```

- [messages_en.properties](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/resources/i18n/messages_en.properties>)
- [messages_es.properties](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/resources/i18n/messages_es.properties>)
- [messages_fr.properties](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/resources/i18n/messages_fr.properties>)

[[SupportedLocales]] · [[Mail delivery]] · [[Validation and errors]]
