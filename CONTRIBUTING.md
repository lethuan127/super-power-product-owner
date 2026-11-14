# Contributing

This is a small, best-effort project with one maintainer. Open an issue before a large pull
request, so we agree on the change first.

## Report a bug or ask for a feature

- Inside Claude: say "report this" or "báo lỗi plugin". The `send-feedback` skill drafts the
  issue and removes private data first.
- On GitHub: use the **Bug** or **Feature** form.

Never paste real company names, customer data, amounts or people's names into an issue.

## Close an issue

Close every issue with one comment, so the reporter learns the outcome. `send-feedback` reads
that comment when a user asks what happened to their feedback.

- `Fixed in <version>: <what changed>. Checked: <how>.`
- `Won't fix: <reason>.`
- `Duplicate of #<n>.`

## Run the checks

```bash
python3 -m unittest discover -s tests -t .           # free, runs in CI
python3 scripts/check_plugin.py                       # free, runs in CI
claude plugin validate .
claude plugin eval . --scaffold --trust-plugin --no-publish --ablation none \
  --runs 1 -j 4 --allow-tools Write Edit Bash         # costs model calls, about $2
```

Run the evals before a pull request that changes a skill.

## Rules for a change

- Skill files are in English. Add trigger words in other languages to the `description`.
- Write each rule in one place. Shared rules live in `skills/core/reference/`.
- No real company, customer or person names anywhere: skills, evals, docs, commit messages.
- Keep a `SKILL.md` under 500 lines. Link files one level deep.
- A change to a skill's behavior needs an eval case, or a reason why not.

## Out of scope

- A server or an API key for any app. The plugin uses the connectors the user already has.
- Rules for one company. The plugin stays general.
