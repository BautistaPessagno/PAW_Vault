---
title: "SearchSuggestionType"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/SearchSuggestionType.java"]
---

# SearchSuggestionType

Suggestion kinds ARTIST and ALBUM. [[PostJdbcDao]] emits them as SQL literals and maps them back with valueOf; the fragment view localizes them through search.suggestion.<type>.

## Connections

Project types referenced: none.

Referenced by: [[PostJdbcDao]], [[PostJdbcDaoTest]], [[PostServiceImplTest]], [[SearchSuggestion]].

## Exact source

[models/src/main/java/ar/edu/itba/paw/models/SearchSuggestionType.java, lines 1–6](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/SearchSuggestionType.java>)

```java
package ar.edu.itba.paw.models;

public enum SearchSuggestionType {
    ARTIST,
    ALBUM
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
