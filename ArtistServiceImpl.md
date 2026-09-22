---
title: "ArtistServiceImpl"
categories: ["Services"]
type: "code"
module: "services"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["services/src/main/java/ar/edu/itba/paw/services/ArtistServiceImpl.java"]
---

# ArtistServiceImpl

Trims the display name and derives identity from lowercase letters and digits only (accented letters kept, spaces and punctuation dropped) before findOrCreate. resolveForEdit rewrites the shared display name when it differs. findSuggestions returns nothing for queries over 255 characters or without letters/digits, compacts the rest with [[SearchText]] and asks the DAO for five matches.

## Connections

Project types referenced: [[Artist]], [[ArtistDao]], [[ArtistService]], [[SearchText]].

Referenced by: [[ArtistServiceImplTest]].

## Exact source

[services/src/main/java/ar/edu/itba/paw/services/ArtistServiceImpl.java, lines 1–64](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/ArtistServiceImpl.java>)

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

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
