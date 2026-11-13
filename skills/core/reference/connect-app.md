# Connect an app

Connect an app only when the current job needs it. A connector is Claude's link to an outside
app. The user adds it once, with their own login.

## The four kinds of app

| Kind | Examples | Read | Write |
|---|---|---|---|
| Knowledge base | Confluence, Notion, Google Drive, SharePoint | yes | a new draft page in the drafts place: yes. An edit: after a "yes" |
| Task tracker | Jira, Linear | yes | after a "yes" |
| Message app | Slack, Microsoft Teams | yes | never |
| Mail app | Gmail, Outlook | yes | never |

## Steps

1. Look at the tools you have. Find a tool for this app, such as a Jira search tool.
2. If you find no tool, tell the user the app is not connected. Give these steps:
   1. Open Claude's settings.
   2. Open "Connectors".
   3. Find the app and click "Connect".
   4. Log in with your own account.
   5. Come back and say "done".
3. Wait for "done". Never ask for a password or a token in the chat.
4. List what you can see: spaces, projects, channels or labels. Ask the user to pick the part for
   this project. This list also proves that the connection works.
5. Add one line to the wiki page `apps.md`:
   `- Jira: project ABC (connected 2026-11-13). Read: yes. Write: after a "yes".`
6. Add a `connect` line to `log.md`.

## Rules

- Read only the part saved in `apps.md`. For another part, ask first, and add it to `apps.md`.
- If the company does not allow a connector, do the job with files the user gives instead.
