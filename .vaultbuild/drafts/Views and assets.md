@title: Views and assets
@categories: Web
@module: webapp
@files: webapp/src/main/webapp/WEB-INF/views/auth/forgot-password.jsp, webapp/src/main/webapp/WEB-INF/views/auth/login.jsp, webapp/src/main/webapp/WEB-INF/views/auth/register.jsp, webapp/src/main/webapp/WEB-INF/views/auth/reset-password.jsp, webapp/src/main/webapp/WEB-INF/views/auth/verify-required.jsp, webapp/src/main/webapp/WEB-INF/views/auth/verify.jsp, webapp/src/main/webapp/WEB-INF/views/cart/index.jsp, webapp/src/main/webapp/WEB-INF/views/error/400.jsp, webapp/src/main/webapp/WEB-INF/views/error/403.jsp, webapp/src/main/webapp/WEB-INF/views/error/404.jsp, webapp/src/main/webapp/WEB-INF/views/error/409.jsp, webapp/src/main/webapp/WEB-INF/views/inquiry/detail.jsp, webapp/src/main/webapp/WEB-INF/views/inquiry/received.jsp, webapp/src/main/webapp/WEB-INF/views/inquiry/sent.jsp, webapp/src/main/webapp/WEB-INF/views/landing/index.jsp, webapp/src/main/webapp/WEB-INF/views/post/contact.jsp, webapp/src/main/webapp/WEB-INF/views/post/detail.jsp, webapp/src/main/webapp/WEB-INF/views/profile/index.jsp, webapp/src/main/webapp/WEB-INF/views/profile/public.jsp, webapp/src/main/webapp/WEB-INF/views/publish/index.jsp, webapp/src/main/webapp/js/account-edit.js, webapp/src/main/webapp/js/autocomplete.js, webapp/src/main/webapp/js/catalog.js, webapp/src/main/webapp/js/confirm-action.js, webapp/src/main/webapp/js/post-gallery.js, webapp/src/main/webapp/js/publish-preview.js, webapp/src/main/webapp/js/sale-detail.js, webapp/src/main/webapp/js/submit-once.js, webapp/src/main/webapp/images/covers/placeholder.svg, webapp/src/main/webapp/images/logo.svg

> [!summary] En una frase
> 20 vistas JSP, 8 scripts y 2 imágenes: las vistas solo componen componentes y muestran lo que el controller dejó en el modelo, y cada script mejora algo que ya funciona sin JavaScript.

Los componentes compartidos están en [[UI components]] y los estilos en [[UI styles and tokens]].

## Cómo llega una vista al navegador

1. El controller devuelve un `ModelAndView` con un nombre lógico, por ejemplo `post/detail`.
2. El `viewResolver` lo convierte en `/WEB-INF/views/post/detail.jsp`. Al estar bajo `WEB-INF`, la JSP no se puede pedir directamente por URL.
3. La JSP lee el modelo con EL (`${post.title}` llama a `getTitle()`), compone tags `ui:` y escribe HTML.
4. `head.tag` enlaza los tres CSS y los scripts comunes con `defer`.

## Vistas

| Vista | Qué muestra | Controller | Flujo | Líneas |
|---|---|---|---|---|
| `auth/forgot-password` | Pedido de recuperación | [[AuthenticationController]] | [[Password recovery flow]] | 34 |
| `auth/login` | Login: mirá los nombres de los campos y el token CSRF | [[AuthenticationController]] | [[Authentication flow]] | 56 |
| `auth/register` | Formulario de registro | [[AuthenticationController]] | [[Authentication flow]] | 46 |
| `auth/reset-password` | Nueva contraseña con el token en un campo oculto | [[AuthenticationController]] | [[Password recovery flow]] | 48 |
| `auth/verify-required` | Pantalla para la cuenta sin verificar | [[AuthenticationController]] | [[Authentication flow]] | 32 |
| `auth/verify` | Resultado de abrir el enlace de verificación | [[AuthenticationController]] | [[Authentication flow]] | 44 |
| `cart/index` | Carrito agrupado por publicante. Mirá la URL de la tapa (línea 53) | [[CartController]] | [[Cart flow]] | 128 |
| `error/400` | Pedido inválido | [[ErrorResponseAdvice]], [[LandingController]] | [[Validation and errors]] | 28 |
| `error/403` | Sin permiso | [[ErrorController]], [[ErrorResponseAdvice]] | [[Validation and errors]] | 18 |
| `error/404` | No encontrado | [[ErrorController]], [[ErrorResponseAdvice]] | [[Validation and errors]] | 30 |
| `error/409` | Conflicto: el estado cambió | [[InquiryController]], [[PostContactController]], [[PublishController]] | [[Validation and errors]] | 18 |
| `inquiry/detail` | La página de la venta: acciones según estado y rol, conversación, reseña | [[InquiryController]] | [[Inquiry and sale flow]] | 287 |
| `inquiry/received` | Bandeja del vendedor, agrupada por publicación | [[InquiryController]] | [[Inquiry and sale flow]] | 81 |
| `inquiry/sent` | Bandeja del comprador | [[InquiryController]] | [[Inquiry and sale flow]] | 79 |
| `landing/index` | Filtros, orden, grilla, estado vacío y paginación | [[LandingController]] | [[Landing flow]] | 223 |
| `post/contact` | Mensaje y elección de dirección | [[PostContactController]] | [[Contact flow]] | 68 |
| `post/detail` | Ficha: galería, vendedor, acciones según quién mira | [[PostController]] | [[Post detail flow]] | 183 |
| `profile/index` | Perfil privado: cuenta, contraseña, cobro, direcciones, publicaciones | [[ProfileController]] | [[Profile flow]] | 341 |
| `profile/public` | Perfil público: reputación, publicaciones, reseñas | [[PublicProfileController]] | [[Public profile flow]] | 108 |
| `publish/index` | Publicar y editar comparten vista | [[PublishController]] | [[Publish flow]] | 155 |

