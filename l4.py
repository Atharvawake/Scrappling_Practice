"""Lesson 4: REUSE saved login after the previous Python process has closed."""
from scrapling.fetchers import StealthySession
from settings import ROLE_URL, STATE, browser_options
from l3 import ensure_login

def main():
    # This launches a NEW browser; the old browser from l3 is already closed.
    with StealthySession(**browser_options()) as session:
        ensure_login(session)  # Loads saved state; checks validity; logs in if expired.
        response = session.fetch(ROLE_URL)
        print('Available roles:', response.css('.role-selection-name::text').getall())
        # Save again if later actions refreshed cookies or local storage.
        session.save_state(STATE)
    # Conceptually the reuse sequence is:
    # with StealthySession(...) as session:
    #     session.load_state(STATE)
    #     response = session.fetch(ROLE_URL)
    # Loading a JSON file does not prove that the server still accepts the login.
if __name__ == '__main__': main()
