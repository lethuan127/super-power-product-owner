# 06 — Onboarding

## In one sentence

Install the plugin, type "set up project <name>", and start work. The project wiki grows while
the PO works, and apps connect the first time a skill needs one.

## Contents

- [The flow](#the-flow)
- [Step 1: install the plugin](#step-1-install-the-plugin)
- [Step 2: set up the project](#step-2-set-up-the-project)
- [Step 3: use it](#step-3-use-it)
- [The four kinds of app](#the-four-kinds-of-app)
- [Rules](#rules)
- [Done when](#done-when)

## The flow

```
 1. install plugin            (by hand, once per PO)
          │
 2. "set up project Order System"
          │                   creates CLAUDE.md, index.md, log.md
          ▼
 3. use it                    "write a user guide for ..."
          │
          └── a fact is missing?
                 wiki ──▶ knowledge base ──▶ ask the PO
                 then add it to the wiki, so nobody asks twice
```

Setup takes under one minute. [02-project-wiki.md](./02-project-wiki.md) explains the wiki.

## Step 1: install the plugin

Done by hand, once. About 5 minutes.

- **Cowork:** upload the plugin file, or add the marketplace in the plugin settings.
- **Claude Code:** run `/plugin marketplace add <repo>`, then `/plugin install <plugin>`.

**Read:** both ways exist. **Not tested** with this plugin yet.

## Step 2: set up the project

The PO types one line, such as "set up project Order System" or "thiết lập dự án Order System".
The `setup-project` skill:

1. Creates `CLAUDE.md`, `index.md` and `log.md` where the chat runs, or in the folder the PO
   names.
2. Writes the schema defaults into `CLAUDE.md`: sources in `sources/`, pages in `wiki/`, the
   suggested pages, and the output language.
3. Says one line: "Give me a doc, a page link, or a folder about the product if you have one.
   Or just start."

If the PO gives something, the skill runs **Add** on it ([the three
operations](./02-project-wiki.md#three-operations)), and shows the pages it wrote.

If the PO already has a layout, the PO says so, such as "my specs are in `docs/specs`". The skill
writes that into `CLAUDE.md`. Every skill follows it.

If the files exist, the skill keeps them. It adds only what is missing.

## Step 3: use it

The PO asks for real work at once. Each skill fills gaps when it meets them.

**A missing fact.** A skill needs a fact the wiki does not have. Example: the user guide needs to
know who the users are. The skill looks in this order:

1. The wiki: `index.md`, then the pages it points to.
2. The knowledge base, in the part saved in `apps.md`. It searches and reads the best few pages.
3. The PO. It asks one short question.

Then it asks: "Add this to the project wiki?" On a "yes", it writes the fact to the right page,
with its source, and adds a line to `log.md`. Next time, no skill looks again.

**A missing app.** A skill needs an app that is not connected. Example: the PO says "create a
ticket for this". The skill then:

1. Checks whether Claude has a connector for that app. A connector is Claude's link to an
   outside app. The PO adds it once, with their own login.
2. If not, shows the exact steps to add it in Claude's settings, and waits for "done". It never
   asks for a password or a token in the chat.
3. Asks which part to use: one Confluence space, one Jira project, one Slack channel, one mail
   label.
4. Writes the app and that part to `apps.md` in the wiki. Next time, it goes straight to work.

## The four kinds of app

| Kind | Examples | Read | Write |
|---|---|---|---|
| Knowledge base | Confluence, Notion, Google Drive, SharePoint | yes | a new page in the PO's drafts place: yes. Any other change: after a "yes" |
| Task tracker | Jira, Linear | yes | after a "yes" |
| Message app | Slack, Microsoft Teams | yes | never |
| Mail app | Gmail, Outlook | yes | never |

All four are **sources** for the wiki. The wiki links to them and keeps short summaries. It
never copies them whole.

**Why a new draft page needs no "yes":** a new page in the PO's own drafts place changes nothing
that other people rely on. The skill shows the link after it saves.

**Why an edit needs a "yes":** other people read the existing pages. A wrong edit misleads them.
So the skill shows the change first, and waits.

The plugin never sends a message or a mail. A person reads a message at once, and nobody can
take it back.

Two more tools follow the same "ask when needed" rule. Their rules are in
[03-skills.md](./03-skills.md#the-core-skill):

- **Claude's browser.** The first time a skill needs it, the skill asks for the site, such as the
  product's test site, and adds it to `apps.md`.
- **Artifacts.** The first time a skill offers a page, it asks if the PO wants one. A "no" goes
  into the schema, so it does not ask again.

## Rules

- **Setup asks nothing required.** The PO can work one minute after install.
- **Wiki, then knowledge base, then the PO.** A skill asks the PO only for a fact that neither
  holds.
- **The schema sets the layout.** Skills read `CLAUDE.md` and put things where it says.
- **Ask when needed, then save.** A skill asks for a fact or an app only when the current job
  needs it. It offers to add the answer to the wiki, so nobody asks twice.
- **Read only the picked part of an app.** The skill never reads outside the space, project,
  channel or label in `apps.md`.
- **No secrets in any file or page.** `apps.md` holds names and parts, such as "Linear, team
  ABC". Logins stay in Claude's connector settings.

## Done when

- One minute after "set up project …", `CLAUDE.md`, `index.md` and `log.md` exist, and the PO
  can ask for real work.
- A new chat in the project folder knows the project without being told.
- No skill creates a folder, moves a file, or edits an existing page that the PO did not ask for.
- A fact the PO gave once, or a skill found once, is never looked up again in the same project.
- An app the PO connected once is never set up again in the same project.
