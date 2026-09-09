---
title: "Validation and errors"
categories: ["Web"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "041ce34404963b689d05443ca00abb7e75aa7f15"
status: "documented"
tags: ["codemap", "web"]
---

# Validation and errors

Validation has two phases. Spring first converts submitted strings into form property types, then Bean Validation checks @Valid. BindingResult immediately follows the form argument, letting controllers inspect both conversion and constraint errors. Services receive already validated web input, but their public methods do not repeat all these constraints for other callers.

| Form | Field | Rules |
|---|---|---|
| [[PublishForm]] | username | NotBlank, max 100 |
| PublishForm | publisherEmail | NotBlank, Email, max 100 |
| PublishForm | title / artistName | NotBlank, max 255 each |
| PublishForm | releaseYear | Integer conversion, NotNull, 1000–9999 |
| [[ContactForm]] | contactName | Trim first, NotBlank, max 100 |
| ContactForm | contactEmail | Trim first, NotBlank, Email, max 100 |
| [[UserForm]] | username | Size 8–100 and ASCII regex, but null allowed by these annotations |
| UserForm | email | NotBlank, Email, no max length |

Only the contact controller registers StringTrimmerEditor. Publishing's length validation counts the submitted outer spaces before service normalization. Empty contact strings become null before validation. Missing or nonnumeric publish years produce errors instead of unboxing null because the controller exits early on BindingResult errors.

## Error translation map

| Origin | Signal | Boundary/result |
|---|---|---|
| Form validation | BindingResult errors | Same JSP and existing form values; usually ordinary 200 render |
| Post pre-check | [[DuplicatePostException]] | Publish publisherEmail field error |
| JDBC duplicate insert | [[DuplicatePostKeyException]] | Service translates to DuplicatePostException |
| Other publish integrity error | [[ConcurrentPublishException]] | Publish publisherEmail retry message |
| Missing contact Post | [[PostNotFoundException]] | Local handler sets 404 |
| Contact render/SMTP failure | [[EmailDeliveryException]] | Controller sets 503 and deliveryFailed |
| Welcome render/SMTP failure | Caught and logged | No exception propagated from welcome body |
| Missing legacy profile User | [[UserNotFoundException]] | No explicit 404 handler |
| Duplicate legacy create email | Database exception | No local form-error translation |

Validation errors resolve through [[WebConfig]]'s message source. The default bundle includes typeMismatch.publishForm.releaseYear for integer-conversion failure. There is no application-wide ControllerAdvice or custom error JSP in the supplied source.

The current startup database enforces NOT NULL and uniqueness but not the form's year range or email syntax. [[Database schema]] describes that boundary. [[Testing and evidence]] records the missing controller tests.

## UI integration at the current commit

Publish and contact retain Spring form:form around [[UI components|ui:text-input]]. spring:bind resolves each relative path within its modelAttribute. The tag loops over status.errorMessages, retaining input and exposing an alert container through aria-describedby. It emits maxlength and numeric bounds when supplied, but no HTML required attribute. This is static source evidence, not an executed invalid-form test.
