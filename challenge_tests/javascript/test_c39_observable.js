const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');

const code = fs.readFileSync(process.env.CODE_FILE, 'utf8');
const mod = { exports: {} };
const fn = new Function('module', 'exports', 'require', code + '\nif (typeof Observable !== "undefined") module.exports = { Observable };');
fn(mod, mod.exports, require);
const Observable = mod.exports.Observable;

describe('Observable', () => {
  it('subscribe and next', () => {
    const obs = new Observable();
    const values = [];
    obs.subscribe({ next: (v) => values.push(v) });
    obs.next(1);
    obs.next(2);
    assert.deepStrictEqual(values, [1, 2]);
  });

  it('multiple subscribers', () => {
    const obs = new Observable();
    const a = [], b = [];
    obs.subscribe({ next: (v) => a.push(v) });
    obs.subscribe({ next: (v) => b.push(v) });
    obs.next(42);
    assert.deepStrictEqual(a, [42]);
    assert.deepStrictEqual(b, [42]);
  });

  it('unsubscribe stops receiving', () => {
    const obs = new Observable();
    const values = [];
    const sub = obs.subscribe({ next: (v) => values.push(v) });
    obs.next(1);
    sub.unsubscribe();
    obs.next(2);
    assert.deepStrictEqual(values, [1]);
  });

  it('complete signals completion', () => {
    const obs = new Observable();
    let completed = false;
    obs.subscribe({ next: () => {}, complete: () => { completed = true; } });
    obs.complete();
    assert.strictEqual(completed, true);
  });

  it('no values after complete', () => {
    const obs = new Observable();
    const values = [];
    obs.subscribe({ next: (v) => values.push(v) });
    obs.next(1);
    obs.complete();
    obs.next(2);
    assert.deepStrictEqual(values, [1]);
  });

  it('error signals error', () => {
    const obs = new Observable();
    let receivedErr = null;
    obs.subscribe({ next: () => {}, error: (e) => { receivedErr = e; } });
    obs.error('fail');
    assert.strictEqual(receivedErr, 'fail');
  });

  it('no values after error', () => {
    const obs = new Observable();
    const values = [];
    obs.subscribe({ next: (v) => values.push(v), error: () => {} });
    obs.next(1);
    obs.error('fail');
    obs.next(2);
    assert.deepStrictEqual(values, [1]);
  });

  it('subscribe after complete calls complete immediately', () => {
    const obs = new Observable();
    obs.subscribe({ next: () => {} });
    obs.complete();
    let completed = false;
    obs.subscribe({ next: () => {}, complete: () => { completed = true; } });
    assert.strictEqual(completed, true);
  });
});
