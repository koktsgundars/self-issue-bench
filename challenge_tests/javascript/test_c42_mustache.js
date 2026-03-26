const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');

const code = fs.readFileSync(process.env.CODE_FILE, 'utf8');
const mod = { exports: {} };
const fn = new Function('module', 'exports', 'require', code + '\nif (typeof renderMustache !== "undefined") module.exports = { renderMustache };');
fn(mod, mod.exports, require);
const renderMustache = mod.exports.renderMustache;

describe('renderMustache', () => {
  it('basic variable substitution', () => {
    assert.strictEqual(renderMustache('Hello {{name}}!', { name: 'World' }), 'Hello World!');
  });

  it('HTML escaping of variables', () => {
    const result = renderMustache('{{text}}', { text: '<b>bold</b>' });
    assert.ok(result.includes('&lt;'));
    assert.ok(result.includes('&gt;'));
    assert.ok(!result.includes('<b>'));
  });

  it('unescaped triple braces', () => {
    assert.strictEqual(renderMustache('{{{html}}}', { html: '<b>bold</b>' }), '<b>bold</b>');
  });

  it('section with truthy value', () => {
    assert.strictEqual(
      renderMustache('{{#show}}visible{{/show}}', { show: true }),
      'visible'
    );
  });

  it('section with array iterates', () => {
    const result = renderMustache('{{#items}}{{.}}{{/items}}', { items: ['a', 'b', 'c'] });
    assert.strictEqual(result, 'abc');
  });

  it('inverted section with falsy', () => {
    assert.strictEqual(
      renderMustache('{{^show}}hidden{{/show}}', { show: false }),
      'hidden'
    );
  });

  it('missing key renders empty', () => {
    assert.strictEqual(renderMustache('{{missing}}', {}), '');
  });

  it('dot notation', () => {
    assert.strictEqual(
      renderMustache('{{person.name}}', { person: { name: 'Alice' } }),
      'Alice'
    );
  });
});
