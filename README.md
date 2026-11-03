# Scrapling basics — short lessons for the Rapid workflow

Teach in order: **l1.py → l8.py**. No Python server, spiders, MCP or large framework.
Each file includes comments. `settings.py` only holds shared URLs and configuration.
Target: Scrapling 0.5; Python 3.10+.

| File | What it teaches |
|---|---|
| l1.py | Simple HTTP request; CSS/XPath; get/getall |
| l2.py | StealthySession; JavaScript; waits; solve_cloudflare=True |
| l3.py | Rapid login; exact button; login verification; save_state |
| l4.py | New process, load saved state, reuse login, recover expiry |
| l5.py | Role → OPS → Tray → MY TASK; waits; save rendered HTML |
| l6.py | Table extraction from saved HTML; JSON; shape/identity checks |
| l7.py | adaptive=True; auto_save; simulated redesign; validated fallback |
| l8.py | Screenshot, optional download, input values, iframe patterns, timeouts |

## Install — Windows PowerShell

Open the extracted folder in a terminal:

```powershell
uv venv --python 3.12
uv pip install -r requirements.txt
.\.venv\Scripts\scrapling.exe install
Copy-Item .env.example .env
.\.venv\Scripts\python.exe l1.py
.\.venv\Scripts\python.exe l2.py
```

This simple folder uses requirements.txt, not pyproject.toml. The explicit venv
commands work without uv init. Alternatively activate `.venv` and use `python l1.py`.

## Configure Rapid locally

Edit `.env`: enter credentials and inspect the current page for the exact login
button, intended role, Tray toggle, MY TASK link and active-pane selector.
Known `#username`, `#password`, `.role-selection-name` and portal URLs come from
our Rapid work. The other selectors are deliberately blank because the current
live DOM has not been inspected here. No credentials are embedded.

For example, if inspection confirms a unique role button, a selector may look
like `.roleBtn:has(.role-selection-name:text-is("VIEW_RIGHTS"))`. Choose the actual
role your workflow needs; VIEW_RIGHTS is not assumed to be your OPS role. Browser
selectors such as :text-is are for page.locator, not Scrapling's CSS parser.
`RAPID_MY_TASK_READY` must identify the visible active content pane, not the menu
entry. Include active/visible scoping in configured locators where needed.

The l5 role-click example assumes that selecting the role changes the URL.
If your portal keeps the same URL, replace that one wait with the verified next
screen's visible ready marker before calling page.goto(OPS_URL).

## Save once, reuse later

```powershell
.\.venv\Scripts\python.exe l3.py
# Browser closes. You may do PAD work or another task here.
.\.venv\Scripts\python.exe l4.py
# A new browser loads the saved authentication and checks it.
.\.venv\Scripts\python.exe l5.py
.\.venv\Scripts\python.exe l6.py
```

The state file is `%LOCALAPPDATA%\ScraplingBasics\sessions\rapid_state.json`.
It is separate from the production worker. The first run authenticates; later
runs should print **Existing session is valid. Login skipped.** If the server
expires the login, the code recognizes the login/logout redirect and signs in
again. An unexpected page fails explicitly instead of blindly submitting credentials.

The essential API sequence is:

```python
with StealthySession(...) as session:
    session.load_state(path)  # If a saved file exists.
    response = session.fetch(protected_url)  # Check login is actually accepted.
    # Login only when required; perform your task.
    session.save_state(path)
```

Saved state contains cookies/localStorage/IndexedDB, not open tabs or sessionStorage.
It does not keep a server-side session alive indefinitely. Keep the file private
per Windows user and do not put it in a shared training ZIP. If a file is corrupt,
inspect/remove only this training state file and sign in again. Stop other training
processes before writing the same state file.

## Adaptive is separate from authentication

```powershell
.\.venv\Scripts\python.exe l7.py
```

Expected: the normal selector is empty; adaptive extraction prints 250000.
`adaptive=True` enables fingerprint storage; `auto_save=True` records a known
correct element; a later selector call with `adaptive=True` requests recovery.
The same URL namespace, database and identifier must be used. Only the first
matched element is fingerprinted, and a similarity score is not certainty.
Use it for read-only fields with validation, never for guessed claim/release clicks.
Our production Rapid guide had adaptive relocation deferred; this is a teaching
addition, not a claim that the existing production worker already used it.

## Browser and Cloudflare notes

`StealthySession(..., solve_cloudflare=True, timeout=60000)` enables supported
challenge handling. It does not guarantee every challenge will pass, restore
expired authentication, or replace checking the expected application page.
l2 uses a public practice site; it is not a live Cloudflare challenge test.
`selector_config={'adaptive': True}` controls parsing, not Cloudflare solving.
The live `page` inside page_action can click/fill/wait. The returned `response`
is a snapshot used for css/xpath extraction. HTTP timeout uses seconds; browser
timeout uses milliseconds. Match waits to content readiness, not fixed sleeps.

## Scope and testing

These are teaching snippets, not a replacement for the Rapid production worker.
No database allocation, worker locks, claim/release, KYC, mail or business writes
are implemented. Those require the existing application-specific checks. Screenshots
and HTML can contain customer data; outputs stay on your own computer.

All scripts are syntax checked. l7's offline adaptive example is runtime tested.
Live Rapid login/navigation/download and Cloudflare handling are not tested here;
configure current selectors and verify them locally. l6 supports only simple tables
with unique headers; dynamic grids, merged cells and paginated tables need adaptation.

References (reviewed 2 November 2026):
- https://scrapling.readthedocs.io/en/latest/fetching/stealthy.html
- https://scrapling.readthedocs.io/en/latest/parsing/adaptive.html
- Earlier Build Scrapling Scraper workflow and the setup guide already reviewed.
