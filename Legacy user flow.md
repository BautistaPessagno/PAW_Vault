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

The cleanup deleted [[HelloWorldController]], [[UserForm]], [[UserNotFoundException]] and both helloworld JSPs. [[UserService]] no longer exposes create; [[UserServiceImpl]] keeps a private creation helper under findOrCreate.

User persistence still supports publishing. A visitor’s normalized email resolves a User through [[Publish flow]], and a new publisher triggers welcome mail. There is no replacement registration/profile UI or authentication.

Historical Java notes retain their exact pre-removal source linked to 041ce34. [[History and specifications]] records how the source documents were updated.
