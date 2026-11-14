# Read the plugin's GitHub repo

The plugin's repo is `lethuan127/super-power-product-owner`. It is public, so reading needs no
login. Use the first way that works:

1. `gh auth status` succeeds: `gh issue list -R lethuan127/super-power-product-owner --state all --search "<skill> in:title"`,
   then `gh issue view <number> -R lethuan127/super-power-product-owner --comments`.
2. A GitHub connector is connected: search and read with it, in the same repo.
3. Otherwise read the public API. It returns JSON. A github.com search page refuses a fetch.
   - Search: `https://api.github.com/search/issues?q=repo:lethuan127/super-power-product-owner+<skill>+in:title`
   - One issue: `https://api.github.com/repos/lethuan127/super-power-product-owner/issues/<number>`
   - Its comments: the same link plus `/comments`.

   Use `curl` first. If the answer says "Use add_repo", call the `add_repo` tool for
   `lethuan127/super-power-product-owner` with read access, then retry. If that tool is missing,
   fetch the same links with the web fetch tool. Tell the user that the app may ask them to
   approve the fetch.
