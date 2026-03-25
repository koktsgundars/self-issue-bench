const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');

const code = fs.readFileSync(process.env.CODE_FILE, 'utf8');
const mod = { exports: {} };
const fn = new Function('module', 'exports', 'require', code + '\nif (typeof deepClone !== "undefined") module.exports = { deepClone };');
fn(mod, mod.exports, require);
const deepClone = mod.exports.deepClone;

describe('deepClone', () => {
  it('clones nested objects', () => {
    const orig = { a: { b: { c: 1 } } };
    const clone = deepClone(orig);
    assert.deepStrictEqual(clone, orig);
    clone.a.b.c = 99;
    assert.strictEqual(orig.a.b.c, 1);
  });

  it('clones arrays', () => {
    const orig = [1, [2, [3]]];
    const clone = deepClone(orig);
    assert.deepStrictEqual(clone, orig);
    clone[1][1][0] = 99;
    assert.strictEqual(orig[1][1][0], 3);
  });

  it('clones mixed objects and arrays', () => {
    const orig = { items: [1, { nested: true }] };
    const clone = deepClone(orig);
    assert.deepStrictEqual(clone, orig);
    clone.items[1].nested = false;
    assert.strictEqual(orig.items[1].nested, true);
  });

  it('handles primitives', () => {
    assert.strictEqual(deepClone(42), 42);
    assert.strictEqual(deepClone('hello'), 'hello');
    assert.strictEqual(deepClone(null), null);
    assert.strictEqual(deepClone(true), true);
  });

  it('does not mutate original', () => {
    const orig = { x: [1, 2], y: { z: 3 } };
    const clone = deepClone(orig);
    clone.x.push(3);
    clone.y.z = 99;
    assert.strictEqual(orig.x.length, 2);
    assert.strictEqual(orig.y.z, 3);
  });

  it('handles empty object', () => {
    assert.deepStrictEqual(deepClone({}), {});
  });

  it('handles empty array', () => {
    assert.deepStrictEqual(deepClone([]), []);
  });
});