"Controller" se calculó buscando el nombre lógico de la vista en las clases de `webapp`.

## Scripts

| Script | Qué hace | Dónde corre |
|---|---|---|
| `account-edit.js` | Filas editables del perfil y diálogo de la foto | Perfil privado (`pageScript`) |
| `autocomplete.js` | Sugerencias: espera, número de secuencia, JSON y nodos armados con textContent | Todas las páginas; actúa en el buscador y en el campo de artista |
| `catalog.js` | Envía el orden al cambiar el select; pliega filtros en pantallas angostas | Todas las páginas; actúa en los formularios `data-auto-submit` (orden del catálogo y rol de las reseñas del perfil público) |
| `confirm-action.js` | Abre el diálogo antes de enviar un formulario destructivo | Todas las páginas; actúa donde hay `data-confirm-message` |
| `post-gallery.js` | Cambia la foto principal al tocar una miniatura | Ficha (`pageScript`) |
| `publish-preview.js` | Vista previa de la tarjeta mientras se completa el formulario | Publicar y editar (lo carga la propia vista) |
| `sale-detail.js` | Página de la venta: alto de la conversación, scroll al último mensaje, Enter para enviar y cancelar la edición de la reseña | Página de la venta (`pageScript`) |
| `submit-once.js` | Evita el doble envío | Todas las páginas (lo carga `head.tag`) |

Todos son JavaScript sin dependencias ni framework, cargados con `defer`.

### Mejora progresiva

Cada script agrega comodidad sobre algo que ya anda con HTML y un POST:

| Sin JavaScript | Con JavaScript |
|---|---|
| El orden del catálogo se aplica con un botón | Se aplica al cambiar el select |
| El buscador envía el formulario | Ofrece sugerencias mientras se escribe |
| Un formulario destructivo se envía directo; el service valida estado y propiedad igual | Pide confirmación en un diálogo |
| Un doble clic podría enviar dos veces; el service lo resuelve con sus guardas | Los botones se deshabilitan al enviar |
| El perfil edita con enlaces y recargas | Las filas se abren y cierran en el lugar |
| En la ficha, cada miniatura es un enlace que abre esa foto | Las miniaturas cambian la foto principal sin salir de la página |

La seguridad nunca depende del script: confirmaciones y bloqueos de doble envío son comodidad; la regla está en el service.

## Imágenes

| Archivo | Uso |
|---|---|
| `images/logo.svg` | Isotipo y favicon |
| `images/covers/placeholder.svg` | Tapa cuando la publicación no tiene foto |

Las fotos subidas no son archivos: se guardan en la base y las sirve [[ImageController]] ([[Cover image flow]]).

## Preguntas de defensa

**¿Por qué las JSP están bajo `WEB-INF`?**
Para que solo se llegue a ellas a través de un controller, que arma el modelo y aplica la seguridad.

**¿Hay lógica en las vistas?**
Solo de presentación: condicionales y bucles de JSTL sobre datos ya resueltos. No hay scriptlets ni llamadas a services.

**¿Qué pasa si el navegador no tiene JavaScript?**
Todo funciona con formularios y enlaces. Los scripts solo mejoran la experiencia.

**¿Cómo evitan XSS en el JavaScript?**
Las sugerencias llegan como JSON y los nodos se arman con `textContent`, nunca con `innerHTML`.

