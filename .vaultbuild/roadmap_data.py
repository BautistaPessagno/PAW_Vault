# -*- coding: utf-8 -*-
"""Etapas del roadmap de lectura. Cada etapa: (titulo, objetivo, notas, preguntas, grupos).
Un grupo es (subtitulo, [items]); un item es un nombre de clase Java, una ruta o un glob."""
W = 'webapp/src/main/webapp/'
V = W + 'WEB-INF/views/'
G = W + 'WEB-INF/tags/'
R = 'webapp/src/main/resources/'
M = 'persistence/src/main/resources/db/migration/'

STAGES = [
 ('Orientación', 'Saber qué es el producto, qué palabras usa y qué reglas sigue el equipo antes de abrir código.',
  ['Project snapshot', 'Domain and identity', 'History and specifications'],
  ['¿Qué diferencia hay entre Álbum, Post y Consulta?', '¿Qué puede hacer una Cuenta sin verificar?', '¿Qué está prohibido en esta etapa de la cursada?'],
  [('Documentos', ['README.md', 'CONTEXT.md', 'CLAUDE.md', 'AGENTS.md', 'docs/setup.md', 'docs/adr/*.md', 'TODO.md'])]),

 ('Build, configuración y arranque', 'Entender cómo seis módulos se convierten en un WAR y cómo arranca el contexto de Spring.',
  ['Architecture', 'Build and dependencies', 'Startup and dependency injection', 'Configuration and running', 'Logging'],
  ['¿Qué impide que un controller use un DAO?', '¿Cómo se crean las tablas al arrancar?', '¿Qué pasa si falta una propiedad de configuración?', '¿Dónde quedan los logs en el servidor?'],
  [('Maven', ['pom.xml', 'models/pom.xml', 'persistence-contracts/pom.xml', 'persistence/pom.xml', 'services-contracts/pom.xml', 'services/pom.xml', 'webapp/pom.xml', '*/.mvn/*', 'models/src/main/resources/.gitkeep']),
   ('Arranque', [W + 'WEB-INF/web.xml', 'WebConfig']),
   ('Configuración y logs', [R + 'database.properties.example', R + 'mail.properties.example', 'webapp/src/pampero/resources/*', R + 'logback.xml', R + 'logback-test.xml', '.gitignore', '.worktreeinclude'])]),

 ('Base de datos', 'Leer el esquema en el orden en que se construyó y conocer los datos con los que corren los tests.',
  ['Database schema', 'Schema history and seeds'],
  ['¿Qué reglas garantiza la base y cuáles el service?', '¿Por qué las migraciones tienen que correr en HSQLDB?', '¿Qué pasa con las consultas si se borra una publicación?'],
  [('Migraciones, en orden', [M + 'V%d__*.sql' % i for i in range(1, 12)]),
   ('Datos de prueba', ['persistence/src/test/resources/populator.sql', 'TestConfiguration']),
   ('Datos de demostración y base local', ['tools/setup_local_postgres.sh', 'tools/seed_local_data.sh', 'database/seed_dev_posts.sql', 'database/demo_posts.tsv', 'tools/sql/demo-users.sql', 'database/users.sql'])]),

 ('Dominio: los modelos', 'Conocer los objetos que viajan entre capas. Son inmutables: mirá qué campos tienen y qué reglas llevan adentro.',
  ['Domain and identity'],
  ['¿Cuáles son entidades y cuáles proyecciones de lectura?', '¿Qué reglas viven en clases *Rules y por qué en models?', '¿Qué estados tiene una publicación y cuáles una consulta?'],
  [('Cuenta', ['User', 'UserRole', 'PaymentInfo', 'PaymentInfoRules', 'EmailRules', 'PublicUserProfile', 'EmailVerificationToken', 'PasswordResetToken']),
   ('Catálogo', ['Artist', 'Album', 'Genre', 'Condition', 'SearchText', 'VinylInputRules']),
   ('Publicación', ['Post', 'PostStatus', 'PostSummary', 'PostDetail', 'PostPage', 'PostSort', 'PostSearchCriteria', 'SearchResult', 'SearchSuggestion', 'SearchSuggestionType', 'Image', 'ImageUpload', 'ImageRules', 'FilterCounts']),
   ('Direcciones', ['Address', 'Province', 'ShippingOptions']),
   ('Consulta y venta', ['Inquiry', 'InquiryStatus', 'InquiryStatusFilter', 'InquirySummary', 'InquiryDetail', 'InquiryGroup', 'InquiryPage', 'InquiryParties', 'Message', 'MessageRules', 'Receipt', 'ReceiptRules', 'ContactState', 'PostContactOptions', 'PostView']),
   ('Reseñas y perfil público', ['Review', 'ReviewRules', 'ReviewStats', 'ReviewPage', 'ReviewSubjectRole', 'PublicProfile']),
   ('Carrito', ['Cart', 'CartItem', 'CartSellerGroup', 'CartCheckout', 'CartCheckoutResult'])]),

 ('Primer recorrido completo: catálogo y búsqueda', 'Seguir un request de solo lectura por todas las capas. Es el flujo más simple para fijar el patrón controller, service, DAO, JSP.',
  ['Landing flow', 'Search suggestions flow', 'Paginated listings'],
  ['¿Cómo llega un filtro de la URL a la cláusula WHERE?', '¿Cómo se evita la inyección SQL en una consulta con filtros opcionales?', '¿Por qué las sugerencias devuelven JSON?', '¿Cómo se calcula la paginación?'],
  [('Web', ['LandingController', 'ListingQueries', 'PostOrigin', 'CatalogFilterForm', 'CatalogFilterValidator', 'ValidCatalogFilters', 'SearchSuggestionController', 'SearchSuggestionDto', 'ArtistSuggestionController', 'ArtistSuggestionDto']),
   ('Service', ['PostService', 'PostServiceImpl', 'Pagination', 'PageNotFoundException', 'InvalidSearchQueryException', 'PostNotFoundException']),
   ('Persistencia', ['PostDao', 'PostJdbcDao']),
   ('Vista', [V + 'landing/index.jsp', G + 'vinyl-card.tag', G + 'pagination.tag', G + 'pagination-link.tag', G + 'post-badge.tag', W + 'js/catalog.js', W + 'js/autocomplete.js']),
   ('Tests', ['PaginationTest', 'PostServiceImplTest', 'PostJdbcDaoTest'])]),

 ('Cuenta y seguridad', 'El tema más preguntado en la defensa: registro, login, verificación, tokens, recuperación y quién puede entrar a qué.',
  ['Authentication flow', 'Tokens and email links', 'Password recovery flow', 'Security and authorization'],
  ['¿Qué pasa, paso a paso, cuando alguien se registra?', '¿Cómo se genera, guarda y consume un token?', '¿Cómo se guarda la contraseña?', '¿Dónde se decide que una ruta exige cuenta verificada?', '¿Qué pasa con las sesiones al cambiar la clave?', '¿Cómo protegen contra CSRF?'],
  [('Configuración de seguridad', ['SecurityConfig', 'AuthenticatedUser', 'AuthenticatedUserDetailsService', 'AuthenticationSessions', 'SameSiteRedirects', 'VerificationAccessDeniedHandler', 'PasswordHasher']),
   ('Web', ['AuthenticationController', 'LoginForm', 'RegisterForm', 'ForgotPasswordForm', 'ResetPasswordForm', 'ValidPassword', 'MatchingPasswords', 'MatchingPasswordsValidator', 'PasswordsMatching']),
   ('Service', ['UserService', 'UserServiceImpl', 'DuplicateUserException', 'UserNotFoundException', 'UnchangedPasswordException', 'InvalidCurrentPasswordException']),
   ('Persistencia', ['UserDao', 'UserJdbcDao', 'EmailVerificationTokenDao', 'EmailVerificationTokenJdbcDao', 'PasswordResetTokenDao', 'PasswordResetTokenJdbcDao']),
   ('Vistas', [V + 'auth/register.jsp', V + 'auth/login.jsp', V + 'auth/verify.jsp', V + 'auth/verify-required.jsp', V + 'auth/forgot-password.jsp', V + 'auth/reset-password.jsp', G + 'resend-verification.tag']),
   ('Tests', ['UserServiceImplTest', 'UserJdbcDaoTest', 'EmailVerificationTokenJdbcDaoTest', 'PasswordResetTokenJdbcDaoTest'])]),
]

