const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');

const code = fs.readFileSync(process.env.CODE_FILE, 'utf8');
const mod = { exports: {} };
const fn = new Function('module', 'exports', 'require', code + '\nif (typeof validateEmail !== "undefined") module.exports = { validateEmail };');
fn(mod, mod.exports, require);
const validateEmail = mod.exports.validateEmail;

describe('validateEmail', () => {
  it('valid basic email', () => {
    const result = validateEmail('user@example.com');
    assert.strictEqual(result.valid, true);
    assert.strictEqual(result.reason, null);
  });

  it('valid with + and .', () => {
    const result = validateEmail('user.name+tag@example.com');
    assert.strictEqual(result.valid, true);
  });

  it('missing @ invalid', () => {
    const result = validateEmail('userexample.com');
    assert.strictEqual(result.valid, false);
    assert.strictEqual(typeof result.reason, 'string');
  });

  it('double @ invalid', () => {
    const result = validateEmail('user@@example.com');
    assert.strictEqual(result.valid, false);
    assert.strictEqual(typeof result.reason, 'string');
  });

  it('local starts with dot invalid', () => {
    const result = validateEmail('.user@example.com');
    assert.strictEqual(result.valid, false);
    assert.strictEqual(typeof result.reason, 'string');
  });

  it('consecutive dots invalid', () => {
    const result = validateEmail('user..name@example.com');
    assert.strictEqual(result.valid, false);
    assert.strictEqual(typeof result.reason, 'string');
  });

  it('domain missing TLD invalid', () => {
    const result = validateEmail('user@localhost');
    assert.strictEqual(result.valid, false);
    assert.strictEqual(typeof result.reason, 'string');
  });

  it('empty string invalid', () => {
    const result = validateEmail('');
    assert.strictEqual(result.valid, false);
    assert.strictEqual(typeof result.reason, 'string');
  });
});
