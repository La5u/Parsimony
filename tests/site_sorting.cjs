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
];
const elements = new Map();
function element(id) {
  if (id === '#graph') id = 'graph';
  if (!elements.has(id)) elements.set(id, {
    innerHTML: '', textContent: '', value: '', hidden: false, listeners: {}, attributes: {},
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
        dataset: {point: match[1]}, listeners: {}, addEventListener(event, fn) { this.listeners[event] = fn; }
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
vm.runInNewContext(html.match(/<script>\n([\s\S]*?)<\/script>/)[1], {document: doc});
const rows = () => [...element('#board tbody').innerHTML.matchAll(/<tr>([\s\S]*?)<\/tr>/g)].map(m => m[1]);
const names = () => rows().map(row => row.match(/<td class="left">(.*?)<\/td>/)?.[1]);
const graph = () => element('graph').innerHTML;
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
assert.match(graph(), /Alpha \(Anthropic\).*Net units added \(mean per attempt\): −2.0, Solved \(%\): 80.0%/);
assert.doesNotMatch(graph(), /Gamma \(Anthropic\)/);
assert.match(graph(), /aria-labelledby="plot-title plot-desc"/);
assert.match(graph(), /tabindex="0"/);
assert.match(element('company-legend').innerHTML, /Anthropic/);
assert.match(element('company-legend').innerHTML, /OpenAI/);
const initialColors = colors();
assert.notEqual(initialColors[0], initialColors[1]);
for (const event of ['mouseenter', 'focus', 'click']) {
  doc.querySelectorAll('#graph circle[data-point]')[0].listeners[event]();
  assert.match(element('graph-detail').textContent, /Alpha \(Anthropic\).*measured 4\/4/);
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
}
axis('x', 'net'); axis('y', 'score');
assert.match(graph(), /Beta \(OpenAI\).*Score \(midpoint if bounded\): 20.0/);
axis('x', 'score'); // Selecting the other axis's metric swaps, rather than duplicating, it.
assert.equal(element('graph-y').value, 'net');
axis('y', 'resolve_rate');
task('org__repo-1');
assert.equal(element('graph-x').value, 'net');
assert.equal(element('graph-y').value, 'score');
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
element('task-reset').listeners.click();
assert.equal(element('graph-x').value, 'score'); // All-task axis choices survive task browsing.
assert.equal(element('graph-y').value, 'resolve_rate');
assert.equal(element('task-footer').hidden, true);
assert.equal(element('ci-help').hidden, false);
assert.deepEqual(names(), ['Beta', 'Alpha', 'Gamma']);
assert.doesNotMatch(element('#board thead').innerHTML, /churn|Per solve/i);
console.log('Column sorting, selectable axes, company colors, bounds and task switching passed');
