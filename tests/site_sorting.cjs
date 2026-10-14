// Run against a rendered page; no browser or npm dependencies required.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const html = fs.readFileSync(process.argv[2], 'utf8');
const data = JSON.parse(html.match(/type="application\/json">([\s\S]*?)<\/script>/)[1]);
delete data.external; // Pages built with --external are checked separately below.
delete data.self_run_models; // Likewise for self-run points.
// Same-task fields are tested on their own fixture below; the base fixture is the plain-mean board.
const base = Object.fromEntries(Object.entries(data.models[0]).filter(([key]) => !key.startsWith('same_task') && !key.includes('complexity')));
data.models = [
  {...base, agent: 'alpha', footprint_population_count: 4, measured_churn_mean: 4, name: 'Alpha', score: 10, lower: 4, upper: 16, ci: [1, 90], resolve_rate: .8,
    company: 'Anthropic', latest: true, measured_net_mean: -2, measured_solved_net_mean: 7, measured_attempts: 4, measured_solved_attempts: 2, upstream_solved_attempts: 4, rank_range: [1, 2]},
  {...base, agent: 'beta', footprint_population_count: 4, measured_churn_mean: 6, name: 'Beta', score: null, lower: 10, upper: 30, ci: [2, 40], resolve_rate: .3,
    company: 'OpenAI', latest: false, measured_net_mean: 0, measured_solved_net_mean: 3, measured_attempts: 3, measured_solved_attempts: 1, upstream_solved_attempts: 4, rank_range: [2, 3]},
  {...base, agent: 'gamma', footprint_population_count: 4, measured_churn_mean: null, name: 'Gamma', score: 5, lower: 5, upper: 5, ci: [3, 20], resolve_rate: .5,
    company: 'Anthropic', measured_net_mean: null, measured_solved_net_mean: null, measured_attempts: 0, measured_solved_attempts: 0, upstream_solved_attempts: 4, rank_range: null},
];
data.sources = [
  {name: 'Current <source>', benchmark: 'Frozen', language: 'python', tasks: 100, attempts_per_task: 4, population_per_model: 400, active: true, board_url: 'current.html', report_url: 'https://example.org/report', manifest_url: 'https://example.org/manifest', manifest_sha256: '<hash>', dataset_sha256: 'dataset'},
  {name: '<img src=x onerror=alert(1)>', benchmark: 'Other', language: 'go', tasks: 50, attempts_per_task: 1, population_per_model: 50, active: false, board_url: 'other.html', report_url: 'javascript:alert(1)', manifest_url: 'https://example.org/other', manifest_sha256: 'manifest', dataset_sha256: 'dataset'},
];
data.task_count = 4;
data.tasks = [
  ['org__repo-1', 99, [['r', 111, 112, 10], ['r', 221, 222, 20], ['f', 331, 332, 5]]],
  ['org__repo-2', 55, [['f', -11, 12, null, -25, 0], ['r', 21, 22, 30], ['r', 31, 32, 40]]],
  ['org__repo-3', null, [['m', null, null, null], ['o', 0, 0, null, 1, 100], ['m', null, null, null]]],
  ['constant', null, [['r', 1200, 1200, 10], ['r', 1200, 1200, 10], ['r', 1200, 1200, 10]]],
  ['single', null, [['r', 1000, 1000, 10], ['m', null, null, null], ['m', null, null, null]]],
  ['negative', null, [['r', -1200, 1200, 10], ['r', -1600, 1600, 20], ['r', -2000, 2000, 30]]],
  ['zero', null, [['r', 0, 0, 0], ['r', 0, 0, 0], ['r', 0, 0, 0]]],
  ['uncalibrated', null, [['c', 11, 12, null, -25, 0, 'f'],
                          ['r', 21, 22, 30, 30, 30, 'r'], ['o', 0, 0, null, 1, 100, 'r']]],
];
data.footprint_tasks = data.tasks;
const elements = new Map();
function element(id) {
  if (id === '#graph') id = 'graph';
  if (!elements.has(id)) elements.set(id, {
    innerHTML: '', textContent: '', value: '', hidden: false, listeners: {}, attributes: {},
    style: {}, offsetWidth: 160, offsetHeight: 24,
    addEventListener(event, fn) { this.listeners[event] = fn; },
    setAttribute(name, value) { this.attributes[name] = value; },
  });
  return elements.get(id);
}
element('parsimony-data').textContent = JSON.stringify(data);
let lastButtons, lastHeader, lastCircles, lastGraph, lastBars, lastBarGraph, lastCompanies, lastCompanyGraph;
const doc = {
  getElementById: element,
  querySelector: element,
  querySelectorAll(selector) {
    if (selector === '#graph circle[data-point]') {
      const graph = element('graph').innerHTML;
      if (lastCircles && lastGraph === graph) return lastCircles;
      lastGraph = graph;
      lastCircles = [...graph.matchAll(/<circle data-point="(\d+)"/g)].map(match => ({
        dataset: {point: match[1]}, listeners: {}, addEventListener(event, fn) { this.listeners[event] = fn; },
        matches: selector => selector === 'circle',
        getBoundingClientRect() { return {left: 100, width: 12, height: 12, top: 188, right: 112, bottom: 200}; }
      }));
      return lastCircles;
    }
    if (selector === '#graph [data-company]') {
      const graph = element('graph').innerHTML;
      if (lastCompanies && lastCompanyGraph === graph) return lastCompanies;
      lastCompanyGraph = graph;
      lastCompanies = [...graph.matchAll(/data-point="(\d+)"[^>]*?data-company="([^"]*)"/g)].map(match => ({
        dataset: {point: match[1], company: match[2]}, dim: false,
        classList: {toggle(name, on) { if (name === 'dim') this.owner.dim = on; }},
      }));
      lastCompanies.forEach(el => { el.classList.owner = el; });
      return lastCompanies;
    }
    if (selector === '#graph [data-bar]') {
      const graph = element('graph').innerHTML;
      if (lastBars && lastBarGraph === graph) return lastBars;
      lastBarGraph = graph;
      lastBars = [...graph.matchAll(/data-bar="(\d+)"/g)].map(match => ({
        dataset: {bar: match[1]}, listeners: {}, addEventListener(event, fn) { this.listeners[event] = fn; },
        getBoundingClientRect() { return {left: 100, width: 12, bottom: 200}; }
      }));
      return lastBars;
    }
    if (selector !== '#board button[data-sort]') return [];
    const head = element('#board thead').innerHTML;
    if (lastButtons && lastHeader === head) return lastButtons;
    lastHeader = head;
    lastButtons = [...head.matchAll(/<th([^>]*)><button type="button" data-sort="([^"]+)"[^>]*>/g)].map(match => {
      const th = element('header-' + match[2]);
      th.attributes['aria-sort'] = match[1].match(/aria-sort="([^"]+)"/)?.[1];
      return {dataset: {sort: match[2]}, parentElement: th, listeners: {},
        focus() { doc.activeElement = this; },
        addEventListener(event, fn) { this.listeners[event] = fn; }};
    });
    return lastButtons;
  },
};
const browser = {innerWidth: 800, innerHeight: 600, listeners: {},
  addEventListener(event, fn) { this.listeners[event] = fn; }};
