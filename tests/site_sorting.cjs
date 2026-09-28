// Run against a rendered page; no browser or npm dependencies required.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const html = fs.readFileSync(process.argv[2], 'utf8');
const data = JSON.parse(html.match(/type="application\/json">([\s\S]*?)<\/script>/)[1]);
const base = data.models[0];
data.models = [
  {...base, name: 'Alpha', score: 10, ci: [1, 90], resolve_rate: .8, solved_mean: 70, churn: 30},
  {...base, name: 'Beta', score: null, lower: 10, upper: 30, ci: [2, 40], resolve_rate: .3, solved_mean: 80, churn: 10},
  {...base, name: 'Gamma', score: 5, ci: [3, 20], resolve_rate: .5, solved_mean: null, churn: null},
];
data.tasks = [['org__repo-1', 99, [['r', 111, 112, 10], ['r', 221, 222, 20], ['f', 331, 332, 5]]]];
const elements = new Map();
function element(id) {
  if (!elements.has(id)) elements.set(id, {
    innerHTML: '', textContent: '', listeners: {}, attributes: {},
    addEventListener(event, fn) { this.listeners[event] = fn; },
    setAttribute(name, value) { this.attributes[name] = value; },
  });
  return elements.get(id);
}
const keys = ['score', 'ci', 'resolve_rate', 'solved_mean', 'churn'];
const buttons = keys.map(key => {
  assert(html.includes(`data-sort="${key}"`));
  return Object.assign(element('button-' + key), {dataset: {sort: key}, parentElement: element('th-' + key)});
});
element('parsimony-data').textContent = JSON.stringify(data);
vm.runInNewContext(html.match(/<script>\n([\s\S]*?)<\/script>/)[1], {
  document: {getElementById: element, querySelector: element, querySelectorAll: () => buttons},
});
const order = () => [...element('#board tbody').innerHTML.matchAll(/<td class="left">(.*?)<\/td>/g)].map(m => m[1]);
function click(key, expected, direction) {
  const button = buttons[keys.indexOf(key)];
  button.listeners.click();
  assert.deepEqual(order(), expected);
  assert.equal(button.parentElement.attributes['aria-sort'], direction);
  for (const other of buttons.filter(b => b !== button)) assert.equal(other.parentElement.attributes['aria-sort'], 'none');
}
assert.deepEqual(order(), ['Beta', 'Alpha', 'Gamma']);
const taskBefore = element('#task-table tbody').innerHTML;
click('score', ['Gamma', 'Alpha', 'Beta'], 'ascending');
click('score', ['Beta', 'Alpha', 'Gamma'], 'descending');
click('ci', ['Gamma', 'Beta', 'Alpha'], 'descending');
click('ci', ['Alpha', 'Beta', 'Gamma'], 'ascending');
click('resolve_rate', ['Alpha', 'Gamma', 'Beta'], 'descending');
click('resolve_rate', ['Beta', 'Gamma', 'Alpha'], 'ascending');
click('solved_mean', ['Beta', 'Alpha', 'Gamma'], 'descending');
click('solved_mean', ['Alpha', 'Beta', 'Gamma'], 'ascending');
click('churn', ['Beta', 'Alpha', 'Gamma'], 'ascending');
click('churn', ['Alpha', 'Beta', 'Gamma'], 'descending');
// Sorting must not change the model-to-task-cell mapping.
assert.equal(element('#task-table tbody').innerHTML, taskBefore);
element('task-search').listeners.input({target: {value: 'org__repo-1'}});
assert.equal(element('#task-table tbody').innerHTML, taskBefore);
assert(taskBefore.includes('<td>+111</td>'));
console.log('Column sorting and task-cell alignment passed');
