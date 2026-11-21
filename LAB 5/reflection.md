# Lab 5 – Reflection

**Student:** Nayana SM (PES1UG24AM174) **Repo:** L5_48_gym_membership_system

### 1. Which issues were the easiest to fix, and which were the hardest? Why?

The easiest were the mechanical ones: unused imports and variables, `== None` → `is None`, snake_case renames, docstrings, the f-string, the final newline and the long lines. Each warning names the exact line and the fix is obvious. Swapping MD5 for SHA-256 and `random` for `secrets` was also a one-line change.

The hardest was the `eval()` in `calculateRenewalRate`. Bandit only says "don't use eval". It doesn't say what to use instead, and `ast.literal_eval` would not work because the string `"base_fee * 0.85"` is an expression, not a literal. I had to work out what the function was meant to do (apply a discount) and change its interface to take a numeric discount rate with range checking. I also had to make sure the output stayed the same (510.0). The hard-coded secret was similar. Removing the string was easy, but I had to decide where the value should come from (an environment variable) and stop the program printing it.

### 2. Did the static analysis tools report any false positives? If so, describe one example.

Partly. Bandit B105 flagged `gym_api_secret = "GYM_CLOUD_PORTAL_SECRET_2026"` as only **Low** severity / **Medium** confidence. Bandit matches variable names containing words like "secret", so the same check fires on harmless strings too, which can produce false positives. Here it was a real problem, though, and the program even printed the secret.

The clearer case is B311 on `random.randint`. Bandit warns about any use of `random`, even though most uses (shuffling, simulations) are fine. For a locker PIN it was a fair warning, but in other code you would mark it with `# nosec`. Pylint's W0612 "unused variable `base_fee`" was technically true but misleading: the variable was used, through the string passed to `eval`, which Pylint can't see.

### 3. How would you integrate static analysis tools into your actual software development workflow?

- **Locally:** add Flake8, Pylint and Bandit to a `pre-commit` config so they run on changed files before every commit, and turn on Flake8/Pylint in the editor so problems show up while typing.
- **In CI:** add a GitHub Actions job that runs `flake8`, `pylint --fail-under=9.5` and `bandit -r . -ll` (fail on Medium and above) on every push and pull request, so a PR can't be merged until the checks pass.
- **Configuration:** keep the rules in `setup.cfg` / `pyproject.toml` so everyone uses the same settings. Use `# nosec` / `# pylint: disable=` only with a comment explaining why, and never silence warnings globally.

### 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

- **Security:** Bandit went from 6 issues (2 High, 1 Medium) to none. The program can no longer run injected shell commands or arbitrary Python through `eval`, and the secret is no longer in the code or the output.
- **Robustness:** the shared mutable `member_log` bug is gone. `cancel_membership` now reports whether it worked instead of hiding all errors. The roster file is always closed and written as UTF-8. The module can be imported without running `main()`.
- **Readability:** Pylint went from 4.81 to 10.00 and Flake8 from 9 issues to 0. Consistent snake_case names, docstrings and shorter functions (`check_membership_status` and `get_active_summary` are now one line each) make the code easier to read.
- The program produces the same results as before (same renewal fee, active count and roster file).

**Observation not caught by any tool:** `register_member` charges a flat `50.0 * months` whatever the plan, while the existing members' fees suggest per-plan pricing (Gold 600 for 6 months, Platinum 1000 for 12). Static analysis can't find logic errors like this. You still need to read the code, run it and test it. I left the pricing unchanged because the correct rates are not specified.