STAGES += [
 ('Correo', 'Cómo sale un mail sin frenar el request ni avisar algo que después se revirtió.',
  ['Mail delivery', 'Transactions and concurrency', 'Localization'],
  ['¿En qué hilo se envía un correo y por qué?', '¿Qué pasa si el SMTP está caído?', '¿Por qué el envío se dispara después del commit?', '¿En qué idioma llega y cómo se arma el enlace?'],
  [('Service', ['EmailService', 'EmailServiceImpl', 'TransactionCallbacks', 'SupportedLocales']),
   ('Cargas de los avisos', ['PostInterestNotification', 'InquiryUpdateNotification', 'InquiryEvent', 'MessageNotification']),
   ('Plantillas', ['services/src/main/resources/mail/*.html']),
   ('Tests', ['EmailServiceImplTest'])]),

 ('Publicar, editar e imágenes', 'El primer flujo de escritura: formulario con archivos, catálogo que se crea al publicar y fotos guardadas en la base.',
  ['Publish flow', 'Edit and delete flow', 'Cover image flow', 'Gallery flow'],
  ['¿Qué pasa si dos personas publican el mismo álbum nuevo a la vez?', '¿Cómo se valida que un archivo sea una imagen?', '¿Dónde se guardan las fotos y cómo se sirven?', '¿Quién puede editar o borrar una publicación?'],
  [('Web', ['PublishController', 'PublishForm', 'PublishFormValidator', 'ValidPublishForm', 'ImageFiles', 'PostAccessHandler', 'ImageController', 'ImageNotFoundException', 'MultipartExceptionHandlerFilter']),
   ('Services', ['ArtistService', 'ArtistServiceImpl', 'AlbumService', 'AlbumServiceImpl', 'ImageService', 'ImageServiceImpl', 'DuplicatePostException', 'ConcurrentPublishException', 'InvalidPostDataException', 'InvalidImageException', 'PostUnavailableException']),
   ('Persistencia', ['ArtistDao', 'ArtistJdbcDao', 'AlbumDao', 'AlbumJdbcDao', 'ImageDao', 'ImageJdbcDao', 'PostImageDao', 'PostImageJdbcDao', 'DuplicatePostKeyException']),
   ('Vista', [V + 'publish/index.jsp', W + 'js/publish-preview.js', W + 'images/covers/placeholder.svg']),
   ('Tests', ['ArtistServiceImplTest', 'AlbumServiceImplTest', 'ImageServiceImplTest', 'InMemoryImageService', 'ArtistJdbcDaoTest', 'AlbumJdbcDaoTest', 'ImageJdbcDaoTest', 'PostImageJdbcDaoTest'])]),

 ('Ficha, contacto, direcciones y datos de cobro', 'Cómo un comprador abre una consulta y qué datos propios necesita cada parte.',
  ['Post detail flow', 'Contact flow', 'Addresses and payment flow'],
  ['¿Qué se valida antes de crear una consulta?', '¿Por qué una dirección se archiva en vez de borrarse?', '¿Cómo se sostiene el tope de tres direcciones con dos pestañas abiertas?', '¿Qué ve el vendedor de la dirección antes de aceptar?'],
  [('Ficha', ['PostController', V + 'post/detail.jsp', W + 'js/post-gallery.js']),
   ('Contacto', ['PostContactController', 'ContactForm', 'ShippingAddressForm', 'ShippingAddressValidator', 'ValidShippingAddress', 'LineBreakNormalizingEditor', 'ContactRules', 'OpenInquiryExistsException', V + 'post/contact.jsp']),
   ('Direcciones', ['AddressService', 'AddressServiceImpl', 'AddressDao', 'AddressJdbcDao', 'AddressForm', 'AddressAccessHandler', 'AddressLimitExceededException', 'AddressNotFoundException', G + 'address-fields.tag', G + 'address.tag']),
   ('Datos de cobro', ['PaymentForm', 'PaymentFormValidator', 'ValidPaymentForm', 'InvalidPaymentInfoException', 'PaymentInfoRequiredException', 'MissingPaymentInfoException']),
   ('Tests', ['ContactRulesTest', 'AddressServiceImplTest', 'AddressJdbcDaoTest'])]),

 ('Consulta, venta y conversación', 'El corazón del negocio: una máquina de estados con bloqueos, comprobante, mensajes y un correo por cada cambio.',
  ['Inquiry and sale flow', 'Conversation flow', 'Status filters flow', 'Transactions and concurrency'],
  ['¿Qué estados tiene una consulta y quién puede pasar de uno a otro?', '¿Qué pasa si el vendedor acepta dos consultas a la vez?', '¿Qué fila se bloquea y por qué esa?', '¿Dónde se guarda el comprobante y quién puede descargarlo?', '¿Cuándo se cierra una conversación?'],
  [('Web', ['InquiryController', 'InquiryAccessHandler', 'MessageForm', 'ReceiptForm', 'ReceiptValidator', 'ValidReceipt']),
   ('Service', ['InquiryService', 'InquiryServiceImpl', 'InquiryNotFoundException', 'InvalidInquiryStateException', 'InvalidMessageException', 'InvalidReceiptException', 'ReceiptNotFoundException', 'ForbiddenOperationException']),
   ('Persistencia', ['InquiryDao', 'InquiryJdbcDao', 'MessageDao', 'MessageJdbcDao']),
   ('Vistas', [V + 'inquiry/received.jsp', V + 'inquiry/sent.jsp', V + 'inquiry/detail.jsp', G + 'inquiry-nav.tag', G + 'inquiry-status.tag', G + 'inbox-group-header.tag', G + 'inbox-last-message.tag', G + 'filter-chips.tag', G + 'confirm-dialog.tag', W + 'js/confirm-action.js', W + 'js/submit-once.js', W + 'js/sale-detail.js']),
   ('Tests', ['InquiryServiceImplTest', 'InquiryStatusFilterTest', 'InquiryJdbcDaoTest', 'MessageJdbcDaoTest', 'ReceiptTest'])]),

 ('Reseñas y perfiles', 'Lo que pasa después de una venta y las dos caras del perfil: la privada y la pública.',
  ['Reviews flow', 'Profile flow', 'Public profile flow'],
  ['¿Quién puede reseñar a quién y cuándo?', '¿Cómo se cambia la contraseña con sesión iniciada y qué pasa después?', '¿Qué datos de una cuenta son públicos?'],
  [('Reseñas', ['ReviewService', 'ReviewServiceImpl', 'ReviewDao', 'ReviewJdbcDao', 'ReviewForm', 'InvalidReviewException', G + 'star-rating-input.tag', G + 'rating.tag', G + 'review-content.tag', G + 'user-byline.tag']),
   ('Perfil privado', ['ProfileController', 'ProfileForm', 'ChangePasswordForm', 'AvatarForm', 'AvatarFormValidator', 'ValidAvatarForm', V + 'profile/index.jsp', G + 'account-nav.tag', G + 'avatar.tag', W + 'js/account-edit.js']),
   ('Perfil público', ['PublicProfileController', 'PublicProfileService', 'PublicProfileServiceImpl', V + 'profile/public.jsp']),
   ('Tests', ['ReviewServiceImplTest', 'ReviewJdbcDaoTest', 'PublicProfileServiceImplTest'])]),

 ('Carrito', 'La funcionalidad más nueva: junta todo lo anterior (contacto, direcciones, bloqueos, correo) en una operación en lote.',
  ['Cart flow'],
  ['¿Qué pasa al enviar el carrito si un vinilo ya no está disponible?', '¿Por qué los posts se bloquean en orden de id?', '¿Cuántos correos salen y a quién?'],
  [('Web', ['CartController', 'CartCountAdvice', 'CartExceptionAdvice', V + 'cart/index.jsp']),
   ('Service y persistencia', ['CartService', 'CartServiceImpl', 'CartAddRejectedException', 'NothingToSendException', 'CartItemDao', 'CartItemJdbcDao']),
   ('Tests', ['CartServiceImplTest', 'CartItemJdbcDaoTest'])]),

 ('Errores', 'Cómo una excepción de negocio se convierte en una respuesta HTTP.',
  ['Validation and errors'],
  ['¿Cuándo responde 403 y cuándo 404?', '¿Qué es un 409 en este proyecto?', '¿Dónde se valida y por qué dos veces?'],
  [('Handlers y páginas', ['ErrorResponseAdvice', 'ErrorController', V + 'error/400.jsp', V + 'error/403.jsp', V + 'error/404.jsp', V + 'error/409.jsp'])]),

 ('Interfaz compartida', 'Los componentes JSP, estilos e imágenes que usan todas las páginas.',
  ['UI components', 'UI styles and tokens', 'Views and assets'],
  ['¿Cómo se evita XSS en las vistas?', '¿Por qué todas las URL pasan por c:url?', '¿Qué funciona sin JavaScript?'],
  [('Estructura de página', [G + 'head.tag', G + 'site-header.tag', G + 'brand.tag', G + 'back-link.tag']),
   ('Texto y acciones', [G + 'h1.tag', G + 'h3.tag', G + 'p.tag', G + 'span.tag', G + 'icon.tag', G + 'button.tag']),
   ('Controles de formulario', [G + 'text-input.tag', G + 'input-control.tag', G + 'textarea.tag', G + 'select.tag', G + 'select-control.tag', G + 'segmented-control.tag']),
   ('Estilos e imágenes', [W + 'css/tokens.css', W + 'css/components.css', W + 'css/style.css', W + 'images/logo.svg'])]),

 ('Textos', 'Los bundles de mensajes. No hace falta leerlos enteros: recorré los prefijos y compará un mismo bloque en los tres idiomas.',
  ['Localization'],
  ['¿Cómo se elige el idioma de una página y el de un correo?', '¿Qué pasa si falta una key?'],
  [('Bundles', [R + 'i18n/messages.properties', R + 'i18n/messages_en.properties', R + 'i18n/messages_fr.properties', R + 'i18n/messages_es.properties'])]),

 ('Herramientas del repositorio', 'Chequeos previos al commit y material para agentes de código. No forma parte de la aplicación.',
  ['Development tools', 'Repository tooling', 'Testing and evidence'],
  ['¿Qué verifica cada chequeo y qué error evita?', '¿Qué prueban los tests y qué no?'],
  [('Chequeos', ['tools/paw_checks.py', 'tools/git-hooks/pre-commit']),
   ('Hooks de Claude Code', ['.claude/hooks/*']),
   ('Procedimientos para agentes (lectura opcional)', ['.claude/skills/**', '.agents/skills/**', '.codex/prompts/**'])]),

 ('Historia: especificaciones, planes e issues', 'Para entender por qué algo es como es. Leé la especificación de una funcionalidad después de haber leído su código.',
  ['History and specifications', 'Recent changes 2026-10-05', 'Recent changes 2026-10-04', 'Known gaps and document drift'],
  ['¿Qué observó la cátedra en el sprint 2 y cómo se resolvió?', '¿Qué documentos del repositorio quedaron desactualizados?'],
  [('Especificaciones', ['docs/specs/**']),
   ('Planes', ['docs/plans/**']),
   ('Issues', ['docs/issues/**'])]),
]
