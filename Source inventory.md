---
title: "Source inventory"
categories: ["Navigation"]
type: "index"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "041ce34404963b689d05443ca00abb7e75aa7f15"
status: "documented"
tags: ["codemap", "navigation"]
---

# Source inventory

This register accounts for all 196 tracked paths at `041ce34404963b689d05443ca00abb7e75aa7f15`. Every production Java and test Java file has a dedicated note. Resources are grouped by mechanism; agent workflow files are indexed as tooling rather than described as application behavior.

External source links use file URLs to open absolute local repository paths. Line numbers are recorded in excerpt labels; opening a file does not guarantee that the default editor jumps to the line. The adjacent wikilink opens the vault explanation. Exact source excerpts are a dated snapshot; the repository remains the authority when it changes. Ignored credentials, generated target output, .git metadata and local plans are excluded from the tracked-source count.

## models

| Source path | Vault explanation |
|---|---|
| [models/.mvn/jvm.config](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/.mvn/jvm.config>) | [[Build and dependencies]] |
| [models/.mvn/maven.config](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/.mvn/maven.config>) | [[Build and dependencies]] |
| [models/pom.xml](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/pom.xml>) | [[Build and dependencies]] |
| [models/src/main/java/ar/edu/itba/paw/models/Album.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Album.java>) | [[Album]] |
| [models/src/main/java/ar/edu/itba/paw/models/AlbumSummary.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/AlbumSummary.java>) | [[AlbumSummary]] |
| [models/src/main/java/ar/edu/itba/paw/models/Artist.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Artist.java>) | [[Artist]] |
| [models/src/main/java/ar/edu/itba/paw/models/Post.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Post.java>) | [[Post]] |
| [models/src/main/java/ar/edu/itba/paw/models/PostSummary.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/PostSummary.java>) | [[PostSummary]] |
| [models/src/main/java/ar/edu/itba/paw/models/User.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/User.java>) | [[User]] |
| [models/src/main/resources/.gitkeep](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/src/main/resources/.gitkeep>) | [[Build and dependencies]] |

## persistence-contracts

| Source path | Vault explanation |
|---|---|
| [persistence-contracts/.mvn/jvm.config](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence-contracts/.mvn/jvm.config>) | [[Build and dependencies]] |
| [persistence-contracts/.mvn/maven.config](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence-contracts/.mvn/maven.config>) | [[Build and dependencies]] |
| [persistence-contracts/pom.xml](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence-contracts/pom.xml>) | [[Build and dependencies]] |
| [persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/AlbumDao.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/AlbumDao.java>) | [[AlbumDao]] |
| [persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/ArtistDao.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/ArtistDao.java>) | [[ArtistDao]] |
| [persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/DuplicatePostKeyException.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/DuplicatePostKeyException.java>) | [[DuplicatePostKeyException]] |
| [persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/PostDao.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/PostDao.java>) | [[PostDao]] |
| [persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/UserDao.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/UserDao.java>) | [[UserDao]] |

## persistence

