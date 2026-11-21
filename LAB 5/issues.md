# Lab 5 – Static Code Analysis: Issue Log

**File:** `gym_membership_system.py` **Student:** Nayana SM (PES1UG24AM174)

Before fixes: Pylint **4.81/10**, Bandit **6 issues** (2 High, 1 Medium, 3 Low), Flake8 **9 issues**.
After fixes: Pylint **10.00/10**, Bandit **No issues identified**, Flake8 **0 issues**.
Reports are in `reports/before/` and `reports/after/`. Line numbers refer to the original file.

Highest severity first:

| # | Issue | Type | Tool / Code | Line(s) | Description | Fix Approach |
|---|-------|------|-------------|---------|-------------|--------------|
| 1 | Shell command injection | Security (High) | Bandit B605 | 58 | `os.system("echo ... " + filename)` passes a filename to the shell. A name like `x; rm -rf ~` would run arbitrary commands. | Removed the shell call; the message is printed with `print()`. |
| 2 | Weak hash (MD5) | Security (High) | Bandit B324 | 47 | MD5 is broken and can collide, so it shouldn't be used for identifiers that need to be unique or tamper-resistant. | Switched to `hashlib.sha256(...)`. |
| 3 | Use of `eval()` | Security (Medium) | Bandit B307, Pylint W0123 | 42 | `calculateRenewalRate` evaluates a caller-supplied string, so it can run any Python code. It also made `base_fee` look unused (W0612). | The function now takes a numeric `discount_rate`, checks it is between 0 and 1, and returns `base_fee * (1 - discount_rate)`. The output is unchanged (510.0). |
| 4 | Hard-coded secret, printed to stdout | Security (Low, but serious in practice) | Bandit B105 | 70, 79 | The portal secret is committed in source code and also printed to the console. | The secret is read from the `GYM_API_SECRET` environment variable. The program only prints whether it is set. |
| 5 | Insecure random for PIN | Security (Low) | Bandit B311 | 51 | `random` is predictable, which is not acceptable for locker PINs. | Uses `1000 + secrets.randbelow(9000)`, which gives the same 4-digit range. |
| 6 | Bare `except: pass` | Bug / Security (Low) | Bandit B110, Pylint W0702, Flake8 E722 | 26–27 | Swallows every exception, including typos and `KeyboardInterrupt`. The caller cannot tell whether the cancel worked. | Catches only `KeyError` and returns `True`/`False`. |
| 7 | Mutable default argument | Bug | Pylint W0102 | 15 | `member_log=[]` is created once and shared, so log entries pile up across calls. | Default changed to `None`; a new list is created inside the function. |
| 8 | File not closed safely, no encoding | Bug / Quality | Pylint R1732, W1514 | 55–57 | `open()`/`close()` leaks the handle if `write` raises, and the encoding depends on the platform. | Uses `with open(filename, "w", encoding="utf-8")`. |
| 9 | Unused variables / import | Quality | Pylint W0612, W0611; Flake8 F841, F401 | 6, 31, 63 | `math`, `locker_deposit` and the loop variable `m` are never used. | Removed them. The loop was rewritten as `sum(... for details in roster.values())`. |
| 10 | Shadowing a global | Quality | Pylint W0621 | 61 | The parameter `members` hides the module-level `members` dict. | Renamed the parameter to `roster`. |
| 11 | `== None` comparison and redundant if/else | Style | Pylint C0121, R1703, R1705; Flake8 E711 | 32–37 | Uses `== None` and an `if/else` that just returns True/False. | Uses `is None` and `return members[m_id]["months_left"] > 0`. |
| 12 | Non-snake_case names, missing docstrings | Style | Pylint C0103, C0116 | 15, 23, 30, 40, all funcs | camelCase function names; no function docstrings. | Renamed to `register_member`, `cancel_membership`, `check_membership_status`, `calculate_renewal_rate`; added docstrings. |
| 13 | Old-style `%` formatting | Style | Pylint C0209 | 19 | `%` string formatting. | Replaced with an f-string. |
| 14 | Lines too long | Style | Flake8 E501 | 10, 11, 18 | Lines longer than 79 characters. | Split the dict literals across lines. |
| 15 | Missing final newline; `main()` runs on import | Style / Quality | Pylint C0304, Flake8 W292 | 82 | No newline at end of file, and `main()` runs whenever the module is imported. | Added the newline and an `if __name__ == "__main__":` guard. |

**Commits**
1. `Fix all Bandit security findings`: issues 1–6
2. `Fix Pylint findings (score 4.81 -> 10.00)`: issues 7–13, 15
3. `Fix Flake8 style findings`: issue 14, plus the after reports and these docs
