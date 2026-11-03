"""Lesson 7: adaptive=True, auto_save and recovery after an HTML change.
No website or server needed: two tiny HTML strings simulate a redesign.
"""
from scrapling import Selector
from settings import output_dir

def main():
    old_html = '<article><span id="amount" data-field="amount">250000</span></article>'
    new_html = '<article><span class="new-amount" data-field="amount">250000</span></article>'
    url = 'https://training.example.com/loan'
    options = dict(url=url, adaptive=True,
                   storage_args={'storage_file': str(output_dir()/'adaptive.db'), 'url': url})
    old = Selector(old_html, **options)
    # 1. Train only on an element you KNOW is correct.
    old.css('#amount', auto_save=True, identifier='loan.amount')
    changed = Selector(new_html, **options)
    print('Normal selector:', changed.css('#amount'))  # Empty: id was removed.
    # 2. Retrieve the stored fingerprint and find similar elements in the new DOM.
    matches = changed.css('#amount', adaptive=True,
                          identifier='loan.amount', percentage=70)
    # 3. Similarity is not proof. Validate before using the recovered value.
    if len(matches) != 1 or matches[0].attrib.get('data-field') != 'amount':
        raise ValueError('Adaptive candidate failed validation.')
    print('Recovered amount:', matches[0].text)
    assert matches[0].text == '250000'
    # With a browser: selector_config={'adaptive': True} enables storage.
    # Then response.css(..., auto_save=True) trains; adaptive=True requests fallback.
    # Adaptive matching does NOT repair page.locator(...) browser clicks.
    # Never use a similarity guess for claim, release, approve or submit buttons.
if __name__ == '__main__': main()
