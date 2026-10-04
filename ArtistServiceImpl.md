---
title: "ArtistServiceImpl"
categories: ["Services"]
type: "code"
module: "services"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["services/src/main/java/ar/edu/itba/paw/services/ArtistServiceImpl.java"]
---

# ArtistServiceImpl

Busca o crea el artista por identidad: el nombre en minúsculas, solo letras y dígitos. Al editar puede actualizar el nombre visible compartido. Sugerencias normalizadas con [[SearchText]], hasta 5.

## Guía de lectura

Datos y dependencias declaradas: `SUGGESTION_LIMIT`, `MAX_QUERY_LENGTH`, `artistDao`.

Operaciones para localizar en la fuente: `findOrCreate`, `resolveForEdit`, `findSuggestions`, `normalizeForIdentity`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Artist]], [[ArtistDao]], [[ArtistService]], [[SearchText]].

Referenciado por: [[ArtistServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [services/src/main/java/ar/edu/itba/paw/services/ArtistServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/ArtistServiceImpl.java>), líneas 1–64.

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Artist;
import ar.edu.itba.paw.models.SearchText;
import ar.edu.itba.paw.persistence.ArtistDao;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Locale;

@Service
public class ArtistServiceImpl implements ArtistService {

    private static final int SUGGESTION_LIMIT = 5;
    private static final int MAX_QUERY_LENGTH = 255;

    private final ArtistDao artistDao;

    @Autowired
    public ArtistServiceImpl(final ArtistDao artistDao) {
        this.artistDao = artistDao;
    }

    @Override
    @Transactional
    public Artist findOrCreate(final String name) {
        final String displayName = name.trim();
        return artistDao.findOrCreate(displayName, normalizeForIdentity(displayName));
    }

    @Override
    @Transactional
    public Artist resolveForEdit(final String name) {
        final String displayName = name.trim();
        final Artist artist = artistDao.findOrCreate(displayName, normalizeForIdentity(displayName));
        if (artist.getName().equals(displayName)) {
            return artist;
        }
        return artistDao.updateDisplayName(artist.getId(), displayName);
    }

    @Override
    @Transactional(readOnly = true)
    public List<Artist> findSuggestions(final String query) {
        if (query != null && query.length() > MAX_QUERY_LENGTH) {
            return List.of();
        }
        final String normalizedQuery = SearchText.compact(query);
        if (normalizedQuery.isEmpty()) {
            return List.of();
        }
        return artistDao.findSuggestions(normalizedQuery, SUGGESTION_LIMIT);
    }

    private static String normalizeForIdentity(final String name) {
        final StringBuilder normalized = new StringBuilder();
        name.toLowerCase(Locale.ROOT).codePoints()
                .filter(Character::isLetterOrDigit)
                .forEach(normalized::appendCodePoint);
        return normalized.toString();
    }
}
```
