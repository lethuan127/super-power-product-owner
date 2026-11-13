# Save output

## Where

1. Read the "Files" part of `CLAUDE.md`. If it names a place for this kind of output, save there.
2. If it names no place, suggest one. Good defaults:
   - a file: an `output/` folder beside `CLAUDE.md`, or the folder of the input file;
   - a knowledge base: a "Drafts" page under the project's space.
3. After the user answers, ask: "Save this place in the project for next time?" On a "yes", add
   it to the "Files" part of `CLAUDE.md`.

Name a file `<YYYY-MM-DD>-<short-name>.<ext>`, such as `2026-11-13-guide-create-order.md`.

## When a "yes" is needed

| Action | Needs a "yes"? |
|---|---|
| A new file in the project | no |
| A new draft page in the drafts place of the knowledge base | no; show the link after you save |
| An edit to an existing file or page | yes; show the change first |
| A new or changed ticket | yes; show the draft first |
| A save, send, pay or delete in a web app (browser) | yes; and only on a test site |
| A message or a mail | never send; give the user a draft to send |

## After you save

1. Tell the user where the output is: the path or the link.
2. Add one line to `log.md`.
3. If the output is a document someone else will read, offer an artifact. See `artifact.md`.
