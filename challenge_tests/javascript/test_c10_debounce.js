const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');

const code = fs.readFileSync(process.env.CODE_FILE, 'utf8');
const mod = { exports: {} };
const fn = new Function('module', 'exports', 'require', code + '\nif (typeof debounce !== "undefined") module.exports = { debounce };');
fn(mod, mod.exports, require);
const debounce = mod.exports.debounce;

describe('debounce', () => {
  it('returns a function', () => {
    const fn = debounce(() => {}, 100);
    assert.strictEqual(typeof fn, 'function');
  });

  it('has cancel method', () => {
    const fn = debounce(() => {}, 100);
    assert.strictEqual(typeof fn.cancel, 'function');
  });

  it('calls function after delay', (t, done) => {
    let called = false;
    const fn = debounce(() => { called = true; }, 50);
    fn();
    assert.strictEqual(called, false);
    setTimeout(() => {
      assert.strictEqual(called, true);
      done();
    }, 100);
  });

  it('resets timer on repeated calls', (t, done) => {
    let callCount = 0;
    const fn = debounce(() => { callCount++; }, 50);
    fn();
    setTimeout(() => fn(), 30);
    setTimeout(() => {
      // Should have only fired once (after second call's delay)
      assert.strictEqual(callCount, 1);
      done();
    }, 150);
  });

  it('cancel prevents invocation', (t, done) => {
    let called = false;
    const fn = debounce(() => { called = true; }, 50);
    fn();
    fn.cancel();
    setTimeout(() => {
      assert.strictEqual(called, false);
      done();
    }, 100);
  });
});
