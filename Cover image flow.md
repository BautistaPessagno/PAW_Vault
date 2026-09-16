---
title: "Cover image flow"
categories: ["Flows", "Web"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java", "services/src/main/java/ar/edu/itba/paw/services/ImageServiceImpl.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ImageController.java", "persistence/src/main/java/ar/edu/itba/paw/persistence/PostJdbcDao.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/security/MultipartExceptionHandlerFilter.java"]
---

# Cover image flow

New uploaded photos belong to the physical exemplar through posts.image_id. AlbumService no longer handles image creation. Existing catalog identities can be reused with a different publication photo, including when the legacy album cover is null.

1. [[PublishController]] passes the upload's declared MIME and bytes to [[PostServiceImpl]].
2. After the duplicate publication check, nonempty bytes go to [[ImageServiceImpl]]. Allowed labels are image/png, image/jpeg and image/webp; size must not exceed 5,242,880 bytes.
3. [[ImageJdbcDao]] stores the bytes; Post.imageId references them in the same publishing transaction. Empty or absent upload gives a null post image.
4. [[PostJdbcDao]] reads COALESCE(p.image_id, a.cover_image_id). ui:vinyl-card uses /covers/{id}, or the SVG placeholder when both references are null.

The whole multipart request limit is 6,291,456 bytes. [[MultipartExceptionHandlerFilter]] redirects overflow to the empty publish form with coverTooLarge. web.xml places multipart parsing before Spring Security so CSRF can read the multipart token.

[[ImageController]] returns stored bytes and Content-Type with public max-age=31536000. The route is public; missing images return 404. No replace/delete route, ETag, decoder, signature check, resizing or content deduplication is implemented. [[Image]] now copies byte arrays on construction and retrieval.

The schema enforces the new posts.image_id foreign key. The retained albums.cover_image_id fallback has no foreign key in the canonical startup schema; a dangling fallback yields 404 without automatic JSP recovery.

[[Database schema]] · [[Publish flow]] · [[UI components]]
