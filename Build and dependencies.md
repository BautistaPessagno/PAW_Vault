---
title: "Build and dependencies"
categories: ["Operations", "Architecture"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["pom.xml", "models/pom.xml", "persistence-contracts/pom.xml", "persistence/pom.xml", "services-contracts/pom.xml", "services/pom.xml", "webapp/pom.xml"]
---

# Build and dependencies

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

Fuente exacta en `8929aea`: [pom.xml](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/pom.xml>), líneas 16–39.

```xml
  <properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <maven.compiler.source>21</maven.compiler.source>
    <maven.compiler.target>21</maven.compiler.target>
    <maven.compiler.parameters>true</maven.compiler.parameters>
    <org.springframework.version>5.3.33</org.springframework.version>
    <org.springframework.security.version>5.8.16</org.springframework.security.version>
    <servlet-api.version>4.0.1</servlet-api.version>
    <jstl.version>1.2</jstl.version>
    <postgresql.version>42.2.5</postgresql.version>
    <javax.validation-api.version>2.0.1.Final</javax.validation-api.version>
    <org.hibernate.validator>6.2.4.Final</org.hibernate.validator>
    <junit-jupiter.version>5.10.2</junit-jupiter.version>
    <mockito.version>5.12.0</mockito.version>
    <hsqldb.version>2.7.3</hsqldb.version>
    <flyway.version>9.22.3</flyway.version>
    <slf4j.version>1.7.36</slf4j.version>
    <logback.version>1.2.13</logback.version>
    <javax.mail.version>1.6.2</javax.mail.version>
    <thymeleaf.version>3.0.15.RELEASE</thymeleaf.version>
    <commons-fileupload.version>1.5</commons-fileupload.version>
    <jackson.version>2.15.2</jackson.version>
    <maven-antrun-plugin.version>3.1.0</maven-antrun-plugin.version>
  </properties>
```

### Perfil `pampero`

Fuente exacta en `8929aea`: [webapp/pom.xml](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/pom.xml>), líneas 173–221.

```xml
    <profile>
      <id>pampero</id>
      <build>
        <resources>
          <resource>
            <directory>src/main/resources</directory>
            <excludes>
              <exclude>database.properties</exclude>
              <exclude>mail.properties</exclude>
            </excludes>
          </resource>
          <resource>
            <directory>src/pampero/resources</directory>
            <includes>
              <include>database.properties</include>
              <include>mail.properties</include>
            </includes>
          </resource>
        </resources>
        <plugins>
          <plugin>
            <artifactId>maven-antrun-plugin</artifactId>
            <executions>
              <execution>
                <id>require-pampero-properties</id>
                <phase>validate</phase>
                <goals>
                  <goal>run</goal>
                </goals>
                <configuration>
                  <target>
                    <available file="${project.basedir}/src/pampero/resources/database.properties"
                               property="pampero.database.properties.present"/>
                    <available file="${project.basedir}/src/pampero/resources/mail.properties"
                               property="pampero.mail.properties.present"/>
                    <fail unless="pampero.database.properties.present">
                      Missing webapp/src/pampero/resources/database.properties. Copy the .example and fill the Pampero database configuration.
                    </fail>
                    <fail unless="pampero.mail.properties.present">
                      Missing webapp/src/pampero/resources/mail.properties. Copy the .example and fill the Pampero mail configuration.
                    </fail>
                  </target>
                </configuration>
              </execution>
            </executions>
          </plugin>
        </plugins>
      </build>
    </profile>
```

## Archivos para seguir el flujo

- [pom.xml](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/pom.xml>)
- [models/pom.xml](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/pom.xml>)
- [persistence-contracts/pom.xml](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence-contracts/pom.xml>)
- [persistence/pom.xml](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/pom.xml>)
- [services-contracts/pom.xml](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/pom.xml>)
- [services/pom.xml](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/pom.xml>)
- [webapp/pom.xml](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/pom.xml>)

Fuente inspeccionada: `8929aea`, 2026-10-04. Es evidencia estática; no implica ejecución de la aplicación. [[Source inventory]] · [[Roadmap de lectura]]