| Source path | Vault explanation |
|---|---|
| [persistence/.mvn/jvm.config](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/.mvn/jvm.config>) | [[Build and dependencies]] |
| [persistence/.mvn/maven.config](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/.mvn/maven.config>) | [[Build and dependencies]] |
| [persistence/pom.xml](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/pom.xml>) | [[Build and dependencies]] |
| [persistence/src/main/java/ar/edu/itba/paw/persistence/AlbumJdbcDao.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/AlbumJdbcDao.java>) | [[AlbumJdbcDao]] |
| [persistence/src/main/java/ar/edu/itba/paw/persistence/ArtistJdbcDao.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/ArtistJdbcDao.java>) | [[ArtistJdbcDao]] |
| [persistence/src/main/java/ar/edu/itba/paw/persistence/PostJdbcDao.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/PostJdbcDao.java>) | [[PostJdbcDao]] |
| [persistence/src/main/java/ar/edu/itba/paw/persistence/UserJdbcDao.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/UserJdbcDao.java>) | [[UserJdbcDao]] |
| [persistence/src/main/resources/db/migration/V1__convert_artist_to_entity.sql](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/main/resources/db/migration/V1__convert_artist_to_entity.sql>) | [[Schema history and seeds]] |
| [persistence/src/main/resources/db/migration/V2__create_posts.sql](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/main/resources/db/migration/V2__create_posts.sql>) | [[Schema history and seeds]] |
| [persistence/src/main/resources/db/migration/V3__seed_initial_post.sql](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/main/resources/db/migration/V3__seed_initial_post.sql>) | [[Schema history and seeds]] |
| [persistence/src/main/resources/schema.sql](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/main/resources/schema.sql>) | [[Database schema]] |
| [persistence/src/test/java/ar/edu/itba/paw/persistence/AlbumJdbcDaoTest.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/AlbumJdbcDaoTest.java>) | [[AlbumJdbcDaoTest]] |
| [persistence/src/test/java/ar/edu/itba/paw/persistence/ArtistJdbcDaoTest.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/ArtistJdbcDaoTest.java>) | [[ArtistJdbcDaoTest]] |
| [persistence/src/test/java/ar/edu/itba/paw/persistence/PostJdbcDaoTest.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/PostJdbcDaoTest.java>) | [[PostJdbcDaoTest]] |
| [persistence/src/test/java/ar/edu/itba/paw/persistence/TestConfiguration.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/TestConfiguration.java>) | [[TestConfiguration]] |
| [persistence/src/test/java/ar/edu/itba/paw/persistence/UserJdbcDaoTest.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/UserJdbcDaoTest.java>) | [[UserJdbcDaoTest]] |
| [persistence/src/test/resources/populator.sql](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/test/resources/populator.sql>) | [[Schema history and seeds]] |
| [persistence/src/test/resources/schema.sql](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/test/resources/schema.sql>) | [[Schema history and seeds]] |

## services-contracts

| Source path | Vault explanation |
|---|---|
| [services-contracts/.mvn/jvm.config](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/.mvn/jvm.config>) | [[Build and dependencies]] |
| [services-contracts/.mvn/maven.config](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/.mvn/maven.config>) | [[Build and dependencies]] |
| [services-contracts/pom.xml](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/pom.xml>) | [[Build and dependencies]] |
| [services-contracts/src/main/java/ar/edu/itba/paw/services/AlbumService.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/AlbumService.java>) | [[AlbumService]] |
| [services-contracts/src/main/java/ar/edu/itba/paw/services/ArtistService.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/ArtistService.java>) | [[ArtistService]] |
| [services-contracts/src/main/java/ar/edu/itba/paw/services/ConcurrentPublishException.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/ConcurrentPublishException.java>) | [[ConcurrentPublishException]] |
| [services-contracts/src/main/java/ar/edu/itba/paw/services/DuplicatePostException.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/DuplicatePostException.java>) | [[DuplicatePostException]] |
| [services-contracts/src/main/java/ar/edu/itba/paw/services/EmailService.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/EmailService.java>) | [[EmailService]] |
| [services-contracts/src/main/java/ar/edu/itba/paw/services/PostInterestNotification.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/PostInterestNotification.java>) | [[PostInterestNotification]] |
| [services-contracts/src/main/java/ar/edu/itba/paw/services/PostNotFoundException.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/PostNotFoundException.java>) | [[PostNotFoundException]] |
| [services-contracts/src/main/java/ar/edu/itba/paw/services/PostService.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/PostService.java>) | [[PostService]] |
| [services-contracts/src/main/java/ar/edu/itba/paw/services/UserService.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/UserService.java>) | [[UserService]] |
| [services-contracts/src/main/java/ar/edu/itba/paw/services/exceptions/EmailDeliveryException.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/exceptions/EmailDeliveryException.java>) | [[EmailDeliveryException]] |

## services

