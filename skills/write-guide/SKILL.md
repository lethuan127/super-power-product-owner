---
name: write-guide
description: "Writes a step-by-step user guide or staff procedure for a feature, in the users' own words, with exact button names and screenshots; or finds the guides a change breaks and drafts their updates. Use when the user says 'write a user guide', 'write a how-to', 'write an SOP', 'update the guide after this release', 'viết hướng dẫn sử dụng', 'viết tài liệu hướng dẫn', 'cập nhật hướng dẫn', 'làm SOP'."
---

# Write a guide

Read [../core/reference/rules.md](../core/reference/rules.md) first. Also read
[../core/reference/plain-writing.md](../core/reference/plain-writing.md).

This skill has two modes. Pick one from the user's words:

- **New:** "write a guide for X".
- **Update:** "update the guides after this change", or the user gives a change list.

## Mode: new guide

1. Find the project and read `index.md`. Read the feature page, `users.md` and `terms.md` if
   they exist.
2. Find out three things. Use the wiki, then the knowledge base, then ask the user (rule 2):
   - the feature: what it does;
   - the reader: which user group;
   - the goal: what the reader can do after the guide.
3. Get the exact screens:
   - If `apps.md` lists a site, walk the feature in Claude's browser. Follow
     [../core/reference/browser.md](../core/reference/browser.md). Copy the exact button and
     field names. Take one screenshot per step.
   - If not, use the spec or the user's description. Write `[screenshot: <screen name>]` where a
     screenshot belongs. At the end, ask the user for those screenshots, or for the site.
4. Write the guide with [reference/guide-template.md](reference/guide-template.md). Use the
   template in `CLAUDE.md` instead, if the project has one.
5. Check the guide against the "Done when" list below. Fix what fails.
6. Save it. Follow [../core/reference/save-output.md](../core/reference/save-output.md).
7. Add the guide to the feature page in the wiki: "Guide: <path or link>". This lets update mode
   find it later.

## Mode: update after a change

1. Get the change: a change list, release notes, a changed spec, or a ticket.
2. Find every guide the change touches. Look at the "Guide:" lines on the wiki feature pages,
   then search the guides for the changed screens, buttons and terms.
3. For each guide, list the exact steps that are now wrong, and draft the new text.
4. Show the user the list:

   ```
   This change breaks 2 guides:
   - Create an order: step 3 (button "Save" is now "Submit"), step 5 (new field "Branch").
   - Cancel an order: no change needed.
   ```

5. Edit a guide only after a "yes". An edit to a published guide changes what other people
   read.
6. Add one `write` line to `log.md`.

## Done when

- Each step is one action on one screen, with the exact button or field name.
- The guide uses the readers' words, not developer words.
- Every screenshot uses test data, or has customer data blurred.
- Every `[screenshot: ...]` gap is listed for the user.
- In update mode: every guide the wiki links to the feature was checked.
