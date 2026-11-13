# super-power-product-owner

Tiếng Việt: [README.vi.md](./README.vi.md)

Claude skills that take the repeat work off a Product Owner's week. Each project gets a small
wiki that grows while you work. The skills read it, so their output uses your product's words.

Works for any company and any product. Version 0.1.0 has the base and the two first jobs.

## Install

**Cowork (Claude desktop app):** open the plugin settings, add the marketplace
`lethuan127/super-power-product-owner`, then install `super-power-product-owner`.

**Claude Code:**

```
/plugin marketplace add lethuan127/super-power-product-owner
/plugin install super-power-product-owner --marketplace lethuan127/super-power-product-owner
```

## Start

Open a folder for your project, then type one line:

```
set up project Order System
```

or `thiết lập dự án Order System`. Then ask for real work at once.

## Skills

| Skill | Say | What you get |
|---|---|---|
| `setup-project` | "set up project X" | `CLAUDE.md`, `index.md`, `log.md`; ready in one minute |
| `add-to-project` | "add this to the project" + a file or a link | the wiki pages it changed |
| `ask-project` | "what did we decide about X?" | an answer with a link behind each claim |
| `write-guide` | "write a user guide for X" / "update the guides after this change" | a step-by-step guide, or the list of broken steps |
| `compare-lists` | "reconcile file A with file B" | four tables: matched, only in A, only in B, amount differs |
| `send-feedback` | "report this" / "suggest a feature" | a GitHub issue for the maintainer, with private data removed, sent after your "yes" |
| `core` | (not called directly) | the shared rules every skill follows |

## Safety

- Claude never sends a message or a mail.
- Claude edits an existing page, creates a ticket, or saves in a web app only after your "yes".
- Claude never asks for a password or a token. You log in to each app yourself.
- `compare-lists` never changes your input files.
- `send-feedback` files a public GitHub issue only after your "yes", and removes company,
  customer and personal data first.

## Develop

The design docs are in [docs/](./docs/). Read them in this order:

| File | What it answers |
|---|---|
| [01-vision.md](./docs/01-vision.md) | Who it is for, the problem, the goals, and what it will not do |
| [02-project-wiki.md](./docs/02-project-wiki.md) | How a project is stored: sources, wiki pages, schema |
| [03-skills.md](./docs/03-skills.md) | Every planned skill: input, output, and how to tell it is done |
| [04-architecture.md](./docs/04-architecture.md) | How the plugin ships, its files, languages and safety |
| [05-roadmap.md](./docs/05-roadmap.md) | Phases, questions for the first user, and the next step |
| [06-onboarding.md](./docs/06-onboarding.md) | Install, set up a project in one line, and start work |
| [07-open-source.md](./docs/07-open-source.md) | The open-source checklist and this repo's status |

Each claim about a PO's work in the docs is marked **Told** (a PO said so), **Assumed** (a common
PO job), or **Tested** (someone ran the skill on real work).

Checks and rules for a change: [CONTRIBUTING.md](./CONTRIBUTING.md). Security reports:
[SECURITY.md](./SECURITY.md).

## Versions

- **0.1.0:** first version. Project wiki (setup, add, ask), `write-guide`, `compare-lists`, and
  the `core` rules.
