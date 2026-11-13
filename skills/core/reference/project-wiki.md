# The project wiki

A project wiki is a small set of markdown pages that Claude writes and keeps up to date for one
project. It has three layers:

| Layer | What it is | Who changes it |
|---|---|---|
| Sources | Raw input: notes, specs, exports, screenshots, links to pages, tickets, messages | nobody; read only |
| Wiki pages | Pages Claude writes from the sources | Claude |
| Schema | `CLAUDE.md`: this project's rules and layout | the user and Claude |

## Contents

- [Where the wiki lives](#where-the-wiki-lives)
- [Find the files](#find-the-files)
- [Read](#read)
- [Find a missing fact](#find-a-missing-fact)
- [Write a fact](#write-a-fact)
- [Log a change](#log-a-change)
- [Page rules](#page-rules)

## Where the wiki lives

Usually the wiki lives in the working folder. Some sessions run in a temporary workspace that
is deleted when the session ends, such as a cloud session with a Project attached. There, the
Project's files are the wiki's home:

1. At the start, look for `CLAUDE.md` in the Project's files too. Copy the wiki files you need
   into the workspace before you read them.
2. After every change, save each changed file back to the Project: wiki pages, `index.md`,
   `log.md`, and source copies. A file that stays only in the workspace is lost.
3. Never tell the user a change can be undone from history in a temporary workspace.

## Find the files

Read `CLAUDE.md` first. Its "Files" part says where the sources and the pages are. The defaults
are `sources/` and `wiki/` beside `CLAUDE.md`. `index.md` and `log.md` are always beside
`CLAUDE.md`.

## Read

1. Read `index.md`. It lists every page with one line about it.
2. Open only the pages the job needs.
3. If a page says "conflict", tell the user before you use that fact.

## Find a missing fact

Do these steps in order. Stop at the first step that gives the fact.

1. Search the wiki pages for the fact.
2. If a knowledge base is listed in `apps.md`, search it in the listed part only. Read the best
   1 to 3 pages.
3. Ask the user one short question.

Then ask: "Add this to the project wiki?" On a "yes", write the fact. See the next section.

A fact from a mail or a message goes into the wiki only after the user sees it.

## Write a fact

1. Pick the page. Use the page list in `CLAUDE.md`. If no page fits, create one and add it to
   `index.md`.
2. Write the fact in one or two short sentences.
3. Add its source on the same line, with the date you read it:
   `(from sources/2026-11-10-kickoff.md, read 2026-11-13)` or
   `(from Confluence page "Billing rules", read 2026-11-13)`.
4. If the fact disagrees with a fact already on the page, keep both. Mark them:
   `CONFLICT: <old fact> vs <new fact>. Ask the user.` Then ask the user which is true.
5. Write roles, not people: "the accounting lead", not a name. See `redact.md`.
6. Add one line to `log.md`. See the next section.

## Log a change

Add one line at the end of `log.md`. Never edit an old line.

```
## [YYYY-MM-DD] <action> | <what>
```

`<action>` is one of: `setup`, `add`, `ask`, `check`, `write`, `compare`, `connect`.
Example: `## [2026-11-13] add | Kickoff notes: 3 pages changed`.

If the project folder is a git repo, commit after each change, with the log line as the message.

## Page rules

- Sources are never edited.
- A summary of a page in an app keeps a link to it. Never copy the whole page, mail or message.
- Each fact names its source. A fact with no source gets "(source: ?)".
- Keep each page under about 200 lines. Split a long page by topic, and update `index.md`.
