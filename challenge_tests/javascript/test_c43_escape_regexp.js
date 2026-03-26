const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');

const code = fs.readFileSync(process.env.CODE_FILE, 'utf8');
const mod = { exports: {} };
const fn = new Function('module', 'exports', 'require', code + '\nif (typeof escapeRegExp !== "undefined") module.exports = { escapeRegExp };');
fn(mod, mod.exports, require);
const escapeRegExp = mod.exports.escapeRegExp;

describe('escapeRegExp', () => {
  it('no special chars unchanged', () => {
    assert.strictEqual(escapeRegExp('hello'), 'hello');
  });

  it('dots escaped', () => {
    assert.strictEqual(escapeRegExp('a.b'), 'a\\.b');
  });

  it('all special chars escaped', () => {
    const special = '.*+?^${}()|[]\\/';
    const escaped = escapeRegExp(special);
    // Every special char should be preceded by a backslash
    for (const ch of '.*+?^${}()|[]\\/') {
      assert.ok(escaped.includes('\\' + ch), `Expected \\${ch} in result`);
    }
  });

  it('result usable in new RegExp', () => {
    const literal = 'price: $10.00';
    const escaped = escapeRegExp(literal);
    const re = new RegExp(escaped);
    assert.ok(re.test('price: $10.00'));
    assert.ok(!re.test('price: X10X00'));
  });

  it('empty string returns empty', () => {
    assert.strictEqual(escapeRegExp(''), '');
  });

  it('complex pattern', () => {
    const input = 'price: $10.00 (USD)';
    const escaped = escapeRegExp(input);
    const re = new RegExp(escaped);
    assert.ok(re.test(input));
  });
});