| Source path | Vault explanation |
|---|---|
| [services/.mvn/jvm.config](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/.mvn/jvm.config>) | [[Build and dependencies]] |
| [services/.mvn/maven.config](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/.mvn/maven.config>) | [[Build and dependencies]] |
| [services/pom.xml](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/pom.xml>) | [[Build and dependencies]] |
| [services/src/main/java/ar/edu/itba/paw/services/AlbumServiceImpl.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/AlbumServiceImpl.java>) | [[AlbumServiceImpl]] |
| [services/src/main/java/ar/edu/itba/paw/services/ArtistServiceImpl.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/ArtistServiceImpl.java>) | [[ArtistServiceImpl]] |
| [services/src/main/java/ar/edu/itba/paw/services/EmailServiceImpl.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/EmailServiceImpl.java>) | [[EmailServiceImpl]] |
| [services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java>) | [[PostServiceImpl]] |
| [services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java>) | [[UserServiceImpl]] |
| [services/src/main/resources/mail/post-interest.html](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/main/resources/mail/post-interest.html>) | [[Mail delivery]] |
| [services/src/main/resources/mail/welcome.html](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/main/resources/mail/welcome.html>) | [[Mail delivery]] |
| [services/src/test/java/ar/edu/itba/paw/services/AlbumServiceImplTest.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/AlbumServiceImplTest.java>) | [[AlbumServiceImplTest]] |
| [services/src/test/java/ar/edu/itba/paw/services/ArtistServiceImplTest.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/ArtistServiceImplTest.java>) | [[ArtistServiceImplTest]] |
| [services/src/test/java/ar/edu/itba/paw/services/EmailServiceImplTest.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/EmailServiceImplTest.java>) | [[EmailServiceImplTest]] |
| [services/src/test/java/ar/edu/itba/paw/services/PostServiceImplTest.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/PostServiceImplTest.java>) | [[PostServiceImplTest]] |
| [services/src/test/java/ar/edu/itba/paw/services/UserServiceImplTest.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/UserServiceImplTest.java>) | [[UserServiceImplTest]] |

## webapp

| Source path | Vault explanation |
|---|---|
| [webapp/.mvn/jvm.config](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/.mvn/jvm.config>) | [[Build and dependencies]] |
| [webapp/.mvn/maven.config](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/.mvn/maven.config>) | [[Build and dependencies]] |
| [webapp/pom.xml](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/pom.xml>) | [[Build and dependencies]] |
| [webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java>) | [[WebConfig]] |
| [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/HelloWorldController.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/HelloWorldController.java>) | [[HelloWorldController]] |
| [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/LandingController.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/LandingController.java>) | [[LandingController]] |
| [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PostContactController.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PostContactController.java>) | [[PostContactController]] |
| [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublishController.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublishController.java>) | [[PublishController]] |
| [webapp/src/main/java/ar/edu/itba/paw/webapp/exceptions/UserNotFoundException.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/exceptions/UserNotFoundException.java>) | [[UserNotFoundException]] |
| [webapp/src/main/java/ar/edu/itba/paw/webapp/form/ContactForm.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/ContactForm.java>) | [[ContactForm]] |
| [webapp/src/main/java/ar/edu/itba/paw/webapp/form/PublishForm.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/PublishForm.java>) | [[PublishForm]] |
| [webapp/src/main/java/ar/edu/itba/paw/webapp/form/UserForm.java](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/UserForm.java>) | [[UserForm]] |
| [webapp/src/main/resources/database.properties.example](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/resources/database.properties.example>) | [[Configuration and running]] |
| [webapp/src/main/resources/i18n/messages.properties](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/resources/i18n/messages.properties>) | [[Localization]] |
| [webapp/src/main/resources/i18n/messages_en.properties](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/resources/i18n/messages_en.properties>) | [[Localization]] |
| [webapp/src/main/resources/i18n/messages_es.properties](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/resources/i18n/messages_es.properties>) | [[Localization]] |
| [webapp/src/main/resources/i18n/messages_fr.properties](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/resources/i18n/messages_fr.properties>) | [[Localization]] |
| [webapp/src/main/resources/logback-test.xml](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/resources/logback-test.xml>) | [[Logging]] |
| [webapp/src/main/resources/logback.xml](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/resources/logback.xml>) | [[Logging]] |
| [webapp/src/main/resources/mail.properties.example](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/resources/mail.properties.example>) | [[Configuration and running]] |
| [webapp/src/main/webapp/WEB-INF/views/helloworld/create.jsp](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/helloworld/create.jsp>) | [[Views and assets]] |
| [webapp/src/main/webapp/WEB-INF/views/helloworld/index.jsp](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/helloworld/index.jsp>) | [[Views and assets]] |
| [webapp/src/main/webapp/WEB-INF/views/landing/index.jsp](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/landing/index.jsp>) | [[Views and assets]] |
| [webapp/src/main/webapp/WEB-INF/views/post/contact.jsp](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/post/contact.jsp>) | [[Views and assets]] |
| [webapp/src/main/webapp/WEB-INF/views/publish/index.jsp](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/publish/index.jsp>) | [[Views and assets]] |
| [webapp/src/main/webapp/WEB-INF/web.xml](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/web.xml>) | [[Startup and dependency injection]] |
| [webapp/src/main/webapp/css/style.css](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/css/style.css>) | [[UI styles and tokens]] |
| [webapp/src/main/webapp/images/covers/versus.png](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/images/covers/versus.png>) | [[Views and assets]] |

