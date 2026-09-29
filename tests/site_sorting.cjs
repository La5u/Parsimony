// Run against a rendered page; no browser or npm dependencies required.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const html = fs.readFileSync(process.argv[2], 'utf8');
const data = JSON.parse(html.match(/type="application\/json">([\s\S]*?)<\/script>/)[1]);
const base = data.models[0];
data.models = [
  {...base, name: 'Alpha', score: 10, lower: 4, upper: 16, ci: [1, 90], resolve_rate: .8,
    company: 'Anthropic', measured_net_mean: -2, measured_attempts: 4, rank_range: [1, 2]},
  {...base, name: 'Beta', score: null, lower: 10, upper: 30, ci: [2, 40], resolve_rate: .3,
    company: 'OpenAI', measured_net_mean: 0, measured_attempts: 3, rank_range: [2, 3]},
  {...base, name: 'Gamma', score: 5, lower: 5, upper: 5, ci: [3, 20], resolve_rate: .5,
    company: 'Anthropic', measured_net_mean: null, measured_attempts: 0, rank_range: null},
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
];
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
let lastButtons, lastHeader, lastCircles, lastGraph;
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
        getBoundingClientRect() { return {left: 100, width: 12, bottom: 200}; }
      }));
      return lastCircles;
    }
    if (selector !== '#board button[data-sort]') return [];
    const head = element('#board thead').innerHTML;
    if (lastButtons && lastHeader === head) return lastButtons;
    lastHeader = head;
    lastButtons = [...head.matchAll(/<th([^>]*)><button type="button" data-sort="([^"]+)"[^>]*>/g)].map(match => {
      const th = element('header-' + match[2]);
      th.attributes['aria-sort'] = match[1].match(/aria-sort="([^"]+)"/)?.[1];
      return {dataset: {sort: match[2]}, parentElement: th, listeners: {}, addEventListener(event, fn) { this.listeners[event] = fn; }};
    });
    return lastButtons;
  },
};
const browser = {innerWidth: 800, innerHeight: 600, listeners: {},
  addEventListener(event, fn) { this.listeners[event] = fn; }};
