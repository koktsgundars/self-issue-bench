const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');

const code = fs.readFileSync(process.env.CODE_FILE, 'utf8');
const mod = { exports: {} };
const fn = new Function('module', 'exports', 'require', code + '\nif (typeof parseJsonStream !== "undefined") module.exports = { parseJsonStream };');
fn(mod, mod.exports, require);
const parseJsonStream = mod.exports.parseJsonStream;

describe('parseJsonStream', () => {
  it('single object', () => {
    assert.deepStrictEqual(parseJsonStream('{"a":1}'), [{ a: 1 }]);
  });

  it('two concatenated objects', () => {
    assert.deepStrictEqual(
      parseJsonStream('{"a":1}{"b":2}'),
      [{ a: 1 }, { b: 2 }]
    );
  });

  it('whitespace between objects', () => {
    assert.deepStrictEqual(
      parseJsonStream('  {"a":1}  {"b":2}  '),
      [{ a: 1 }, { b: 2 }]
    );
  });

  it('nested braces in object', () => {
    assert.deepStrictEqual(
      parseJsonStream('{"a":{"b":{"c":1}}}'),
      [{ a: { b: { c: 1 } } }]
    );
  });

  it('quoted braces', () => {
    assert.deepStrictEqual(
      parseJsonStream('{"a":"{"}'),
      [{ a: '{' }]
    );
  });

  it('empty string returns empty array', () => {
    assert.deepStrictEqual(parseJsonStream(''), []);
  });
});
