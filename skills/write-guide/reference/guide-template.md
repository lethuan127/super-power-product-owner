# Guide template

Write the headings in the project language. Keep the four parts in this order.

```markdown
# <Task, as the reader says it, such as "Create an order">

**For:** <user group>. **After this guide you can:** <one goal>.
**Before you start:** <what the reader needs, such as a login or a customer code>.

## Steps

1. Open <screen>.
   [screenshot: <screen name>]
2. Click **<exact button name>**.
3. In **<exact field name>**, enter <what>.
   > Note: <one short warning, only if a step can go wrong>.
4. ...

**Result:** <what the reader sees when it worked>.

## Common mistakes

| You see | Why | What to do |
|---|---|---|
| "<exact error message>" | <cause> | <fix> |
| <a likely mistake> (to confirm) | <likely cause> | <likely fix> |

## Help

Ask <role, such as "the system admin">, in <channel or place>.
```

Rules:

- One action per step. If a step has "and", split it.
- Bold every button and field name, exactly as the screen shows it.
- Put a warning before the step it protects, never after.
- Keep the guide under about 15 steps. Split a longer task into two guides.
- Fill "Common mistakes" with every error the input gives. Then add 2 to 4 likely mistakes for
  this task, such as the wrong record picked, a required field left empty, or a step done out of
  order. Mark each one "(to confirm)". Never leave the table empty.
