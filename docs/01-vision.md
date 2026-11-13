# 01 — Vision

## In one sentence

The plugin turns a PO's raw input (notes, chats, ideas, files) into the documents the team
needs, in the words of that PO's product. The PO then spends the time on decisions and not on
typing.

## Who uses it

A Product Owner of any product, in any company. The plugin suits most a PO who:

- is not an engineer;
- works with developers on one side and with users on the other;
- writes a lot, in one or two languages.

Internal business tools are a good fit, such as an order system or a finance tool. There, the
PO also writes guides for staff and checks numbers with other teams.

## The problem

A PO writes all day. Two jobs are **Told** by a real PO:

- The PO writes user guides for the product's users.
- The PO reconciles costs and revenue with the accounting team. To reconcile means to compare
  two lists of the same money, line by line, and explain each line that does not match.

The rest are **Assumed** common PO jobs:

- The PO turns meetings into tasks by hand.
- The PO writes user stories and specs. (**Told:** the first PO writes specs for developers in
  Vietnamese, the same language as everything else.)
- The PO explains business terms to developers again and again.
- The PO collects feedback from chat apps and email, and sorts it by hand.
- The PO writes status reports for the manager every week.

Each job is small. Together they fill the week. Claude can do the first draft of each one. But
plain Claude chat forgets the product context every time. The PO has to explain the users and
the terms at the start of each chat.

## Goals

1. **The PO explains the product once.** A project wiki holds the users, the terms, the
   features and the decisions. Every skill reads it, and every job adds to it.
2. **Each repeat job takes one paste.** The PO pastes the raw input. The skill returns a draft
   the PO can send after a short edit.
3. **Drafts use the PO's format.** Each kind of document follows one template. The PO can
   change the template.
4. **The PO can use it without a terminal.** The PO installs it once. Then one chat line sets up
   a project ([06-onboarding.md](./06-onboarding.md)).
5. **No skill names one company or product.** A new PO starts a project wiki, and every
   skill works for them.

## Non-goals

- **No change to shared work without a yes.** The plugin may read the knowledge base, the task
  tracker, the message app and the mail app, in the part the PO picked. It may add a new draft
  page in the PO's own drafts place. Before it edits an existing page or creates a ticket, it
  shows the draft and waits for the PO's "yes". It never sends a message or a mail.
- **No company data in the plugin.** The plugin holds rules and templates. Product facts stay in
  the PO's own project wiki. Real customer data stays in the PO's own files.
- **No decisions for the PO.** The plugin can score a backlog or flag a gap. The PO makes the
  call.

## How we know it works

After two weeks of real use, ask each PO:

- Which skills did you use more than three times?
- Which draft did you send with less than five minutes of edits?
- Which skill did you stop using, and why?

A skill nobody uses after two weeks gets cut or rewritten.
