@title: Feature map
@categories: Navigation, Flows
@tags: codemap, navigation

> [!summary] En una frase
> Índice de funcionalidades: para cada una, qué rutas atiende, qué clases la implementan en cada capa, qué tablas toca, qué herramientas usa y en qué nota está explicada a fondo.

Las rutas salen de los `@RequestMapping` de `c3e2a4c` (52 en total) más `POST /login` y `POST /logout`, que atiende Spring Security. "Acceso" resume la regla de [[SecurityConfig]] y los `@PreAuthorize`; el detalle está en [[Security and authorization]].

## Cuenta

| Funcionalidad | Rutas | Acceso | Web | Service | Tablas | Nota |
|---|---|---|---|---|---|---|
| Registro | `GET/POST /register` | Público | [[AuthenticationController]], [[RegisterForm]] | [[UserServiceImpl]] | `users`, `email_verification_tokens` | [[Authentication flow]] |
| Login y logout | `GET /login`, `POST /login`, `POST /logout` | Público | Filtros de Spring Security, [[AuthenticatedUserDetailsService]] | [[UserServiceImpl]] | `users` | [[Authentication flow]] |
| Verificación de correo | `GET /verify`, `GET /verify/required`, `POST /verify/resend` | El enlace es público; reenviar exige sesión | [[AuthenticationController]], [[VerificationAccessDeniedHandler]] | [[UserServiceImpl]] | `email_verification_tokens`, `users` | [[Tokens and email links]] |
| Recuperación de contraseña | `GET/POST /forgot-password`, `GET/POST /reset-password` | Público | [[AuthenticationController]] | [[UserServiceImpl]] | `password_reset_tokens`, `users` | [[Password recovery flow]] |
| Perfil privado | `GET/POST /profile` (`GET` con `postStatus` y `page`), `POST /profile/avatar`, `POST /profile/password` | Cuenta verificada | [[ProfileController]] | [[UserServiceImpl]], [[ImageServiceImpl]], [[PostServiceImpl]] | `users`, `images`, `posts` | [[Profile flow]], [[Status filters flow]] |
| Datos de cobro | `POST /profile/payment` (con `returnInquiryId`, vuelve a la venta) | Cuenta verificada | [[ProfileController]], [[PaymentForm]] | [[UserServiceImpl]], [[InquiryServiceImpl]] | `users` | [[Addresses and payment flow]] |
| Direcciones | `POST /profile/addresses`, `.../{id}/edit`, `.../{id}/delete` | Cuenta verificada y dueña | [[ProfileController]], [[AddressAccessHandler]] | [[AddressServiceImpl]] | `addresses` | [[Addresses and payment flow]] |
| Perfil público | `GET /users/{id}?page&reviewRole&reviewPage` | Público | [[PublicProfileController]] | [[PublicProfileServiceImpl]], [[ReviewServiceImpl]] | `users`, `posts`, `reviews`, `inquiries` | [[Public profile flow]] |

## Catálogo

| Funcionalidad | Rutas | Acceso | Web | Service | Tablas | Nota |
|---|---|---|---|---|---|---|
| Portada, búsqueda, filtros y orden | `GET /` | Público | [[LandingController]], [[CatalogFilterForm]] | [[PostServiceImpl]], [[Pagination]] | `posts`, `albums`, `artists` | [[Landing flow]] |
| Sugerencias del buscador | `GET /search/suggestions` | Público | [[SearchSuggestionController]] | [[PostServiceImpl]] | `albums`, `artists` | [[Search suggestions flow]] |
| Sugerencias de artista al publicar | `GET /artists/suggestions` | Público | [[ArtistSuggestionController]] | [[ArtistServiceImpl]] | `artists` | [[Search suggestions flow]] |
| Ficha de una publicación | `GET /post/{id}?from&origin&originPage&postStatus` | Público | [[PostController]] | [[CartServiceImpl]] (arma la vista), [[PostServiceImpl]] | `posts`, `post_images` | [[Post detail flow]] |
| Imágenes | `GET /post/{id}/images/{id}`, `GET /users/{id}/avatar/{id}`, `GET /albums/{id}/cover/{id}` | Público | [[ImageController]] | [[ImageServiceImpl]] | `images` | [[Cover image flow]] |

## Vender

| Funcionalidad | Rutas | Acceso | Web | Service | Tablas | Nota |
|---|---|---|---|---|---|---|
| Publicar | `GET/POST /publish` | Cuenta verificada | [[PublishController]], [[PublishForm]] | [[PostServiceImpl]], [[ArtistServiceImpl]], [[AlbumServiceImpl]], [[ImageServiceImpl]] | `posts`, `albums`, `artists`, `images`, `post_images` | [[Publish flow]], [[Gallery flow]] |
| Editar y eliminar | `GET/POST /post/{id}/edit`, `POST /post/{id}/delete` | Publicante o ADMIN | [[PublishController]], [[PostAccessHandler]] | [[PostServiceImpl]] | `posts`, `inquiries` | [[Edit and delete flow]] |
| Bandeja de recibidas | `GET /inquiries?status&page` | Cuenta verificada | [[InquiryController]] | [[InquiryServiceImpl]], [[InquiryStatusFilter]] | `inquiries`, `inquiry_messages` | [[Inquiry and sale flow]], [[Status filters flow]] |
| Aceptar, rechazar, pedir otro comprobante, confirmar | `POST /inquiries/{id}/accept`, `/reject`, `/request-receipt`, `/confirm` | Vendedor de esa consulta | [[InquiryController]], [[InquiryAccessHandler]] | [[InquiryServiceImpl]] | `inquiries`, `posts` | [[Inquiry and sale flow]] |

