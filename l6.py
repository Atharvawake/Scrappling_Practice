"""Lesson 6: Parse saved Rapid HTML; extract table rows and write JSON."""
import json
from scrapling import Selector
from settings import OPS_URL, required, output_dir

def main():
    source = output_dir()/'my_task.html'
    if not source.exists():
        raise FileNotFoundError('Run l5.py first to capture MY TASK HTML.')
    page = Selector(source.read_bytes(), url=OPS_URL)
    tables = page.css(required('RAPID_TABLE_SELECTOR'))
    if len(tables) != 1:
        raise ValueError('Select exactly one active table; reject ambiguous matches.')
    table = tables[0]
    headers = [str(x.get_all_text(strip=True)) for x in table.css('thead th')]
    if not headers or len(set(headers)) != len(headers):
        raise ValueError('Expected unique table headers; adapt for this table layout.')
    records = []
    for row in table.css('tbody tr'):
        values = [str(x.get_all_text(strip=True)) for x in row.css('td')]
        # This basic example handles regular tables, not rowspan/colspan grids.
        if len(values) != len(headers):
            raise ValueError('Unexpected row layout or no-results message.')
        records.append(dict(zip(headers, values)))
    (output_dir()/'my_task.json').write_text(
        json.dumps(records, indent=2, ensure_ascii=False), encoding='utf-8')
    print('Saved rows:', len(records))
    # For one loan: filter by its EXACT loan-number column and require one match.
    # Do not assume the first row belongs to the requested application.
    # LIVE form values are read inside page_action with locator.input_value().
    # The HTML value attribute can be stale after JavaScript edits.
if __name__ == '__main__': main()