## Código de las vistas

### auth/forgot-password

Pedido de recuperación.

{{file:webapp/src/main/webapp/WEB-INF/views/auth/forgot-password.jsp}}

### auth/login

Login: mirá los nombres de los campos y el token CSRF.

{{file:webapp/src/main/webapp/WEB-INF/views/auth/login.jsp}}

### auth/register

Formulario de registro.

{{file:webapp/src/main/webapp/WEB-INF/views/auth/register.jsp}}

### auth/reset-password

Nueva contraseña con el token en un campo oculto.

{{file:webapp/src/main/webapp/WEB-INF/views/auth/reset-password.jsp}}

### auth/verify-required

Pantalla para la cuenta sin verificar.

{{file:webapp/src/main/webapp/WEB-INF/views/auth/verify-required.jsp}}

### auth/verify

Resultado de abrir el enlace de verificación.

{{file:webapp/src/main/webapp/WEB-INF/views/auth/verify.jsp}}

### cart/index

Carrito agrupado por publicante. Mirá la URL de la tapa (línea 53).

{{file:webapp/src/main/webapp/WEB-INF/views/cart/index.jsp}}

### error/400

Pedido inválido.

{{file:webapp/src/main/webapp/WEB-INF/views/error/400.jsp}}

### error/403

Sin permiso.

{{file:webapp/src/main/webapp/WEB-INF/views/error/403.jsp}}

### error/404

No encontrado.

{{file:webapp/src/main/webapp/WEB-INF/views/error/404.jsp}}

### error/409

Conflicto: el estado cambió.

{{file:webapp/src/main/webapp/WEB-INF/views/error/409.jsp}}

### inquiry/detail

La página de la venta: acciones según estado y rol, conversación, reseña.

{{file:webapp/src/main/webapp/WEB-INF/views/inquiry/detail.jsp}}

### inquiry/received

Bandeja del vendedor, agrupada por publicación.

{{file:webapp/src/main/webapp/WEB-INF/views/inquiry/received.jsp}}

### inquiry/sent

Bandeja del comprador.

{{file:webapp/src/main/webapp/WEB-INF/views/inquiry/sent.jsp}}

### landing/index

Filtros, orden, grilla, estado vacío y paginación.

{{file:webapp/src/main/webapp/WEB-INF/views/landing/index.jsp}}

### post/contact

Mensaje y elección de dirección.

{{file:webapp/src/main/webapp/WEB-INF/views/post/contact.jsp}}

### post/detail

Ficha: galería, vendedor, acciones según quién mira.

{{file:webapp/src/main/webapp/WEB-INF/views/post/detail.jsp}}

### profile/index

Perfil privado: cuenta, contraseña, cobro, direcciones, publicaciones.

{{file:webapp/src/main/webapp/WEB-INF/views/profile/index.jsp}}

### profile/public

Perfil público: reputación, publicaciones, reseñas.

{{file:webapp/src/main/webapp/WEB-INF/views/profile/public.jsp}}

### publish/index

Publicar y editar comparten vista.

{{file:webapp/src/main/webapp/WEB-INF/views/publish/index.jsp}}

## Código de los scripts

### account-edit.js

Filas editables del perfil y diálogo de la foto.

{{file:webapp/src/main/webapp/js/account-edit.js}}

### autocomplete.js

Sugerencias: espera, número de secuencia, JSON y nodos armados con textContent.

{{file:webapp/src/main/webapp/js/autocomplete.js}}

### catalog.js

Envía el orden al cambiar el select; pliega filtros en pantallas angostas.

{{file:webapp/src/main/webapp/js/catalog.js}}

### confirm-action.js

Abre el diálogo antes de enviar un formulario destructivo.

{{file:webapp/src/main/webapp/js/confirm-action.js}}

### post-gallery.js

Cambia la foto principal al tocar una miniatura.

{{file:webapp/src/main/webapp/js/post-gallery.js}}

### publish-preview.js

Vista previa de la tarjeta mientras se completa el formulario.

{{file:webapp/src/main/webapp/js/publish-preview.js}}

### sale-detail.js

Página de la venta: alto de la conversación, scroll al último mensaje, Enter para enviar y cancelar la edición de la reseña.

{{file:webapp/src/main/webapp/js/sale-detail.js}}

### submit-once.js

Evita el doble envío.

{{file:webapp/src/main/webapp/js/submit-once.js}}

## Imágenes

### placeholder.svg

{{file:webapp/src/main/webapp/images/covers/placeholder.svg}}

### logo.svg

{{file:webapp/src/main/webapp/images/logo.svg}}