vm.runInNewContext(html.match(/<script>\n([\s\S]*?)<\/script>/)[1], {document: doc, window: browser});
assert.match(html, /color-scheme: light/);
assert.doesNotMatch(html, /prefers-color-scheme|color-scheme: dark/);
const rows = () => [...element('#board tbody').innerHTML.matchAll(/<tr>([\s\S]*?)<\/tr>/g)].map(m => m[1]);
const names = () => rows().map(row => row.match(/<td class="left">(.*?)<\/td>/)?.[1]);
const graph = () => element('graph').innerHTML;
function tickValues(axis) {
  const anchor = axis === 'x' ? 'middle' : 'end';
  const pattern = new RegExp(`<text class="tick" text-anchor="${anchor}"[^>]*>([−\\d.]+%?)<\\/text>`, 'g');
  return [...graph().matchAll(pattern)].map(m => Number.parseFloat(m[1].replace('−', '-')));
}
const colors = () => [...graph().matchAll(/<circle[^>]*fill="([^"]+)"/g)].map(m => m[1]);
function click(key, expected, direction) {
  const button = doc.querySelectorAll('#board button[data-sort]').find(b => b.dataset.sort === key);
  assert(button, `missing sort button ${key}`);
  button.listeners.click();
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
assert.doesNotMatch(element('#board thead').innerHTML, /Per solve|churn/i);
assert.doesNotMatch(html.split('<script id="parsimony-data"')[0], /Per solve|churn/i);
assert.match(element('#board tbody').innerHTML, /−2.0/);
click('score', ['Gamma', 'Alpha', 'Beta'], 'ascending');
click('score', ['Beta', 'Alpha', 'Gamma'], 'descending');
click('ci', ['Gamma', 'Beta', 'Alpha'], 'descending');
click('ci', ['Alpha', 'Beta', 'Gamma'], 'ascending');
click('resolve_rate', ['Alpha', 'Gamma', 'Beta'], 'descending');
click('resolve_rate', ['Beta', 'Gamma', 'Alpha'], 'ascending');
click('net', ['Alpha', 'Beta', 'Gamma'], 'ascending');
click('net', ['Beta', 'Alpha', 'Gamma'], 'descending');
assert.equal(element('graph-x').value, 'net');
assert.equal(element('graph-y').value, 'resolve_rate');
assert.equal(tickValues('x')[0], -2.1);
assert.equal(tickValues('x').at(-1), .1);
assert.deepEqual(tickValues('y'), [0, 25, 50, 75, 100]);
assert.match(graph(), /Alpha \(Anthropic\).*Net units added \(mean per attempt\): −2.0, Solved \(%\): 80.0%/);
assert.doesNotMatch(graph(), /Gamma \(Anthropic\)/);
assert.match(graph(), /aria-describedby="plot-desc"/);
assert.doesNotMatch(graph(), /<title\b/); // Native SVG titles would create a second, delayed tooltip.
assert.match(graph(), /tabindex="0"/);
assert.match(element('company-legend').innerHTML, /Anthropic/);
assert.match(element('company-legend').innerHTML, /OpenAI/);
const initialColors = colors();
assert.notEqual(initialColors[0], initialColors[1]);
const tooltip = element('graph-tooltip');
assert.equal(tooltip.hidden, true);
const firstCircle = doc.querySelectorAll('#graph circle[data-point]')[0];
for (const event of ['mouseenter', 'mousemove', 'focus', 'click']) {
  firstCircle.listeners[event]();
  assert.equal(tooltip.textContent, 'Alpha'); // Immediate, model name only; no metrics/company.
  assert.equal(tooltip.hidden, false);
  firstCircle.listeners.mouseleave();
  assert.equal(tooltip.hidden, true);
}
firstCircle.listeners.mouseenter({clientX: 799, clientY: 599});
assert.equal(tooltip.style.left, '632px');
assert.equal(tooltip.style.top, '563px');
firstCircle.listeners.blur();
assert.equal(tooltip.hidden, true);
for (const event of ['scroll', 'resize']) {
  firstCircle.listeners.focus();
  browser.listeners[event]();
  assert.equal(tooltip.hidden, true);
}
// Every numeric table value is selectable; ranges expose explicit endpoints.
const keys = ['score', 'ci', 'ci_high', 'resolve_rate', 'net', 'rank_low', 'rank_high'];
for (const key of keys) assert(element('graph-x').innerHTML.includes(`value="${key}"`));
assert.doesNotMatch(element('graph-x').innerHTML, /churn|solved_mean/i);
for (const x of keys) for (const y of keys.filter(k => k !== x)) {
  axis('x', x); axis('y', y);
  assert.equal(element('graph-x').value, x);
  assert.equal(element('graph-y').value, y);
  assert.doesNotMatch(graph(), /NaN|Infinity/);
  if (x === 'resolve_rate') assert.deepEqual(tickValues('x'), [0, 25, 50, 75, 100]);
  if (y === 'resolve_rate') assert.deepEqual(tickValues('y'), [0, 25, 50, 75, 100]);
}
axis('x', 'net'); axis('y', 'score');
assert.match(graph(), /Beta \(OpenAI\).*Score \(midpoint if bounded\): 20.0/);
axis('x', 'score'); // Selecting the other axis's metric swaps, rather than duplicating, it.
assert.equal(element('graph-y').value, 'net');
axis('y', 'resolve_rate');
task('org__repo-1');
assert.equal(element('graph-x').value, 'net');
assert.equal(element('graph-y').value, 'score');
assert.equal(tickValues('x')[0], 100); // 111..331 with 5% padding, not anchored at zero.
assert.equal(tickValues('x').at(-1), 342);
assert.doesNotMatch(element('graph-x').innerHTML, /ci|resolve_rate|rank_low/);
assert.match(element('#board tbody').innerHTML, /<td class="left">Alpha<\/td><td class="left r">solved<\/td><td>10\.0<\/td><td>\+111<\/td><\/tr>/);
assert.match(graph(), /Gamma \(Anthropic\): failed task attempt/);
assert.deepEqual(colors(), [initialColors[0], initialColors[1], initialColors[0]]);
assert.equal(element('ci-help').hidden, true);
assert.equal(element('rank-note').hidden, true);
click('score', ['Gamma', 'Alpha', 'Beta'], 'ascending');
click('score', ['Beta', 'Alpha', 'Gamma'], 'descending');
click('net', ['Alpha', 'Beta', 'Gamma'], 'ascending');
click('net', ['Gamma', 'Beta', 'Alpha'], 'descending');
axis('x', 'score');
assert.equal(element('graph-y').value, 'net');
task('org__repo-2');
assert.match(element('#board tbody').innerHTML, /−25.0–0.0/);
assert.match(graph(), /Task score \(midpoint if bounded\): −12.5/);
task('not-a-task');
assert.match(element('task-status').textContent, /Still showing org__repo-2/);
task('org__repo-3');
assert.match(element('graph-legend').textContent, /No measured points/);
assert.doesNotMatch(graph(), /<circle|NaN|Infinity/);
assert.deepEqual(tickValues('x'), [0, .3, .5, .8, 1]);
assert.deepEqual(tickValues('y'), [0, .3, .5, .8, 1]);
axis('x', 'net');
for (const [id, low, high] of [['constant', 1140, 1260], ['single', 950, 1050],
                              ['negative', -2040, -1160], ['zero', -1, 1]]) {
  task(id);
  assert.equal(tickValues('x')[0], low);
  assert.equal(tickValues('x').at(-1), high);
  assert.equal(tickValues('x').length, 5);
  assert.doesNotMatch(graph(), /NaN|Infinity/);
}
element('task-reset').listeners.click();
assert.equal(element('graph-x').value, 'score'); // All-task axis choices survive task browsing.
assert.equal(element('graph-y').value, 'resolve_rate');
assert.equal(element('task-footer').hidden, true);
assert.equal(element('ci-help').hidden, false);
assert.deepEqual(names(), ['Beta', 'Alpha', 'Gamma']);
assert.doesNotMatch(element('#board thead').innerHTML, /churn|Per solve/i);
console.log('Light mode, instant name tooltips, sorting, axes and task switching passed');
