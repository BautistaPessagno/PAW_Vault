@title: Build and dependencies
@categories: Operations, Architecture
@files: pom.xml, models/pom.xml, persistence-contracts/pom.xml, persistence/pom.xml, services-contracts/pom.xml, services/pom.xml, webapp/pom.xml

> [!summary] En una frase
> Un POM raíz fija todas las versiones y seis módulos hijos declaran solo qué usan; el resultado es un único `app.war` para Tomcat, y en desarrollo se corre con el plugin de Jetty.

## Herramientas y versiones

| Área | Dependencia | Versión | Para qué |
|---|---|---|---|
| Lenguaje | Java | 21 | `maven.compiler.source/target`, con `parameters=true` para que Spring lea los nombres de los parámetros |
| Web | Spring MVC (`spring-webmvc`) | 5.3.33 | Controllers, binding, vistas |
| Seguridad | Spring Security (`web`, `config`, `taglibs`) | 5.8.16 | Autenticación y autorización ([[Security and authorization]]) |
| Persistencia | Spring JDBC | 5.3.33 | `JdbcTemplate`, `SimpleJdbcInsert` |
| Base | PostgreSQL driver | 42.2.5 | Producción y desarrollo |
| Esquema | Flyway | 9.22.3 | Migraciones ([[Database schema]]) |
| Validación | `validation-api` 2.0.1 + Hibernate Validator 6.2.4 | | Bean Validation ([[Validation and errors]]) |
| Vistas | Servlet API 4.0.1, JSTL 1.2 | | JSP |
| Correo | `spring-context-support`, JavaMail 1.6.2, Thymeleaf 3.0.15 | | Envío y plantillas HTML de correo ([[Mail delivery]]) |
| Archivos | Commons FileUpload | 1.5 | Multipart ([[Cover image flow]]) |
| JSON | Jackson Databind | 2.15.2 | Respuestas de sugerencias ([[Search suggestions flow]]) |
| Logs | SLF4J 1.7.36 + Logback 1.2.13 | | [[Logging]] |
| Tests | JUnit Jupiter 5.10.2, Mockito 5.12.0, HSQLDB 2.7.3, `spring-test` | | [[Testing and evidence]] |
| Servidor local | Jetty Maven Plugin | 9.4.58 | `mvn jetty:run` en el puerto 8080 |

No hay Spring Boot ni JPA/Hibernate ORM: la cátedra los prohíbe en esta etapa. Thymeleaf se usa **solo** para el HTML de los correos; las páginas son JSP.

## Cómo se organiza

- El POM raíz es `packaging=pom`, lista los seis módulos y declara cada dependencia en `<dependencyManagement>` con su versión tomada de una `<property>`.
- Cada módulo hijo declara `groupId` y `artifactId`, sin versión. Así no puede haber dos versiones de lo mismo.
- Los módulos hermanos también están en `<dependencyManagement>`. El scope `runtime` de las implementaciones se declara en el hijo que las consume ([[Architecture]]).
- `webapp` es `packaging=war` con `finalName=app`: el artefacto es `webapp/target/app.war`.

## Qué depende de qué

| Módulo | Depende de |
|---|---|
| `models` | Nada |
| `persistence-contracts` | `models` |
| `persistence` | `persistence-contracts`, Spring JDBC, driver PostgreSQL; en test: HSQLDB, Flyway, `spring-test`, JUnit |
| `services-contracts` | `models` |
| `services` | `services-contracts`, `persistence-contracts`, `persistence` (runtime), `spring-tx`, correo, Thymeleaf; en test: JUnit, Mockito |
| `webapp` | `services-contracts`, `services` (runtime), `persistence` (runtime), Spring MVC, Security, Flyway, validación, JSTL, Jackson, FileUpload, Logback |

`webapp` depende de `flyway-core` y `spring-jdbc` porque la configuración (`WebConfig`) crea el `DataSource` y el bean de Flyway.

## Comandos

Todos desde la raíz del repositorio.

| Comando | Qué hace |
|---|---|
| `mvn clean package` | Compila, corre tests y arma el WAR con la configuración local |
| `mvn clean package -Ppampero` | Arma el WAR para el servidor de la cátedra ([[Configuration and running]]) |
| `mvn clean install` | Instala los módulos en el repositorio local; hace falta antes de correr `webapp` solo |
| `cd webapp && mvn jetty:run` | Levanta la aplicación en `http://localhost:8080` |
| `mvn test` | Todos los tests |
| `mvn test -pl persistence` / `-pl services` | Tests de un módulo |
| `mvn test -pl persistence -Dtest=UserJdbcDaoTest` | Una clase de test |
| `python3 tools/paw_checks.py all` | Chequeos propios: paridad de i18n, versiones Flyway, balance de tags JSTL ([[Development tools]]) |

## El perfil `pampero`

El servidor de la cátedra recibe solo el WAR por SFTP: no se le pueden pasar variables de entorno. El perfil resuelve la configuración en tiempo de build:

1. Excluye `database.properties` y `mail.properties` de `src/main/resources`.
2. Incluye los de `src/pampero/resources`.
3. En la fase `validate`, una tarea `antrun` **falla el build** si esos dos archivos no existen, con un mensaje que dice cuál falta.

Los cuatro archivos reales están en `.gitignore`; solo se versionan los `.example`.

## Decisiones y por qué

| Decisión | Motivo | Fuente |
|---|---|---|
| Versiones solo en el POM raíz, vía propiedades | Un solo lugar para actualizar; ningún hijo puede desalinearse | `docs/setup.md` |
| Spring 5 clásico con WAR | Requisito de la cátedra; Spring Boot está penalizado | `docs/setup.md` |
| Perfil Maven para producción | El despliegue no admite configuración externa al WAR | `docs/setup.md` |
| El build falla si faltan las propiedades de Pampero | Evitar subir un WAR sin configuración, que fallaría al arrancar | `webapp/pom.xml` |
| `useTestScope` en Jetty | Que el plugin vea las dependencias de scope test al correr en desarrollo | `pom.xml` (el motivo es inferencia) |

## Preguntas de defensa

**¿Cómo se construye y se despliega?**
`mvn clean package -Ppampero` genera `app.war` con las propiedades del servidor adentro; ese archivo se sube por SFTP.

**¿Por qué las versiones están en el POM raíz?**
Para que todos los módulos usen la misma. Los hijos no declaran versión.

**¿Usan Thymeleaf para las vistas?**
No. Las páginas son JSP con JSTL; Thymeleaf procesa únicamente las plantillas HTML de los correos.

**¿Por qué `services` tiene `persistence` como dependencia runtime?**
Para que esté en el classpath al ejecutar y en los tests, pero el código de `services` solo pueda compilar contra las interfaces.

## Evidencia de código

### Versiones

{{code:pom.xml:16-39}}

### Perfil `pampero`

{{code:webapp/pom.xml:173-221}}
