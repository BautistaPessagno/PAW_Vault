---
title: "InquiryPage"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/InquiryPage.java"]
---

# InquiryPage

One page of [[InquiryGroup]] values with its page number and total pages. Inbox pagination counts publications rather than inquiries, so a group is never split across pages. hasPrevious and hasNext are derived from the known total and feed ui:pagination.

## Connections

Project types referenced: [[InquiryGroup]].

Referenced by: [[InquiryService]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]].

## Exact source

[models/src/main/java/ar/edu/itba/paw/models/InquiryPage.java, lines 1–37](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/InquiryPage.java>)

```java
package ar.edu.itba.paw.models;

import java.util.List;

// Pagina de la bandeja de consultas: se pagina por publicacion, no por consulta, para que
// un grupo nunca quede partido entre dos paginas.
public final class InquiryPage {
    private final List<InquiryGroup> groups;
    private final int pageNumber;
    private final int totalPages;

    public InquiryPage(final List<InquiryGroup> groups, final int pageNumber, final int totalPages) {
        this.groups = List.copyOf(groups);
        this.pageNumber = pageNumber;
        this.totalPages = totalPages;
    }

    public List<InquiryGroup> getGroups() {
        return groups;
    }

    public int getPageNumber() {
        return pageNumber;
    }

    public int getTotalPages() {
        return totalPages;
    }

    public boolean isHasPrevious() {
        return pageNumber > 1;
    }

    public boolean isHasNext() {
        return pageNumber < totalPages;
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
