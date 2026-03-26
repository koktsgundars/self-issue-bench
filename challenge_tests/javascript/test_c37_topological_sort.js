const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');

const code = fs.readFileSync(process.env.CODE_FILE, 'utf8');
const mod = { exports: {} };
const fn = new Function('module', 'exports', 'require', code + '\nif (typeof topologicalSort !== "undefined") module.exports = { topologicalSort };');
fn(mod, mod.exports, require);
const topologicalSort = mod.exports.topologicalSort;

describe('topologicalSort', () => {
  it('linear chain', () => {
    const result = topologicalSort({ a: [], b: ['a'], c: ['b'] });
    assert.ok(result.indexOf('a') < result.indexOf('b'));
    assert.ok(result.indexOf('b') < result.indexOf('c'));
  });

  it('diamond dependency', () => {
    const result = topologicalSort({ a: [], b: ['a'], c: ['a'], d: ['b', 'c'] });
    assert.ok(result.indexOf('a') < result.indexOf('b'));
    assert.ok(result.indexOf('a') < result.indexOf('c'));
    assert.ok(result.indexOf('b') < result.indexOf('d'));
    assert.ok(result.indexOf('c') < result.indexOf('d'));
  });

  it('cycle throws Error', () => {
    assert.throws(() => {
      topologicalSort({ a: ['b'], b: ['a'] });
    }, Error);
  });

  it('single node', () => {
    const result = topologicalSort({ a: [] });
    assert.deepStrictEqual(result, ['a']);
  });

  it('empty graph', () => {
    const result = topologicalSort({});
    assert.deepStrictEqual(result, []);
  });

  it('verify ordering is valid', () => {
    const graph = { a: [], b: ['a'], c: ['a'], d: ['b', 'c'], e: ['d'] };
    const result = topologicalSort(graph);
    // Every node appears after all its dependencies
    for (const [node, deps] of Object.entries(graph)) {
      for (const dep of deps) {
        assert.ok(result.indexOf(dep) < result.indexOf(node),
          `${dep} should appear before ${node}`);
      }
    }
  });
});
