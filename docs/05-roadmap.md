# 05 — Roadmap

## Questions for the first user

The plugin is general, but the first test needs one real PO. Ask that PO these before Phase 1.
The answers go into that PO's project wiki, not into the skills.

| # | Question | What the answer decides |
|---|---|---|
| Q1 | Which job in your week tires you most, or takes the most hours? | which skill to build first |
| Q2 | Where do you use Claude: the desktop app, the web, or not yet? | how the plugin ships for the test |
| Q3 | Which knowledge base, task tracker, message app and mail app does your team use? Can you add a Claude connector for each? | which connectors to test first |
| Q4 | Can you share one user guide you wrote before, with names removed? | the guide template |
| Q5 | Can you share one small reconciliation: the product export and the accounting file, with names removed? Which column links them? | the test input for `compare-lists` |
| Q6 | How often do you reconcile, and how long does one round take? | the time the skill must save |

## Phases

### Phase 0 — Design (now)

- Write these docs. **Done.**
- Ask the first user Q1 to Q6.

### Phase 0.5 — Test the platform (about 30 minutes)

Test these in Cowork before any skill is built. Each one changes the design if it fails.

| Test | If it fails |
|---|---|
| A new chat in a folder reads its `CLAUDE.md` | add a pointer step to `setup-project` |
| A skill reads a file in another skill's folder | a build script copies the core files into each skill |
| A skill publishes an artifact, and a person with no Claude account opens it | send files only, and keep artifacts for the PO |
| A skill installs `openpyxl` and reads an `.xlsx` file | ask the PO for CSV files |
| The first user's product has a test site, and what data it holds | mark the site kind in `apps.md`; plan guides around it |

**Results so far (2026-11-14, Cowork cloud, v0.2.0 from the GitHub marketplace):**

- **Install: works.** The marketplace synced at the release commit, and the content scan passed.
  The plugin starts switched off; the user must turn it on in Customize → Plugins.
- **Sync: manual.** Cowork keeps the synced commit until a new sync. Auto sync needs the Claude
  GitHub app on the repo.
- **`setup-project` fires from "thiết lập dự án Thử nghiệm" and answers in Vietnamese.**
- **The cloud workspace is temporary.** Claude saved the 3 wiki files to the Cowork Project by
  itself, so the next session can read them. Open: does a new session read `CLAUDE.md` from the
  Project? If not, the wiki needs a Project home in `setup-project` and `core`.
- **Fixed in 0.2.1:** the reply showed `<file A>` placeholders, and promised an undo history that
  a temporary workspace loses.

### Phase 1 — The base plus two Told skills (about 2 days)

1. Build the plugin frame, `core` and `setup-project`.
2. Run "set up project" with the first user, in one 30-minute session.
3. Build `write-guide`, and test it on the input from Q4.
4. Build `compare-lists` and its script, and test it on the input from Q5.

**Done when:** the first user uses each skill on real work, and the reconciliation totals match
to the smallest unit.

### Phase 2 — The other P1 skills (about 2 days)

Build the rest of the P1 skills from [03-skills.md](./03-skills.md), one at a time. Test each on
one real input before the next.

**Done when:** each P1 skill has one real draft the user sent.

### Phase 3 — Review after two weeks

Ask the three questions in [01-vision.md](./01-vision.md#how-we-know-it-works). Cut or rewrite
any skill nobody used. Then decide on the P2 skills and the "Cut or later" list.

### Phase 4 — A second PO

Give the plugin to a PO with a different product. That PO fills in their own project wiki.
Do not change any skill for them.

**Done when:** the second PO gets a usable draft from two skills. If a skill needs a change to
work for them, it held a product fact. Move that fact to the project wiki.

## Next step

Ask the first user Q1 to Q6. Put the answers into their project wiki, not into these docs.
