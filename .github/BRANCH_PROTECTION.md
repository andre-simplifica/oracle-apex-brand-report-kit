# Recommended main-branch protection

After the first successful CI run, configure `main` to require a pull request, at least one approving review, conversation resolution, and the `validate` status check. Restrict force pushes and deletion. Keep administrator bypass available only for repository recovery.

This setting is intentionally documented rather than automated because GitHub plan, owner policy, and bootstrap timing vary.
