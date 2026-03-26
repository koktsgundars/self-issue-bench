const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');

const code = fs.readFileSync(process.env.CODE_FILE, 'utf8');
const mod = { exports: {} };
const fn = new Function('module', 'exports', 'require', code + '\nif (typeof parseQueryString !== "undefined") module.exports = { parseQueryString };');
fn(mod, mod.exports, require);
const parseQueryString = mod.exports.parseQueryString;

describe('parseQueryString', () => {
  it('basic key=value pairs', () => {
    assert.deepStrictEqual(parseQueryString('a=1&b=2'), { a: '1', b: '2' });
  });

  it('percent encoding', () => {
    const result = parseQueryString('q=hello%20world');
    assert.strictEqual(result.q, 'hello world');
  });

  it('plus as space', () => {
    const result = parseQueryString('q=hello+world');
    assert.strictEqual(result.q, 'hello world');
  });

  it('repeated keys become array', () => {
    assert.deepStrictEqual(parseQueryString('a=1&a=2'), { a: ['1', '2'] });
  });

  it('key with no value', () => {
    const result = parseQueryString('key');
    assert.strictEqual(result.key, '');
  });

  it('leading ? stripped', () => {
    assert.deepStrictEqual(parseQueryString('?a=1'), { a: '1' });
  });

  it('empty string returns empty object', () => {
    assert.deepStrictEqual(parseQueryString(''), {});
  });

  it('mixed: a=1&b=&c', () => {
    const result = parseQueryString('a=1&b=&c');
    assert.strictEqual(result.a, '1');
    assert.strictEqual(result.b, '');
    assert.strictEqual(result.c, '');
  });
});
