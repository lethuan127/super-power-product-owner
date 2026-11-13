# Project wiki: Order System

This folder holds the project wiki for **Order System**, created on 2026-11-01. Claude reads this file at
the start of every chat in this folder. The skills of the `super-power-product-owner` plugin
follow it.

## Language

- All output: English. This covers guides, reports and specs for developers.
- Keep product terms, button names and column names exactly as the product shows them.

## Files

Where things live. Change any line. Every skill follows this list.

- Sources (raw input, never edited): `sources/`
- Wiki pages (Claude writes them): `wiki/`
- Drafts and results: `output/`

Folders appear the first time a skill needs them.

## Pages

These pages are a suggestion. Rename, add or remove any of them.

| Page | What it holds |
|---|---|
| `product.md` | What the product does, in a few sentences |
| `users.md` | Each user group, what they do, and the words they use |
| `terms.md` | Business words and their meanings |
| `features/<feature>.md` | One feature: how it works, its rules, its open questions |
| `decisions.md` | Each decision: what, when, why, and the source |
| `edge-cases.md` | Known hard cases in this business |
| `money.md` | Currency, period, link column and number format for money compares |
| `roles.md` | Roles, such as "the accounting lead"; never personal data |
| `apps.md` | Connected apps and sites, the part to use, and the site kind. No logins |

## Rules

- Each fact on a wiki page names its source and the date it was read.
- Sources are never edited.
- The wiki holds roles, not people.
- A new fact that disagrees with an old one is marked `CONFLICT`, and the user decides.
- `index.md` lists every page. `log.md` gets one line per change, at the end.
