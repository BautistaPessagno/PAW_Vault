---
title: "SearchSuggestion"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/SearchSuggestion.java"]
---

# SearchSuggestion

Autocomplete entry for the global catalog search: a [[SearchSuggestionType]], the displayed value and, for albums, the artist name. [[PostJdbcDao]] builds these only from AVAILABLE publications, and search/suggestions.jsp renders them as listbox options.

## Connections

Project types referenced: [[SearchSuggestionType]].

Referenced by: [[PostDao]], [[PostJdbcDao]], [[PostJdbcDaoTest]], [[PostService]], [[PostServiceImpl]], [[PostServiceImplTest]].

## Exact source

[models/src/main/java/ar/edu/itba/paw/models/SearchSuggestion.java, lines 1–25](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/SearchSuggestion.java>)

```java
package ar.edu.itba.paw.models;

public class SearchSuggestion {
    private final SearchSuggestionType type;
    private final String value;
    private final String artistName;

    public SearchSuggestion(final SearchSuggestionType type, final String value, final String artistName) {
        this.type = type;
        this.value = value;
        this.artistName = artistName;
    }

    public SearchSuggestionType getType() {
        return type;
    }

    public String getValue() {
        return value;
    }

    public String getArtistName() {
        return artistName;
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
