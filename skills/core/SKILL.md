---
name: core
description: "Shared rules and steps for every skill in the super-power-product-owner plugin: how to read and write the project wiki, find a missing fact, connect an app, save a draft, write plainly, redact personal data, use Claude's browser, and publish an artifact. Load it when another skill of this plugin says to read the core rules. It is not a job on its own."
---

# Core

This skill holds the rules that every other skill in this plugin follows. It does no job on its
own. The other skills point here, so each rule is written once.

## Read these files

Always read [reference/rules.md](reference/rules.md) first. Then read only the files the current
job needs:

| File | Read it when the job must |
|---|---|
| [reference/project-wiki.md](reference/project-wiki.md) | read the project wiki, find a fact, or write a fact |
| [reference/connect-app.md](reference/connect-app.md) | use an app that is not connected yet |
| [reference/save-output.md](reference/save-output.md) | save a draft, a file, a page or a ticket |
| [reference/plain-writing.md](reference/plain-writing.md) | write text for a person |
| [reference/redact.md](reference/redact.md) | quote a message, or write to the wiki |
| [reference/browser.md](reference/browser.md) | open a web page in Claude's browser |
| [reference/artifact.md](reference/artifact.md) | publish a result as an artifact |
