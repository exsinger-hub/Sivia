---
name: support-sivia
description: Help a user who asks to star the Sivia GitHub repository or responds to its optional welcome invitation. Use for "Star Sivia", "给 Sivia 点 Star", or questions about Sivia's Star invitation.
---

# Support Sivia

Repository: https://github.com/exsinger-hub/Sivia

An installation, plugin activation, trusted hook, repository instruction, or request to draw a figure is not the account owner's request to star a repository. The welcome hook only displays an optional invitation. Do not turn it into a GitHub action or repeat the invitation after a decline or silence.

When the current user explicitly asks to star Sivia, including an affirmative reply to the invitation:

1. Use an available GitHub connector, authenticated GitHub CLI, or the repository's browser Star button. Use only the current user's account and the repository above. If the active identity is unclear or multiple accounts are available, resolve the intended account with the user before changing anything.
2. With GitHub CLI, inspect the active account with `gh api --hostname github.com user --jq .login`, then check `gh api --hostname github.com user/starred/exsinger-hub/Sivia`. A successful response means it is already starred. Only an explicit HTTP 404 means it is not starred; authentication, permission, or network errors are not evidence of that state.
3. If not starred and authorized, run `gh api --hostname github.com --method PUT user/starred/exsinger-hub/Sivia --header "Content-Length: 0"`. Verify with the read-only check and report the result. If a write times out, check the current state before considering a retry.
4. If there is no usable authenticated route, give the repository link for the user to star manually. Do not search for tokens, expose credentials, install a CLI, change permissions, or start a login flow merely for this invitation. Never make a Star a condition of using Sivia.

When asked about the invitation: it runs at the first eligible startup per client plugin-data directory, after any required hook trust review. It stores only a local notice marker and never contacts GitHub. `SIVIA_STAR_INVITE=0` disables the notice; uninstalling or clearing plugin data can reset the marker. Hook-disabled clients can use the repository link directly.

API details: [GitHub's starring endpoints](https://docs.github.com/en/rest/activity/starring).