## Comprar

| Funcionalidad | Rutas | Acceso | Web | Service | Tablas | Nota |
|---|---|---|---|---|---|---|
| Consultar por un vinilo | `GET/POST /post/{id}/contact` | Cuenta verificada, no la publicante | [[PostContactController]], [[ShippingAddressForm]] | [[InquiryServiceImpl]], [[ContactRules]], [[AddressServiceImpl]] | `inquiries`, `inquiry_messages`, `addresses` | [[Contact flow]] |
| Carrito | `GET /cart`, `POST /cart/add/{id}`, `POST /cart/remove/{id}`, `POST /cart/checkout` | Cuenta verificada | [[CartController]], [[CartExceptionAdvice]], [[CartCountAdvice]] | [[CartServiceImpl]] | `cart_items`, `inquiries` | [[Cart flow]] |
| Bandeja de enviadas | `GET /inquiries/sent?status&page` | Cuenta verificada | [[InquiryController]] | [[InquiryServiceImpl]], [[InquiryStatusFilter]] | `inquiries` | [[Inquiry and sale flow]], [[Status filters flow]] |
| Subir y ver el comprobante | `POST/GET /inquiries/{id}/receipt` | Comprador sube; las dos partes lo ven | [[InquiryController]], [[ReceiptForm]] | [[InquiryServiceImpl]] | `inquiries` | [[Inquiry and sale flow]] |
| Cancelar | `POST /inquiries/{id}/cancel` | Parte de la consulta, según estado | [[InquiryController]] | [[InquiryServiceImpl]] | `inquiries`, `posts` | [[Inquiry and sale flow]] |

## Entre las dos partes

| Funcionalidad | Rutas | Acceso | Web | Service | Tablas | Nota |
|---|---|---|---|---|---|---|
| Página de la venta | `GET /inquiries/{id}` | Comprador o vendedor de esa consulta | [[InquiryController]] | [[InquiryServiceImpl]] | `inquiries`, `inquiry_messages`, `reviews` | [[Inquiry and sale flow]] |
| Conversación | `POST /inquiries/{id}/messages` | Parte, con la consulta abierta | [[InquiryController]], [[MessageForm]] | [[InquiryServiceImpl]] | `inquiry_messages` | [[Conversation flow]] |
| Reseñas | `POST /inquiries/{id}/review`, `/review/remove` | Parte de una venta confirmada | [[InquiryController]], [[ReviewForm]] | [[InquiryServiceImpl]], [[ReviewServiceImpl]] | `reviews` | [[Reviews flow]] |

## Transversales

| Mecanismo | Dónde vive | Herramientas | Nota |
|---|---|---|---|
| Autenticación y autorización | [[SecurityConfig]], paquete `webapp.security` | Spring Security, BCrypt, CSRF, `SessionRegistry`, `@PreAuthorize` | [[Security and authorization]] |
| Tokens y enlaces | [[UserServiceImpl]], DAO de tokens | `SecureRandom`, Base64 URL | [[Tokens and email links]] |
| Correo | [[EmailServiceImpl]], [[TransactionCallbacks]] | JavaMail, Thymeleaf, `@Async`, pool de hilos | [[Mail delivery]] |
| Transacciones y bloqueos | Services | `@Transactional`, `FOR UPDATE`, `UPDATE` condicional | [[Transactions and concurrency]] |
| Validación y errores | Formularios, `*Rules`, [[ErrorResponseAdvice]] | Bean Validation, `@ControllerAdvice` | [[Validation and errors]] |
| Paginación | [[Pagination]], `PostPage`, `InquiryPage` | `LIMIT`/`OFFSET` con `COUNT` | [[Paginated listings]] |
| Filtros por estado | [[InquiryStatusFilter]], [[FilterCounts]], `filter-chips.tag` | `status IN (...)`, `GROUP BY status` | [[Status filters flow]] |
| Idiomas | Bundles, [[SupportedLocales]] | `MessageSource`, `Accept-Language` | [[Localization]] |
| Esquema | Migraciones | Flyway | [[Database schema]] |
| Logs | Services | SLF4J, Logback | [[Logging]] |
| Interfaz | Tags JSP, CSS, JS | JSP, JSTL, Spring form tags | [[UI components]], [[UI styles and tokens]], [[Views and assets]] |

## Rutas de error

`/error/403` y `/error/404` las atiende [[ErrorController]]; el contenedor reenvía ahí los 404 de rutas sin controller, y [[VerificationAccessDeniedHandler]] reenvía los 403.

## Cómo leer una funcionalidad

1. Abrí su nota de flujo: tiene el recorrido paso a paso, las decisiones y las preguntas de defensa.
2. Seguí las clases de la fila de izquierda a derecha: web, service, tablas.
3. Para el orden de lectura archivo por archivo, [[Roadmap de lectura]].
