const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');

const code = fs.readFileSync(process.env.CODE_FILE, 'utf8');
const mod = { exports: {} };
const fn = new Function('module', 'exports', 'require', code + '\nif (typeof countTokens !== "undefined") module.exports = { countTokens };');
fn(mod, mod.exports, require);
const countTokens = mod.exports.countTokens;

describe('countTokens', () => {
  it('counts basic words', () => {
    assert.strictEqual(countTokens('hello world'), 2);
  });

  it('handles punctuation splitting', () => {
    const count = countTokens('hello, world!');
    assert.ok(count >= 2, `Expected at least 2 tokens, got ${count}`);
  });

  it('handles empty string', () => {
    assert.strictEqual(countTokens(''), 0);
  });

  it('handles single word', () => {
    assert.strictEqual(countTokens('hello'), 1);
  });

  it('handles multiple spaces', () => {
    assert.strictEqual(countTokens('hello   world'), 2);
  });

  it('handles only whitespace', () => {
    assert.strictEqual(countTokens('   '), 0);
  });
});
