---
name: setup-project
description: "Sets up a new project in under one minute: creates a CLAUDE.md schema, an index.md and a log.md, so a project wiki can grow while the user works. Use when the user says 'set up project X', 'new project X', 'onboard project X', 'thiết lập dự án X', 'tạo dự án X', 'cài đặt dự án X', or when another skill of this plugin finds no project."
---

# Set up a project

Read [../core/reference/rules.md](../core/reference/rules.md) first.

The goal: the user can ask for real work one minute after this skill starts. Ask nothing that
is not required. The wiki grows later, while the user works.

## Steps

1. Get the project name from the user's line. If the line has no name, ask for one. This is the
   only required question.
2. Pick the folder. Use the working folder, unless the user names another one.
3. Check for a `CLAUDE.md` in that folder:
   - It has a `# Project wiki` heading: the project exists. Keep every file. Create only the
     files that are missing. Go to step 7.
   - It exists with no such heading: keep its text. Add the template at the end, below a blank
     line.
   - It does not exist: create it.
4. Write `CLAUDE.md` from [reference/schema-template.md](reference/schema-template.md). Fill in:
   - `<name>`: the project name (leave `<feature>` as it is);
   - `<date>`: today, as `YYYY-MM-DD`;
   - `<language>`: the language the user writes in the chat. Do not ask. Step 9 tells the user,
     and the user can change it.
5. Create `index.md`:

   ```markdown
   # <name> — index

   Every wiki page, one line each. Claude updates this list.

   (No pages yet.)
   ```

6. Create `log.md`:

   ```markdown
   # <name> — log

   New lines go at the end. Old lines never change.

   ## [<date>] setup | Project created
   ```

7. If `git` works on this computer and the folder is not in a git repo yet, run `git init` and
   commit the three files. Tell the user in one line: "I keep a history of every change, so we
   can undo one." If `git` does not work, skip this step.
8. Do not create any other folder or file.
9. Answer with this message, in the project language:

   ```
   Project "<name>" is ready.
   Language: <language>. Every guide, report and spec will use it. To change it, say "change the language to ...".
   Give me a doc, a page link or a folder about the product if you have one. Or just start.

   Try:
   - "write a user guide for <a feature>"
   - "compare <file A> with <file B>"
   - "add this to the project" (with a file or a link)
   ```

10. If the user gives a doc, a page link or a folder, run the `add-to-project` skill on it.

## If the user changes the language

Edit the "All output" line in `CLAUDE.md`. Add one `setup` line to `log.md`. Pages already in the
wiki keep their language.

## If the user names a layout

The user may say "my specs are in `docs/specs`". Write it into the "Files" part of `CLAUDE.md`.
Every skill reads that part.

## Done when

- `CLAUDE.md`, `index.md` and `log.md` exist, and no other new file or folder.
- The user's next message can be real work.
