---
title: "PaymentInfoRules"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/PaymentInfoRules.java"]
---

# PaymentInfoRules

Formato de los datos de cobro: CBU de 22 dígitos con sus dos dígitos verificadores y alias de 6 a 20 caracteres. Normaliza y valida igual en el formulario y en [[UserServiceImpl]].

## Guía de lectura

Datos y dependencias declaradas: `CBU_LENGTH`, `ALIAS_MIN_LENGTH`, `ALIAS_MAX_LENGTH`, `ALIAS_PATTERN`, `FIRST_BLOCK_LENGTH`, `FIRST_BLOCK_WEIGHTS`, `SECOND_BLOCK_WEIGHTS`, `BASE`.

Operaciones para localizar en la fuente: `normalizeCbu`, `normalizeAlias`, `isValidCbu`, `isValidAlias`, `blankToNull`, `hasValidCheckDigit`.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[PaymentFormValidator]], [[UserServiceImpl]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [models/src/main/java/ar/edu/itba/paw/models/PaymentInfoRules.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/PaymentInfoRules.java>), líneas 1–56.

```java
package ar.edu.itba.paw.models;

import java.util.regex.Pattern;

// Formato de los datos de cobro, compartido por el formulario del perfil y por UserService.
public final class PaymentInfoRules {

    public static final int CBU_LENGTH = 22;
    public static final int ALIAS_MIN_LENGTH = 6;
    public static final int ALIAS_MAX_LENGTH = 20;

    private static final Pattern ALIAS_PATTERN =
            Pattern.compile("[A-Za-z0-9.-]{" + ALIAS_MIN_LENGTH + "," + ALIAS_MAX_LENGTH + "}");
    // CBU y CVU comparten formato: un bloque de 8 digitos (entidad y sucursal) y otro de 14
    // (cuenta), cada uno cerrado por un digito verificador con estos pesos.
    private static final int FIRST_BLOCK_LENGTH = 8;
    private static final int[] FIRST_BLOCK_WEIGHTS = {7, 1, 3, 9, 7, 1, 3};
    private static final int[] SECOND_BLOCK_WEIGHTS = {3, 9, 7, 1, 3, 9, 7, 1, 3, 9, 7, 1, 3};
    private static final int BASE = 10;

    private PaymentInfoRules() {
    }

    // El CBU se tipea en bloques: se descartan los espacios. Vacio queda en null.
    public static String normalizeCbu(final String cbu) {
        return blankToNull(cbu == null ? null : cbu.replaceAll("\\s", ""));
    }

    public static String normalizeAlias(final String alias) {
        return blankToNull(alias == null ? null : alias.trim());
    }

    public static boolean isValidCbu(final String cbu) {
        if (cbu == null || cbu.length() != CBU_LENGTH || !cbu.chars().allMatch(c -> c >= '0' && c <= '9')) {
            return false;
        }
        return hasValidCheckDigit(cbu.substring(0, FIRST_BLOCK_LENGTH), FIRST_BLOCK_WEIGHTS)
                && hasValidCheckDigit(cbu.substring(FIRST_BLOCK_LENGTH), SECOND_BLOCK_WEIGHTS);
    }

    public static boolean isValidAlias(final String alias) {
        return alias != null && ALIAS_PATTERN.matcher(alias).matches();
    }

    private static String blankToNull(final String value) {
        return value == null || value.isEmpty() ? null : value;
    }

    private static boolean hasValidCheckDigit(final String block, final int[] weights) {
        int sum = 0;
        for (int i = 0; i < weights.length; i++) {
            sum += (block.charAt(i) - '0') * weights[i];
        }
        return block.charAt(weights.length) - '0' == (BASE - sum % BASE) % BASE;
    }
}
```
