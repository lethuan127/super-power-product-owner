---
name: ask-project
description: "Answers a question about the project from the project wiki, with a link to the page or source behind each claim. Use when the user asks what the project decided, how a feature works, who uses it, what a term means, or what is still open, such as 'what did we decide about X', 'how does X work in our product', 'dự án đã chốt gì về X', 'tính năng X chạy thế nào', 'còn câu hỏi nào mở'."
---

# Ask the project

Read [../core/reference/rules.md](../core/reference/rules.md) and
[../core/reference/project-wiki.md](../core/reference/project-wiki.md) first.

## Steps

1. Find the project. If there is none, say so, and offer the `setup-project` skill.
2. Read `index.md`. Open only the pages that can answer the question.
3. If the pages answer it, write a short answer. Put a link after each claim, to the wiki page
   or the source: `(wiki/decisions.md)`.
4. If a page marks the fact as `CONFLICT`, give both versions and say the user must decide.
5. If the wiki has no answer, say: "The project wiki does not have this." Then:
   1. If a knowledge base is connected, search it in the part listed in `apps.md`. Answer with
      links to the pages you read.
   2. If it is still not found, say so. Do not answer from general knowledge as if the project
      said it. You may add general knowledge in a separate part named "General knowledge, not
      from the project".
6. If the answer is useful and new, ask: "Save this answer to the project wiki?" On a "yes",
   follow "Write a fact" in `project-wiki.md`.

## Done when

- Every claim about the project has a link the user can open.
- Nothing from general knowledge is shown as a project fact.
