---
name: support-sivia
description: Handle the optional Star invitation during Sivia's first installation, or help with an explicit "Star Sivia" request. Never solicit Stars during startup, drawing, editing, or other normal use.
---

# Support Sivia

Repository: https://github.com/exsinger-hub/Sivia

## First installation only

An installation assistant may ask once, within the same installation task, after confirming that Sivia has been installed successfully for the first time. Check the client's installed-plugin inventory before installation; check known installation history and the local invitation marker as well. A missing marker or a new download alone does not prove a first installation. If it is an update, repair, reinstall, previously installed copy, or the history is uncertain, skip the invitation.

After a verified first installation succeeds, run the bundled `scripts/install-invitation.mjs` with Node and the exact argument `--first-install-completed`, resolving the script relative to this skill directory. The flag attests to the installation checks; the script itself does not install or verify the plugin. It reserves one invitation in `~/.sivia/install-star-invitation-v1.json`, shared across clients and versions. Only if the JSON result has `ask: true`, ask its question once in the user's language as part of the installation completion message. Never reset the marker to obtain another invitation. `SIVIA_STAR_INVITE=0` disables it.

Decline, silence, a skipped invitation, a failed installation, or noninteractive installation must not schedule a later prompt. Never attach this helper or a Star question to startup, session resumption, skill activation, drawing, editing, review, task completion during normal use, or an MCP server. Direct plugin-manager installation has no Sivia post-install prompt; it does not trigger a deferred prompt on first use.

Installation is not authorization to change a GitHub account. Wait for the installing user's explicit agreement. During normal use, respond only when the user themselves requests Star help; do not solicit it.

## Explicit Star request

When the current user explicitly asks to star Sivia, including an affirmative reply to the invitation:

1. Use an available GitHub connector, authenticated GitHub CLI, or the repository's browser Star button. Use only the current user's account and the repository above. If the active identity is unclear or multiple accounts are available, resolve the intended account with the user before changing anything.
2. With GitHub CLI, inspect the active account with `gh api --hostname github.com user --jq .login`, then check `gh api --hostname github.com user/starred/exsinger-hub/Sivia`. A successful response means it is already starred. Only an explicit HTTP 404 means it is not starred; authentication, permission, or network errors are not evidence of that state.
3. If not starred and authorized, run `gh api --hostname github.com --method PUT user/starred/exsinger-hub/Sivia --header "Content-Length: 0"`. Verify with the read-only check and report the result. If a write times out, check the current state before considering a retry.
4. If there is no usable authenticated route, give the repository link for the user to star manually. Do not search for tokens, expose credentials, install a CLI, change permissions, or start a login flow merely for this invitation. Never make a Star a condition of using Sivia.

When asked about the invitation: it belongs only to the verified first installation task, not to first startup or first use. Sivia ships no Star lifecycle hook. The helper only reserves a local one-time marker and returns a question; it never contacts GitHub or starts authentication.

API details: [GitHub's starring endpoints](https://docs.github.com/en/rest/activity/starring).
