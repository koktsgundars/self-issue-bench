const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');

const code = fs.readFileSync(process.env.CODE_FILE, 'utf8');
const mod = { exports: {} };
const fn = new Function('module', 'exports', 'require', code + '\nif (typeof PriorityQueue !== "undefined") module.exports = { PriorityQueue };');
fn(mod, mod.exports, require);
const PriorityQueue = mod.exports.PriorityQueue;

describe('PriorityQueue', () => {
  it('enqueue and peek', () => {
    const pq = new PriorityQueue();
    pq.enqueue('task', 1);
    assert.strictEqual(pq.peek(), 'task');
  });

  it('dequeue returns highest priority', () => {
    const pq = new PriorityQueue();
    pq.enqueue('low', 10);
    pq.enqueue('high', 1);
    pq.enqueue('mid', 5);
    assert.strictEqual(pq.dequeue(), 'high');
    assert.strictEqual(pq.dequeue(), 'mid');
    assert.strictEqual(pq.dequeue(), 'low');
  });

  it('FIFO for equal priority', () => {
    const pq = new PriorityQueue();
    pq.enqueue('first', 1);
    pq.enqueue('second', 1);
    pq.enqueue('third', 1);
    assert.strictEqual(pq.dequeue(), 'first');
    assert.strictEqual(pq.dequeue(), 'second');
    assert.strictEqual(pq.dequeue(), 'third');
  });

  it('dequeue empty throws', () => {
    const pq = new PriorityQueue();
    assert.throws(() => pq.dequeue(), Error);
  });

  it('peek empty throws', () => {
    const pq = new PriorityQueue();
    assert.throws(() => pq.peek(), Error);
  });

  it('size and isEmpty', () => {
    const pq = new PriorityQueue();
    assert.strictEqual(pq.size(), 0);
    assert.strictEqual(pq.isEmpty(), true);
    pq.enqueue('a', 1);
    assert.strictEqual(pq.size(), 1);
    assert.strictEqual(pq.isEmpty(), false);
  });

  it('mixed priorities', () => {
    const pq = new PriorityQueue();
    pq.enqueue('c', 3);
    pq.enqueue('a', 1);
    pq.enqueue('b', 2);
    pq.enqueue('d', 1);
    assert.strictEqual(pq.dequeue(), 'a');
    assert.strictEqual(pq.dequeue(), 'd');
    assert.strictEqual(pq.dequeue(), 'b');
    assert.strictEqual(pq.dequeue(), 'c');
  });
});
