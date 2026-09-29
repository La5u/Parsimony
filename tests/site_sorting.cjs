// Run against a rendered page; no browser or npm dependencies required.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const html = fs.readFileSync(process.argv[2], 'utf8');
const data = JSON.parse(html.match(/type="application\/json">([\s\S]*?)<\/script>/)[1]);
const base = data.models[0];
data.models = [
  {...base, name: 'Alpha', score: 10, lower: 4, upper: 16, ci: [1, 90], resolve_rate: .8, solved_mean: 70, churn: 30, company: 'Anthropic', measured_net_mean: -2, measured_churn_mean: 12, measured_attempts: 4},
  {...base, name: 'Beta', score: null, lower: 10, upper: 30, ci: [2, 40], resolve_rate: .3, solved_mean: 80, churn: 10, company: 'OpenAI', measured_net_mean: 0, measured_churn_mean: 6, measured_attempts: 3},
  {...base, name: 'Gamma', score: 5, lower: 5, upper: 5, ci: [3, 20], resolve_rate: .5, solved_mean: null, churn: null, company: 'Anthropic', measured_net_mean: null, measured_churn_mean: null, measured_attempts: 0},
];
data.task_count = 4;
data.tasks = [
  ['org__repo-1', 99, [['r', 111, 112, 10], ['r', 221, 222, 20], ['f', 331, 332, 5]]],
  ['org__repo-2', 55, [['f', -11, 12, null, 2, 8], ['r', 21, 22, 30], ['r', 31, 32, 40]]],
  ['org__repo-3', null, [['m', null, null, null], ['m', null, null, null], ['m', null, null, null]]],
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
let lastButtons = null, lastHeader = null, lastCircles = null, lastGraph = null;
const doc = {
  getElementById: element,
  querySelector: selector => selector === '#graph' ? element('graph') : element(selector),
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
      const sort = match[1].match(/aria-sort="([^"]+)"/);
      th.attributes['aria-sort'] = sort?.[1];
      return {dataset: {sort: match[2]}, parentElement: th, listeners: {}, addEventListener(event, fn) { this.listeners[event] = fn; }};
    });
    return lastButtons;
  },
};
vm.runInNewContext(html.match(/<script>\n([\s\S]*?)<\/script>/)[1], {document: doc});
const rows = () => [...element('#board tbody').innerHTML.matchAll(/<tr>([\s\S]*?)<\/tr>/g)].map(m => m[1]);
const names = () => rows().map(row => row.match(/<td class="left">(.*?)<\/td>/)?.[1]);
function click(key, expected, direction) {
  const button = doc.querySelectorAll('#board button[data-sort]').find(b => b.dataset.sort === key);
  assert(button, `missing sort button ${key}`);
  button.listeners.click();
  assert.deepEqual(names(), expected);
  assert.equal(button.parentElement.attributes['aria-sort'], direction);
  for (const other of doc.querySelectorAll('#board button[data-sort]').filter(b => b.dataset.sort !== key)) assert.equal(other.parentElement.attributes['aria-sort'], 'none');
}
assert.deepEqual(names(), ['Beta', 'Alpha', 'Gamma']);
let activeSort = 'score', isAscending = false;
for (const [key, ascOrder, descOrder] of [
  ['score', ['Gamma', 'Alpha', 'Beta'], ['Beta', 'Alpha', 'Gamma']],
  ['ci', ['Alpha', 'Beta', 'Gamma'], ['Gamma', 'Beta', 'Alpha']],
  ['resolve_rate', ['Beta', 'Gamma', 'Alpha'], ['Alpha', 'Gamma', 'Beta']],
  ['solved_mean', ['Alpha', 'Beta', 'Gamma'], ['Beta', 'Alpha', 'Gamma']],
  ['churn', ['Beta', 'Alpha', 'Gamma'], ['Alpha', 'Beta', 'Gamma']],
]) {
  isAscending = key === activeSort ? !isAscending : ['churn', 'net'].includes(key);
  click(key, isAscending ? ascOrder : descOrder, isAscending ? 'ascending' : 'descending');
  activeSort = key;
  isAscending = !isAscending;
  click(key, isAscending ? ascOrder : descOrder, isAscending ? 'ascending' : 'descending');
}
assert.match(element('#graph').innerHTML, /aria-labelledby="plot-title plot-desc"/);
assert.match(element('#graph').innerHTML, /Alpha \(Anthropic\): all measured attempts; net units −2.0, churn 12.0; measured 4\/4/);
assert.doesNotMatch(element('#graph').innerHTML, /Gamma \(Anthropic\): all measured/);
assert.match(element('#graph').innerHTML, /<title id="plot-title">/);
assert.match(element('#graph').innerHTML, /tabindex="0"/);
assert.match(element('company-legend').innerHTML, /Anthropic/);
assert.match(element('company-legend').innerHTML, /OpenAI/);
const colors = () => [...element('graph').innerHTML.matchAll(/<circle[^>]*fill="([^"]+)"/g)].map(m => m[1]);
const initialColors = colors();
assert.equal(initialColors.length, 2);
assert.notEqual(initialColors[0], initialColors[1]);
for (const event of ['mouseenter', 'focus', 'click']) {
  doc.querySelectorAll('#graph circle[data-point]')[0].listeners[event]();
  assert.match(element('graph-detail').textContent, /Alpha \(Anthropic\).*measured 4\/4/);
}
element('task-search').listeners.input({target: {value: 'org__repo-1'}});
assert.match(element('#board thead').innerHTML, /Net units added/);
assert.match(element('#board tbody').innerHTML, /<td class="left">Alpha<\/td><td class="left r">solved<\/td><td>10\.0<\/td><td>\+111<\/td><td>112\.0/);
assert.match(element('#board tbody').innerHTML, /<td class="left">Beta<\/td><td class="left r">solved<\/td><td>20\.0<\/td><td>\+221<\/td><td>222\.0/);
assert.match(element('#graph').innerHTML, /Alpha \(Anthropic\): resolved task attempt; net units 111.0, churn 112.0/);
assert.match(element('#graph').innerHTML, /Gamma \(Anthropic\): failed task attempt; net units 331.0, churn 332.0/);
assert.doesNotMatch(element('#graph').innerHTML, /all measured attempts;/);
assert.doesNotMatch(element('#graph').innerHTML, /Mean churn per attempt<\/text>/);
assert.deepEqual(colors(), [initialColors[0], initialColors[1], initialColors[0]]);
assert.match(element('graph-legend').textContent, /Dashed outline: failed/);
assert.equal(element('ci-help').hidden, true);
assert.equal(element('rank-note').hidden, true);
click('task_score', ['Gamma', 'Alpha', 'Beta'], 'ascending');
click('task_score', ['Beta', 'Alpha', 'Gamma'], 'descending');
click('net', ['Alpha', 'Beta', 'Gamma'], 'ascending');
click('net', ['Gamma', 'Beta', 'Alpha'], 'descending');
click('churn', ['Alpha', 'Beta', 'Gamma'], 'ascending');
click('churn', ['Gamma', 'Beta', 'Alpha'], 'descending');
element('task-search').listeners.input({target: {value: 'org__repo-2'}});
assert.match(element('#board tbody').innerHTML, /<td class="left">Alpha<\/td><td class="left f">failed<\/td><td>2\.0–8\.0<\/td>/);
element('task-search').listeners.input({target: {value: 'not-a-task'}});
assert.match(element('task-status').textContent, /No task matches/);
assert.match(element('#board tbody').innerHTML, /Alpha/);
element('task-search').listeners.input({target: {value: 'org__repo-3'}});
assert.match(element('graph-legend').textContent, /No measured points/);
assert.doesNotMatch(element('#graph').innerHTML, /<circle|NaN|Infinity/);
element('task-reset').listeners.click();
assert.match(element('#board thead').innerHTML, /95% CI/);
assert.equal(element('task-footer').hidden, true);
assert.equal(element('ci-help').hidden, false);
assert.deepEqual(names(), ['Beta', 'Alpha', 'Gamma']);
console.log('All-task and task sorting, cell alignment, and plot checks passed');
