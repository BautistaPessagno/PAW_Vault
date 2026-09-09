---
title: "Validation and errors"
categories: ["Web"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
tags: ["codemap", "web"]
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/form/PublishForm.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/form/ContactForm.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublishController.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PostContactController.java", "services/src/main/java/ar/edu/itba/paw/services/ImageServiceImpl.java"]
---

# Validation and errors

Spring converts ordinary fields before Bean Validation runs. BindingResult follows the @Valid form parameter so the controller can redisplay conversion and constraint failures. Publish’s optional MultipartFile is validated separately by the transport resolver and image service.

| Form/field | Rules |
|---|---|
| Publish username | NotBlank, maximum 100 |
| Publish publisherEmail | NotBlank, Email, maximum 100 |
| Publish title/artistName | NotBlank, maximum 255 each |
| Publish releaseYear | Integer conversion, NotNull, 1000–9999 |
| Contact name/email | Trim first; NotBlank; maximum 100; Email for email field |
| Cover transport | Whole multipart request maximum 6 MiB |
| New-album cover bytes | Allowed MIME label, nonempty, maximum 5 MiB |

Only [[PostContactController]] registers StringTrimmerEditor. Publishing’s annotations count outer spaces before service normalization. Empty or absent upload is allowed. ImageService checks are bypassed when AlbumService reuses an existing album; the uploaded cover is then ignored.

## Error translation

| Origin | Result |
|---|---|
| Field binding/validation | Same form and text values, field errors |
| InvalidImageException | Publish cover error publish.cover.invalid |
| MaxUploadSizeExceededException | New empty PublishForm with coverTooLarge; no explicit non-200 response status |
| DuplicatePostException | Publish publisherEmail error publish.duplicate |
| ConcurrentPublishException | Publish publisherEmail error publish.concurrent |
| PostNotFoundException | Contact HTTP 404 |
| ImageNotFoundException | Cover HTTP 404 |
| Mail rendering/sending failure in worker | Logged/swallowed; no 503 feedback path |
| IOException reading MultipartFile | Propagates; no dedicated local mapping |

[[UI components|ui:text-input]] resolves relative paths inside form:form and renders every field message in an alert container, with aria-invalid/aria-describedby. The file input uses form:errors directly. A browser upload selection is not restored on redisplay.

Image validation checks declared MIME and length only, not decodable content or signatures. Startup SQL enforces uniqueness/NOT NULL but no image-size/MIME or year constraints. The removed [[UserForm]] rules are historical. No global ControllerAdvice or custom error JSP exists in this snapshot.

[[Publish flow]] · [[Contact flow]] · [[Cover image flow]] · [[Testing and evidence]]
