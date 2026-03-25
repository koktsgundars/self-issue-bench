const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');

const code = fs.readFileSync(process.env.CODE_FILE, 'utf8');
const mod = { exports: {} };
const fn = new Function('module', 'exports', 'require', code + '\nif (typeof decodeEntities !== "undefined") module.exports = { decodeEntities };');
fn(mod, mod.exports, require);
const decodeEntities = mod.exports.decodeEntities;

describe('decodeEntities', () => {
  it('decodes &amp;', () => {
    assert.strictEqual(decodeEntities('&amp;'), '&');
  });

  it('decodes &lt; and &gt;', () => {
    assert.strictEqual(decodeEntities('&lt;div&gt;'), '<div>');
  });

  it('decodes &quot;', () => {
    assert.strictEqual(decodeEntities('&quot;hello&quot;'), '"hello"');
  });

  it('decodes &apos;', () => {
    assert.strictEqual(decodeEntities('&apos;'), "'");
  });

  it('decodes numeric decimal entity', () => {
    assert.strictEqual(decodeEntities('&#65;'), 'A');
  });

  it('decodes numeric hex entity', () => {
    assert.strictEqual(decodeEntities('&#x41;'), 'A');
  });

  it('leaves unknown entities unchanged', () => {
    assert.strictEqual(decodeEntities('&unknown;'), '&unknown;');
  });

  it('handles mixed content', () => {
    assert.strictEqual(
      decodeEntities('hello &amp; &#x77;orld'),
      'hello & world'
    );
  });

  it('handles no entities', () => {
    assert.strictEqual(decodeEntities('hello world'), 'hello world');
  });

  it('handles empty string', () => {
    assert.strictEqual(decodeEntities(''), '');
  });
});
