"""Opt-in real Firefox smoke test (pip install selenium; PARSIMONY_BROWSER_TESTS=1).

Requires Firefox and geckodriver (Selenium Manager can locate/download the driver).
The normal offline suite does not require browser dependencies or fetch a driver.
"""
import json
import os
from contextlib import contextmanager
import tempfile
import unittest
from pathlib import Path

from parsimony.scoring import freeze
from parsimony.site import build, render
from tests.test_scoring import record


@unittest.skipUnless(os.environ.get('PARSIMONY_BROWSER_TESTS') == '1', 'opt-in Firefox smoke test')
class SiteBrowserTests(unittest.TestCase):
    @contextmanager
    def rendered_browser(self, javascript=True):
        from selenium import webdriver

        records = [record('Alpha', 'task', net=1, churn=1),
                   record('Beta', 'task', net=-2, churn=2, resolved=False)]
        options = webdriver.FirefoxOptions()
        options.add_argument('-headless')
        options.set_preference('javascript.enabled', javascript)
        with tempfile.TemporaryDirectory() as directory, webdriver.Firefox(options=options) as browser:
            page = Path(directory) / 'index.html'
            page.write_text(render(build(freeze(records, 'browser-audit'), records, draws=10)))
            browser.get(page.as_uri())
            yield browser, Path(directory)

    def narrow_viewport(self, browser, directory, url, width):
        from selenium.webdriver.common.by import By

        # Headless Firefox clamps top-level windows to 500 CSS px. A real browsing
        # context in an iframe exercises narrower CSS viewports without pretending
        # that set_window_size(320, ...) actually made innerWidth 320.
        wrapper = directory / 'mobile.html'
        wrapper.write_text(f'<!doctype html><iframe src="{url}" '
                           f'style="width:{width}px;height:760px;border:0"></iframe>')
        browser.switch_to.default_content()
        browser.get(wrapper.as_uri())
        browser.switch_to.frame(browser.find_element(By.TAG_NAME, 'iframe'))
        self.assertEqual(browser.execute_script('return innerWidth'), width)

    def test_keyboard_sort_focus_and_escape_tooltips(self):
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.support.ui import Select

        with self.rendered_browser() as (browser, directory):
            for task_view in [False, True]:
                if task_view:
                    search = browser.find_element(By.ID, 'task-search')
                    search.send_keys('task')
                    self.assertEqual(browser.switch_to.active_element, search)
                for key in (['net'] if task_view else ['net', 'solved_net', 'resolve_rate', 'coverage']):
                    selector = f'#board button[data-sort="{key}"]'
                    button = browser.find_element(By.CSS_SELECTOR, selector)
                    browser.execute_script('arguments[0].focus()', button)
                    for activation in [Keys.ENTER, Keys.SPACE]:
                        before = button.find_element(By.XPATH, '..').get_attribute('aria-sort')
                        button.send_keys(activation)
                        button = browser.find_element(By.CSS_SELECTOR, selector)
                        self.assertEqual(browser.switch_to.active_element, button)
                        self.assertIn(button.find_element(By.XPATH, '..').get_attribute('aria-sort'),
                                      ['ascending', 'descending'])
                        if before != 'none':
                            self.assertNotEqual(button.find_element(By.XPATH, '..').get_attribute('aria-sort'), before)
                    button.send_keys(Keys.TAB)
                    self.assertNotEqual(browser.switch_to.active_element, button)
                for chart, selector in [('scatter', '#graph circle[data-point]'), ('bar', '[data-bar]')]:
                    Select(browser.find_element(By.ID, 'chart-type')).select_by_value(chart)
                    point = browser.find_element(By.CSS_SELECTOR, selector)
                    # Settle scrolling before focus: scroll intentionally dismisses tooltips.
                    browser.execute_async_script('''
                        const point = arguments[0], done = arguments[1];
                        point.scrollIntoView({block: 'center'});
                        requestAnimationFrame(() => requestAnimationFrame(done));
                    ''', point)
                    browser.execute_script('arguments[0].focus({preventScroll: true})', point)
                    tooltip = browser.find_element(By.ID, 'graph-tooltip')
                    self.assertTrue(tooltip.is_displayed())
                    point.send_keys(Keys.ESCAPE)
                    self.assertFalse(tooltip.is_displayed())
                    self.assertEqual(browser.switch_to.active_element, point)
                    browser.execute_script("arguments[0].dispatchEvent(new MouseEvent('mousemove'))", point)
                    self.assertFalse(tooltip.is_displayed())
                    browser.execute_script('arguments[0].blur(); arguments[0].focus({preventScroll: true})', point)
                    self.assertTrue(tooltip.is_displayed())
                    browser.execute_script('arguments[0].blur()', point)
                    self.assertFalse(tooltip.is_displayed())
            reset = browser.find_element(By.ID, 'task-reset')
            reset.send_keys(Keys.ENTER)
            self.assertEqual(browser.switch_to.active_element, reset)

    def test_fixed_metrics_table_task_and_charts(self):
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import Select

        with self.rendered_browser() as (browser, directory):
            browser.get((directory / 'index.html').as_uri() + '?keep=1#board')
            rows = browser.find_elements(By.CSS_SELECTOR, '#board tbody tr')
            self.assertEqual([row.find_elements(By.TAG_NAME, 'td')[1].text for row in rows], ['Alpha', 'Beta'])
            self.assertEqual(rows[0].find_elements(By.TAG_NAME, 'td')[0].text, '1')
            self.assertEqual(rows[1].find_elements(By.TAG_NAME, 'td')[0].text, '—')
            self.assertEqual([cell.text for cell in rows[0].find_elements(By.TAG_NAME, 'td')[2:]],
                             ['1.0', '1.0', '100.0%', '1/1'])
            self.assertEqual([cell.text for cell in rows[1].find_elements(By.TAG_NAME, 'td')[2:]],
                             ['—', '−2.0', '0.0%', '0/0'])
            self.assertIn('Measured', browser.find_element(By.CSS_SELECTOR, '#board thead').text)
            x = Select(browser.find_element(By.ID, 'graph-x'))
            self.assertEqual(x.first_selected_option.get_attribute('value'), 'solved_net')
            self.assertEqual([p.get_attribute('data-model') for p in browser.find_elements(By.CSS_SELECTOR, '#graph circle[data-point]')], ['Alpha'])
            Select(browser.find_element(By.ID, 'chart-type')).select_by_value('bar')
            self.assertEqual([p.text for p in browser.find_elements(By.CSS_SELECTOR, '.bar-name')], ['Alpha'])
            self.assertEqual(browser.find_element(By.ID, 'graph-x-label').text, 'Metric')
            self.assertFalse(browser.find_element(By.ID, 'graph-y-control').is_displayed())
            self.assertIn('Net units added, solved (mean)', browser.find_element(By.ID, 'graph-legend').text)
            x.select_by_value('net')
            self.assertEqual([p.text for p in browser.find_elements(By.CSS_SELECTOR, '.bar-name')], ['Beta', 'Alpha'])
            x.select_by_value('resolve_rate')
            self.assertEqual([p.text for p in browser.find_elements(By.CSS_SELECTOR, '.bar-name')], ['Alpha', 'Beta'])
            self.assertEqual([p.text for p in browser.find_elements(By.CSS_SELECTOR, '.bar-value')], ['100%', '0%'])
            self.assertEqual(browser.find_element(By.ID, 'graph-legend').text, 'Solved (%).')
            self.assertEqual(browser.execute_script('return location.search'), '?keep=1&chart=bar')
            self.assertEqual(browser.execute_script('return location.hash'), '#board')
            browser.find_element(By.ID, 'task-search').send_keys('task')
            self.assertEqual(len(browser.find_elements(By.CSS_SELECTOR, '#board tbody tr')), 2)
            self.assertEqual([p.text for p in browser.find_elements(By.CSS_SELECTOR, '.bar-name')], ['Beta', 'Alpha'])
            self.assertEqual(Select(browser.find_element(By.ID, 'graph-x')).first_selected_option.get_attribute('value'), 'net')
            Select(browser.find_element(By.ID, 'chart-type')).select_by_value('scatter')
            self.assertEqual(len(browser.find_elements(By.CSS_SELECTOR, '#graph circle[data-point]')), 2)
            self.assertTrue(browser.find_element(By.ID, 'graph-y-control').is_displayed())
            browser.find_element(By.ID, 'task-reset').click()
            self.assertEqual(len(browser.find_elements(By.CSS_SELECTOR, '#board tbody tr')), 2)
            self.assertEqual(Select(browser.find_element(By.ID, 'graph-x')).first_selected_option.get_attribute('value'), 'resolve_rate')
            # Swapping to the all-measured footprint shows the failed model too.
            Select(browser.find_element(By.ID, 'graph-y')).select_by_value('net')
            self.assertEqual(len(browser.find_elements(By.CSS_SELECTOR, '#graph circle[data-point]')), 2)

    def test_published_structure_titles_and_disabled_javascript_fallback(self):
        from selenium.webdriver.common.by import By

        titles = dict(index='DeepSWE · Python', javascript='DeepSWE · JavaScript',
                      typescript='DeepSWE · TypeScript', go='DeepSWE · Go',
                      verified='SWE-bench Verified · Python', live='SWE-bench Live Lite · Python')
        root = Path(__file__).resolve().parents[1] / 'site'
        with self.rendered_browser() as (browser, directory):
            for name, title in titles.items():
                with self.subTest(board=name):
                    browser.get((root / (name + '.html')).as_uri())
                    self.assertEqual(browser.title, 'Parsimony: which AI coding agent changes the least code?' if name == 'index' else 'Parsimony: ' + title)
                    self.assertTrue(browser.execute_script("return !!document.head.querySelector('title') && !!document.head.querySelector('style') && !document.body.querySelector('title, meta, style')"))
                    nav = browser.find_element(By.CSS_SELECTOR, 'nav[aria-label="Leaderboards"]')
                    self.assertTrue(nav.is_displayed())
                    self.assertEqual(len(nav.find_elements(By.TAG_NAME, 'a')), 6)
                    from selenium.webdriver.common.keys import Keys
                    button = browser.find_element(By.CSS_SELECTOR, '#board button[data-sort="net"]')
                    browser.execute_script('arguments[0].focus()', button)
                    button.send_keys(Keys.ENTER)
                    self.assertEqual(browser.switch_to.active_element,
                                     browser.find_element(By.CSS_SELECTOR, '#board button[data-sort="net"]'))
        with self.rendered_browser(javascript=False) as (browser, directory):
            for name in titles:
                with self.subTest(board=name, javascript=False):
                    browser.get((root / (name + '.html')).as_uri())
                    # WebDriver treats the noscript element itself as hidden, even
                    # with scripting disabled; test its actually rendered paragraph.
                    fallback = browser.find_element(By.CSS_SELECTOR, 'noscript p')
                    self.assertTrue(fallback.is_displayed())
                    self.assertIn('JavaScript is required', fallback.text)
                    link = fallback.find_element(By.TAG_NAME, 'a')
                    self.assertEqual(link.get_attribute('href'),
                                     'https://github.com/La5u/Parsimony/tree/main/examples')

    def test_local_import_security_validation_and_same_file_reload(self):
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait

        with self.rendered_browser() as (browser, directory):
            wait = WebDriverWait(browser, 5)
            official = browser.find_element(By.ID, 'board').text
            # Observe page-level network/storage calls during imports (not browser telemetry).
            browser.execute_script("""
                window.auditCalls = []; window.auditXss = false;
                for (const name of ['fetch']) window[name] = () => {
                    window.auditCalls.push(name); throw new Error('Unexpected network');
                };
                XMLHttpRequest.prototype.open = function () { window.auditCalls.push('xhr'); };
                navigator.sendBeacon = () => { window.auditCalls.push('beacon'); return false; };
                Storage.prototype.setItem = function () { window.auditCalls.push('storage'); };
            """)
            attack = '<img src="https://example.invalid/audit" onerror="window.auditXss=true">'
            data = dict(benchmark=attack, unit=attack, measurement='net', results=[
                dict(model=attack, task='one', amount=-2, solved=True),
                dict(model='__proto__', task='one', amount=0),
                dict(model='constructor', task='one', amount=None)])
            upload = directory / 'benchmark.json'

            def select(content, success):
                upload.write_text(content)
                browser.find_element(By.ID, 'custom-file').send_keys(str(upload))
                prefix = 'Loaded. Nothing was uploaded.' if success else 'Unable to load benchmark:'
                wait.until(lambda b: b.find_element(By.ID, 'custom-status').text.startswith(prefix))
                self.assertEqual(browser.find_element(By.ID, 'custom-file').get_attribute('value'), '')

            select(json.dumps(data), True)
            output = browser.find_element(By.ID, 'custom-results')
            self.assertIn(attack, output.text)
            self.assertIn('__proto__', output.text)
            self.assertIn('constructor', output.text)
            self.assertEqual(output.find_elements(By.CSS_SELECTOR, 'img, script, iframe, a'), [])
            self.assertFalse(browser.execute_script('return window.auditXss'))
            data['benchmark'] = 'Same file, edited'
            select(json.dumps(data), True)
            self.assertIn('Same file, edited', output.text)
            for invalid in ['{broken', json.dumps(dict(data, extra=True)),
                            json.dumps(dict(data, results=data['results'] * 2)),
                            json.dumps(dict(data, results=[dict(model='A', task='t', amount=1e309)])),
                            json.dumps(dict(data, results=[dict(model='A', task='t', amount=1, solved='true')])),
                            json.dumps(dict(data, results=[dict(model='A', task='t', amount=1)] * 10001)),
                            ' ' * (5 * 1024 * 1024 + 1)]:
                select(invalid, False)
                self.assertEqual(output.text, '')
            select(json.dumps(data), True)
            browser.find_element(By.ID, 'custom-clear').click()
            self.assertEqual(output.text, '')
            self.assertEqual(browser.find_element(By.ID, 'custom-status').text, '')
            self.assertEqual(browser.find_element(By.ID, 'board').text, official)
            self.assertEqual(browser.execute_script('return window.auditCalls'), [])

    def test_keyboard_task_reset_and_tooltip_bounds(self):
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.support.ui import Select, WebDriverWait

        with self.rendered_browser() as (browser, directory):
            self.narrow_viewport(browser, directory, browser.current_url, 390)
            Select(browser.find_element(By.ID, 'chart-type')).select_by_value('bar')
            search = browser.find_element(By.ID, 'task-search')
            search.send_keys('task')
            self.assertIn('Selected task: task', browser.find_element(By.ID, 'task-status').text)
            search.send_keys(Keys.CONTROL, 'a')
            search.send_keys('unknown-task')
            self.assertIn('Still showing task', browser.find_element(By.ID, 'task-status').text)
            search.send_keys(Keys.TAB)
            self.assertEqual(browser.switch_to.active_element.get_attribute('id'), 'task-reset')
            browser.switch_to.active_element.send_keys(Keys.ENTER)
            self.assertEqual(search.get_attribute('value'), '')
            row = browser.find_element(By.CSS_SELECTOR, '[data-bar]')
            browser.execute_async_script('''
                const row = arguments[0], done = arguments[1];
                row.scrollIntoView({block: 'center'});
                requestAnimationFrame(() => requestAnimationFrame(done));
            ''', row)
            browser.execute_script('arguments[0].focus({preventScroll: true})', row)
            tooltip = browser.find_element(By.ID, 'graph-tooltip')
            self.assertTrue(tooltip.is_displayed())
            self.assertTrue(browser.execute_script("""
                const r = arguments[0].getBoundingClientRect();
                return r.left >= 0 && r.top >= 0 && r.right <= innerWidth && r.bottom <= innerHeight;
            """, tooltip))
            browser.switch_to.default_content()
            browser.execute_script("document.querySelector('iframe').style.width = '320px'")
            browser.switch_to.frame(browser.find_element(By.TAG_NAME, 'iframe'))
            WebDriverWait(browser, 5).until(lambda b: not tooltip.is_displayed())
            self.assertTrue(browser.find_element(By.ID, 'axis-controls').is_displayed())
            self.assertFalse(browser.find_element(By.ID, 'graph-y-control').is_displayed())
            self.assertEqual(browser.find_element(By.ID, 'graph-x-label').text, 'Metric')
            self.assertEqual(browser.execute_script('return document.documentElement.lang'), 'en')
            self.assertEqual(browser.find_element(By.ID, 'custom-status').get_attribute('aria-live'), 'polite')

    def test_published_boards_at_mobile_widths(self):
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import Select, WebDriverWait

        with self.rendered_browser() as (browser, directory):
            for name in ['index', 'verified', 'live', 'javascript', 'typescript', 'go']:
                for width in [320, 390]:
                    with self.subTest(board=name, width=width):
                        url = (Path(__file__).resolve().parents[1] / 'site' / (name + '.html')).as_uri()
                        self.narrow_viewport(browser, directory, url, width)
                        WebDriverWait(browser, 5).until(lambda b: b.find_elements(By.CSS_SELECTOR, '#board tbody tr'))
                        self.assertTrue(browser.find_element(By.ID, 'custom-file').is_displayed())
                        self.assertEqual(browser.execute_script('return document.documentElement.lang'), 'en')
                        self.assertIn('width=device-width', browser.find_element(By.CSS_SELECTOR, 'meta[name="viewport"]').get_attribute('content'))
                        Select(browser.find_element(By.ID, 'chart-type')).select_by_value('bar')
                        self.assertTrue(browser.find_elements(By.CSS_SELECTOR, '[data-bar]'))
                        self.assertTrue(browser.execute_script("""
                            const r = document.getElementById('graph').getBoundingClientRect();
                            return r.left >= 0 && r.right <= innerWidth;
                        """))

    def test_rendered_visibility_missing_values_and_task_bar_tooltip(self):
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import Select

        records = [record('Alpha', 'task', net=1, churn=1),
                   record('Beta', 'task', net=-2, churn=2, resolved=False)]
        data = build(freeze(records, 'browser-smoke'), records, draws=10)
        next(m for m in data['models'] if m['agent'] == 'Alpha')['resolve_rate'] = None
        options = webdriver.FirefoxOptions()
        options.add_argument('-headless')
        with tempfile.TemporaryDirectory() as directory, webdriver.Firefox(options=options) as browser:
            page = Path(directory) / 'index.html'
            page.write_text(render(data))
            browser.get(page.as_uri())
            toggle = browser.find_element(By.ID, 'self-run-toggle-label')
            self.assertFalse(toggle.is_displayed())
            self.assertEqual(browser.execute_script('return arguments[0].getClientRects().length', toggle), 0)
            alpha = next(row for row in browser.find_elements(By.CSS_SELECTOR, '#board tbody tr')
                         if row.find_elements(By.TAG_NAME, 'td')[1].text == 'Alpha')
            self.assertEqual(alpha.find_elements(By.TAG_NAME, 'td')[4].text, '—')
            Select(browser.find_element(By.ID, 'chart-type')).select_by_value('bar')
            browser.execute_script("""
                const input = document.getElementById('task-search');
                input.value = 'task'; input.dispatchEvent(new Event('input'));
            """)
            failed = next(row for row in browser.find_elements(By.CSS_SELECTOR, '[data-bar]')
                          if 'Beta' in row.get_attribute('aria-label'))
            self.assertIn('failed task attempt', failed.get_attribute('aria-label'))
            browser.execute_async_script('''
                const row = arguments[0], done = arguments[1];
                row.scrollIntoView({block: 'center'});
                requestAnimationFrame(() => requestAnimationFrame(done));
            ''', failed)
            browser.execute_script('arguments[0].focus({preventScroll: true})', failed)
            tooltip = browser.find_element(By.ID, 'graph-tooltip')
            self.assertTrue(tooltip.is_displayed())
            self.assertIn('failed task attempt', tooltip.text)
            browser.execute_script("window.dispatchEvent(new Event('scroll'))")
            self.assertFalse(tooltip.is_displayed())
            data['self_run_models'] = [dict(agent='owner', name='Owner', company='Other', self_run=True,
                                          harness='pi', tasks=1, footprint_population_count=1,
                                          measured_attempts=1, measured_net_mean=0.4,
                                          measured_churn_mean=1, resolve_rate=None)]
            page.write_text(render(data))
            browser.refresh()
            Select(browser.find_element(By.ID, 'graph-x')).select_by_value('net')
            self.assertTrue(browser.find_element(By.ID, 'self-run-toggle-label').is_displayed())
            Select(browser.find_element(By.ID, 'chart-type')).select_by_value('bar')
            owner = next(row for row in browser.find_elements(By.CSS_SELECTOR, '[data-bar]')
                         if 'Owner' in row.get_attribute('aria-label'))
            self.assertIn('Net units added, all measured (mean): 0.4', owner.get_attribute('aria-label'))
            self.assertGreater(owner.rect['width'], 0)
            browser.execute_async_script('''
                const row = arguments[0], done = arguments[1];
                row.scrollIntoView({block: 'center'});
                requestAnimationFrame(() => requestAnimationFrame(done));
            ''', owner)
            browser.execute_script('arguments[0].focus({preventScroll: true})', owner)
            self.assertIn('Net units added, all measured (mean): 0.4',
                          browser.find_element(By.ID, 'graph-tooltip').text)
