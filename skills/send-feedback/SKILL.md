---
name: send-feedback
description: "Turns the user's feedback about this plugin into a GitHub issue for the plugin's maintainer, so the plugin gets better every week. Drafts the issue, removes every company, customer and personal detail, shows the draft, and files it only after the user's yes. Use when the user says 'report this', 'this skill is wrong', 'send feedback', 'suggest a feature', 'the plugin should...', 'báo lỗi', 'báo lỗi plugin', 'góp ý', 'góp ý plugin', 'đề xuất tính năng', or when rule 11 offers it."
---

# Send feedback

Read [../core/reference/rules.md](../core/reference/rules.md) first. Also read
[../core/reference/redact.md](../core/reference/redact.md).

The issue goes to `lethuan127/super-power-product-owner`. **That repo is public.** Anyone on
the internet can read the issue, forever. So the issue describes how the plugin behaved, never
the user's business.

## Steps

1. Find out what happened. Use the chat first, and ask only for what is missing:
   - **Kind:** `bug` (a skill did something wrong), `enhancement` (a new job or a better way),
     or `documentation` (a README or a message is unclear).
   - **Skill:** which skill ran, such as `compare-lists`. Write "?" if none or unknown.
   - **What the user asked**, **what Claude did**, and **what the user expected**.
2. Write the draft. Use English for the headings, and keep the user's own words in a quote, in
   their language:

   ```markdown
   Title: <kind>: <skill>: <one short line>

   **Skill:** <skill>  **Plugin version:** <version in .claude-plugin/plugin.json, or ?>
   **App:** <Cowork or Claude Code, or ?>

   ## What the user asked
   <one or two lines>

   ## What happened
   <one or two lines; the exact error text if there was one>

   ## What the user expected
   <one or two lines>

   ## User's words
   > <the user's feedback, as they said it>
   ```

3. Remove private data from every line, the quote too. Replace it with a role or a
   placeholder:
   - company, customer, supplier and product names → "the company", "a customer", "the product";
   - people → their role; never a name, a phone number, a mail address or a chat handle;
   - amounts, invoice numbers, order numbers and file contents → "<amount>", "INV-<n>";
   - file names and paths that name the business → "<file A>";
   - links to the user's own apps and sites → "<internal link>";
   - examples: never reuse a real value as an example. Write a made-up one, such as `1.234.567`.
4. Show the user the full draft. Say: "This goes to a public GitHub page. Check that nothing
   private is left. Reply yes to send it." Wait for the yes. Apply every change the user asks
   for, and show the draft again.
5. After the yes, file it with the first way that works:
   1. `gh auth status` succeeds: run
      `gh issue create -R lethuan127/super-power-product-owner --title "<title>" --body-file <file> --label <kind>`.
      Write the body to a temp file first. If the label fails, run it again without `--label`.
   2. A GitHub connector is connected: create the issue with it, in the same repo.
   3. Otherwise build a link that opens a filled-in issue form. Run:

      ```bash
      python3 -c "import urllib.parse,sys; print('https://github.com/lethuan127/super-power-product-owner/issues/new?' + urllib.parse.urlencode({'title': sys.argv[1], 'body': open(sys.argv[2]).read(), 'labels': sys.argv[3]}))" "<title>" "<body file>" "<kind>"
      ```

      Give the user the link. Say: "Open it, log in to GitHub, and press **Create**." If the
      user has no GitHub account, save the draft as `feedback-<YYYY-MM-DD>.md` in the
      project's output place, and ask the user to send that file to the person who installed
      the plugin.
6. Give the user the issue link, or the file path. Add one `feedback` line to `log.md` if a
   project exists.

## Done when

- The user saw the final draft and said yes before anything left this computer.
- The draft has no company, customer or person name, and no real number or link from the
  user's work, not even as an example.
- The user has the issue link, the form link, or the file path.
