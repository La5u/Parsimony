'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const {validateBenchmark, summarizeBenchmark, MAX_FILE_BYTES} = require('../site/custom-benchmark.js');
const row = {model: 'A', task: 't', amount: 2, solved: true};
const data = (results = [row], measurement = 'total') => ({benchmark: 'Test', unit: 'lines', measurement, results});
assert.equal(validateBenchmark(data()).benchmark, 'Test');
for (const input of [null, [], {}, {...data(), benchmark: ' '}, {...data(), unit: 4}, {...data(), measurement: 'other'}, {...data(), results: {}}, {...data(), extra: 1}, data(Array(10001).fill(row))]) assert.throws(() => validateBenchmark(input));
for (const patch of [{model: ''}, {task: null}, {attempt: null}, {amount: undefined}, {amount: '2'}, {amount: NaN}, {amount: Infinity}, {amount: -Infinity}, {solved: 1}, {solved: 'true'}, {extra: true}]) assert.throws(() => validateBenchmark(data([{...row, ...patch}])));
for (const measurement of ['total', 'churn']) assert.throws(() => validateBenchmark(data([{...row, amount: -1}], measurement)));
validateBenchmark(data([{...row, amount: -1}], 'net'));
validateBenchmark(data([{...row, amount: null, solved: null}]));
validateBenchmark(data([{model: 'A', task: 't', amount: 0}]));
assert.throws(() => validateBenchmark(data([row, row])));
assert.throws(() => validateBenchmark(data([row, {...row, attempt: ''}])));
validateBenchmark(data([row, {...row, attempt: '2'}]));
validateBenchmark(data([{...row, model: '__proto__'}, {...row, model: 'constructor'}]));
assert.deepEqual(summarizeBenchmark(data([])), []);
const summaries = summarizeBenchmark(data([
  {model: 'A', task: '1', amount: 10, solved: true},
  {model: 'A', task: '2', amount: 0, solved: false},
  {model: 'A', task: '3', amount: null, solved: true},
  {model: 'A', task: '4', amount: 20},
  {model: 'A', task: '5', amount: null, solved: null},
  {model: 'B', task: '1', amount: -2},
  {model: 'C', task: '1', amount: null, solved: false}
], 'net'));
assert.deepEqual(summaries.map(s => s.model), ['B', 'A', 'C']);
assert.deepEqual(summaries[1], {model: 'A', recorded: 5, measured: 3, solved: 2, known: 3, unknown: 2, solvedMeasured: 1, mean: 10, solvedMean: 10});
assert.equal(summaries[0].solvedMean, null);
assert.equal(summaries[2].mean, null);
assert.equal(summarizeBenchmark(data([row, {...row, task: '2', amount: Number.MAX_VALUE}, {...row, task: '3', amount: Number.MAX_VALUE}]))[0].mean < Infinity, true);

// Minimal DOM: any use of HTML injection fails the test.
class Element {
  constructor(tag) { this.tag = tag; this.children = []; this.listeners = {}; this.textContent = ''; this.value = ''; }
  set innerHTML(_) { throw new Error('Unsafe HTML assignment'); }
  addEventListener(name, fn) { this.listeners[name] = fn; }
  appendChild(child) { this.children.push(child); return child; }
  replaceChildren() { this.children = []; }
  click() { this.clicked = true; }
}
const elements = Object.fromEntries(['custom-file', 'custom-status', 'custom-results', 'custom-clear', 'custom-example'].map(id => [id, new Element(id)]));
const created = [];
let blob, revoked;
const context = {
  document: {readyState: 'complete', getElementById: id => elements[id], createElement: tag => { const e = new Element(tag); created.push(e); return e; }},
  Blob: class { constructor(parts, options) { blob = {parts, options}; } },
  URL: {createObjectURL: () => 'blob:local', revokeObjectURL: url => { revoked = url; }},
  setTimeout: fn => fn()
};
const source = fs.readFileSync(require.resolve('../site/custom-benchmark.js'), 'utf8');
vm.runInNewContext(source, context);
vm.runInNewContext(source, {document: {readyState: 'complete', getElementById: () => null}});
const text = e => [e.textContent, ...e.children.map(text)].join(' ');
async function upload(value, size = 100) {
  elements['custom-file'].value = 'C:\\fakepath\\benchmark.json';
  elements['custom-file'].files = [{size, text: async () => typeof value === 'string' ? value : JSON.stringify(value)}];
  const pending = elements['custom-file'].listeners.change();
  assert.equal(elements['custom-file'].value, '', 'Selection resets before reading, allowing same-file reloads even after errors');
  await pending;
}
(async () => {
  const attack = '<img src=x onerror=alert(1)>';
  await upload({...data([{...row, model: attack}]), benchmark: attack, unit: attack});
  const output = text(elements['custom-results']);
  assert.ok(output.includes(attack));
  for (const label of ['User-provided, unverified', 'Measurement: total', 'Unit:', 'not part of the official board', 'known outcomes only', 'Unknown outcomes', 'Measured / recorded', 'Missing amounts are excluded, not zero']) assert.ok(output.includes(label), label);
  // Simulate editing and selecting the same path again.
  await upload(data([{...row, amount: 7}]));
  assert.match(text(elements['custom-results']), /7/);
  await upload('{broken');
  assert.equal(elements['custom-results'].children.length, 0);
  assert.match(elements['custom-status'].textContent, /Unable to load/);
  await upload(data(), MAX_FILE_BYTES + 1);
  assert.match(elements['custom-status'].textContent, /5 MB/);
  elements['custom-file'].files = [{size: 1, text: async () => { throw new Error('read failed'); }}];
  await elements['custom-file'].listeners.change();
  assert.match(elements['custom-status'].textContent, /read failed/);
  let finish;
  elements['custom-file'].files = [{size: 1, text: () => new Promise(resolve => { finish = resolve; })}];
  const pending = elements['custom-file'].listeners.change();
  elements['custom-clear'].listeners.click();
  finish(JSON.stringify(data()));
  await pending;
  assert.equal(elements['custom-results'].children.length, 0);
  assert.equal(elements['custom-status'].textContent, '');
  assert.equal(elements['custom-file'].value, '');
  elements['custom-example'].listeners.click();
  validateBenchmark(JSON.parse(blob.parts.join('')));
  assert.equal(blob.options.type, 'application/json');
  assert.equal(revoked, 'blob:local');
  assert.ok(created.some(e => e.tag === 'a' && e.clicked && e.download.endsWith('.json')));
  console.log('custom benchmark tests passed');
})().catch(error => { console.error(error); process.exitCode = 1; });
