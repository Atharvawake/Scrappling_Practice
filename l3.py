"""Lesson 3: Verify Rapid login, sign in only if needed, and SAVE session state."""
from urllib.parse import urlsplit
from scrapling.fetchers import StealthySession
from settings import LOGIN_URL, ROLE_URL, STATE, required, browser_options

def authenticated(response):
    # Validate the final route AND a role-page marker, not just HTTP 200.
    expected, actual = urlsplit(ROLE_URL), urlsplit(response.url)
    return (actual.netloc == expected.netloc and actual.path == expected.path
            and bool(response.css('.role-selection-name')))

def login_action(page):
    # This is a LIVE browser Page. .css() is for the later Scrapling snapshot.
    page.locator('#username').wait_for(state='visible')
    page.locator('#username').fill(required('RAPID_USERNAME'))
    page.locator('#password').fill(required('RAPID_PASSWORD'))
    button = page.locator(required('RAPID_LOGIN_BUTTON'))
    # Avoid the strict-mode problem we encountered with ambiguous buttons.
    if button.count() != 1:
        raise RuntimeError('Login button selector must identify exactly one button.')
    button.click()
    page.wait_for_url(ROLE_URL)
    page.locator('.role-selection-name').first.wait_for(state='visible')

def ensure_login(session):
    # load_state is called AFTER entering the session context.
    if STATE.exists():
        session.load_state(STATE)
    response = session.fetch(ROLE_URL)
    if authenticated(response):
        print('Existing session is valid. Login skipped.')
    else:
        # Only a known login/logout redirect is a reason to authenticate again.
        actual, login = urlsplit(response.url), urlsplit(LOGIN_URL)
        known_path = actual.path in (login.path, '/security/logout_sucess')
        if actual.netloc != login.netloc or not known_path:
            raise RuntimeError('Unexpected page; do not submit login blindly.')
        response = session.fetch(LOGIN_URL, page_action=login_action)
        if not authenticated(response):
            raise RuntimeError('Login failed: role-selection page not verified.')
        print('Login completed and verified.')
    STATE.parent.mkdir(parents=True, exist_ok=True)
    session.save_state(STATE)
    print('Authentication saved at:', STATE)
    return response

def main():
    with StealthySession(**browser_options()) as session:
        ensure_login(session)
if __name__ == '__main__': main()
