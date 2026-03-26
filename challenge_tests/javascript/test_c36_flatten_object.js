const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');

const code = fs.readFileSync(process.env.CODE_FILE, 'utf8');
const mod = { exports: {} };
const fn = new Function('module', 'exports', 'require', code + '\nif (typeof flattenObject !== "undefined") module.exports = { flattenObject };');
fn(mod, mod.exports, require);
const flattenObject = mod.exports.flattenObject;

describe('flattenObject', () => {
  it('basic nested object', () => {
    assert.deepStrictEqual(flattenObject({ a: { b: 1 } }), { 'a.b': 1 });
  });

  it('deep nesting', () => {
    assert.deepStrictEqual(
      flattenObject({ a: { b: { c: { d: 2 } } } }),
      { 'a.b.c.d': 2 }
    );
  });

  it('arrays use numeric indices', () => {
    const result = flattenObject({ a: [10, 20] });
    assert.strictEqual(result['a.0'], 10);
    assert.strictEqual(result['a.1'], 20);
  });

  it('null values preserved', () => {
    assert.deepStrictEqual(flattenObject({ a: null }), { a: null });
  });

  it('empty object returns empty', () => {
    assert.deepStrictEqual(flattenObject({}), {});
  });

  it('mixed objects and arrays', () => {
    const result = flattenObject({ a: { b: [1, 2] }, c: 3 });
    assert.strictEqual(result['a.b.0'], 1);
    assert.strictEqual(result['a.b.1'], 2);
    assert.strictEqual(result['c'], 3);
  });

  it('top-level primitives unchanged', () => {
    assert.deepStrictEqual(flattenObject({ a: 1, b: 'hello' }), { a: 1, b: 'hello' });
  });
});
