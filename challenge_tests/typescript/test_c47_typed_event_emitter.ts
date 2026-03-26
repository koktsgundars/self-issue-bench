// Tests for c47_typed_event_emitter: TypedEventEmitter
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';

const codeFile = process.env.CODE_FILE!;
const code = fs.readFileSync(codeFile, 'utf8');

const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'ts-test-'));
const tmpFile = path.join(tmpDir, 'code.ts');
fs.writeFileSync(tmpFile, code + '\nexport { TypedEventEmitter };');
const imported = require(tmpFile);
const TypedEventEmitter = imported.TypedEventEmitter;

let passed = 0;
let failed = 0;

function test(name: string, fn: () => void) {
  try { fn(); console.log(`PASS ${name}`); passed++; }
  catch (e: any) { console.log(`FAIL ${name}: ${e.message}`); failed++; }
}

function assertEqual(actual: any, expected: any) {
  if (JSON.stringify(actual) !== JSON.stringify(expected)) {
    throw new Error(`Expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)}`);
  }
}

test('on and emit', () => {
  const emitter = new TypedEventEmitter();
  let received: string | null = null;
  emitter.on('greet', (name: string) => { received = name; });
  emitter.emit('greet', 'Alice');
  assertEqual(received, 'Alice');
});

test('off removes listener', () => {
  const emitter = new TypedEventEmitter();
  let count = 0;
  const listener = () => { count++; };
  emitter.on('event', listener);
  emitter.emit('event');
  emitter.off('event', listener);
  emitter.emit('event');
  assertEqual(count, 1);
});

test('once fires once', () => {
  const emitter = new TypedEventEmitter();
  let count = 0;
  emitter.once('event', () => { count++; });
  emitter.emit('event');
  emitter.emit('event');
  assertEqual(count, 1);
});

test('multiple listeners', () => {
  const emitter = new TypedEventEmitter();
  const results: number[] = [];
  emitter.on('event', () => { results.push(1); });
  emitter.on('event', () => { results.push(2); });
  emitter.emit('event');
  assertEqual(results, [1, 2]);
});

test('listenerCount', () => {
  const emitter = new TypedEventEmitter();
  assertEqual(emitter.listenerCount('event'), 0);
  const fn1 = () => {};
  const fn2 = () => {};
  emitter.on('event', fn1);
  assertEqual(emitter.listenerCount('event'), 1);
  emitter.on('event', fn2);
  assertEqual(emitter.listenerCount('event'), 2);
  emitter.off('event', fn1);
  assertEqual(emitter.listenerCount('event'), 1);
});

test('emit with no listeners does not throw', () => {
  const emitter = new TypedEventEmitter();
  emitter.emit('nonexistent');
});

test('different event types', () => {
  const emitter = new TypedEventEmitter();
  let strResult = '';
  let numResult = 0;
  emitter.on('str', (s: string) => { strResult = s; });
  emitter.on('num', (n: number) => { numResult = n; });
  emitter.emit('str', 'hello');
  emitter.emit('num', 42);
  assertEqual(strResult, 'hello');
  assertEqual(numResult, 42);
});

fs.rmSync(tmpDir, { recursive: true, force: true });
console.log(`\n${passed} passed, ${failed} failed`);
if (failed > 0) process.exit(1);
