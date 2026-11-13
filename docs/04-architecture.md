# 04 — Architecture

## How it ships

The same skill files work in three places. Only the wrapper changes.

| Where the PO uses Claude | How the plugin ships | Setup for the PO |
|---|---|---|
| Claude desktop app with Cowork | A plugin file the PO uploads | about 5 minutes, once |
| Claude Code in a terminal | A marketplace the PO installs from | about 10 minutes, and a terminal |
| claude.ai chat only | A Project with the skills as instructions | about 5 minutes; not a real plugin |

**Decision (2026-11-13): Cowork.** Most POs are not engineers, and Goal 4 in
[01-vision.md](./01-vision.md) says the PO needs no terminal. Cowork can also run the
`compare-lists` script. (Read: Cowork loads plugins and runs code. Not yet tested with this
plugin.)

**Rejected: the Code tab in Claude Desktop.** It fits the design better on paper. It reads
`CLAUDE.md` on its own, and scripts run on the PO's computer. But it asks for permission before
each command and file change. It also needs Python and a package tool on the computer. Those
steps confuse a user who is not an engineer, and a wrong "allow" can change files outside the
project. Cowork keeps the PO in a safer, simpler space. The skills stay the same, so a technical
PO can still use the Code tab.

## Folder layout

```
super-power-product-owner/          the git repo root, and the plugin root
├── .claude-plugin/
│   ├── marketplace.json            lists one plugin, source "./"
│   └── plugin.json                 the plugin manifest (name, version)
├── README.md, README.vi.md         user guide, English and Vietnamese
├── LICENSE, CONTRIBUTING.md, SECURITY.md
├── docs/                           these design docs
├── skills/
│   ├── core/                       shared rules; no job of its own
│   │   ├── SKILL.md
│   │   ├── reference/              rules, project-wiki, connect-app, save-output,
│   │   │                           plain-writing, redact, browser, artifact
│   │   └── locales/vi.md           Vietnamese headings, formats and tone
│   ├── setup-project/              SKILL.md, reference/schema-template.md
│   ├── add-to-project/, ask-project/
│   ├── write-guide/                SKILL.md, reference/guide-template.md
│   ├── compare-lists/              SKILL.md, scripts/compare.py
│   └── send-feedback/              files a GitHub issue after a "yes"
├── evals/                          claude plugin eval cases and fixtures
├── tests/                          unit tests for compare.py
├── scripts/check_plugin.py         manifests, skill names, dead links
└── .github/                        CI and issue forms
```

Each skill follows the Agent Skills spec. The `name` matches the folder. The `description` says
what the skill does and the words that should start it. Claude reads only the description to
decide whether to load a skill. So the description must contain the words a PO will actually
type, in English and in Vietnamese, such as "write a user guide" and "viết hướng dẫn sử dụng".

## The project wiki

Every skill reads the project wiki first. The wiki holds what is true about one project, and it
grows while the PO works. The skills hold how to do a job, which is the same for every PO.
[02-project-wiki.md](./02-project-wiki.md) has the full design.

```
  PO's input ──▶ skill ──▶ draft
                   │ ▲
     adds facts    │ │ reads index.md first,
     and a log line▼ │ then the pages it needs
               project wiki
       (CLAUDE.md, index.md, log.md,
        wiki pages, sources)
```

The plugin ships the schema defaults and the page templates. It never ships a filled-in wiki.
Two reasons:

- Product facts belong to the PO's company. They must not travel inside a plugin.
- The PO changes the wiki without a new plugin version.

## Scripts

Only `compare-lists` needs a script in version 1. The script reads two files, matches them, and
writes the result tables. It reads files and writes files. It does not call any outside service.

**It needs one package: `openpyxl`.** The Python standard library cannot read `.xlsx` files, and
most accounting exports are `.xlsx`. The skill installs it on first use if it is missing.
(**Assumed:** Cowork allows the install. To test.) If the install fails, the skill asks the PO to
save each file as CSV.

## Language

**Decision (2026-11-13): one plugin, skills in English, user-facing text in both languages.**

- Skill files (`SKILL.md`): English. Claude follows English rules well, and one copy cannot drift.
- Descriptions: English plus Vietnamese trigger words.
- Output: the language set in the project's `CLAUDE.md`, or the one the user asks for.
- User docs: `README.md` and `README.vi.md`.
- Per-language guidance: `skills/core/locales/<code>.md` holds the fixed headings, the number
  and date format, and the tone. Rule 5 loads it when the project language has one. A language
  with no file still works; it only loses the fixed phrases. The pattern comes from the
  `understand-anything` plugin, which ships `locales/{ja,ko,zh,...}.md` the same way.
- `setup-project` does not ask for the language. It takes the chat language and tells the user
  how to change it, so setup stays at one question.

**Rejected: two plugins or two repos, one per language.** Every rule change would need two
edits, and the copies would drift apart within a few changes. **Tested:** two eval cases with
Vietnamese prompts (`setup-project-vi`, `compare-asks-columns`) fire the right skill and answer
in Vietnamese. `write-guide-vi` and `compare-vi` check that the guide and the report use
Vietnamese headings and keep the English button and column names.

## Safety

- The plugin writes files and pages only where the PO said. It never moves or deletes a PO's
  file or page.
- A new page in the PO's drafts place needs no "yes". An edit to an existing page, or any write
  to the task tracker, needs a "yes" after the PO sees the draft.
- It never sends a message or a mail.
- The plugin reads each app only in the scope the PO picked: one space, project, channel or label.
- The plugin ships no server for any app. The PO uses the connector their
  company allows, with their own login. No file holds a token or a password.
- `sort-feedback` removes phone numbers, emails and customer names before it quotes a message.
- `compare-lists` never edits an input file.
- No real company data goes into the plugin or this repo. Examples use neutral names, such as
  "Customer A" and "ORD-001".
