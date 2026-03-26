// Tests for c46_memoize: memoize(fn, keyFn?)
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';

const codeFile = process.env.CODE_FILE!;
const code = fs.readFileSync(codeFile, 'utf8');

const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'ts-test-'));
const tmpFile = path.join(tmpDir, 'code.ts');
fs.writeFileSync(tmpFile, code + '\nexport { memoize };');
const imported = require(tmpFile);
const memoize = imported.memoize;

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

test('caches results (fn called once for same args)', () => {
  let callCount = 0;
  const fn = (x: number) => { callCount++; return x * 2; };
  const memoized = memoize(fn);
  memoized(5);
  memoized(5);
  assertEqual(callCount, 1);
  assertEqual(memoized(5), 10);
});

test('different args get different results', () => {
  const fn = (x: number) => x * 3;
  const memoized = memoize(fn);
  assertEqual(memoized(2), 6);
  assertEqual(memoized(4), 12);
});

test('custom keyFn works', () => {
  let callCount = 0;
  const fn = (a: number, b: number) => { callCount++; return a + b; };
  const memoized = memoize(fn, (a, b) => `${a},${b}`);
  memoized(1, 2);
  memoized(1, 2);
  assertEqual(callCount, 1);
  assertEqual(memoized(1, 2), 3);
});

test('.clear() invalidates cache', () => {
  let callCount = 0;
  const fn = (x: number) => { callCount++; return x; };
  const memoized = memoize(fn);
  memoized(1);
  assertEqual(callCount, 1);
  memoized.clear();
  memoized(1);
  assertEqual(callCount, 2);
});

test('.cache is accessible', () => {
  const fn = (x: number) => x * 2;
  const memoized = memoize(fn);
  memoized(3);
  if (!(memoized.cache instanceof Map)) throw new Error('cache should be a Map');
  if (memoized.cache.size !== 1) throw new Error(`Expected cache size 1, got ${memoized.cache.size}`);
});

test('works with multiple argument types', () => {
  const fn = (a: string, b: number) => `${a}-${b}`;
  const memoized = memoize(fn);
  assertEqual(memoized('hello', 42), 'hello-42');
  assertEqual(memoized('world', 1), 'world-1');
});

fs.rmSync(tmpDir, { recursive: true, force: true });
console.log(`\n${passed} passed, ${failed} failed`);
if (failed > 0) process.exit(1);
