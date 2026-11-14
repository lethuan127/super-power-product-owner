---
name: feedback-status
description: "Tells the user what happened to feedback, a bug report or a suggestion they sent about this plugin: not looked at yet, fixed in which version, or won't fix and why. Reads the GitHub issue and the maintainer's comments. Use whenever the user asks about the status of their feedback, even when the project log already mentions it, because the log cannot know what the maintainer did. Use when the user says 'what happened to my feedback?', 'is my bug fixed?', 'status of my suggestion', 'góp ý của tôi tới đâu rồi?', 'góp ý về <skill> sao rồi?', 'lỗi mình báo sửa chưa?', 'đề xuất của mình thế nào rồi?'."
---

# Feedback status

Read [../core/reference/rules.md](../core/reference/rules.md) and
[../core/reference/github.md](../core/reference/github.md) first.

## Steps

1. Find the issue. Use the first that has it:
   1. a link or a `feedback-*.md` file name on a `feedback` line in `log.md`;
   2. a link in the chat;
   3. a search for the skill's name, with `github.md`.
2. If you find a `feedback-*.md` file and no issue, the feedback was never filed. Say so, and
   offer the `send-feedback` skill to file it now.
3. Read the issue and its comments, with `github.md`.
4. Answer in one or two plain sentences, in the project language:
   - open, with no comment from the maintainer: "Not looked at yet";
   - open, with a comment: what the comment says;
   - closed with "Fixed in <version>": what changed, and that it works once the plugin updates;
   - closed with "Won't fix": the reason.
   Put the issue link after the answer.
5. If every way in `github.md` fails, say that you could not read GitHub, and give the user the
   issue link to open. Never answer the status from `log.md` alone.

## Done when

- The answer names the issue's state and comes from the issue itself, with its link.
- Or the answer says plainly that GitHub could not be read, and gives the link.
