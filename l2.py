"""Lesson 2: StealthySession, Cloudflare handling and waiting for JavaScript."""
from scrapling.fetchers import StealthySession

def main():
    with StealthySession(
        headless=True,           # Show the browser while learning.
        timeout=60000,            # Browser timeout is in milliseconds.
        solve_cloudflare=True,   # Try supported Cloudflare challenge handling.
        selector_config={'adaptive': True},  # Enables parser storage capability.
    ) as session:
        response = session.fetch('https://quotes.toscrape.com/js/',
                                 wait_selector='.quote',
                                 wait_selector_state='visible')
        print(response.css('.quote .text::text').get())
        # Reuse the SAME running browser session for another page.
        second = session.fetch('https://quotes.toscrape.com/js/page/2/',
                               wait_selector='.quote')
        print(second.css('.quote .text::text').get())
    # Exiting with closes the browser. Persisted login is taught next.
    # This practice website does not demonstrate a Cloudflare challenge itself.
    # adaptive=True does not automatically train selectors: see l7.py.
if __name__ == '__main__': main()
