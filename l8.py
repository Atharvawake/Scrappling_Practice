"""Lesson 8: Live values, screenshots, downloads, iframes and timeout handling.
Run: python l8.py             (screenshot only)
     python l8.py --download  (also click your configured download link)
"""
import argparse
from pathlib import Path
from scrapling.fetchers import StealthySession
from patchright.sync_api import TimeoutError as BrowserTimeout
from settings import ROLE_URL, STATE, required, browser_options, output_dir
from l3 import ensure_login
from l5 import open_my_task

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--download', action='store_true')
    args = parser.parse_args()
    if args.download: required('RAPID_DOWNLOAD_SELECTOR')
    def actions(page):
        open_my_task(page)
        page.screenshot(path=str(output_dir()/'my_task.png'), full_page=True)
        if args.download:
            # Register the listener BEFORE the click, otherwise an event can be missed.
            with page.expect_download() as event:
                page.locator(required('RAPID_DOWNLOAD_SELECTOR')).click()
            download = event.value
            if download.failure(): raise RuntimeError('Browser reported a failed download')
            filename = Path(download.suggested_filename).name
            download.save_as(str(output_dir()/filename))
        # Optional patterns: uncomment only after inspecting the target page.
        # page.locator('#loanNumber').fill('YOUR_EXACT_LOAN')
        # current_value = page.locator('#loanNumber').input_value()
        # page.locator('select#department').select_option(label='Operations')
        # For a custom dropdown, click the widget then its exact option instead.
        # frame = page.frame_locator('iframe#YOUR_FRAME_ID')
        # print(frame.locator('#YOUR_FIELD').inner_text())
        # Iframe contents are NOT included in the main-page response HTML.
    try:
        with StealthySession(**browser_options()) as session:
            ensure_login(session)
            session.fetch(ROLE_URL, page_action=actions)
            session.save_state(STATE)
    except BrowserTimeout as error:
        # Do not silently repeat a claim/submit if its outcome is uncertain.
        raise RuntimeError('Page/element did not become ready; inspect the selector and page.') from error
if __name__ == '__main__': main()
