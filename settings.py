"""Small shared settings file: URLs from our Rapid discussion, secrets from .env."""
import os
from pathlib import Path
from dotenv import load_dotenv
ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / '.env')
BASE = 'https://rapid.hfs.in'
LOGIN_URL = BASE + '/security/login'
ROLE_URL = BASE + '/hfs-housing-ui/session/role/selection'
OPS_URL = BASE + '/hfs-housing-ui/page/dic/dictasks'
# Keep training state separate from your production worker's state.
PRIVATE = Path(os.environ.get('LOCALAPPDATA', str(Path.home()/'.local/share')))
STATE = PRIVATE / 'ScraplingBasics' / 'sessions' / 'rapid_state.json'
OUTPUT = ROOT / 'output'

def required(name):
    value = os.getenv(name, '').strip()
    if not value:
        raise ValueError(f'Fill {name} in .env first (see .env.example).')
    return value

def browser_options():
    # Timeouts here are milliseconds. 60000 = 60 seconds.
    return dict(headless=False, timeout=60000, solve_cloudflare=True,
                selector_config={'adaptive': True})
    # real_chrome=True is optional if Chrome is installed for this Windows user.
    # Cloudflare solving is opt-in assistance, not a guarantee of access.

def output_dir():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    return OUTPUT
