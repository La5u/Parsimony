/* Local, unverified benchmark viewer. No network or persistent storage. */
(function () {
  'use strict';
  const MAX_FILE_BYTES = 5 * 1024 * 1024;
  const MAX_RESULTS = 10000;
  const own = (object, key) => Object.prototype.hasOwnProperty.call(object, key);
  function object(value, keys, label) {
    if (!value || typeof value !== 'object' || Array.isArray(value)) throw new Error(label + ' must be an object.');
    if (Object.keys(value).some(key => !keys.includes(key))) throw new Error(label + ' contains an unsupported field.');
  }
  function string(value, label) {
    if (typeof value !== 'string' || !value.trim()) throw new Error(label + ' must be a nonempty string.');
  }
  function validateBenchmark(data) {
    object(data, ['benchmark', 'unit', 'measurement', 'results'], 'Benchmark');
    string(data.benchmark, 'benchmark');
    string(data.unit, 'unit');
    if (!['total', 'net', 'churn'].includes(data.measurement)) throw new Error('measurement must be total, net, or churn.');
    if (!Array.isArray(data.results) || data.results.length > MAX_RESULTS) throw new Error('results must be an array of at most 10000 entries.');
    const seen = new Set();
    data.results.forEach((row, index) => {
      const label = 'Result ' + (index + 1);
      object(row, ['model', 'task', 'attempt', 'amount', 'solved'], label);
      string(row.model, label + ' model');
      string(row.task, label + ' task');
      if (own(row, 'attempt') && typeof row.attempt !== 'string') throw new Error(label + ' attempt must be a string.');
      if (row.amount !== null && (typeof row.amount !== 'number' || !Number.isFinite(row.amount))) throw new Error(label + ' amount must be a finite number or null.');
      if (data.measurement !== 'net' && row.amount !== null && row.amount < 0) throw new Error(label + ' amount cannot be negative for total or churn.');
      if (own(row, 'solved') && row.solved !== null && typeof row.solved !== 'boolean') throw new Error(label + ' solved must be boolean or null.');
      const key = JSON.stringify([row.model, row.task, row.attempt === undefined ? '' : row.attempt]);
      if (seen.has(key)) throw new Error(label + ' duplicates a model/task/attempt.');
      seen.add(key);
    });
    return data;
  }
  function summarizeBenchmark(data) {
    validateBenchmark(data);
    const models = new Map();
    for (const row of data.results) {
      if (!models.has(row.model)) models.set(row.model, {model: row.model, recorded: 0, measured: 0, solved: 0, known: 0, unknown: 0, solvedMeasured: 0, mean: null, solvedMean: null});
      const summary = models.get(row.model);
      summary.recorded++;
      if (typeof row.solved === 'boolean') summary.known++;
      else summary.unknown++;
      if (row.solved === true) summary.solved++;
      // Weighted updates avoid overflowing a sum of finite input amounts.
      if (row.amount !== null) {
        summary.measured++;
        summary.mean = summary.measured === 1 ? row.amount : summary.mean * ((summary.measured - 1) / summary.measured) + row.amount / summary.measured;
        if (row.solved === true) {
          summary.solvedMeasured++;
          summary.solvedMean = summary.solvedMeasured === 1 ? row.amount : summary.solvedMean * ((summary.solvedMeasured - 1) / summary.solvedMeasured) + row.amount / summary.solvedMeasured;
        }
      }
    }
    return Array.from(models.values()).sort((a, b) => {
      if (a.mean === null) return b.mean === null ? a.model.localeCompare(b.model) : 1;
      if (b.mean === null) return -1;
      return a.mean - b.mean || a.model.localeCompare(b.model);
    });
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = {validateBenchmark, summarizeBenchmark, MAX_FILE_BYTES, MAX_RESULTS};
  if (typeof document === 'undefined') return;
  function initialize() {
    const fileInput = document.getElementById('custom-file');
    if (!fileInput) return;
    const status = document.getElementById('custom-status');
    const results = document.getElementById('custom-results');
    let generation = 0;
    function clear() {
      generation++;
      fileInput.value = '';
      results.replaceChildren();
      status.textContent = '';
    }
    function node(tag, text) {
      const element = document.createElement(tag);
      if (text !== undefined) element.textContent = text;
      return element;
    }
    function render(data) {
      results.replaceChildren();
      results.appendChild(node('h3', data.benchmark));
      results.appendChild(node('p', 'User-provided, unverified · Unit: ' + data.unit + ' · Measurement: ' + data.measurement + '. Independent per-model summaries; not part of the official board.'));
      results.appendChild(node('p', 'Missing amounts are excluded, not zero. Solved-only means include measured solved results only. Outcome denominators include known outcomes only; unknown outcomes are shown separately.'));
      const table = node('table');
      const head = node('thead');
      const headings = node('tr');
      ['Model', 'Mean amount', 'Solved-only mean', 'Solved / known outcomes', 'Unknown outcomes', 'Measured / recorded'].forEach(text => headings.appendChild(node('th', text)));
      head.appendChild(headings);
      table.appendChild(head);
      const body = node('tbody');
      for (const summary of summarizeBenchmark(data)) {
        const row = node('tr');
        [summary.model, summary.mean === null ? 'Not measured' : String(summary.mean), summary.solvedMean === null ? 'Not measured' : String(summary.solvedMean), summary.solved + ' / ' + summary.known, String(summary.unknown), summary.measured + ' / ' + summary.recorded].forEach(text => row.appendChild(node('td', text)));
        body.appendChild(row);
      }
      table.appendChild(body);
      results.appendChild(table);
    }
    fileInput.addEventListener('change', async () => {
      const current = ++generation;
      results.replaceChildren();
      status.textContent = '';
      try {
        const file = fileInput.files && fileInput.files[0];
        // Capture the File first, then allow the same path to be selected again.
        // Reset before awaiting so an older read cannot clear a newer selection.
        fileInput.value = '';
        if (!file) return;
        if (file.size > MAX_FILE_BYTES) throw new Error('File exceeds the 5 MB limit.');
        status.textContent = 'Reading local file…';
        const text = await file.text();
        if (current !== generation) return;
        const data = validateBenchmark(JSON.parse(text));
        render(data);
        status.textContent = 'Loaded locally. User-provided, unverified data; nothing uploaded or saved.';
      } catch (error) {
        if (current !== generation) return;
        results.replaceChildren();
        status.textContent = 'Unable to load benchmark: ' + error.message;
      }
    });
    document.getElementById('custom-clear').addEventListener('click', clear);
    document.getElementById('custom-example').addEventListener('click', () => {
      const example = {benchmark: 'Example benchmark', unit: 'lines', measurement: 'net', results: [
        {model: 'Example model', task: 'task-1', attempt: '1', amount: -2, solved: true},
        {model: 'Example model', task: 'task-2', amount: null, solved: null}
      ]};
      const url = URL.createObjectURL(new Blob([JSON.stringify(example, null, 2) + '\n'], {type: 'application/json'}));
      const link = node('a');
      link.href = url;
      link.download = 'custom-benchmark-example.json';
      try { link.click(); } finally { setTimeout(() => URL.revokeObjectURL(url), 0); }
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initialize);
  else initialize();
})();