## database

| Source path | Vault explanation |
|---|---|
| [database/albums.sql](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/database/albums.sql>) | [[Schema history and seeds]] |
| [database/seed_dev_posts.sql](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/database/seed_dev_posts.sql>) | [[Schema history and seeds]] |
| [database/users.sql](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/database/users.sql>) | [[Schema history and seeds]] |

## tools

| Source path | Vault explanation |
|---|---|
| [tools/git-hooks/pre-commit](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/tools/git-hooks/pre-commit>) | [[Development tools]] |
| [tools/paw_checks.py](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/tools/paw_checks.py>) | [[Development tools]] |
| [tools/setup_local_postgres.sh](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/tools/setup_local_postgres.sh>) | [[Development tools]] |

## docs

| Source path | Vault explanation |
|---|---|
| [docs/adr/0001-establish-quiero-vinilos-domain.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/adr/0001-establish-quiero-vinilos-domain.md>) | [[History and specifications]] |
| [docs/adr/0002-own-the-album-catalog-locally.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/adr/0002-own-the-album-catalog-locally.md>) | [[History and specifications]] |
| [docs/issues/01-mostrar-primer-album-en-landing.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/issues/01-mostrar-primer-album-en-landing.md>) | [[History and specifications]] |
| [docs/issues/02-completar-catalogo-inicial.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/issues/02-completar-catalogo-inicial.md>) | [[History and specifications]] |
| [docs/issues/03-terminar-landing-editorial-responsive.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/issues/03-terminar-landing-editorial-responsive.md>) | [[History and specifications]] |
| [docs/issues/publicacion-albumes/01-convertir-artist-en-entidad.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/issues/publicacion-albumes/01-convertir-artist-en-entidad.md>) | [[History and specifications]] |
| [docs/issues/publicacion-albumes/02-publicar-album-nuevo.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/issues/publicacion-albumes/02-publicar-album-nuevo.md>) | [[History and specifications]] |
| [docs/issues/publicacion-albumes/03-reutilizar-catalogo-en-publicaciones.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/issues/publicacion-albumes/03-reutilizar-catalogo-en-publicaciones.md>) | [[History and specifications]] |
| [docs/issues/publicacion-albumes/04-rechazar-posts-duplicados.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/issues/publicacion-albumes/04-rechazar-posts-duplicados.md>) | [[History and specifications]] |
| [docs/issues/publicacion-mailing/01-contactar-publicante-desde-post.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/issues/publicacion-mailing/01-contactar-publicante-desde-post.md>) | [[History and specifications]] |
| [docs/issues/publicacion-mailing/02-recuperarse-de-fallo-de-entrega.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/issues/publicacion-mailing/02-recuperarse-de-fallo-de-entrega.md>) | [[History and specifications]] |
| [docs/setup.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/setup.md>) | [[History and specifications]] |
| [docs/specs/feature_contacto-post_20260904.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/specs/feature_contacto-post_20260904.md>) | [[History and specifications]] |
| [docs/specs/feature_publicacion-albumes_20260904.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/specs/feature_publicacion-albumes_20260904.md>) | [[History and specifications]] |
| [docs/specs/landing-quiero-vinilos.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/specs/landing-quiero-vinilos.md>) | [[History and specifications]] |

