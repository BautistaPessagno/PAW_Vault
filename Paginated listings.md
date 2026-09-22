---
title: "Paginated listings"
categories: ["Services", "Web"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["services/src/main/java/ar/edu/itba/paw/services/Pagination.java", "services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java", "services/src/main/java/ar/edu/itba/paw/services/InquiryServiceImpl.java", "models/src/main/java/ar/edu/itba/paw/models/PostPage.java", "webapp/src/main/webapp/WEB-INF/tags/pagination.tag", "webapp/src/main/webapp/WEB-INF/tags/pagination-link.tag"]
---

# Paginated listings

Three listings are paged in this revision: the public catalog, the owner's publications on the profile and both inbox views. They share [[Pagination]] for page arithmetic, [[PageNotFoundException]] for invalid pages and the ui:pagination tag for links. Page numbers arrive as a `page` query parameter defaulting to 1.

| Listing | Page size | Total | Page model | Out-of-range page |
|---|---|---|---|---|
| Catalog `/` | 15 posts | Unknown: fetch 16 rows, a 16th means another page | [[PostPage]] with totalKnown=false | Below 1, or empty beyond page 1: 404 |
| Profile `/profile` | 12 posts | COUNT(*) of the owner's posts | [[PostPage]] with known total | Below 1 or past the last page: 404 |
| Received `/inquiries`, sent `/inquiries/sent` | 5 publications (groups) | COUNT(DISTINCT group key) | [[InquiryPage]] | Below 1 or past the last page: 404 |

Page 1 always exists, even for an empty listing, so empty states render normally. offsetFor computes the offset in long arithmetic and rejects anything above Integer.MAX_VALUE, which prevents overflow from huge page numbers. The catalog avoids a COUNT query on the filtered search, so it cannot show a page count; its heading counts only the rows on the current page.

The inbox pages by publication rather than by inquiry: [[InquiryJdbcDao]] first selects a page of group keys, then every inquiry of those keys. A group is therefore never split across pages, and a page can contain more than five inquiries. See [[Inquiry and sale flow]].

ui:pagination renders nothing when there is neither a previous nor a next page. With a known total it draws previous/next chevrons and numbered links: all pages up to seven, otherwise the first, the last, the current page with two neighbours and ellipses. Without a total it draws only the chevrons. ui:pagination-link builds each URL once from the base path, the current filters (the catalog passes q, sort and every active filter), the target page and an optional fragment such as `#posts` or `#inquiries`. Links carry aria-label and rel prev/next.

[[Landing flow]] · [[Profile flow]] · [[PaginationTest]] · [[UI components]]

## Shared arithmetic

[services/src/main/java/ar/edu/itba/paw/services/Pagination.java, lines 1–36](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/Pagination.java>)

```java
package ar.edu.itba.paw.services;

// Aritmetica de paginado compartida por los services que listan de a paginas. Una sola
// regla para "pagina fuera de rango": la pagina 1 siempre existe, aunque este vacia; con el
// total conocido, cualquier otra tiene que caer dentro de el.
final class Pagination {

    private Pagination() {
    }

    // Paginas necesarias para un total; 0 cuando no hay filas.
    static int pagesFor(final int total, final int pageSize) {
        return (total + pageSize - 1) / pageSize;
    }

    // Offset de una pagina cuando el total es conocido.
    static int offsetFor(final int pageNumber, final int pageSize, final int totalPages) {
        if (pageNumber > 1 && pageNumber > totalPages) {
            throw new PageNotFoundException();
        }
        return offsetFor(pageNumber, pageSize);
    }

    // Offset de una pagina cuando el total no se conoce (la busqueda del catalogo mira una
    // fila de mas en lugar de contar).
    static int offsetFor(final int pageNumber, final int pageSize) {
        if (pageNumber < 1) {
            throw new PageNotFoundException();
        }
        final long offset = ((long) pageNumber - 1L) * pageSize;
        if (offset > Integer.MAX_VALUE) {
            throw new PageNotFoundException();
        }
        return (int) offset;
    }
}
```

## Catalog look-ahead

[services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java, lines 116–123](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java>)

```java
    private static PostPage toPage(final List<PostSummary> rows, final int pageNumber, final int pageSize) {
        if (pageNumber > 1 && rows.isEmpty()) {
            throw new PageNotFoundException();
        }
        final boolean hasNext = rows.size() > pageSize;
        final List<PostSummary> posts = hasNext ? rows.subList(0, pageSize) : rows;
        return new PostPage(posts, pageNumber, pageNumber > 1, hasNext);
    }
```

## Inbox page

[services/src/main/java/ar/edu/itba/paw/services/InquiryServiceImpl.java, lines 87–94](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/InquiryServiceImpl.java>)

```java
    @Override
    @Transactional(readOnly = true)
    public InquiryPage findReceivedGroupedByPost(final long sellerId, final int pageNumber) {
        final int totalPages = Pagination.pagesFor(inquiryDao.countGroupsBySellerId(sellerId), INBOX_PAGE_SIZE);
        final int offset = Pagination.offsetFor(pageNumber, INBOX_PAGE_SIZE, totalPages);
        return new InquiryPage(groupByPost(inquiryDao.findBySellerId(sellerId, INBOX_PAGE_SIZE, offset)),
                pageNumber, totalPages);
    }
```
