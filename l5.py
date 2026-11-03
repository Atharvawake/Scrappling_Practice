"""Lesson 5: Role → OPS → Tray → MY TASK, with explicit browser waits."""
from scrapling.fetchers import StealthySession
from settings import ROLE_URL, OPS_URL, STATE, required, browser_options, output_dir
from l3 import ensure_login

def click_one(page, selector):
    locator = page.locator(selector)
    locator.first.wait_for(state='visible')
    if locator.count() != 1:
        raise RuntimeError(f'Expected one visible target: {selector}')
    locator.click()

def open_my_task(page):
    # Fill these selectors from the real active page. Do not guess the role.
    click_one(page, required('RAPID_ROLE_SELECTOR'))
    # A role click can navigate asynchronously; wait before opening the OPS URL.
    page.wait_for_url(lambda url: '/session/role/selection' not in str(url))
    page.goto(OPS_URL, wait_until='domcontentloaded')
    page.get_by_text('COMMON APPLICATION TASKS', exact=True).wait_for(state='visible')
    click_one(page, required('RAPID_TRAY_BUTTON'))
    click_one(page, required('RAPID_MY_TASK_SELECTOR'))
    # This must identify the ACTIVE MY TASK pane, not its menu label.
    page.locator(required('RAPID_MY_TASK_READY')).wait_for(state='visible')

def fetch_my_task(session):
    return session.fetch(ROLE_URL, page_action=open_my_task)

def main():
    # Validate configuration before opening a browser or attempting login.
    for key in ('RAPID_ROLE_SELECTOR','RAPID_TRAY_BUTTON',
                'RAPID_MY_TASK_SELECTOR','RAPID_MY_TASK_READY'):
        required(key)
    with StealthySession(**browser_options()) as session:
        ensure_login(session)
        response = fetch_my_task(session)
        (output_dir()/'my_task.html').write_bytes(response.body)
        session.save_state(STATE)
        print('Saved the rendered MY TASK HTML for the next lesson.')
if __name__ == '__main__': main()