## .agents

| Source path | Vault explanation |
|---|---|
| [.agents/skills/README.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.agents/skills/README.md>) | [[Repository tooling]] |
| [.agents/skills/bug/SKILL.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.agents/skills/bug/SKILL.md>) | [[Repository tooling]] |
| [.agents/skills/corrector-eyes/SKILL.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.agents/skills/corrector-eyes/SKILL.md>) | [[Repository tooling]] |
| [.agents/skills/design/SKILL.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.agents/skills/design/SKILL.md>) | [[Repository tooling]] |
| [.agents/skills/enhancer/SKILL.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.agents/skills/enhancer/SKILL.md>) | [[Repository tooling]] |
| [.agents/skills/feature-engineering/SKILL.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.agents/skills/feature-engineering/SKILL.md>) | [[Repository tooling]] |
| [.agents/skills/feature-engineering/context.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.agents/skills/feature-engineering/context.md>) | [[Repository tooling]] |
| [.agents/skills/forensic-audit/SKILL.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.agents/skills/forensic-audit/SKILL.md>) | [[Repository tooling]] |
| [.agents/skills/frontend-analyzer/SKILL.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.agents/skills/frontend-analyzer/SKILL.md>) | [[Repository tooling]] |
| [.agents/skills/frontend-analyzer/context.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.agents/skills/frontend-analyzer/context.md>) | [[Repository tooling]] |
| [.agents/skills/frontend-analyzer/scripts/research.py](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.agents/skills/frontend-analyzer/scripts/research.py>) | [[Repository tooling]] |
| [.agents/skills/general-audit/SKILL.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.agents/skills/general-audit/SKILL.md>) | [[Repository tooling]] |
| [.agents/skills/good-practice/SKILL.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.agents/skills/good-practice/SKILL.md>) | [[Repository tooling]] |
| [.agents/skills/handoff/SKILL.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.agents/skills/handoff/SKILL.md>) | [[Repository tooling]] |
| [.agents/skills/i18n-sync/SKILL.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.agents/skills/i18n-sync/SKILL.md>) | [[Repository tooling]] |
| [.agents/skills/implementation/SKILL.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.agents/skills/implementation/SKILL.md>) | [[Repository tooling]] |
| [.agents/skills/jdbc-to-jpa/SKILL.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.agents/skills/jdbc-to-jpa/SKILL.md>) | [[Repository tooling]] |
| [.agents/skills/planning/SKILL.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.agents/skills/planning/SKILL.md>) | [[Repository tooling]] |
| [.agents/skills/pre-delivery/SKILL.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.agents/skills/pre-delivery/SKILL.md>) | [[Repository tooling]] |
| [.agents/skills/skillset-port/SKILL.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.agents/skills/skillset-port/SKILL.md>) | [[Repository tooling]] |
| [.agents/skills/smoke/SKILL.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.agents/skills/smoke/SKILL.md>) | [[Repository tooling]] |
| [.agents/skills/wiki-sync/SKILL.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.agents/skills/wiki-sync/SKILL.md>) | [[Repository tooling]] |

