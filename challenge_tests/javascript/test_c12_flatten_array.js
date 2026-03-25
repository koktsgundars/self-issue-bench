const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const vm = require('vm');

// Load generated code — use Function constructor to capture declarations
const code = fs.readFileSync(process.env.CODE_FILE, 'utf8');
const wrapper = code + '\nif (typeof EventEmitter !== "undefined") module.exports = { EventEmitter };';
const mod = { exports: {} };
const fn = new Function('module', 'exports', 'require', wrapper);
fn(mod, mod.exports, require);
const EventEmitter = mod.exports.EventEmitter;

describe('EventEmitter', () => {
  it('on and emit basic', () => {
    const ee = new EventEmitter();
    const calls = [];
    ee.on('test', (v) => calls.push(v));
    ee.emit('test', 'a');
    assert.deepStrictEqual(calls, ['a']);
  });

  it('multiple listeners fire in order', () => {
    const ee = new EventEmitter();
    const calls = [];
    ee.on('test', () => calls.push(1));
    ee.on('test', () => calls.push(2));
    ee.emit('test');
    assert.deepStrictEqual(calls, [1, 2]);
  });

  it('off removes listener', () => {
    const ee = new EventEmitter();
    const calls = [];
    const fn = (v) => calls.push(v);
    ee.on('test', fn);
    ee.off('test', fn);
    ee.emit('test', 'a');
    assert.deepStrictEqual(calls, []);
  });

  it('once fires only once', () => {
    const ee = new EventEmitter();
    const calls = [];
    ee.once('test', (v) => calls.push(v));
    ee.emit('test', 'a');
    ee.emit('test', 'b');
    assert.deepStrictEqual(calls, ['a']);
  });

  it('emit passes multiple args', () => {
    const ee = new EventEmitter();
    let received;
    ee.on('test', (a, b) => { received = [a, b]; });
    ee.emit('test', 1, 2);
    assert.deepStrictEqual(received, [1, 2]);
  });

  it('removal during emit does not affect current emission', () => {
    const ee = new EventEmitter();
    const calls = [];
    const fn1 = () => {
      calls.push(1);
      ee.off('test', fn2);
    };
    const fn2 = () => calls.push(2);
    ee.on('test', fn1);
    ee.on('test', fn2);
    ee.emit('test');
    // Both should fire during this emit
    assert.deepStrictEqual(calls, [1, 2]);
  });

  it('once removal during emit does not affect current emission', () => {
    const ee = new EventEmitter();
    const calls = [];
    ee.once('test', () => calls.push('once'));
    ee.on('test', () => calls.push('on'));
    ee.emit('test');
    assert.deepStrictEqual(calls, ['once', 'on']);
  });

  it('emit with no listeners does not throw', () => {
    const ee = new EventEmitter();
    ee.emit('nonexistent', 'data');
  });
});