browser.location = new URL('https://example.org/index.html');
browser.history = {replaceState(state, title, next) { browser.location = new URL(next); }};
vm.runInNewContext(html.match(/<script>\n([\s\S]*?)<\/script>/)[1], {document: doc, window: browser, URL, URLSearchParams});
const script = html.match(/<script>\n([\s\S]*?)<\/script>/)[1];
assert(html.indexOf('id="graph"') < html.indexOf('id="task-search"'));
assert(html.indexOf('id="task-search"') < html.indexOf('id="board"'));
assert(html.indexOf('id="graph"') < html.indexOf('id="board"'));
assert(html.indexOf('id="board"') < html.indexOf('id="data-sources"'));
assert(html.indexOf('id="data-sources"') < html.indexOf('id="method"'));
assert.equal(element('data-sources').hidden, false);
assert.match(element('source-counts').innerHTML, /width:100%/);
assert.match(element('source-counts').innerHTML, /width:50%/);
assert.match(element('source-counts').innerHTML, /100 tasks × 4 attempts/);
assert.match(element('source-counts').innerHTML, /50 tasks × 1 attempt</);
assert.match(element('source-counts').innerHTML, /this board/);
assert.match(element('source-counts').innerHTML, /href="current.html">Current &lt;source&gt;<\/a>/);
assert.doesNotMatch(element('source-counts').innerHTML, /<img|rank|contribution/i);
assert.match(element('source-evidence').innerHTML, /href="https:\/\/example.org\/manifest">Manifest<\/a>/);
assert.doesNotMatch(element('source-evidence').innerHTML, /javascript:|<hash>/);
assert.equal(element('metric-source').textContent, `${data.benchmark?.name || 'SWE-bench Verified'}: ${data.benchmark?.results || "SWE-bench's published results"}`);
const savedSources = data.sources;
delete data.sources;
element('parsimony-data').textContent = JSON.stringify(data);
vm.runInNewContext(script, {document: doc, window: browser, URL, URLSearchParams});
assert.equal(element('data-sources').hidden, true);
assert.equal(element('source-counts').innerHTML, '');
data.sources = savedSources;
element('parsimony-data').textContent = JSON.stringify(data);
vm.runInNewContext(script, {document: doc, window: browser, URL, URLSearchParams});
assert.match(html, /#graph \.point-label \{ position: absolute; font: 400 8px/);
assert.match(html, /#graph circle \{ stroke: none/);
assert.match(html, /circle:focus-visible \{ outline: 2px solid #000; outline-offset: 4px/);
assert.match(html, /white-space: pre-line/);
for (const [company, color] of Object.entries({OpenAI: '#000000', xAI: '#8b5cf6', Google: '#34a853', Anthropic: '#d97757', DeepSeek: '#2756bd'})) assert(html.includes(`'${company}': '${color}'`));
assert.match(html, /#graph text \{ fill: #000;/);
assert.doesNotMatch(html, /best-label|class="leader"|Smaller footprint, more solved|Better on both axes|const candidates|const boxes/);
assert.match(html, /transform: translate\(10px,-50%\); line-height: 10px/);
assert.match(html, /<summary>How to read this<\/summary>/);
assert.match(html, /id="units-definition">It takes the patches that benchmarks already publish and counts <b>coding units<\/b>/);
assert.match(html, /cramming code isn't rewarded, and deleted code is subtracted: net units = added − removed\./);
assert(html.indexOf('id="units-definition"') < html.indexOf('<summary>How to read this</summary>'));
assert.doesNotMatch(html, /paint-order|box-shadow|text-shadow/);
const tooltipCSS = html.match(/#graph-tooltip \{([\s\S]*?)\}/)[1];
assert.match(tooltipCSS, /color: #000/);
assert.doesNotMatch(tooltipCSS, /(?:^|;)\s*(?:border(?:-[\w-]+)?|[\w-]*shadow)\s*:/);
assert.match(html, /color-scheme: light/);
assert.doesNotMatch(html, /prefers-color-scheme|color-scheme: dark/);
const rows = () => [...element('#board tbody').innerHTML.matchAll(/<tr>([\s\S]*?)<\/tr>/g)].map(m => m[1]);
const names = () => rows().map(row => row.match(/<td class="left">(.*?)<\/td>/)?.[1]);
const graph = () => {
  const markup = element('graph').innerHTML;
  assert.doesNotMatch(markup, /best-label|class="leader"|Smaller footprint, more solved|Better on both axes/);
  for (const label of markup.matchAll(/<span class="point-label(?: older-label)?" data-point="(\d+)" style="left:([^%]+)%;top:([^%]+)%">/g)) {
    const circle = markup.match(new RegExp(`<circle data-point="${label[1]}"[^>]*cx="([^"]+)" cy="([^"]+)"`));
    assert(circle, 'label must anchor to an actual dot');
    assert(Math.abs(Number(label[2]) - Number(circle[1]) / 720 * 100) < 1e-8);
    assert(Math.abs(Number(label[3]) - Number(circle[2]) / 440 * 100) < 1e-8);
  }
  return markup;
};
// The left margin fits the widest y tick label; read it from the y axis line.
const left = () => Number(graph().match(/<line class="axis" x1="([\d.]+)" y1="18"/)[1]);
function tickValues(axis) {
  const anchor = axis === 'x' ? 'middle' : 'end';
  const pattern = new RegExp(`<text class="tick" text-anchor="${anchor}"[^>]*>([−\\d.,]+%?)<\\/text>`, 'g');
  return [...graph().matchAll(pattern)].map(m => Number.parseFloat(m[1].replace('−', '-').replace(/,/g, '')));
}
// The fitted axis range (data-driven); tick labels sit at round values inside it.
const domain = axis => graph().match(new RegExp(`data-${axis}-domain="([^"]+)"`))[1].split(',').map(Number);
function domainNear(axis, low, high, tolerance = 0.06) {
  const [lo, hi] = graph().match(new RegExp(`data-${axis}-domain="([^"]+)"`))[1].split(',').map(Number);
  assert(Math.abs(lo - low) < tolerance && Math.abs(hi - high) < tolerance, `${axis} domain ${lo},${hi} != ${low},${high}`);
  for (const v of tickValues(axis)) assert(v >= lo - 1e-9 && v <= hi + 1e-9, `${axis} tick ${v} outside ${lo},${hi}`);
}
// Circles are drawn older-generation first; report colors in model (point index) order.
const colors = () => [...graph().matchAll(/<circle data-point="(\d+)"[^>]*fill="([^"]+)"/g)]
  .sort((a, b) => a[1] - b[1]).map(m => m[2]);
function click(key, expected, direction) {
  const button = doc.querySelectorAll('#board button[data-sort]').find(b => b.dataset.sort === key);
  assert(button, `missing sort button ${key}`);
  button.focus();
  button.listeners.click();
  assert.equal(doc.activeElement, doc.querySelectorAll('#board button[data-sort]').find(b => b.dataset.sort === key));
  assert.deepEqual(names(), expected);
  assert.equal(button.parentElement.attributes['aria-sort'], direction);
  for (const other of doc.querySelectorAll('#board button[data-sort]').filter(b => b.dataset.sort !== key)) {
    assert.equal(other.parentElement.attributes['aria-sort'], 'none');
  }
}
function axis(which, key) {
  element('graph-' + which).listeners.change({target: {value: key}});
}
function task(id) {
  element('task-search').listeners.input({target: {value: id}});
}
assert.deepEqual(names(), ['Beta', 'Alpha', 'Gamma']);
assert.equal(element('header-solved_net').attributes['aria-sort'], 'ascending');
assert.deepEqual([...element('#board thead').innerHTML.matchAll(/<th[^>]*>(?:<button[^>]*>)?([^<]+)/g)].map(m => m[1]),
  ['#', 'Model', 'Net units, solved (mean)', 'Net units, all measured (mean)', 'Solved', 'Measured']);
assert.match(rows()[0], /<td>1<\/td><td class="left">Beta<\/td><td>3.0<\/td><td>0.0<\/td><td>30.0%<\/td><td>1\/4<\/td>/);
assert.match(rows()[2], /<td>—<\/td><td class="left">Gamma<\/td><td>—<\/td><td>—<\/td><td>50.0%<\/td><td>0\/4<\/td>/);
assert.doesNotMatch(element('#board thead').innerHTML, /Per solve|churn|95% CI|data-sort="ci"/i);
assert(rows().every(row => [...row.matchAll(/<td\b/g)].length === 6));
assert.doesNotMatch(element('#board thead').innerHTML, /Score|churn|95% CI/i);
assert.match(element('#board tbody').innerHTML, /2\/4/);
assert.match(element('#board tbody').innerHTML, /1\/4/);
assert.match(element('#board tbody').innerHTML, /0\/4/);
assert.match(element('#board tbody').innerHTML, /−2.0/);
click('coverage', ['Alpha', 'Beta', 'Gamma'], 'descending');
click('coverage', ['Gamma', 'Beta', 'Alpha'], 'ascending');
click('resolve_rate', ['Alpha', 'Gamma', 'Beta'], 'descending');
click('resolve_rate', ['Beta', 'Gamma', 'Alpha'], 'ascending');
click('net', ['Alpha', 'Beta', 'Gamma'], 'ascending');
click('net', ['Beta', 'Alpha', 'Gamma'], 'descending');
assert.equal(element('graph-x').value, 'solved_net');
assert.equal(element('graph-y').value, 'resolve_rate');
domainNear('x', 2.8, 7.2);
assert.match(graph(), /Alpha \(Anthropic\).*Net units added, solved \(mean\): 7.0/);
axis('x', 'net');
domainNear('x', -2.1, .1);
assert.deepEqual(tickValues('x'), [-2, -1.5, -1, -.5, 0]); // round values, not -2.1 / -1.55 / …
assert.deepEqual(tickValues('y'), [0, 20, 40, 60, 80, 100]);
assert.match(graph(), /Alpha \(Anthropic\).*Net units added, all measured \(mean\): −2.0, Solved \(%\): 80.0%/);
// Both footprint columns and axes keep their fixed meanings; sorting all measured does not change rank.
assert.match(element('graph-x').innerHTML, /value="solved_net">Net units added, solved \(mean\)/);
assert.doesNotMatch(element('graph-x').innerHTML + element('#board thead').innerHTML, /trimmed/i);
click('solved_net', ['Beta', 'Alpha', 'Gamma'], 'ascending');
assert.match(element('#board tbody').innerHTML, /<td>2<\/td><td class="left">Alpha<\/td><td>7.0<\/td><td>−2.0<\/td>/);
click('solved_net', ['Alpha', 'Beta', 'Gamma'], 'descending');
click('net', ['Alpha', 'Beta', 'Gamma'], 'ascending');
assert.match(rows()[0], /<td>2<\/td><td class="left">Alpha<\/td><td>7.0<\/td><td>−2.0<\/td>/);
assert.match(rows()[1], /<td>1<\/td><td class="left">Beta/);
assert.doesNotMatch(graph(), /Gamma \(Anthropic\)/);
// Every generation is labelled; earlier generations remain legible but lighter.
assert.match(graph(), /<span class="point-label"[^>]*>Alpha<\/span>/);
assert.match(graph(), /<span class="point-label older-label"[^>]*>Beta<\/span>/);
assert.match(html, /fill-opacity: 0\.70/);
assert.match(html, /older-label \{ opacity: 0\.75/);
assert.match(graph(), /<circle data-point="1" data-model="Beta" class="all-point older"/);
assert.match(graph(), /<circle data-point="0" data-model="Alpha" class="all-point"/);
// Lower net units and higher solved are better: the green zone sits in the top-left corner.
assert.match(graph(), new RegExp(`<rect class="best-zone" x="${left()}" y="18"`));
assert.equal(element('graph-legend').textContent, 'Older generations faded.');
element('graph-y').listeners.change({target: {value: 'coverage'}});
assert.doesNotMatch(graph(), /best-zone/); // Coverage has no better direction.
assert.doesNotMatch(graph(), /<polyline/);

element('graph-y').listeners.change({target: {value: 'resolve_rate'}});
assert.match(graph(), /best-zone/);
assert.match(graph(), /aria-describedby="plot-desc"/);
assert.doesNotMatch(graph(), /<title\b/); // Native SVG titles would create a second, delayed tooltip.
assert.match(graph(), /tabindex="0"/);
assert.match(element('company-legend').innerHTML, /Anthropic/);
assert.match(element('company-legend').innerHTML, /OpenAI/);
const initialColors = colors();
assert.notEqual(initialColors[0], initialColors[1]);
const tooltip = element('graph-tooltip');
assert.equal(tooltip.hidden, true);
// Draw order puts earlier generations first, so select Alpha's circle by its point index.
const firstCircle = doc.querySelectorAll('#graph circle[data-point]').find(c => c.dataset.point === '0');
for (const event of ['mouseenter', 'mousemove', 'focus', 'click']) {
  firstCircle.listeners[event]();
  assert.equal(tooltip.textContent, 'Alpha\nNet units added, all measured (mean): −2.0\nSolved (%): 80.0%');
  assert.equal(tooltip.hidden, false);
  firstCircle.listeners.mouseleave();
  assert.equal(tooltip.hidden, true);
}
firstCircle.listeners.mouseenter({clientX: 799, clientY: 599});
// Beside the point (right side when nothing is there), not at the cursor and never over the point itself.
assert.equal(tooltip.style.left, '124px');
assert.equal(tooltip.style.top, '182px');
// Hover fades other companies' points and labels; leaving restores them.
{
  const dimmed = () => doc.querySelectorAll('#graph [data-company]').filter(el => el.dim).map(el => el.dataset.company);
  firstCircle.listeners.mouseenter({clientX: 1, clientY: 1});
  const company = doc.querySelectorAll('#graph [data-company]').find(el => el.dataset.point === '0').dataset.company;
  assert.ok(dimmed().length > 0 && dimmed().every(c => c !== company));
  firstCircle.listeners.mouseleave();
  assert.deepEqual(dimmed(), []);
}
firstCircle.listeners.blur();
assert.equal(tooltip.hidden, true);
for (const event of ['scroll', 'resize']) {
  firstCircle.listeners.focus();
  browser.listeners[event]();
  assert.equal(tooltip.hidden, true);
}
// Numeric metrics remain selectable; archived combined-score axes are gone.
const fixedOptions = [
  ['solved_net', 'Net units added, solved (mean)'],
  ['net', 'Net units added, all measured (mean)'],
  ['churn', 'Units changed, all measured (mean)'],
  ['resolve_rate', 'Solved (%)'],
  ['coverage', 'Measured (%)'],
];
for (const which of ['x', 'y']) assert.deepEqual(
  [...element('graph-' + which).innerHTML.matchAll(/<option value="([^"]+)">([^<]+)<\/option>/g)].map(m => [m[1], m[2]]), fixedOptions);
const keys = fixedOptions.map(([key]) => key);
for (const gone of ['score', 'ci', 'ci_high', 'rank_low', 'rank_high']) assert(!element('graph-x').innerHTML.includes(`value="${gone}"`));
for (const key of keys) assert(element('graph-x').innerHTML.includes(`value="${key}"`));
assert.doesNotMatch(element('graph-x').innerHTML, /solved_mean/i);
for (const x of keys) for (const y of keys.filter(k => k !== x)) {
  axis('x', x); axis('y', y);
  assert.equal(element('graph-x').value, x);
  assert.equal(element('graph-y').value, y);
  assert.doesNotMatch(graph(), /NaN|Infinity/);
  const circle = doc.querySelectorAll('#graph circle[data-point]').find(c => c.dataset.point === '0');
  circle.listeners.focus();
  assert(tooltip.textContent.includes(element('graph-x').innerHTML.match(new RegExp(`value="${x}">([^<]+)`))[1] + ':'));
  assert(tooltip.textContent.includes(element('graph-y').innerHTML.match(new RegExp(`value="${y}">([^<]+)`))[1] + ':'));
  if (['resolve_rate', 'coverage'].includes(x)) assert.deepEqual(tickValues('x'), [0, 20, 40, 60, 80, 100]);
  if (['resolve_rate', 'coverage'].includes(y)) assert.deepEqual(tickValues('y'), [0, 20, 40, 60, 80, 100]);
}
axis('x', 'net'); axis('y', 'resolve_rate');
axis('x', 'resolve_rate'); // Selecting the other axis's metric swaps, rather than duplicating, it.
assert.equal(element('graph-y').value, 'net');
assert.doesNotMatch(graph(), /<polyline/);
axis('y', 'resolve_rate');
task('org__repo-1');
assert.equal(element('graph-x').value, 'net');
assert.equal(element('graph-y').value, 'churn');
domainNear('x', 100, 342); // 111..331 with 5% padding, not anchored at zero.
assert.deepEqual(tickValues('x'), [100, 150, 200, 250, 300]);
assert.doesNotMatch(element('graph-x').innerHTML, /score|resolve_rate|rank_low/);
assert.deepEqual(names(), ['Alpha', 'Beta', 'Gamma']);
assert.equal(element('header-net').attributes['aria-sort'], 'ascending');
assert.match(element('#board tbody').innerHTML, /<td class="left">Alpha<\/td><td class="left r">solved<\/td><td>\+111<\/td><\/tr>/);
assert.match(graph(), /Gamma \(Anthropic\): failed task attempt/);
assert.equal(element('graph-legend').textContent, 'Older generations faded. Status on hover.');
assert.doesNotMatch(graph(), /<polyline/); // Alpha dominates both task-footprint axes.
assert.deepEqual(colors(), [initialColors[0], initialColors[1], initialColors[0]]);
click('net', ['Gamma', 'Beta', 'Alpha'], 'descending');
click('net', ['Alpha', 'Beta', 'Gamma'], 'ascending');
axis('x', 'churn');
assert.equal(element('graph-y').value, 'net');
axis('x', 'net'); axis('y', 'churn');
task('org__repo-2');
assert.doesNotMatch(element('#board tbody').innerHTML, /−25.0–0.0/);
task('not-a-task');
assert.match(element('task-status').textContent, /Still showing org__repo-2/);
task('org__repo-3');
assert.match(element('graph-legend').textContent, /No data for this view/);
assert.doesNotMatch(graph(), /<circle|NaN|Infinity/);
assert.deepEqual(tickValues('x'), [0, .2, .4, .6, .8, 1]);
assert.deepEqual(tickValues('y'), [0, .2, .4, .6, .8, 1]);
axis('x', 'net');
task('uncalibrated');
assert.match(element('#board tbody').innerHTML, /class="left f">failed/);
assert.match(element('#board tbody').innerHTML, /solved · not measured/);
assert.match(graph(), /Alpha \(Anthropic\): failed task attempt/);
assert.equal(colors().length, 2); // Known failed footprint remains visible; excluded footprint does not.
for (const [id, low, high] of [['constant', 1140, 1260], ['single', 950, 1050],
                              ['negative', -2040, -1160], ['zero', -1, 1]]) {
  task(id);
  domainNear('x', low, high);
  assert(tickValues('x').length >= 3);
  assert.doesNotMatch(graph(), /NaN|Infinity/);
}
element('task-reset').listeners.click();
assert.equal(element('graph-x').value, 'net'); // All-task axis choices survive task browsing.
assert.equal(element('graph-y').value, 'resolve_rate');
assert.equal(element('task-footer').hidden, true);
assert.equal(element('ci-help').hidden, false);
assert.deepEqual(names(), ['Beta', 'Alpha', 'Gamma']);
assert.doesNotMatch(element('#board thead').innerHTML, /Score|churn|Per solve|95% CI|data-sort="ci"/i);
assert(rows().every(row => [...row.matchAll(/<td\b/g)].length === 6));
const tied = structuredClone(data);
tied.models[1].measured_solved_net_mean = 7;
tied.models[1].resolve_rate = 1; // Correctness must not break a footprint tie.
element('parsimony-data').textContent = JSON.stringify(tied);
vm.runInNewContext(html.match(/<script>\n([\s\S]*?)<\/script>/)[1], {document: doc, window: browser, URL, URLSearchParams});
assert.deepEqual(names(), ['Alpha', 'Beta', 'Gamma']);
assert.match(element('#board tbody').innerHTML, /<td>1<\/td><td class="left">Alpha/);
assert.match(element('#board tbody').innerHTML, /<td>1<\/td><td class="left">Beta/);
assert.match(element('#board tbody').innerHTML, /<td>—<\/td><td class="left">Gamma/);
assert.doesNotMatch(graph(), /<polyline/); // Earlier Beta dominates latest Alpha at equal x.
axis('x', 'resolve_rate'); axis('y', 'solved_net');
assert.doesNotMatch(graph(), /<polyline/); // Earlier Beta also dominates in a swapped mixed-direction view.
assert.match(graph(), /<circle data-point="1" data-model="Beta" class="all-point older/);
function load(fixture, url = 'https://example.org/index.html') {
  element('parsimony-data').textContent = JSON.stringify(fixture);
  if (url) {
    browser.location = new URL(url);
    browser.history = {replaceState(state, title, next) { browser.location = new URL(next); }};
  } else {
    delete browser.location;
    delete browser.history;
  }
  vm.runInNewContext(script, {document: doc, window: browser, URL, URLSearchParams});
}
const cropped = structuredClone(data);
cropped.models[0].resolve_rate = .2;
cropped.models[1].resolve_rate = .6;
cropped.models[2] = {...cropped.models[0], name: 'Gemini 3.1 Pro (high)', company: 'Google', latest: false, measured_net_mean: -500, resolve_rate: .08};
function coordinates() {
  const circle = graph().match(/<circle[^>]*data-model="Gemini 3\.1 Pro \(high\)"[^>]*>/)[0];
  return ['cx', 'cy'].map(attr => Number(circle.match(new RegExp(`${attr}="([^"]+)"`))[1]));
}
function near(a, b) { assert(Math.abs(a - b) < 1e-8); }
load(cropped);
axis('x', 'net');
domainNear('x', -2.1, .1);
assert.match(element('graph-legend').textContent, /Gemini 3.1 Pro is off the scale/);
domainNear('y', 18, 62);
assert.deepEqual(tickValues('y'), [20, 30, 40, 50, 60]);
near(coordinates()[0], left() + (-500 + 2.1) / 2.2 * (690 - left()));
near(coordinates()[1], 388 - (8 - 18) / 44 * 370);
assert(coordinates()[0] < left() && coordinates()[1] > 388);
assert(Number.parseFloat(element('graph').style.marginBottom) > coordinates()[1] - 440);
assert.match(html, /height: auto; overflow: visible/);
assert.doesNotMatch(graph(), /marker|third quadrant/i);
assert.match(graph(), /<span class="point-label older-label"[^>]*>Gemini 3.1 Pro \(high\) \(off-scale\)<\/span>/); // labels keep the effort
const outlier = doc.querySelectorAll('#graph circle[data-point]').find(c => c.dataset.point === '2');
outlier.listeners.focus();
assert.match(tooltip.textContent, /off the chart's scale.*\nNet units added, all measured \(mean\): −500.0\nSolved \(%\): 8.0%/);
assert.doesNotMatch(tooltip.textContent, /marker/i);
assert.match(element('#board tbody').innerHTML, /−500.0/);
axis('x', 'resolve_rate');
near(coordinates()[0], left() + (8 - 18) / 44 * (690 - left()));
near(coordinates()[1], 388 - (-500 + 2.1) / 2.2 * 370);
axis('x', 'net');
axis('x', 'coverage');
assert.deepEqual(tickValues('x'), [0, 20, 40, 60, 80, 100]);
task('org__repo-1');
domainNear('x', 100, 342);
assert.doesNotMatch(element('graph-legend').textContent, /off the scale/);
const preview = structuredClone(cropped);
preview.models[2].name = 'Gemini 3.1 Pro Preview (high)';
load(preview);
axis('x', 'net');
domainNear('x', -2.1, .1);
domainNear('y', 18, 62);
assert.deepEqual(tickValues('y'), [20, 30, 40, 50, 60]);
assert.match(element('graph-legend').textContent, /Gemini 3.1 Pro is off the scale/);
for (const name of ['Gemini 3.1 Professional', 'Gemini 3.1 Pro Plus']) {
  const similar = structuredClone(cropped);
  similar.models[2].name = name;
  load(similar);
  axis('x', 'net');
  assert(domain('x')[0] < -500); // the outlier is inside the fitted range
  assert.deepEqual(tickValues('y'), [0, 20, 40, 60, 80, 100]);
  assert.doesNotMatch(element('graph-legend').textContent, /off the scale/);
}
const singleton = structuredClone(cropped);
singleton.models[1].measured_net_mean = null;
load(singleton);
axis('x', 'net');
assert(domain('x')[0] < -500); // the outlier is inside the fitted range
assert.deepEqual(tickValues('y'), [0, 20, 40, 60, 80, 100]);
assert.doesNotMatch(element('graph-legend').textContent, /off the scale/);
const inside = structuredClone(cropped);
inside.models[2].measured_net_mean = -1;
inside.models[2].resolve_rate = .4;
load(inside);
axis('x', 'net');
assert.doesNotMatch(graph(), /\(off-scale\)/);
assert.deepEqual(tickValues('y'), [0, 20, 40, 60, 80, 100]);
assert.equal(element('graph').style.marginBottom, '0px');
assert.doesNotMatch(element('graph-legend').textContent, /off the scale/);
const right = structuredClone(cropped);
right.models[2].measured_net_mean = 10000;
load(right);
axis('x', 'net');
assert(coordinates()[0] > 690);
axis('y', 'net'); // Swap direction: the same numeric outlier now appears above the plot.
assert(coordinates()[1] < 18);
// A pinned external index becomes the default Y axis, adds one column and stays missing when unmatched.
const withExternal = structuredClone(data);
withExternal.external = {source: 'Artificial Analysis', attribution: 'https://artificialanalysis.ai/', fetched_at: '2026-10-08T00:00:00Z', response_sha256: 'x'};
Object.assign(withExternal.models[0], {aa_coding: 70, aa_intelligence: 40, aa_match: 'exact'});
Object.assign(withExternal.models[1], {aa_coding: 60, aa_intelligence: 30, aa_match: 'effort_unlabelled'});
Object.assign(withExternal.models[2], {aa_coding: null, aa_intelligence: null, aa_match: null});
load(withExternal);
assert.equal(element('graph-y').value, 'aa_intelligence');
assert.match(element('graph-y').innerHTML, /Artificial Analysis Coding Index/);
assert.match(element('graph-y').innerHTML, /value="resolve_rate"/);
assert(rows().every(row => [...row.matchAll(/<td\b/g)].length === 7));
assert.match(element('#board thead').innerHTML, /AA Intel\./);
assert.match(element('external-note').innerHTML, /href="https:\/\/artificialanalysis.ai\/"/);
assert.equal(element('external-help').hidden, false);
assert.match(graph(), /Beta \(OpenAI\).*Artificial Analysis entry has no effort label/);
assert.doesNotMatch(graph(), /Alpha \(Anthropic\)[^"]*no effort label/);
axis('y', 'resolve_rate');
assert.doesNotMatch(graph(), /no effort label/);
assert.doesNotMatch(element('graph-legend').textContent, /Artificial Analysis/);
axis('y', 'aa_intelligence');
const noGamma = structuredClone(withExternal);
noGamma.models[2].measured_solved_net_mean = 1;
load(noGamma);
assert.match(element('graph-legend').textContent, /1 model has no AA score\./);
// Self-run configurations are faded, explained on hover, listed unranked and absent from task views.
const withSelfRun = structuredClone(data);
withSelfRun.self_run_models = [{agent: 'self-run-v1_x', name: 'Delta (high)', company: 'OpenAI', self_run: true, latest: true,
  harness: 'pi', tasks: 2, attempts: 4, footprint_population_count: 20, measured_attempts: 4, measured_net_mean: -5,
  measured_churn_mean: 9, measured_solved_net_mean: null, resolve_rate: null}];
withSelfRun.sources = [...data.sources, {name: 'Self-run pilot', benchmark: 'self-run', language: 'python', tasks: 10,
  attempts_per_task: 2, population_per_model: '6–20', active: false, self_run: true, board_url: 'index.html',
  report_url: 'https://example.org/self-run', manifest_url: 'https://example.org/plan', manifest_sha256: 'plan', deepswe_commit: 'abc'}];
load(withSelfRun);
assert.match(element('source-counts').innerHTML, /Self-run pilot<\/a> — run by me, not ranked/);
assert.match(element('source-counts').innerHTML, /up to 10 tasks × 2 attempts/);
assert.match(element('source-evidence').innerHTML, /Plan SHA-256: plan<br>DeepSWE commit: abc/);
assert.doesNotMatch(graph(), /Delta/); // Not graded: no point on the Solved axis.
axis('x', 'net'); axis('y', 'churn');
assert.match(graph(), /<circle[^>]*data-model="Delta \(high\)"[^>]*class="all-point self-run"/);
assert.match(graph(), /class="point-label self-run-label"[^>]*>Delta/);
assert.match(graph(), /Delta \(high\) \(OpenAI\)[^"]*Run by me with pi on 2 of \d+ tasks, not graded/);
assert.match(element('#board tbody').innerHTML, /<tr class="self-run"[^>]*><td>—<\/td><td class="left">Delta \(high\)<\/td><td>—<\/td><td>−5.0<\/td><td>—<\/td><td>—<\/td>/);
assert.match(element('#board tbody').innerHTML, /<td>2<\/td><td class="left">Alpha/); // Self-run never takes a rank.
assert.match(element('#board tbody').innerHTML, /Beta[\s\S]*<tr class="self-run-head"><td colspan="6">My runs · not ranked, 5–10 tasks<\/td><\/tr><tr class="self-run"[^>]*><td>—<\/td><td class="left">Delta/); // after ranked rows, even with the smallest mean
assert.match(element('self-run-note').textContent, /^Faded: models I ran myself on 3–10 of these tasks\. Not ranked\./);
assert.equal(element('self-run-help').hidden, false);
assert.equal(element('self-run-note').hidden, false);
task('org__repo-1');
assert.doesNotMatch(graph(), /Delta/);
assert.doesNotMatch(element('#board tbody').innerHTML, /Delta/);
// Self-graded self-runs appear on the default axes and use the same fixed table columns.
const gradedSelfRun = structuredClone(withSelfRun);
Object.assign(gradedSelfRun.self_run_models[0], {graded: true, upstream_solved_attempts: 2, measured_solved_attempts: 2,
  measured_solved_net_mean: 12, measured_solved_churn_mean: 14, resolve_rate: 0.5});
load(gradedSelfRun);
assert.match(graph(), /<circle[^>]*data-model="Delta \(high\)"[^>]*class="all-point self-run"/);
assert.match(graph(), /Run by me with pi on 2 of \d+ tasks, 2 solved/);
assert.match(element('#board tbody').innerHTML, /<tr class="self-run"[^>]*><td>—<\/td><td class="left">Delta \(high\)<\/td><td>12.0<\/td><td>−5.0<\/td><td>50.0%<\/td><td>2\/2<\/td>/);
assert.equal(element('self-run-note').hidden, false);
// Bars use the X metric, ascending for footprints; self-run stays in a separate group.
load(withSelfRun);
assert.equal(element('chart-type').value, 'scatter');
axis('x', 'net');
element('chart-type').listeners.change({target: {value: 'bar'}});
assert.equal(element('axis-controls').hidden, false);
assert.equal(element('graph-y-control').hidden, true);
assert.equal(element('graph-x-label').textContent, 'Metric');
const barNames = () => [...element('graph').innerHTML.matchAll(/<span class="bar-name">([^<]*)<\/span>/g)].map(m => m[1]);
assert.deepEqual(barNames(), ['Alpha', 'Beta', 'Delta (high)']); // Gamma has no measurement; self-run listed after, never interleaved
assert.match(element('graph').innerHTML, /data-bar="1"[\s\S]*?<div class="bar-group" role="presentation">My runs: 5–10 tasks only, so not comparable with the bars above<\/div><div class="bar-row self-run"[^>]*data-bar="2"/);
assert.match(element('graph').innerHTML, /class="bar-row self-run"[^>]*>[\s\S]*?background:#000000/);
assert.match(element('graph').innerHTML, /class="bar-row older"[^>]*aria-label="Beta \(OpenAI\); Net units added, all measured \(mean\): 0; Measured 1\/4 solved attempts"/);
assert.match(element('graph').innerHTML, /<span class="bar-zero" style="left:100%"><\/span>/);
assert.match(element('graph').innerHTML, /<span class="bar-value">−5<\/span>/);
assert.equal(element('graph-legend').textContent, 'Net units added, all measured (mean). Older generations faded.');
doc.querySelectorAll('#graph [data-bar]')[2].listeners.focus({});
assert.match(element('graph-tooltip').textContent, /^Delta \(high\) · self-run \(OpenAI\)\nNet units added, all measured \(mean\): −5\nMeasured 0\/0 solved attempts\nRun by me with pi/);
task('org__repo-1');
assert.deepEqual(barNames(), ['Alpha', 'Beta', 'Gamma']); // a measured failed attempt still has a bar
assert.match(element('graph').innerHTML, /<span class="bar-value">331<\/span>/);
assert.match(element('graph-legend').textContent, /^Net units added in this attempt/);
assert.doesNotMatch(element('graph').innerHTML, /Delta/);
task('');
element('chart-type').listeners.change({target: {value: 'scatter'}});
assert.equal(element('axis-controls').hidden, false);
assert.equal(element('graph-y-control').hidden, false);
assert.equal(element('graph-x-label').textContent, 'X axis');
assert.match(graph(), /<circle/);
// Self-run toggle: hides self-run models from scatter, bars and table, and refits the axes; ?selfrun=0 starts hidden.
load(withSelfRun);
assert.equal(element('self-run-toggle-label').hidden, false);
axis('x', 'net'); axis('y', 'churn');
assert.match(graph(), /data-model="Delta \(high\)"/);
element('self-run-toggle').listeners.change({target: {checked: false}});
assert.doesNotMatch(graph(), /Delta/);
assert.doesNotMatch(element('#board tbody').innerHTML, /Delta|self-run-head/);
assert.equal(element('self-run-note').hidden, true);
element('chart-type').listeners.change({target: {value: 'bar'}});
assert.doesNotMatch(element('graph').innerHTML, /Delta|bar-group/);
element('chart-type').listeners.change({target: {value: 'scatter'}});
element('self-run-toggle').listeners.change({target: {checked: true}});
assert.match(graph(), /data-model="Delta \(high\)"/);
assert.equal(element('self-run-note').hidden, false);
load(data); // no self-run models: no toggle
assert.equal(element('self-run-toggle-label').hidden, true);
// CSS must not override the hidden attribute on boards without a self-run pilot.
assert.match(html, /#self-run-toggle-label:not\(\[hidden\]\)\s*\{\s*display: inline-flex/);
const missingSolved = structuredClone(data);
missingSolved.models[0].resolve_rate = null;
missingSolved.models[1].resolve_rate = 0;
load(missingSolved);
assert.match(element('#board tbody').innerHTML, /Alpha<\/td><td>7.0<\/td><td>−2.0<\/td><td>—<\/td>/);
assert.match(element('#board tbody').innerHTML, /Beta<\/td><td>3.0<\/td><td>0.0<\/td><td>0.0%<\/td>/);
click('resolve_rate', ['Gamma', 'Beta', 'Alpha'], 'descending');
click('resolve_rate', ['Beta', 'Gamma', 'Alpha'], 'ascending');
assert.doesNotMatch(graph(), /data-model="Alpha"/);
const fractional = structuredClone(data);
fractional.models[0].measured_net_mean = -0.4;
fractional.models[1].measured_net_mean = 0.4;
fractional.models[2].measured_net_mean = 1.6;
load(fractional);
axis('x', 'net');
element('chart-type').listeners.change({target: {value: 'bar'}});
for (const value of ['−0.4', '0.4', '1.6']) assert.ok(graph().includes(`Net units added, all measured (mean): ${value};`));
doc.querySelectorAll('#graph [data-bar]')[0].listeners.focus({});
assert.match(element('graph-tooltip').textContent, /Net units added, all measured \(mean\): −0.4\n/);
task('org__repo-1');
assert.match(graph(), /Gamma[^"\n]*; failed task attempt/);
doc.querySelectorAll('#graph [data-bar]')[2].listeners.focus({});
assert.match(element('graph-tooltip').textContent, /\nfailed task attempt$/);
assert.match(graph(), /Alpha[^"\n]*; solved task attempt/);
task('uncalibrated');
assert.match(graph(), /Alpha[^"\n]*; failed task attempt/);
// An eligible footprint may have an explicitly unknown outcome.
fractional.footprint_tasks[0][2][2] = ['c', 331, 332, null, -25, 100, 'u', true];
load(fractional);
axis('x', 'net');
element('chart-type').listeners.change({target: {value: 'bar'}});
task('org__repo-1');
assert.match(graph(), /Gamma[^"\n]*; unknown task attempt/);
// Fixed solved ranks and attempt denominators; chart membership depends only on selected values.
const outcomes = structuredClone(withSelfRun);
outcomes.task_count = 2; // Coverage must never fall back to the number of tasks or planned attempts.
outcomes.population_count = 8;
Object.assign(outcomes.models[0], {measured_solved_net_mean: 7, measured_solved_churn_mean: 11,
  measured_solved_attempts: 2, upstream_solved_attempts: 6, footprint_population_count: 8});
Object.assign(outcomes.models[1], {measured_solved_net_mean: 7, measured_solved_churn_mean: 13,
  measured_solved_attempts: 1, upstream_solved_attempts: 4, footprint_population_count: 8});
Object.assign(outcomes.models[2], {measured_net_mean: -100, measured_attempts: 3,
  measured_solved_net_mean: null, measured_solved_churn_mean: null,
  measured_solved_attempts: 0, upstream_solved_attempts: 0});
// Unknown and failed footprints remain eligible in task view.
outcomes.footprint_tasks[0][2][1] = ['c', 221, 222, 20, 20, 20, 'u', true];
outcomes.footprint_tasks[0][2][2] = ['f', 331, 332, 5, 5, 5, 'f', true];
load(outcomes, 'https://example.org/index.html?keep=1#board');
assert.deepEqual(names(), ['Alpha', 'Beta', 'Gamma']);
assert.match(element('#board tbody').innerHTML, /<td>1<\/td><td class="left">Alpha<\/td><td>7.0<\/td><td>−2.0<\/td>/);
assert.match(element('#board tbody').innerHTML, /<td>1<\/td><td class="left">Beta/);
assert.match(element('#board tbody').innerHTML, /<td>—<\/td><td class="left">Gamma/);
assert.match(element('#board tbody').innerHTML, /2\/6<\/td>/);
assert.match(element('#board tbody').innerHTML, /1\/4<\/td>/);
assert.match(element('#board tbody').innerHTML, /0\/0<\/td>/);
assert.match(element('#board tbody').innerHTML, /Delta/); // Ungraded rows are still shown.
assert.doesNotMatch(graph(), /data-model="Gamma"|Delta/); // Missing selected solved means.
assert.match(graph(), /measured 2\/6 solved attempts/);
axis('y', 'churn');
assert.match(graph(), /Units changed, all measured \(mean\): 4.0/);
axis('x', 'coverage');
assert.match(graph(), /Measured \(%\): 33.3%/);
axis('x', 'net'); axis('y', 'resolve_rate');
assert.match(graph(), /data-model="Gamma"/); // No measured successes, but both selected values exist.
assert.doesNotMatch(graph(), /Delta/); // Missing Solved value.
axis('y', 'churn');
assert.match(graph(), /Delta/);
assert.doesNotMatch(graph(), /data-model="Gamma"/); // Missing churn value.
element('chart-type').listeners.change({target: {value: 'bar'}});
assert.deepEqual(barNames(), ['Gamma', 'Alpha', 'Beta', 'Delta (high)']);
axis('x', 'churn');
assert.deepEqual(barNames(), ['Alpha', 'Beta', 'Delta (high)']);
assert.equal(element('graph-legend').textContent, 'Units changed, all measured (mean). Older generations faded.');
axis('x', 'coverage');
assert.deepEqual(barNames(), ['Alpha', 'Beta']);
assert.match(graph(), /<span class="bar-value">33.3%<\/span>/);
assert.equal(element('graph-legend').textContent, 'Measured (%). Older generations faded.');
axis('x', 'solved_net');
assert.deepEqual(barNames(), ['Alpha', 'Beta']);
assert.match(graph(), /Net units added, solved \(mean\): 7; Measured 2\/6 solved attempts/);
axis('x', 'resolve_rate');
assert.deepEqual(barNames(), ['Alpha', 'Gamma', 'Beta']);
assert.match(graph(), /<span class="bar-value">80%<\/span>/);
assert.match(graph(), /Solved \(%\): 80%;/);
assert.equal(element('graph-legend').textContent, 'Solved (%). Older generations faded.');
doc.querySelectorAll('#graph [data-bar]')[0].listeners.focus({});
assert.match(tooltip.textContent, /Solved \(%\): 80%\n/);
assert.equal(browser.location.search, '?keep=1&chart=bar');
assert.equal(browser.location.hash, '#board');
task('org__repo-1');
assert.deepEqual(names(), ['Alpha', 'Beta', 'Gamma']);
assert.deepEqual(barNames(), ['Alpha', 'Beta', 'Gamma']);
assert.equal(element('graph-x').value, 'net');
assert.equal(element('header-net').attributes['aria-sort'], 'ascending');
element('chart-type').listeners.change({target: {value: 'scatter'}});
assert.match(graph(), /unknown task attempt/);
assert.match(graph(), /failed task attempt/);
task('');
assert.equal(element('header-solved_net').attributes['aria-sort'], 'ascending');
assert.equal(element('graph-x').value, 'resolve_rate'); // All-task axes survive task browsing.
const externalOutcomes = structuredClone(outcomes);
externalOutcomes.external = structuredClone(withExternal.external);
for (const m of externalOutcomes.models) Object.assign(m, {aa_intelligence: 50, aa_coding: 60});
load(externalOutcomes);
assert.equal(element('graph-x').value, 'solved_net');
assert.equal(element('graph-y').value, 'aa_intelligence');
assert.doesNotMatch(graph(), /data-model="Gamma"|Delta/);
axis('x', 'aa_coding');
assert.match(graph(), /Artificial Analysis Coding Index: 60.0/);
assert.match(graph(), /data-model="Gamma"/); // External-only axes need no footprint measurement.
load(gradedSelfRun, 'https://example.org/index.html?chart=bar&selfrun=0');
assert.equal(element('chart-type').value, 'bar');
assert.equal(element('self-run-toggle').checked, false);
assert.equal(element('self-run-note').hidden, true);
assert.doesNotMatch(graph() + element('#board tbody').innerHTML, /Delta/);
element('self-run-toggle').listeners.change({target: {checked: true}});
assert.match(graph(), /Delta/);
assert.equal(element('self-run-note').hidden, false);
assert.equal(browser.location.search, '?chart=bar');
// Same-task ratio (task difficulty): ranks, defaults, task averages and self-run range bars.
const sameTask = structuredClone(gradedSelfRun);
Object.assign(sameTask.models[0], {same_task_net: 1.2, same_task_net_ci: [1.1, 1.3], same_task_net_tasks: 8,
  same_task_complexity: 1.1, same_task_complexity_ci: null, same_task_complexity_tasks: 3, measured_solved_complexity_mean: 9});
Object.assign(sameTask.models[1], {same_task_net: 0.9, same_task_net_ci: [0.8, 1.0], same_task_net_tasks: 8,
  same_task_complexity: 0.7, same_task_complexity_ci: [0.6, 0.8], same_task_complexity_tasks: 8, measured_solved_complexity_mean: 4});
Object.assign(sameTask.self_run_models[0], {same_task_net: 0.5, same_task_net_ci: [0.3, 0.9], same_task_net_tasks: 5,
  same_task_complexity: 0.6, same_task_complexity_ci: null, same_task_complexity_tasks: 2, measured_solved_complexity_mean: 3});
sameTask.task_typical = {'org__repo-1': [150.5, 12, 4]};
for (const row of sameTask.footprint_tasks) for (const cell of row[2]) { while (cell.length < 8) cell.push(true); cell[8] = 7; }
load(sameTask, 'https://example.org/index.html');
assert.equal(element('graph-x').value, 'same_net');
assert.equal(element('header-same_net').attributes['aria-sort'], 'ascending');
assert.deepEqual(names(), ['Beta', 'Alpha', 'Gamma']); // Beta writes less than others on its tasks despite fewer solves
assert.match(element('#board tbody').innerHTML, /<tr><td>1<\/td><td class="left">Beta<\/td><td title="95% range 0.80–1.00× over 8 tasks">0.90×<\/td>/);
assert.match(element('#board tbody').innerHTML, /<td>2<\/td><td class="left">Alpha<\/td>/);
assert.match(element('rank-help').textContent, /same tasks/);
assert.match(element('graph-x').innerHTML, /value="same_cx">Complexity vs\. other models, same tasks/);
assert.match(element('graph-x').innerHTML, /value="solved_cx">Complexity added, solved \(mean\)/);
assert.equal((graph().match(/<line class="range/g) || []).length, 0); // ranges are in the tooltip only, also for self-runs
assert.match(graph(), /0\.50×/);
const selfRunPoint = doc.querySelectorAll('#graph circle[data-point]').find(c => /Delta/.test(graph().match(new RegExp(`<circle data-point="${c.dataset.point}"[^>]*>`))[0]));
selfRunPoint.listeners.focus({});
assert.match(tooltip.textContent, /95% range 0\.30–0\.90× over 5 tasks/);
axis('x', 'same_cx');
selfRunPoint.listeners.focus({});
doc.querySelectorAll('#graph circle[data-point]').find(c => /Delta/.test(graph().match(new RegExp(`<circle data-point="${c.dataset.point}"[^>]*>`))[0])).listeners.focus({});
assert.match(tooltip.textContent, /Only 2 shared tasks: too few for a range/);
task('org__repo-1');
assert.match(element('task-status').textContent, /Typical solved patch: \+150\.5 net units, complexity \+12 \(mean of 4 models\)\./);
assert.match(element('graph-x').innerHTML, /value="cx">Complexity added/);
axis('x', 'cx');
assert.match(graph(), /Complexity added: 7\.0/);
task('');
assert.equal(element('header-same_net').attributes['aria-sort'], 'ascending');
console.log('Sorting, chart views, task switching, external/self-run axes and fixed metric regressions passed');
