---
name: send-feedback
description: "Turns the user's feedback about this plugin into a GitHub issue for the plugin's maintainer, so the plugin gets better every week. Drafts the issue, removes every company, customer and personal detail, shows the draft, and files it only after the user's yes. Use when the user says 'report this', 'this skill is wrong', 'send feedback', 'suggest a feature', 'the plugin should...', 'báo lỗi', 'báo lỗi plugin', 'góp ý', 'góp ý plugin', 'đề xuất tính năng', or when rule 11 offers it."
---

# Send feedback

Read [../core/reference/rules.md](../core/reference/rules.md) first. Also read
[../core/reference/redact.md](../core/reference/redact.md) and
[../core/reference/github.md](../core/reference/github.md).

The issue goes to `lethuan127/super-power-product-owner`. **That repo is public.** Anyone on
the internet can read the issue, forever. So the issue describes how the plugin behaved, never
the user's business.

A good issue lets the maintainer do three things without asking back: rank it, reproduce it,
and tell when it is fixed. The draft has one section for each.

## Steps

1. Collect the facts. Take them from the chat first:
   - **Kind:** `bug` (a skill did something wrong), `enhancement` (a new job or a better way),
     or `documentation` (a README or a message is unclear).
   - **Skill:** which skill ran, such as `compare-lists`. Write "?" if none or unknown.
   - **Impact:** who could not use the result, and whether the user found a way around it.
   - **Input:** what the user gave the skill: the request and the kind of files.
   - **Actual output:** the wrong part of what Claude wrote, copied as a short excerpt.
   - **Expected:** what the user wanted instead.

   Fill every unknown fact with "Not given", and go on to the draft. If the impact is "Not
   given", ask about it in step 5, together with the draft.
2. Write the draft. Use English for the headings, and keep the user's own words in a quote, in
   their language:

   ```markdown
   Title: <skill>: <one short line about the behavior>

   **Skill:** <skill>  **Plugin version:** <version in .claude-plugin/plugin.json, or ?>
   **App:** <Cowork or Claude Code, or ?>

   ## Impact
   - Who is blocked: <a role, such as "the warehouse lead">
   - Workaround: <what the user did instead, or "none">

   ## Steps to reproduce
   1. <the request, with private data replaced>
   2. <the files given: kind, columns, row count; never their contents>

   ## What happened
   <one or two lines>

   > <a short excerpt of the wrong output, with private data replaced>

   ## Expected
   <one or two lines>

   ## Done when
   - [ ] <a check anyone can run on the output, such as "the table has at least 2 rows">
   - [ ] <one more check, if needed>

   ## User's words
   > <the user's feedback, as they said it>
   ```

3. Remove private data from every line, the quotes too. Replace it with a role or a
   placeholder:
   - company, customer, supplier and product names → "the company", "a customer", "the product";
   - people → their role; never a name, a phone number, a mail address or a chat handle;
   - amounts, invoice numbers, order numbers and file contents → "<amount>", "INV-<n>";
   - file names and paths that name the business → "<file A>";
   - links to the user's own apps and sites → "<internal link>";
   - examples: never reuse a real value as an example. Write a made-up one, such as `1.234.567`.
4. Look for the same problem among open issues, with `github.md`.
   Search for `<skill>`. If an open issue describes the same behavior, plan to add a comment
   there instead of a new issue, and tell the user its link.
5. Show the user the full draft. Say: "This goes to a public GitHub page. Check that nothing
   private is left. Reply yes to send it." Wait for the yes. Apply every change the user asks
   for, and show the draft again.
6. After the yes, file it with the first way that works:
   1. `gh auth status` succeeds: write the body to a temp file. For a match from step 4, run
      `gh issue comment <number> -R lethuan127/super-power-product-owner --body-file <file>`.
      Otherwise run
      `gh issue create -R lethuan127/super-power-product-owner --title "<title>" --body-file <file> --label <kind>`.
      If the label fails, run it again without `--label`.
   2. A GitHub connector is connected: do the same with it, in the same repo.
   3. Otherwise build a link that opens a filled-in issue form. Run:

      ```bash
      python3 -c "import urllib.parse,sys; print('https://github.com/lethuan127/super-power-product-owner/issues/new?' + urllib.parse.urlencode({'title': sys.argv[1], 'body': open(sys.argv[2]).read(), 'labels': sys.argv[3]}))" "<title>" "<body file>" "<kind>"
      ```

      Also save the draft as `feedback-<YYYY-MM-DD>.md` in the project's output place. Give the
      user both, in this order:
      - "Have a GitHub account? Open this link, log in, and press **Create**."
      - "No GitHub account? Send this file to the person who installed the plugin."
      Then say once: "To send feedback with no extra step next time, ask the person who
      installed the plugin to connect GitHub to this app."
7. Give the user the issue link, or the file path. Add one `feedback` line to `log.md` if a
   project exists, with the link or the file name.

## Done when

- The user saw the final draft and said yes before anything left this computer.
- The draft has no company, customer or person name, and no real number or link from the
  user's work, not even as an example.
- The draft has an impact line, steps to reproduce, an excerpt, and at least one "Done when" check.
- The user has the issue link, the comment link, the form link, or the file path.
- The `log.md` line has that link or file name, so `feedback-status` can find it later.
