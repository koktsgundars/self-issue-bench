const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');

const code = fs.readFileSync(process.env.CODE_FILE, 'utf8');
const mod = { exports: {} };
const fn = new Function('module', 'exports', 'require', code + '\nif (typeof throttle !== "undefined") module.exports = { throttle };');
fn(mod, mod.exports, require);
const throttle = mod.exports.throttle;

describe('throttle', () => {
  it('returns a function', () => {
    const throttled = throttle(() => {}, 100);
    assert.strictEqual(typeof throttled, 'function');
  });

  it('has cancel method', () => {
    const throttled = throttle(() => {}, 100);
    assert.strictEqual(typeof throttled.cancel, 'function');
  });

  it('first call executes immediately', () => {
    let called = false;
    const throttled = throttle(() => { called = true; }, 100);
    throttled();
    assert.strictEqual(called, true);
  });

  it('second call within limit is ignored', (t, done) => {
    let callCount = 0;
    const throttled = throttle(() => { callCount++; }, 100);
    throttled();
    throttled();
    throttled();
    assert.strictEqual(callCount, 1);
    setTimeout(() => {
      assert.strictEqual(callCount, 1);
      done();
    }, 50);
  });

  it('call after limit passes executes', (t, done) => {
    let callCount = 0;
    const throttled = throttle(() => { callCount++; }, 50);
    throttled();
    assert.strictEqual(callCount, 1);
    setTimeout(() => {
      throttled();
      assert.strictEqual(callCount, 2);
      done();
    }, 100);
  });
});