## .claude

| Source path | Vault explanation |
|---|---|
| [.claude/hooks/commit-gate.py](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.claude/hooks/commit-gate.py>) | [[Repository tooling]] |
| [.claude/hooks/db-server-guard.py](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.claude/hooks/db-server-guard.py>) | [[Repository tooling]] |
| [.claude/hooks/i18n-parity-posttool.py](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.claude/hooks/i18n-parity-posttool.py>) | [[Repository tooling]] |
| [.claude/hooks/skill-autolaunch.py](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.claude/hooks/skill-autolaunch.py>) | [[Repository tooling]] |
| [.claude/scripts/paw_checks.py](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.claude/scripts/paw_checks.py>) | [[Repository tooling]] |
| [.claude/skills/README.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.claude/skills/README.md>) | [[Repository tooling]] |
| [.claude/skills/bug/SKILL.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.claude/skills/bug/SKILL.md>) | [[Repository tooling]] |
| [.claude/skills/corrector-eyes/SKILL.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.claude/skills/corrector-eyes/SKILL.md>) | [[Repository tooling]] |
| [.claude/skills/design/SKILL.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.claude/skills/design/SKILL.md>) | [[Repository tooling]] |
| [.claude/skills/enhancer/SKILL.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.claude/skills/enhancer/SKILL.md>) | [[Repository tooling]] |
| [.claude/skills/feature-engineering/SKILL.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.claude/skills/feature-engineering/SKILL.md>) | [[Repository tooling]] |
| [.claude/skills/feature-engineering/context.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.claude/skills/feature-engineering/context.md>) | [[Repository tooling]] |
| [.claude/skills/forensic-audit/SKILL.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.claude/skills/forensic-audit/SKILL.md>) | [[Repository tooling]] |
| [.claude/skills/frontend-analyzer/SKILL.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.claude/skills/frontend-analyzer/SKILL.md>) | [[Repository tooling]] |
| [.claude/skills/frontend-analyzer/context.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.claude/skills/frontend-analyzer/context.md>) | [[Repository tooling]] |
| [.claude/skills/frontend-analyzer/scripts/research.py](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.claude/skills/frontend-analyzer/scripts/research.py>) | [[Repository tooling]] |
| [.claude/skills/general-audit/SKILL.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.claude/skills/general-audit/SKILL.md>) | [[Repository tooling]] |
| [.claude/skills/good-practice/SKILL.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.claude/skills/good-practice/SKILL.md>) | [[Repository tooling]] |
| [.claude/skills/handoff/SKILL.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.claude/skills/handoff/SKILL.md>) | [[Repository tooling]] |
| [.claude/skills/i18n-sync/SKILL.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.claude/skills/i18n-sync/SKILL.md>) | [[Repository tooling]] |
| [.claude/skills/implementation/SKILL.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.claude/skills/implementation/SKILL.md>) | [[Repository tooling]] |
| [.claude/skills/jdbc-to-jpa/SKILL.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.claude/skills/jdbc-to-jpa/SKILL.md>) | [[Repository tooling]] |
| [.claude/skills/planning/SKILL.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.claude/skills/planning/SKILL.md>) | [[Repository tooling]] |
| [.claude/skills/pre-delivery/SKILL.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.claude/skills/pre-delivery/SKILL.md>) | [[Repository tooling]] |
| [.claude/skills/skillset-port/SKILL.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.claude/skills/skillset-port/SKILL.md>) | [[Repository tooling]] |
| [.claude/skills/smoke/SKILL.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.claude/skills/smoke/SKILL.md>) | [[Repository tooling]] |
| [.claude/skills/wiki-sync/SKILL.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.claude/skills/wiki-sync/SKILL.md>) | [[Repository tooling]] |

## .codex

