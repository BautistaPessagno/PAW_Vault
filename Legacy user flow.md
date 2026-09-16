---
title: "Legacy user flow"
categories: ["History"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "removed"
tags: ["codemap", "flows"]
sources: []
---

# Legacy user flow

> [!note] Removed routes
> At ff96f27, /create and /profile/{id} are no longer controller mappings. This note records the removed course scaffold, not a supported current flow.

The cleanup deleted [[HelloWorldController]], [[UserForm]], [[Legacy UserNotFoundException]] and both helloworld JSPs. At that removal revision, UserServiceImpl retained a private creation helper under findOrCreate. That was an intermediate implementation.

At ff96f27, a visitor email resolved a publisher and there was no authentication. The current implementation has registration, verification and login through [[Authentication flow]]; [[Publish flow]] now requires an authenticated account. The removed /create and /profile routes have not returned.

Historical Java notes retain their exact pre-removal source linked to 041ce34. [[History and specifications]] records how the source documents were updated.
