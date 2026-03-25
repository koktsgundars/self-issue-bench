const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');

const code = fs.readFileSync(process.env.CODE_FILE, 'utf8');
const mod = { exports: {} };
const fn = new Function('module', 'exports', 'require', code + '\nif (typeof deduplicate !== "undefined") module.exports = { deduplicate };');
fn(mod, mod.exports, require);
const deduplicate = mod.exports.deduplicate;

describe('deduplicate', () => {
  it('removes duplicates', () => {
    assert.deepStrictEqual(deduplicate([1, 2, 2, 3]), [1, 2, 3]);
  });

  it('preserves first occurrence order', () => {
    assert.deepStrictEqual(deduplicate([3, 1, 2, 1, 3]), [3, 1, 2]);
  });

  it('handles empty array', () => {
    assert.deepStrictEqual(deduplicate([]), []);
  });

  it('handles single element', () => {
    assert.deepStrictEqual(deduplicate([5]), [5]);
  });

  it('handles strings', () => {
    assert.deepStrictEqual(deduplicate(['a', 'b', 'a']), ['a', 'b']);
  });

  it('handles no duplicates', () => {
    assert.deepStrictEqual(deduplicate([1, 2, 3]), [1, 2, 3]);
  });

  it('handles all duplicates', () => {
    assert.deepStrictEqual(deduplicate([7, 7, 7]), [7]);
  });
});