| Source path | Vault explanation |
|---|---|
| [.codex/prompts/bug.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.codex/prompts/bug.md>) | [[Repository tooling]] |
| [.codex/prompts/corrector-eyes.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.codex/prompts/corrector-eyes.md>) | [[Repository tooling]] |
| [.codex/prompts/design.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.codex/prompts/design.md>) | [[Repository tooling]] |
| [.codex/prompts/enhancer.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.codex/prompts/enhancer.md>) | [[Repository tooling]] |
| [.codex/prompts/feature-engineering.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.codex/prompts/feature-engineering.md>) | [[Repository tooling]] |
| [.codex/prompts/forensic-audit.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.codex/prompts/forensic-audit.md>) | [[Repository tooling]] |
| [.codex/prompts/frontend-analyzer.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.codex/prompts/frontend-analyzer.md>) | [[Repository tooling]] |
| [.codex/prompts/general-audit.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.codex/prompts/general-audit.md>) | [[Repository tooling]] |
| [.codex/prompts/good-practice.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.codex/prompts/good-practice.md>) | [[Repository tooling]] |
| [.codex/prompts/handoff.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.codex/prompts/handoff.md>) | [[Repository tooling]] |
| [.codex/prompts/i18n-sync.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.codex/prompts/i18n-sync.md>) | [[Repository tooling]] |
| [.codex/prompts/implementation.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.codex/prompts/implementation.md>) | [[Repository tooling]] |
| [.codex/prompts/jdbc-to-jpa.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.codex/prompts/jdbc-to-jpa.md>) | [[Repository tooling]] |
| [.codex/prompts/planning.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.codex/prompts/planning.md>) | [[Repository tooling]] |
| [.codex/prompts/pre-delivery.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.codex/prompts/pre-delivery.md>) | [[Repository tooling]] |
| [.codex/prompts/skillset-port.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.codex/prompts/skillset-port.md>) | [[Repository tooling]] |
| [.codex/prompts/smoke.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.codex/prompts/smoke.md>) | [[Repository tooling]] |
| [.codex/prompts/wiki-sync.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.codex/prompts/wiki-sync.md>) | [[Repository tooling]] |

## root

| Source path | Vault explanation |
|---|---|
| [.gitignore](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/.gitignore>) | [[Repository tooling]] |
| [AGENTS.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/AGENTS.md>) | [[Repository tooling]] |
| [CLAUDE.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/CLAUDE.md>) | [[Repository tooling]] |
| [CONTEXT.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/CONTEXT.md>) | [[Domain and identity]] |
| [README.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/README.md>) | [[Configuration and running]] |
| [TODO.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/TODO.md>) | [[History and specifications]] |
| [pom.xml](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/pom.xml>) | [[Build and dependencies]] |

[[Home]] · [[Project snapshot]] · [[Verification record]]

## Committed UI additions

These nine files are now tracked: seven JSP tags and two CSS files. The four additional tags recorded in the provisional snapshot are absent from the current repository.

| Source path | Vault explanation |
|---|---|
| [webapp/src/main/webapp/WEB-INF/tags/button.tag](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/button.tag>) | [[UI components]] |
| [webapp/src/main/webapp/WEB-INF/tags/h1.tag](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/h1.tag>) | [[UI components]] |
| [webapp/src/main/webapp/WEB-INF/tags/h3.tag](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/h3.tag>) | [[UI components]] |
| [webapp/src/main/webapp/WEB-INF/tags/p.tag](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/p.tag>) | [[UI components]] |
| [webapp/src/main/webapp/WEB-INF/tags/span.tag](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/span.tag>) | [[UI components]] |
| [webapp/src/main/webapp/WEB-INF/tags/text-input.tag](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/text-input.tag>) | [[UI components]] |
| [webapp/src/main/webapp/WEB-INF/tags/vinyl-card.tag](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/vinyl-card.tag>) | [[UI components]] |
| [webapp/src/main/webapp/css/tokens.css](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/css/tokens.css>) | [[UI styles and tokens]] |
| [webapp/src/main/webapp/css/components.css](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/webapp/css/components.css>) | [[UI styles and tokens]] |
